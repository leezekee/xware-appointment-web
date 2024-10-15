from aioredis import Redis
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.exceptions import HTTPException
from contextvars import ContextVar

import config
from models import *
from schemas import *
from util.Response import Response
from util.JWTUtil import decode_jwt, encode_jwt
from database import SessionLocal
from config import *

import logging
import aioredis
import uvicorn

logging.basicConfig(
	level=logging.DEBUG if Settings.ENV == Settings.ENVIRONMENT.DEVELOPMENT and Settings.DEBUG else logging.INFO,
	format='%(levelname)s:     %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI()

token_context: ContextVar[dict] = ContextVar("token_context")

redis: Optional[Redis] = None


@app.on_event("startup")
async def startup():
	global redis
	try:
		redis = await aioredis.from_url(Settings.Redis.REDIS_URL)
		if Settings.Redis.CHECK_CONNECTION_WHEN_START:
			await redis.ping()
			logger.info("Redis connection success")
	except Exception as e:
		logger.error(f"Redis connection error: {e}")
		redis = None


@app.on_event("shutdown")
async def shutdown():
	global redis
	if redis:
		await redis.close()


# 登录验证装饰器
def login_required(func) -> callable:
	if Settings.ENV == Settings.ENVIRONMENT.DEVELOPMENT and Settings.PASS_LOGIN_CHECK:
		return func
	func._login_required = True
	return func


def admin_required(func) -> callable:
	if Settings.ENV == Settings.ENVIRONMENT.DEVELOPMENT and Settings.PASS_ADMIN_CHECK:
		return func
	func._admin_required = True
	return func


@app.middleware("http")
async def auth_check(request: Request, call_next):
	# 获取请求路由地址
	current_route: str = request.url.path
	# 获取路由处理函数
	for route in app.routes:
		if isinstance(route, APIRoute) and route.path == current_route:
			handler = route.endpoint  # 路由处理函数
			if hasattr(handler, "_login_required") or hasattr(handler, "_admin_required"):
				# 获取请求头中的token
				token: str = request.headers.get("Authorization")
				if not token:
					return Response.error(ResponseCode.TOKEN_REQUIRED, "Token is required")

				# 验证token是否有效
				global redis
				if not await redis.exists(token):
					return Response.error(ResponseCode.INVALID_TOKEN, "Token is invalid")
				redis_token = await redis.get(token)
				if not redis_token:
					return Response.error(ResponseCode.INVALID_TOKEN, "Token is invalid")
				decode_token = decode_jwt(redis_token)
				if hasattr(handler, "_admin_required") and decode_token.get("role") != UserRole.ADMIN:
					return Response.error(ResponseCode.PERMISSION_DENIED, "Permission denied")
				# 存储token
				decode_token["raw_token"] = token
				token_context.set(decode_token)

	response = await call_next(request)
	return response


@app.get("/")
# @login_required
async def read_root():
	return Response.success_with_msg("Hello World")


@app.post("/login")
async def login(loginModel: UserLogin):
	session = SessionLocal()
	db_user = session.query(User).filter(User.username == loginModel.username).first()
	if not db_user:
		return Response.error(ResponseCode.USER_NOT_FOUND, "用户不存在")
	if db_user.password != loginModel.password:
		return Response.error(ResponseCode.WRONG_PASSWORD, "密码错误")
	payload = {"username": db_user.username, "id": db_user.id, "role": db_user.role}
	token = encode_jwt(payload)

	await redis.set(token, token, ex=3600 * 24 * 31)

	return Response.success(token, "登录成功")


@app.post("/register")
async def register(registerModel: UserRegister):
	if registerModel.password != registerModel.repassword:
		return Response.error(ResponseCode.PASSWORD_NOT_MATCH, "两次密码不一致")
	session = SessionLocal()
	db_user = session.query(User).filter(User.username == registerModel.username).first()
	if db_user:
		return Response.error(ResponseCode.USER_EXISTED, "用户已存在")
	new_user = User(username=registerModel.username, password=registerModel.password, sid=registerModel.sid,
	                tel=registerModel.phone, email=registerModel.email, role=UserRole.USER)
	session.add(new_user)
	session.commit()
	session.refresh(new_user)
	payload = {"username": new_user.username, "id": new_user.id, "role": new_user.role}
	token = encode_jwt(payload)

	# token 存入redis
	await redis.set(token, token, ex=3600 * 24 * 31)

	return Response.success(token, "注册成功")


@app.post("/logout")
@login_required
async def logout():
	token = token_context.get()
	await redis.delete(token['raw_token'])
	return Response.success_with_msg("登出成功")


@app.post("/user/info")
@login_required
async def change_user_info(userModel: UserInfo):
	token = token_context.get()
	username = token.get("username")
	session = SessionLocal()
	user = session.query(User).filter(User.username == username).first()
	if not user:
		return Response.error(ResponseCode.USER_NOT_FOUND, "用户不存在")
	if userModel.phone:
		user.tel = userModel.phone
	if userModel.email:
		user.email = userModel.email
	if userModel.sid:
		user.sid = userModel.sid
	session.commit()
	return Response.success_with_msg("修改成功")


@app.get("/user/info")
@login_required
async def get_user_info():
	token = token_context.get()
	username = token.get("username")
	user_id = token.get("id")
	session = SessionLocal()
	user = session.query(User).filter(User.username == username).first()
	if not user:
		return Response.error(ResponseCode.USER_NOT_FOUND, "用户不存在")
	count = session.query(Appointment).filter(Appointment.status == 0).filter(Appointment.user_id == user_id).count()
	user_info = {
		"username": user.username,
		"sid": user.sid,
		"phone": user.tel,
		"email": user.email,
		"pending_count": count
	}
	return Response.success(user_info, "获取成功")


@app.post("/appointment")
@login_required
async def make_appointment(appointmentModel: AppointmentModel):
	token = token_context.get()
	user_id = token.get("id")
	session = SessionLocal()
	new_appointment = Appointment(user_id=user_id, timeslot_id=appointmentModel.timeslot_id,
	                              problem_id=appointmentModel.problem_id, description=appointmentModel.description,
	                              status=0)
	session.add(new_appointment)
	session.commit()
	session.refresh(new_appointment)
	return Response.success_with_msg("预约成功")


@app.delete("/appointment")
@login_required
async def cancel_appointment(appointment_id: int):
	token = token_context.get()
	user_id = token.get("id")
	session = SessionLocal()
	appointment = session.query(Appointment).filter(Appointment.id == appointment_id).first()
	if not appointment:
		return Response.error(ResponseCode.APPOINTMENT_NOT_FOUND, "预约不存在")
	if appointment.user_id != user_id:
		return Response.error(ResponseCode.APPOINTMENT_NOT_MATCH, "预约不匹配")
	appointment.status = AppointmentStatus.CANCELED
	session.commit()
	return Response.success_with_msg("取消成功")


@app.get("/appointment/list")
@login_required
async def get_appointment():
	token = token_context.get()
	user_id = token.get("id")
	session = SessionLocal()
	queries = session.query(
		Appointment.id,
		Appointment.status,
		Timeslot.start_time,
		Timeslot.end_time,
		ProblemType.type.label('problem_type'),
		MainProblemType.type.label('main_problem_type')
	).select_from(Appointment). \
		join(Timeslot, Appointment.timeslot_id == Timeslot.id). \
		outerjoin(ProblemType, Appointment.problem_id == ProblemType.id). \
		outerjoin(MainProblemType, ProblemType.main_problem_id == MainProblemType.id). \
		order_by(Appointment.id.desc()). \
		filter(Appointment.user_id == user_id)

	for query in queries:
		appointments = [{
			'id': query.id,
			'status': config.AppointmentStatus.get_status(query.status, query.end_time),
			'start_time': query.start_time.strftime("%Y-%m-%d %H:%M:%S"),
			'end_time': query.end_time.strftime("%Y-%m-%d %H:%M:%S"),
			'problem_type': query.problem_type,
			'main_problem_type': query.main_problem_type
		}]
		appointments.append(appointments)

	appointments = []
	for query in queries:
		appointments.append({
			'id': query.id,
			'status': config.AppointmentStatus.get_status(query.status, query.end_time),
			'start_time': query.start_time.strftime("%Y-%m-%d %H:%M:%S"),
			'end_time': query.end_time.strftime("%Y-%m-%d %H:%M:%S"),
			'problem_type': query.problem_type,
			'main_problem_type': query.main_problem_type
		})
	return Response.success(appointments, "获取成功")


@app.get("/appointment/pending")
@login_required
async def get_pending_appointment():
	token = token_context.get()
	user_id = token.get("id")
	session = SessionLocal()
	queries = session.query(
		Appointment.id,
		Appointment.status,
		Timeslot.start_time,
		Timeslot.end_time,
		ProblemType.type.label('problem_type'),
		MainProblemType.type.label('main_problem_type')
	).select_from(Appointment). \
		join(Timeslot, Appointment.timeslot_id == Timeslot.id). \
		outerjoin(ProblemType, Appointment.problem_id == ProblemType.id). \
		outerjoin(MainProblemType, ProblemType.main_problem_id == MainProblemType.id). \
		order_by(Appointment.id.desc()). \
		filter(Appointment.status == 0). \
		filter(Appointment.user_id == user_id)

	appointments = []
	for query in queries:
		appointments.append({
			'id': query.id,
			'status': config.AppointmentStatus.get_status(query.status, query.end_time),
			'start_time': query.start_time.strftime("%Y-%m-%d %H:%M:%S"),
			'end_time': query.end_time.strftime("%Y-%m-%d %H:%M:%S"),
			'problem_type': query.problem_type,
			'main_problem_type': query.main_problem_type
		})

	return Response.success(appointments, "获取成功")


@app.get("/appointment/detail")
@login_required
async def get_appointment_detail(appointment_id: int):
	token = token_context.get()
	user_id = token.get("id")
	# user_id = 10
	session = SessionLocal()
	query = session.query(
		Appointment.id,
		Appointment.description,
		Appointment.status,
		Appointment.user_id,
		Timeslot.start_time,
		Timeslot.end_time,
		ProblemType.type.label('problem_type'),
		MainProblemType.type.label('main_problem_type')
	).select_from(Appointment). \
		join(Timeslot, Appointment.timeslot_id == Timeslot.id). \
		outerjoin(ProblemType, Appointment.problem_id == ProblemType.id). \
		outerjoin(MainProblemType, ProblemType.main_problem_id == MainProblemType.id). \
		order_by(Appointment.id.desc()). \
		filter(Appointment.id == appointment_id).first()
	if not query:
		return Response.error(ResponseCode.APPOINTMENT_NOT_FOUND, "预约不存在")
	if query.user_id != user_id:
		return Response.error(ResponseCode.APPOINTMENT_NOT_MATCH, "不能查看他人预约")
	appointment = {
		'id': query.id,
		'description': query.description,
		'status': config.AppointmentStatus.get_status(query.status, query.end_time),
		'start_time': query.start_time.strftime("%Y-%m-%d %H:%M:%S"),
		'end_time': query.end_time.strftime("%Y-%m-%d %H:%M:%S"),
		'problem_type': query.problem_type,
		'main_problem_type': query.main_problem_type
	}

	return Response.success(appointment, "获取成功")


@app.get("/timeslot")
@login_required
async def get_timeslot():
	session = SessionLocal()
	queries = session.query(Timeslot).all()
	timeslots = []
	for query in queries:
		if query.start_time < datetime.now():
			continue
		timeslots.append({
			'id': query.id,
			'start': query.start_time.strftime("%Y-%m-%d %H:%M:%S"),
			'end': query.end_time.strftime("%Y-%m-%d %H:%M:%S")
		})
	return Response.success(timeslots, "获取成功")


@app.get("/problem/type")
@login_required
async def get_problem_type():
	session = SessionLocal()
	queries = session.query(
		ProblemType.id.label('id'),
		ProblemType.type.label('problem_type'),
		MainProblemType.type.label('main_problem_type')
	).select_from(ProblemType). \
		outerjoin(MainProblemType, ProblemType.main_problem_id == MainProblemType.id). \
		all()
	problem_types = {}
	for query in queries:
		if query.main_problem_type not in problem_types:
			problem_types[query.main_problem_type] = []
		problem_types[query.main_problem_type].append({
			'id': query.id,
			'type': query.problem_type
		})
	return Response.success(problem_types, "获取成功")


# 管理员接口
@app.post("/admin/timeslot")
@admin_required
async def add_timeslot(timeslotModel: TimeslotModel):
	session = SessionLocal()
	# 转化时间戳
	start_time = datetime.fromtimestamp(timeslotModel.start_time)
	end_time = datetime.fromtimestamp(timeslotModel.end_time)
	new_timeslot = Timeslot(start_time=start_time, end_time=end_time)
	session.add(new_timeslot)
	session.commit()
	session.refresh(new_timeslot)
	return Response.success_with_msg("添加成功")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8888)
	    