
# -*- encoding:utf-8 -*-
import random
 
import requests
import json
import datetime
import calendar
import time
from bs4 import BeautifulSoup
from zhdate import ZhDate
import emoji
import urllib.request
import urllib.parse
 
class SendMessage():
    def __init__(self):
        rq = self.get_rq()
        tq = self.get_tq()
        jnr = self.get_jnr()
        sr = self.get_sr()
        body =rq+"\n"+tq+"\n"+jnr+"\n"+sr;
        self.dataJson ={"first":"哈喽,宝贝！",
                        "body":body+" ",
                        "remark":self.get_qh()[random.randint(0, len(self.get_qh())-2)]+" "
                        }
        self.appID = 'wxb4b7d44e40c6483d'
        self.appsecret = '1df402c9679d35eded78f50a8bc3fa18'
        self.template_id = 'h5gLEvvGk7tX4R5eOM8i9QNF7W0kVbv8rqdDDvFb-5s'//模板id
        self.access_token = self.get_access_token()
        self.opend_ids = self.get_openid()
 
 
    def get_qh(self):
        qhStr="";
        file_object1 = open("D:\workspaces\python/venv\qh.txt", 'r',encoding="utf-8")
        try:
            while True:
                line = file_object1.readline()
                if line:
                     qhStr+=line.rstrip()+"#"
                else:
                    break
        finally:
            file_object1.close()
        return qhStr.split("#")
 
    def get_rq(self):
        sysdate = datetime.date.today()  # 只获取日期
        now_time = datetime.datetime.now()  # 获取日期加时间
        week_day = sysdate.isoweekday()  # 获取周几
        week = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
        return '现在是' + str(now_time)[0:16] + ',' + week[week_day - 1]+"。"
 
    def get_tq(self):
        url = 'http://www.weather.com.cn/weather/101010300.shtml'
        sysdate = datetime.date.today()
        r = requests.get(url, timeout=30)  # 用requests抓取网页信息
        r.raise_for_status()  # 可以让程序产生异常时停止程序
        r.encoding = r.apparent_encoding  # 编码格式
        html = r.text
        final_list = []
        soup = BeautifulSoup(html, 'html.parser')  # 用BeautifulSoup库解析网页 #soup里有对当前天气的建议
        body = soup.body  # 从soup里截取body的一部分
        data = body.find('div', {'id': '7d'})
        ul = data.find('ul')
        lis = ul.find_all('li')
 
        for day in lis:
            temp_list = []
 
            date = day.find('h1').string  # 找到日期
            if date.string.split('日')[0] == str(sysdate.day):
                temp_list = []
 
                date = day.find('h1').string  # 找到日期
                temp_list.append(date)
 
                info = day.find_all('p')  # 找到所有的p标签
                temp_list.append(info[0].string)
 
                if info[1].find('span') is None:  # 找到p标签中的第二个值'span'标签——最高温度
                    temperature_highest = ' '  # 用一个判断是否有最高温度
                else:
                    temperature_highest = info[1].find('span').string
                    temperature_highest = temperature_highest.replace('℃', ' ')
 
                if info[1].find('i') is None:  # 找到p标签中的第二个值'i'标签——最高温度
                    temperature_lowest = ' '  # 用一个判断是否有最低温度
                else:
                    temperature_lowest = info[1].find('i').string
                    temperature_lowest = temperature_lowest.replace('℃', ' ')
 
                temp_list.append(temperature_highest)  # 将最高气温添加到temp_list中
                temp_list.append(temperature_lowest)  # 将最低气温添加到temp_list中
 
                final_list.append(temp_list)  # 将temp_list列表添加到final_list列表中
                return '天气情况是' + final_list[0][1] + ',温度是' + final_list[0][3].strip() + '~' + \
                               final_list[0][2].strip() + '摄氏度。'
 
    def get_sr(self):
        today = datetime.datetime.now()
        data_str = today.strftime('%Y-%m-%d')
        oneDay = ZhDate(today.year, 9, 6).to_datetime()
        difference = oneDay.toordinal() - today.toordinal()
        if difference >0 :
            return ("距离我滴宝生日,还有 %d 天。" % (difference))
        elif difference==0:
            return ('生日快乐！！🍓我滴宝🍓')
        else:
            return ('还要很久才过生日,别琢磨啦！')
 
    def get_jnr(self):
        today = datetime.datetime.now()
        data_str = today.strftime('%Y-%m-%d')
        oneDay = ZhDate(2020, 12, 29).to_datetime()
        d =  today.toordinal()-oneDay.toordinal()
        return ("\t我们已经相爱 %d 天。\n\t%d 年 %d 个月 %d 天。\n\t%d 个月 %d 天。\n\t%d 周 %d 天。" % (d,d // 365, (d % 365) // 30, (d % 365) % 30, d // 30, d % 30, d // 7, d % 7))
 
    def get_access_token(self):
        """
        获取微信公众号的access_token值
        """
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.\
            format(self.appID, self.appsecret)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
        }
        response = requests.get(url, headers=headers).json()
        access_token = response.get('access_token')
        return access_token
 
    def get_openid(self):
        """
        获取所有粉丝的openid
        """
        next_openid = ''
        url_openid = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s' % (self.access_token, next_openid)
        ans = requests.get(url_openid)
        open_ids = json.loads(ans.content)['data']['openid']
        return open_ids
 
    def sendmsg(self):
        """
        给所有粉丝发送文本消息
        """
        url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(self.access_token)
 
        if self.opend_ids != '':
            for open_id in self.opend_ids:
                body = {
                        "touser": open_id,
                        "template_id": self.template_id,
                        "url": "https://www.baidu.com/",
                        "topcolor": "#FF0000",
                        "data": {
                            "first": {
                                "value": self.dataJson.get("first"),
                                "color": "#FF99CC"
                            },
                            "body": {
                                "value": self.dataJson.get("body"),
                                "color": "#000000"
                            },
                            "remark": {
                                "value": self.dataJson.get("remark"),
                                "color": "#66CCFF"
                            }
                        }
                    }
                data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))
                response = requests.post(url, data=data)
                # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
                result = response.json()
                print(result)
        else:
            print("当前没有用户关注该公众号！")
 
if __name__ == "__main__":
    sends = SendMessage()

————————————————
版权声明：本文为CSDN博主「山西的洛阳」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_37266628/article/details/126499175
