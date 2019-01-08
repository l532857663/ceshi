#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import datetime
import json
import email
import eml_parser

def json_serial (obj):
	if isinstance (obj, datetime.datetime):
		serial = obj.isoformat ()
		return serial


with open ('1.eml', 'rb') as fhdl:
	raw_email = fhdl.read()

parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email)

print(json.dumps(parsed_eml, default=json_serial))
