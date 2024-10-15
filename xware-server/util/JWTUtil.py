import time

import jwt


def encode_jwt(payload, secret='secret', algorithm='HS256') -> str:
	# 获得当前时间戳
	timestamp = int(time.time())
	payload['t'] = timestamp
	return jwt.encode(payload, secret, algorithm)


def decode_jwt(token, secret='secret', algorithm='HS256') -> dict:
	return jwt.decode(token, secret, algorithms=[algorithm])
