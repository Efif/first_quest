#!/usr/bin/python3
# -*- coding: utf-8 -*-

import uuid
import json
import logging
import threading
import tornado.websocket
from tornado.options import define, options
from pymongo import MongoClient

class LoginHandler(tornado.websocket.WebSocketHandler):
	def __init__(self, *args, **kwargs):
		self.db_client = MongoClient(options.db_ip, options.db_port)
		self.db = self.db_client["db_first_quest"]
		self.clients = {}
		self.lock = threading.Lock()
		super(LoginHandler, self).__init__(*args, **kwargs)

	def open(self, *args, **kwargs):
		self.clients[self] = {
			"login": False,
			"request": self,
			"account_key": None
		}
		logging.debug("connect from : {0}".format(self.request.remote_ip))

	def on_message(self, json_message):
		message = json.loads(json_message)
		if message.get("class_name") == "LoginMessage":
			self.process_login(message)
		elif message.get("class_name") == "LogoutMessage":
			self.process_logout(message)
		elif message.get("class_name") == "GetCharacterListMessage":
			self.process_get_character_list(message)
		elif message.get("class_name") == "CreateCharacterMessage":
			self.process_create_character(message)
		elif message.get("class_name") == "DeleteCharacterMessage":
			self.process_delete_character(message)
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

	def get_next_character_id(self):
		self.lock.acquire()
		tbl = self.db["tbl_count"]
		result = tbl.find_and_modify(
			query={"_id": "character_id"}, 
			update={"$inc": {"seq": 1}}
		)
		if result is None:
			tbl.insert({
				"_id": "character_id",
				"seq": 1
			})
			result = {"seq": 0}
		self.lock.release()
		return result["seq"]

	def process_login(self, message):
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
		logging.debug("LoginMessage(account_id: {0} password: {1} result:{2})".format(message.get("account_id"), message.get("password"), result["result"]))
		self.write_message(result);

	def process_logout(self, message):
		result = {
			"result": False
		}
		if self.clients[self]["account_key"] is not None:
			# TODO : 特定条件下でのログアウト禁止対応
			tbl = self.db["tbl_account"]
			records = tbl.find({ "_id": self.clients[self]["account_key"] })
			record["login_status"] = -1
			tbl.save(record)
			result["result"] = True
		logging.debug("LogoutMessage(account_key: {0} result:{1})".format(self.clients[self]["account_key"], len(result)))
		self.clients[self]["account_key"] = None
		self.write_message(result);

	def process_get_character_list(self, message):
		result = []
		if self.clients[self]["account_key"] is not None:
			tbl = self.db["tbl_character"]
			records = tbl.find({ "account_key": self.clients[self]["account_key"] })
			for record in records:
				result.append({
					"id": record["_id"],
					"name": record["name"],
					"sex": record["sex"],
					"hp": record["hp"]
				})
		logging.debug("GetCharacterListMessage(account_key: {0} result:{1})".format(self.clients[self]["account_key"], len(result)))
		self.write_message({ "list": result });

	def process_create_character(self, message):
		result = {
			"result": False
		}
		if self.clients[self]["account_key"] is not None:
			tbl = self.db["tbl_character"]
			tbl.insert({
				"_id": self.get_next_id(),
				"account_key": self.clients[self]["account_key"],
				"name": message.get("name"),
				"sex": int(message.get("sex")),
				"hp": 100
			})
			result["result"] = True
		logging.debug("CreateCharacterMessage(account_key: {0} result:{1})".format(self.clients[self]["account_key"], result["result"]))
		self.write_message(result);

	def process_delete_character(self, message):
		result = {
			"result": False
		}
		if self.clients[self]["account_key"] is not None:
			tbl = self.db["tbl_character"]
			del_result = tbl.delete_one({ "_id": int(message.get("character_id"))})
			if del_result.deleted_count == 1:
				result["result"] = True
			else:
				result["error_type"] = 1
		logging.debug("DeleteCharacterMessage(account_key: {0} result:{1})".format(self.clients[self]["account_key"], result["result"]))
		self.write_message(result);
