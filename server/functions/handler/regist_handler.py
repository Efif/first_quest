import tornado.web
from tornado.options import define, options
from pymongo import MongoClient

class RegistHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.db_client = MongoClient(options.db_ip, options.db_port)
		self.db = self.db_client["db_first_quest"]
	
	def get(self):
		param = {}
		self.render("regist.html", param=param)

	def post(self):
		param = {}
		param["message"] = []
		param["user_id"] = self.get_argument("user_id")
		param["password"] = self.get_argument("password")
		if param["user_id"] == "":
			param["message"].append("ユーザーIDが未入力です。")
		if param["password"] == "":
			param["message"].append("パスワードが未入力です。")
		if len(param["message"]) == 0:
			tbl = self.db["tbl_account"]
			try:
				tbl.insert({
					"user_id": param["user_id"],
					"password": param["password"]
				})
				param["user_id"] = ""
				param["password"] = ""
				param["message"].append("アカウントを登録しました。")
			except Exception as e:
				for arg in e.arg:
					param["message"].append(arg)
			
		
		self.render("regist.html", param=param)
