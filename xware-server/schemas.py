from typing import Optional

from pydantic import BaseModel


class UserRegister(BaseModel):
	username: str
	password: str
	repassword: str
	sid: str
	phone: str
	email: str


class UserLogin(BaseModel):
	username: str
	password: str


class UserInfo(BaseModel):
	sid: Optional[str] = None
	phone: Optional[str] = None
	email: Optional[str] = None


class AppointmentModel(BaseModel):
	timeslot_id: int
	problem_id: int
	description: str


class TimeslotModel(BaseModel):
	start_time: int
	end_time: int
