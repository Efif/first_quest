#!/usr/bin/python3
# -*- coding: utf-8 -*-

import uuid
import json
import time
import logging
import tornado.websocket
from tornado.options import define, options
from pymongo import MongoClient

class WorldHandler(tornado.websocket.WebSocketHandler):
	def __init__(self, *args, **kwargs):
		self.db_client = MongoClient(options.db_ip, options.db_port)
		self.db = self.db_client["db_first_quest"]
		self.waiters = set()
		self.flg = False
		super(WorldHandler, self).__init__(*args, **kwargs)

	def run(self):
		interval = 1
		base_time = time.time()
		next_time = 0
		while True:
			self.write_message({ "message": "test" });
			next_time = ((base_time - time.time()) % interval) or interval
			time.sleep(next_time)
	
	def open(self, *args, **kwargs):
		if not self.flg:
			self.flg = True
			tornado.ioloop.IOLoop.instance().call_later(1, self.run)

	def on_message(self, message):
		pass

	def on_close(self):
		pass

