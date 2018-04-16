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
		tbl_account = self.db["tbl_account"]
		self.param["lst_account"] = tbl_account.find()
		tbl_character = self.db["tbl_character"]
		self.param["lst_character"] = tbl_character.find()
		tbl_count = self.db["tbl_count"]
		self.param["lst_count"] = tbl_count.find()
		tbl_have_item = self.db["tbl_have_item"]
		self.param["tbl_have_item"] = tbl_have_item.find()

		mst_item = self.db["mst_item"]
		self.param["mst_item"] = mst_item.find()
		self.render("control.html", param=self.param)

	def post(self):
		if self.get_argument("target_data") == "count":
			tbl = self.db["tbl_count"]
			tbl.remove({ "_id": self.get_argument("target_id") })
			self.param["message"].append("カウント情報を削除しました。")
		if self.get_argument("target_data") == "account":
			tbl = self.db["tbl_account"]
			tbl.remove({ "_id": int(self.get_argument("target_id")) })
			self.param["message"].append("アカウントを削除しました。")
		if self.get_argument("target_data") == "character":
			tbl = self.db["lst_character"]
			tbl.remove({ "_id": self.get_argument("target_id") })
			self.param["message"].append("キャラクターを削除しました。")
		self.get()
