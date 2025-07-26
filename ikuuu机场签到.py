"""
new Env("ikuuu机场")
cron 22 5 0 * * *
环境变量名称 huazhu_cookies
"""

#使用方法
#添加环境变量 ikuuuEMAIL 值为邮箱
#添加环境变量 ikuuuPASSWD 值为密码

import requests, json, re, os
session = requests.session()
# 配置用户名（一般是邮箱）
email = os.environ.get('ikuuuEMAIL')
# 配置用户名对应的密码 和上面的email对应上
passwd = os.environ.get('ikuuuPASSWD')

login_url = 'https://ikuuu.ch/auth/login'
check_url = 'https://ikuuu.ch/user/checkin'
info_url = 'https://ikuuu.ch/user/profile'

header = {
        'origin': 'https://ikuuu.ch',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
data = {
        'email': email,
        'passwd': passwd
}
try:
    print('进行登录...')
    response = json.loads(session.post(url=login_url,headers=header,data=data).text)
    print(response['msg'])
    # 获取账号名称
    info_html = session.get(url=info_url,headers=header).text
    # 进行签到
    result = json.loads(session.post(url=check_url,headers=header).text)
    print(result['msg'])
    content = result['msg']
    # 进行推送
    push_url = f'https://api.day.app/{os.environ.get("BARK_PUSH")}/iKuuu自动签到/{content}'
    requests.post(url=push_url)
    print('推送成功')
except:
    content = '签到失败'
    print(content)
    push_url = f'https://api.day.app/{os.environ.get("BARK_PUSH")}/iKuuu自动签到/{content}'
    requests.post(url=push_url)
