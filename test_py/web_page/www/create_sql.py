#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import asyncio
import orm
from models import User

def test(loop):
    yield from orm.create_pool(loop=loop, user='sss_root', password='123456', db='awesome')

    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')

    yield from u.save()

print("START")
loop = asyncio.get_event_loop()
for x in test(loop):
    pass
print("END")
