#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import logging;logging.basicConfig(level = logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web

def index(request):
	return web.Response (body = b"<h1>Awesome</h1>")

@asyncio.coroutine
def init(loop):
	ip_address = "127.0.0.1"
	the_port = 9000
	app = web.Application (loop = loop)
	app.router.add_route("GET", "/", index)
	srv = yield from loop.create_server(app.make_handler(), ip_address, the_port)
	logging.info('server started at http://' + ip_address + ':' + str(the_port))
	return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
