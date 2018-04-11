#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import logging
import time
import threading
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape
import tornado.options
from tornado.options import define, options

define("port", default=8000, type=int)

class TestHandler(tornado.websocket.WebSocketHandler):
	def __init__(self, *args, **kwargs):
		self.waiters = set()
		self.flg = False
		super(TestHandler, self).__init__(*args, **kwargs)

	def run(self):
		interval = 1
		base_time = time.time()
		next_time = 0
		while True:
			for waiter in self.waiters:
				try:
					waiter.write_message(
						{
							"message": "test!!"
						}
					)
				except:
					pass
			
			next_time = ((base_time - time.time()) % interval) or interval
			time.sleep(next_time)
	
	def open(self, *args, **kwargs):
		self.waiters.add(self)
		if not self.flg:
			self.flg = True
			tornado.ioloop.IOLoop.instance().call_later(1, self.run)
	
	def on_message(self, message):
		message = json.loads(message)
		for waiter in self.waiters:
			#if waiter == self:
			#	continue
			waiter.write_message(
				{
					"name": message["name"], 
					"message": message["message"]
				}
			)
	
	def on_close(self):
		self.waiters.remove(self)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/', TestHandler)
		]
		settings = dict(
			cookie_secret="test",
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			xsrf_cookies=True,
			autoescape="xhtml_escape",
			debug=True,
		)
		tornado.web.Application.__init__(
			self, 
			handlers, 
			**settings
		)

def main():
	tornado.options.parse_config_file(
		os.path.join(os.path.dirname(__file__), 'server.conf')
	)
	tornado.options.parse_command_line()
	app = Application()
	app.listen(options.port)
	logging.debug("run on port {0} in {1} mode".format(options.port, options.logging))
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()