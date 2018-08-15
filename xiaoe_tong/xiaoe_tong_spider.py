# coding: utf-8
import requests
import os



url_base = "https://admin.xiaoe-tech.com/finance_manage/get_collect?picked_date=2018-08&page=%d"
cookie = 'appsc=appXFN9kGvz4286; XIAOEID=7b522c0f137f8703745eeb1de457d241; xe_username=15201702995; xe_passwd=xmcmk39320177; tgw_l7_route=77e4ba278a5fb8674c841243e94e54eb; cookie_channel=pingpai_area; Hm_lvt_081e3681cee6a2749a63db50a17625e2=1534217652,1534313823; appsc=appXFN9kGvz4286; with_app_id=appXFN9kGvz4286; Hm_lpvt_081e3681cee6a2749a63db50a17625e2=1534313837; laravel_session=eyJpdiI6IjB2M1RXVU5FSkhKa05cL0FzcTFSN29RPT0iLCJ2YWx1ZSI6ImFsQzhobjk1SThMdzk0dzRTMFg0TVFKZHVTcWg2UTFINTZiZUNrd2huejZ1elkwSnZCMEFlZmtlYTBLdzgyZ3FEMmNncEsyOE9sMzJZbUt1VmhuXC9sdz09IiwibWFjIjoiNTM5OWQwYTY1OTEyYzJmODMzNjRlMDJkZjU1MzZlMzM2NGFjZGNkNzk0Y2IxMDc2YWZmYzllYmM2NmIyMTQwZiJ9'

headers = {'Host': 'admin.xiaoe-tech.com',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
           'Referer': 'https://admin.xiaoe-tech.com/finance_manage/account_list',
           'Cookie':cookie,
           'X-Requested-With': 'XMLHttpRequest'}

def get_message(page):
    url = url_base%page
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        res = html.json()
        results = res.get('data').get('result')
        message = {}
        for result in results:
            message['结算日期'] = result.get('check_date')
            message['收入(元)'] = str(result.get('income_money'))[:-2] if result.get('income_money') != None else 0
            message['交易数'] = result.get('income_deal_count')
            yield message

def save_data(message,save_path):
    with open(save_path,'a') as f:
        f.write(message['结算日期'] + ' ' + str(message['收入(元)']) + ' ' + str(message['交易数']) + '\n')


if __name__ == '__main__':
    current_path = os.path.realpath(__file__)
    # 获取当前文件的父目录
    father_path = os.path.realpath(os.path.dirname(current_path) + os.path.sep + ".")
    file_path = os.path.join(father_path, 'message.txt')
    for page in range(1,3):
        messages = get_message(page)
        for message in messages:
            save_data(message,file_path)
