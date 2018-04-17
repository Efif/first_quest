#!/usr/bin/python3
# -*- coding: utf-8 -*-

import uuid
import json
import logging
import tornado.websocket
from tornado.options import define, options
from pymongo import MongoClient

class LoginHandler(tornado.websocket.WebSocketHandler):
	def __init__(self, *args, **kwargs):
		self.db_client = MongoClient(options.db_ip, options.db_port)
		self.db = self.db_client["db_first_quest"]
		self.clients = {}
		super(LoginHandler, self).__init__(*args, **kwargs)

	def open(self, *args, **kwargs):
		self.clients[self] = {
			"login": False,
			"request": self,
			"account_key": None
		}
		logging.debug("connect from : {0}".format(self.request.remote_ip))

	def on_message(self, message):
		message = json.loads(message)
		if message.get("class_name") == "LoginMessage":
			# TODO : サーバメンテナンス状態の取得
			tbl = self.db["tbl_account"]
			record = tbl.find_one({ "account_id": message.get("account_id", "") })
			result = {
				"result": False
			}
			if record is not None and message.get("account_id", "") == record.get("account_id") and message.get("password", "") == record.get("password"):
				# TODO : 二重ログイン防止策の実装
				record["login_key"] = str(uuid.uuid4())
				record["login_status"] = 0
				tbl.save(record)
				result["result"] = True
				result["key"] = record["login_key"]
				self.clients[self]["account_key"] = record["_id"]
			logging.debug("receive(account_id: {0} password: {1} result:{2})".format(message.get("account_id"), message.get("password"), result["result"]))
			self.write_message(result);
		elif message.get("class_name") == "GetCharacterListMessage":
			tbl = self.db["tbl_character"]
			records = tbl.find({ "account_key": self.clients[self]["account_key"] })


			logging.debug("receive({0})".format(message))
			self.write_message({ "list": [
				{ "name": "test1", "sex": 0 }, 
				{ "name": "test2", "sex": 1 }
			] });
		elif message.get("class_name") == "CreateCharacterMessage":
			pass
		elif message.get("class_name") == "DeleteCharacterMessage":
			pass
		else:
			logging.debug("receive({0})".format(message))
			self.write_message({ "message": "馬鹿め" });

	def on_close(self):
		# ログアウト処理
		if self.clients[self]["account_key"] is not None:
			record = tbl.find_one({ "_id": self.clients[self]["account_key"] })
			record["login_status"] = -1
			tbl.save(record)

		del self.clients[self]
		logging.debug("disconeect from : {0}".format(self.request.remote_ip))
