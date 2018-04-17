import threading
import tornado.web
from tornado.options import define, options
from pymongo import MongoClient

class RegistHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.db_client = MongoClient(options.db_ip, options.db_port)
		self.db = self.db_client["db_first_quest"]
		self.lock = threading.Lock()
	
	def get(self):
		param = {}
		self.render("regist.html", param=param)

	def post(self):
		param = {}
		param["message"] = []
		param["account_id"] = self.get_argument("account_id")
		param["password"] = self.get_argument("password")
		if param["account_id"] == "":
			param["message"].append("アカウントIDが未入力です。")
		if param["password"] == "":
			param["message"].append("パスワードが未入力です。")
		if len(param["message"]) == 0:
			tbl = self.db["tbl_account"]
			try:
				tbl.insert({
					"_id": self.get_next_id(),
					"account_id": param["account_id"],
					"password": param["password"],
					"login_status": -1
				})
				param["account_id"] = ""
				param["password"] = ""
				param["message"].append("アカウントを登録しました。")
			except Exception as e:
				for arg in e.args:
					param["message"].append(arg)
			
		
		self.render("regist.html", param=param)

	def get_next_id(self):
		self.lock.acquire()
		tbl = self.db["tbl_count"]
		result = tbl.find_and_modify(
			query={"_id": "user_id"}, 
			update={"$inc": {"seq": 1}}
		)
		if result is None:
			tbl.insert({
				"_id": "user_id",
				"seq": 1
			})
			result = {"seq": 0}
		self.lock.release()
		return result["seq"]
