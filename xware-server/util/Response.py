from fastapi import status
from fastapi.responses import JSONResponse

from config import ResponseCode


class Response:
	@staticmethod
	def success_with_data(data):
		response = {
			"msg": "success",
			"data": data,
			"code": ResponseCode.SUCCESS
		}
		return JSONResponse(status_code=status.HTTP_200_OK, content=response)

	@staticmethod
	def success_with_msg(msg):
		response = {
			"msg": msg,
			"code": ResponseCode.SUCCESS
		}
		return JSONResponse(status_code=status.HTTP_200_OK, content=response)

	@staticmethod
	def success(data, msg):
		response = {
			"msg": msg,
			"data": data,
			"code": ResponseCode.SUCCESS
		}
		return JSONResponse(status_code=status.HTTP_200_OK, content=response)

	@staticmethod
	def error_with_status(status_code, code, msg):
		response = {
			"msg": msg,
			"code": code
		}
		return JSONResponse(status_code=status_code, content=response)

	@staticmethod
	def error(code, msg):
		response = {
			"msg": msg,
			"code": code
		}
		return JSONResponse(status_code=status.HTTP_200_OK, content=response)
