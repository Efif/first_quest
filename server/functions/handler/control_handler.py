import tornado.web
from tornado.options import define, options
from pymongo import MongoClient

class ControlHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.db_client = MongoClient(options.db_ip, options.db_port)
		self.db = self.db_client["db_first_quest"]
		self.param = {}
		self.param["message"] = []


	def get(self):
		tbl = self.db["tbl_account"]
		self.param["lst_account"] = tbl.find()
		self.render("control.html", param=self.param)

	def post(self):
		tbl = self.db["tbl_account"]
		tbl.remove({ "user_id": self.get_argument("user_id") })
		self.param["message"].append("アカウントを削除しました。")
		self.get()
