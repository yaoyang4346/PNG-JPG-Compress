# -*- coding: UTF-8 -*-
from Compress import Compress
import os
print("请输入目录的绝对路径，例如：/home/***/123")
while True:
	dir = raw_input("请输入：")
	if os.path.exists(dir) and os.path.isdir(dir):
		break
	else:
		print("该路径不存在")
print("请选择输出模式：")
print("1.覆盖源文件")
print("2.在新目录下输出")
while True:
	mode = raw_input("请选择：")
	try:
		mode = int(mode)
		if mode < 1 or mode > 2:
			print("请输入正确序号")
		else:
			mode -= 1
			break
	except Exception as e:
		print("请输入数字！！")

print("请选择遍历模式：")
print("1.仅遍历一级目录")
print("2.递归遍历所有子目录")
while True:
	recursive = raw_input("请选择：")
	try:
		recursive = int(recursive)
		if recursive < 1 or recursive > 2:
			print("请输入正确序号")
		else:
			recursive = True if recursive == 2 else False
			break
	except Exception as e:
		print("请输入数字！！")
compose = Compress(dir, mode, recursive, 1)
compose.run()
