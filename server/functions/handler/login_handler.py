#!/usr/bin/python3
# -*- coding: utf-8 -*-

import uuid
import json
import tornado.websocket
from tornado.options import define, options
from pymongo import MongoClient

class LoginHandler(tornado.websocket.WebSocketHandler):
	def __init__(self, *args, **kwargs):
		self.db_client = MongoClient(options.db_ip, options.db_port)
		self.db = self.db_client["db_first_quest"]
		super(LoginHandler, self).__init__(*args, **kwargs)

	def open(self, *args, **kwargs):
		pass

	def on_message(self, message):
		message = json.loads(message)
		# TODO : サーバメンテナンス状態の取得
		tbl = self.db["tbl_account"]
		record = tbl.find_one({ "account_id": message["account_id"] })
		if message["account_id"] == record.get("account_id") and message["password"] == record.get("password"):
			# TODO : 二重ログイン防止策の実装
			record["login_key"] = str(uuid.uuid4())
			tbl.save(record)
			self.write_message({ "result": True, "key": record["login_key"] });
		else:
			self.write_message({ "result": False });

	def on_close(self):
		pass
