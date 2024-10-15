from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.dialects.mysql import VARCHAR

from database import Base


class Appointment(Base):
	__tablename__ = 'appointment'

	id = Column(Integer, primary_key=True, autoincrement=True)
	timeslot_id = Column(Integer, nullable=False)
	problem_id = Column(Integer, nullable=True)
	description = Column(VARCHAR(1024), nullable=True)
	status = Column(Integer, nullable=True, comment="0 - 待维修, 1 - 已完成, 2 - 已取消, 3 - 已过期")
	user_id = Column(Integer, nullable=True)


class MainProblemType(Base):
	__tablename__ = 'main_problem_type'

	id = Column(Integer, primary_key=True, autoincrement=True)
	type = Column(VARCHAR(255), nullable=True)


class ProblemType(Base):
	__tablename__ = 'problem_type'

	id = Column(Integer, primary_key=True, autoincrement=True)
	type = Column(VARCHAR(255), nullable=True)
	main_problem_id = Column(Integer, nullable=True)


class Timeslot(Base):
	__tablename__ = 'timeslot'

	id = Column(Integer, primary_key=True, autoincrement=True)
	start_time = Column(DateTime, nullable=False)
	end_time = Column(DateTime, nullable=False)


class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True, autoincrement=True)
	sid = Column(VARCHAR(20), nullable=True)
	username = Column(VARCHAR(255), nullable=True)
	password = Column(VARCHAR(255), nullable=True)
	tel = Column(VARCHAR(255), nullable=True)
	email = Column(VARCHAR(255), nullable=True)
	role = Column(Integer, nullable=True, comment="0 - 普通用户, 1 - 管理员")
