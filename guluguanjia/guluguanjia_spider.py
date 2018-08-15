# coding: utf-8
import requests
import os
from pyquery import PyQuery as pq

url = 'http://manager.gulugj.com/Qrcode/GroupQrcode/Index?token=0962a27a6fae778309de6538b125f6b3'

cookie = 'PHPSESSID=asf6ti4o20rocon9hdu85bs6l5'

headers = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	'Host':'manager.gulugj.com',
	'Referer':'http://me.gulugj.com/Member/Member/Login?jumpUrl=http%3A%2F%2Fmanager.gulugj.com%2FQrcode%2FGroupQrcode%2FIndex&p=qrcode',
	'Cookie':cookie
}

def get_message():
	html = requests.get(url,headers)
	if html.status_code != 200:
		return None
	text = html.text
	doc = pq(text)
	results = doc('tbody tr').items()
	for result in results:
		message = {}
		nums = []
		tmps = result('div').items()
		for tmp in tmps:
			if tmp.attr('style') == 'padding: 5px 0 5px;word-wrap: break-word;':
				message['群'] = tmp.text()
		temps = result('td.center').items()
		for temp in temps:
			nums.append(temp.text())
		message['今日长按识别人数'] = nums[1]
		message['累计长按识别人数'] = nums[3]
		yield message

def save_file(path,message):
	with open(path,'a') as f:
		f.write(message['群'] + ' ' + message['今日长按识别人数'] + ' ' + message['累计长按识别人数'] + '\n')

if __name__ == '__main__':
	current_path = os.path.realpath(__file__)
	# 获取当前文件的父目录
	father_path = os.path.realpath(os.path.dirname(current_path) + os.path.sep + ".")
	path = os.path.join(father_path, 'message_gulu.txt')
	messages = get_message()
	if messages == None:
		print('fail')
	else:
		for message in messages:
			save_file(path,message)