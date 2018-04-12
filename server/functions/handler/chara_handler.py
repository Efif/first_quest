#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import tornado.websocket
from tornado.options import define, options
from pymongo import MongoClient

class CharaHandler(tornado.websocket.WebSocketHandler):
	def __init__(self, *args, **kwargs):
		self.waiters = set()
		super(CharaHandler, self).__init__(*args, **kwargs)

	def open(self, *args, **kwargs):
		pass

	def on_message(self, message):
		message = json.loads(message)

	def on_close(self):
		pass

