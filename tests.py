users_data = {}

def init():
	with open("users.csv") as f:
		f.readline()
		for line in f:
			line = line.strip(" \t\n")
			if line != "":
				t = line.split()
				users_data[t[0]] = t[1]

def add_user(login, password):
	users_data[login] = password
	with open("users.csv","a") as f:
		f.write(login+" "+password+"\n")

def success(**kwargs):
	kwargs["success"] = True
	return kwargs


from typing import NamedTuple
from collections import namedtuple
import pickle
class C(NamedTuple):
	msg: str = ""

class A(NamedTuple):
	# def __init__(self):
	# 	self.a = True
	a: int = 24
	error: C = None

	def hi(self):
		print("hi1")

class B(A):
	def __init__(self):
		super().__init__()
		self.msg = "hi"

# print( pickle.dumps(A()))
print(A(4,C("hi"))._asdict())
# print(success(hi=5))
# test()
# add_user("hi4", "1")
# print(users_data)
