#! /usr/bin/env python
#encoding=utf-8
import smtplib
from email.mime.text import MIMEText

def send_mail(text, active_map):
    active_content = ''
    if active_map != None:
        value_list = active_map.values()
        active_content = '<br>'.join(value_list)
    text = '报告存存，阿就西又在水知乎啦！！！ %s: <br> %s' % (text, active_content)
    #text = text.encode('utf-8')
    msg = MIMEText(text, _subtype='html', _charset='utf-8')
    msg['Accept-Language'] = "zh-CN"
    msg['Accept-Charset'] = "ISO-8859-1,utf-8"

    msg['Subject'] = u'阿就西在知乎有新的动态'
    sender = 'xiangzi777@sjtu.edu.cn'
    receivers = ['xiangzi777@sjtu.edu.cn', 'bubble_chun@sjtu.edu.cn']
    #sender = 'dengxiang.liu@datayes.com'
    #receiver = 'dengxiang.liu@datayes.com'
    msg['From'] = sender
    msg['To'] = ','.join(receivers)

    s = smtplib.SMTP('smtp.datayes.com')
    #s = smtplib.SMTP('mail.sjtu.edu.cn')
    s.sendmail(sender, receivers, msg.as_string()) 

active_pre_list = {}
active_now_list = {}

pre_file_obj = open('active_pre.log', 'r')
now_file_obj = open('active_now.log', 'r')

for num, line in enumerate(pre_file_obj):
    link = line.strip().split('\t')[2]
    active_pre_list[link] = line

for num, line in enumerate(now_file_obj):
    link = line.strip().split('\t')[2]
    if link not in active_pre_list:
        active_pre_list[link] = line
        active_now_list[link] = line

pre_file_obj.close()
now_file_obj.close()

if len(active_now_list) > 0:
    pre_file_obj = open('active_pre.log', 'w')
    for link in active_pre_list:
        pre_file_obj.write(active_pre_list[link])
    print "have new active"
    pre_file_obj.close()
    send_mail('new', active_now_list)
    print "send email"
else:
    print "have no new active"
    #send_mail('no', None)
