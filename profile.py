from database import DataBase

class Profile():

	def __init__(self,user_id):
		self.name = None
		self.surname = None
		self.age = None
		self.sex = None
		self.email = None
		self.username = None
		self.user_id = user_id
		self.GetAllData()

	def GetAllData(self):
		db = DataBase()
		db.cursor.execute("SELECT username,email FROM users WHERE user_id=\"%s\"" % self.user_id)
		user = db.cursor.fetchone()
		self.username,self.email = user
		db.cursor.execute("SELECT * FROM settings WHERE user_id=\"%s\"" % self.user_id)
		settings = db.cursor.fetchone()
		self.user_id,self.name,self.surname,self.age,self.sex = settings

	def print_user_data(self):
		print(self.__dict__)