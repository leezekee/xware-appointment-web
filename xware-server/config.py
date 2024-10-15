from datetime import datetime


class AppointmentStatus:
	PENDING = 0
	CANCELED = 1
	COMPLETED = 2
	EXPIRED = 3

	@staticmethod
	def get_status(status, end_time):
		if status == 0:
			if end_time < datetime.now():
				return "已过期"
			else:
				return "待维修"
		elif status == 1:
			return "已完成"
		elif status == 2:
			return "已取消"
		elif status == 3:
			return "已过期"


class UserRole:
	USER = 0
	ADMIN = 1


class ResponseCode:
	# Description: Define response code for API
	SUCCESS = 200200
	# Custom
	USER_EXISTED = 2004002    # User already exists
	WRONG_PASSWORD = 2004003    # Password error
	PASSWORD_NOT_MATCH = 2004001    # Password not match
	APPOINTMENT_NOT_MATCH = 2004004    # Appointment not match
	TOKEN_REQUIRED = 2004011  # Token is required
	INVALID_TOKEN = 2004012  # Invalid token
	USER_NOT_FOUND = 2004041    # User not found
	APPOINTMENT_NOT_FOUND = 2004042    # Appointment not found
	PERMISSION_DENIED = 2004031   # Permission denied


class Settings:
	class ENVIRONMENT:
		PRODUCTION = 0
		DEVELOPMENT = 1
		TEST = 2

	class Database:
		HOST = "localhost"
		PORT = 3306
		DB = "xware_appointment"
		USER = "root"
		PASSWORD = "123456"
		PROTOCOL = "mysql+pymysql"
		DATABASE_URL = f"{PROTOCOL}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

	class Redis:
		HOST = "localhost"
		PORT = 6379
		REDIS_URL = f"redis://{HOST}:{PORT}"
		CHECK_CONNECTION_WHEN_START = True

	ENV = ENVIRONMENT.TEST
	PASS_LOGIN_CHECK = True
	PASS_ADMIN_CHECK = True
	DEBUG = True    # logger 控制台输出


