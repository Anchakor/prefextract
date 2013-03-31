import base64
import os
import shutil

def cutup(str, length=255):
	"""
	:param str: string to cut up
	:param length: how each piece should be long
	:rtype list of strings
	"""
	return cutup2([str], length)

def cutup2(sl, length):
	last = sl.pop()
	if (len(last) >= length):
		sl.append(last[:length])
		sl.append(last[length:])
		return cutup2(sl, length)
	else:
		sl.append(last)
		return sl

def getUserPath(id):
	longFileName = base64.urlsafe_b64encode(id)
	path = os.path.normpath("/".join(cutup(longFileName)))
	path = os.path.join("users", path)
	return path

def deleteUser(id):
	path = getUserPath(id)
	if(os.path.isdir(path)):
		shutil.rmtree(path)

class User:
	def __init__(self, id):
		"""
		:param id: the user id
		:type id: string
		"""
		path = getUserPath(id)
		if(not os.path.isdir(path)):
			os.makedirs(path, 0777)
		print path
		

u = "testUser"
t = User(u)
deleteUser(u)
deleteUser("test")

