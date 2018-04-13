#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import logging
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape
import tornado.options
from tornado.options import define, options
from functions.handler.login_handler import LoginHandler
from functions.handler.chara_handler import CharaHandler
from functions.handler.chat_handler import ChatHandler
from functions.handler.world_handler import WorldHandler
from functions.handler.regist_handler import RegistHandler
from functions.handler.control_handler import ControlHandler

define("port", default=8000, type=int)
define("db_ip", default="127.0.0.1")
define("db_port", default=27017, type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/login', LoginHandler),
			(r'/chara', CharaHandler),
			(r'/chat', ChatHandler),
			(r'/world', WorldHandler),
			(r'/regist', RegistHandler),
			(r'/control', ControlHandler)
		]
		settings = dict(
			cookie_secret="test",
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			xsrf_cookies=False,
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