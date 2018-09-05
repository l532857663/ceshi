#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import threading
from urllib import request, parse

'''
发送http请求，把数据字符串进行分析，返回json字符串
eg:	
{
	"res_code":{
		"analysis":"新乡市/ns|-*-|人民检察院劳/nis", #数据分词结果
		"keyword_list":"", #关键词5个
		"sentence_list":"", #摘要3个
		"judge_result":"" #分词结果
	}
}
'''

def connect_server(url):
	headers = {
		'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'	 			r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
		'Referer': url,
		'Connection': 'keep-alive'
}
	req = request.Request(url, headers=headers)
	data = {
		"username1" : "admin",
		"data_str" : r'新乡市 卫滨区 人民检察院劳务服务项目(二次)结果公告 \n\n招标文件中科华水工程管理有限公司受新乡市卫滨区人民检察院的委托，就新乡市卫滨区人民检察院劳务服务项目（二次）进行公开招标，按规定程序进行了开标、评标、定标，现就本次招标的结果公布如下：\n一、招标项目名称及招标编号：\n项目名称：新乡市卫滨区人民检察院劳务服务项目（二次）\n招标编号：WCF17012\n二、招标项目简要说明\n预算金额：财政资金，采购预算金额每人每月2500元。\n服务期：两年。\n招标公告发布日期：2017年09月12日\n三、评标信息：\n评标日期：2017年10月12日\n评标委员会成员：郭海娟、杨玉东、付萍、雷翠花、杨新\n四、评标结果：\n中标人名称：新乡市现代人力资源开发服务有限公司\n地址：新乡市平原路宏生数码天城1号楼509室\n中标人法定代表人：席霞\n联系人：马峥剑    \n联系电话：13383801711\n中标金额：每人每月2474.00元\n五、本次招标项目联系事项：\n采购人：新乡市卫滨区人民检察院\n地 址：河南省新乡市南环路216号\n联系人：李先生\n联系电话：0373-5121511\n代理机构：中科华水工程管理有限公司\n地址：新乡市新一街道清路\n联系人：张女士\n联系电话：0373-5116868\n公告期限：本结果公告自发布之日起公示期限为1个工作日。\n中科华水工程管理有限公司\n2017年 10月 12日\n政府采购信息报社 版权所有    地址：北京市丰台区南四环西路186号汉威国际广场一区1号楼201-202单元    技术支持：政府采购信息网\n网址：http://www.caigou2003.com/   电话：010-88587089   E-mail:webmaster#caigou2003.com(*发送邮件时请把#改成@)'
	}
	data = parse.urlencode(data).encode('utf-8')
	try:
		page = request.urlopen(req, data=data).read()
		page = page.decode('utf-8')
		print("result:",page)
	except BaseException as e:
		print("The_error:",e)

if __name__ == "__main__":
	print("Start")
	url = r"http://192.168.11.133:8931/Evaluate"
	connect_server(url)
