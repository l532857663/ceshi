#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import shutil
import base64
import zipfile
import logging
logger = logging.getLogger("Inductive_file")
logger.setLevel(logging.DEBUG)

#["----","\t","    "]
split_list = ["LS0tLQ==", "CQ==", "ICAgIA=="]
raletion_dict = {
        "LS0tLQ==" : "/home/w123/change_file/hengxian",
        "CQ==" : "/home/w123/change_file/zhibiao",
        "ICAgIA==" : "/home/w123/change_file/kongge",
        }

def logging_in():
    #输出到屏幕
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    #输出到文件
    fh = logging.FileHandler("log_get_file.log")
    fh.setLevel(logging.INFO)
    #设置日志格式
    fomatter = logging.Formatter('%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s')
    ch.setFormatter(fomatter)
    fh.setFormatter(fomatter)
    logger.addHandler(ch)
    logger.addHandler(fh)

def mk_path(the_path):
	if not os.path.exists(the_path):
		try:
			os.mkdir(the_path)
		except Exception as e:
			logger.info("mkdir path:"+str(e))
			mk_path(os.path.split(the_path)[0])

def file_cp_new(the_path):
	with open(the_path, "rb") as f:
		content_str = f.readline()
	res_dict = {}
	for split_str in split_list:
		split_byte = base64.b64decode(split_str.encode('utf-8'))
		res_dict[split_str] = len(content_str.split(split_byte))
	for name in res_dict:
		if res_dict[name] > 1:
			tmp_path = os.path.join(raletion_dict[name], the_path)
			try:
				shutil.copy(the_path, tmp_path)
			except Exception as e:
				logger.warning("shutil copy:"+str(e))
				logger.info("source_file_path:" + the_path)
				logger.info("copy_file_to_path:" + tmp_path)

def zip_cp_new(the_path):
    try:
        unzip_dir = the_path+"_unzip_file"
        with zipfile.ZipFile(the_path) as zfile:
            zfile.extractall(path=unzip_dir)
        file_dir_operating(unzip_dir)
    except zipfile.BadZipFile as e:
        logger.info("unzip file:"+str(e))


def file_dir_operating(src_path):
	#读取目的文件夹列表
	target_list = os.listdir(src_path)
	for target_path in target_list:
		files_path = os.path.join(src_path, target_path)
		if os.path.isdir(files_path):
			#创建文件夹,各个类别的都创建
			for name in raletion_dict.values():
				tmp_path = os.path.join(name, files_path)
				mk_path(tmp_path)
			#下层目录
			file_dir_operating(files_path)
		elif os.path.isfile(files_path):
			ext_str = os.path.splitext(files_path)[1].lower()
			if ext_str == ".txt" or ext_str == ".text":
				file_cp_new(files_path)
			elif ext_str == ".zip":
				zip_cp_new(files_path)


def main():
    print("main start")
    #文件遍历
    s_path = sys.argv[1]
    file_dir_operating(s_path)
    print("main end")

if __name__ == "__main__":
    print("START")
    if len(sys.argv) != 2:
        sys.exit("eg: ./get_type.py src_path")
    logging_in()
    main()
    print("END")
