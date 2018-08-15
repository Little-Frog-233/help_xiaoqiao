# coding: utf-8
import requests
import re
import demjson
import os
from pyquery import PyQuery as pq

url = 'https://mp.weixin.qq.com/misc/useranalysis?=&token=1285731513&lang=zh_CN'

cookie = 'pgv_pvi=9379506176; pgv_pvid=441636726; pt2gguin=o2300734143; RK=iAo0DiAB7E; ptcz=cfdadb06387fc6988343ad29621252b7a3fe990d93d7ac0854cd76ae744ad141; ua_id=oBrUdy284sGWNtjXAAAAAPoTAj2ViZA132z-gGd86rg=; mm_lang=zh_CN; pgv_si=s763461632; uuid=e0a05a1cda39dde284c126b1a1eb6929; ticket=024dd4db228a32a9991f435a1baacde8955d1d40; ticket_id=gh_9f0017502197; cert=T7erAXl7f5ChcnoP4MBj66ygzgMJfQcu; data_bizuin=3287916939; bizuin=3298915493; data_ticket=rNLwfIQ6js+EBovO67tQCGgqWS0ZycBe5aLveeTR9MkjaYtOZWsVOcWhIk46Pfre; slave_sid=TjJUa0E3SG5rUVNHSkxVbGh0SWplRzBaeUM3WjZOQl83YURIZ2t5SVlhYkI4cVFXMVp6MEo2eUxBZFVkMTJnemJrVFhtRFQ1TFNNQ3NsdXByUVRYZzNxeFFzeWljb0NOYWU2MlFPNHZVNUkyV3BoajhtQ2p0djh3ZHVvRUdPSzhBZHJlT2N1Vk9VOTZ6QTJK; slave_user=gh_9f0017502197; xid=02a8b88ddcd2c4d2dfb1f934a6c27417; openid2ticket_oi6H5w8kquZ4UUdJ4m3chTEJgHkk=Nkc1SzF3rKxvDGYfIeloUvgHsZUEEBxQDL/j1SJhc6Y='

headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	'Host': 'mp.weixin.qq.com',
	'Referer': 'https://mp.weixin.qq.com/misc/useranalysis?=&token=1285731513&lang=zh_CN',
	'Cookie': cookie
}


def get_message():
	html = requests.get(url, headers=headers)
	if html.status_code != 200:
		return None
	text = html.text
	doc = pq(text)
	results = doc('script').items()
	for result in results:
		if result.attr('type') == 'text/javascript':
			tmp = result.text()
			if 'window.cgiData' in tmp:
				res = tmp[17:].split(';')[0]
				res = re.sub('\'', '\"', res)
				res = demjson.decode(res)
				results = res['list']
				results = results[0]['list']
				for result in results:
					message = {}
					message['日期'] = result.get('date')
					message['取消关注人数'] = result.get('cancel_user')
					message['新关注人数'] = result.get('new_user')
					message['净关注人数'] = result.get('netgain_user')
					message['累积关注人数'] = result.get('cumulate_user')
					yield message


def save_file(path, message):
	with open(path, 'a') as f:
		f.write(message['日期'] + ' ' + str(message['新关注人数']) + ' ' + str(message['取消关注人数']) + ' ' + str(
			message['净关注人数']) + ' ' + str(message['累积关注人数']) + '\n')


if __name__ == '__main__':
	current_path = os.path.realpath(__file__)
	# 获取当前文件的父目录
	father_path = os.path.realpath(os.path.dirname(current_path) + os.path.sep + ".")
	path = os.path.join(father_path, 'message_wechat.txt')
	messages = get_message()
	if messages == None:
		print('fail')
	else:
		for message in messages:
			save_file(path, message)
