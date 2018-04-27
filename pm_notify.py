# -*- coding:utf-8 -*-
# Telegram pm notifier by hehehwang 2018.04.27
import configparser as cp
import json
from urllib import request, parse

import telegram

def telegram_alert(d, g, v):
    t_tkn = ini_reader.get('Telegram', 'token')
    t_id = ini_reader.get('Telegram', 'id')
    tbot = telegram.Bot(t_tkn)

    for j in ['pm10', 'pm25', 'khai']:
        for k in [0, 1]:
            if g[j][k] > 2: g[j][k] = '*' + str(g[j][k]) + '*'

    # if you don't like code-like notifing style, you may delete '```' lines
    alert_msg = ''
    alert_msg += '```'
    alert_msg += '\n!===== PM Notice =====!'
    alert_msg += '\nTime:\t' + str(d[1]) + ' → ' + str(d[0][11:])
    for w in ['pm10', 'pm25']:
        alert_msg += '\n' + w + ':\t' + str(v[w][1]) + '(' + str(g[w][1]) + ')' + ' → ' + str(v[w][0]) + '(' + str(g[w][0]) + ')'
    alert_msg += '\nCAI: ' + str(v['khai'][0]) + '(' + str(g['khai'][0]) + ')'
    alert_msg += '\n======================='
    alert_msg += '```'

    tbot.sendMessage(chat_id=t_id, text=alert_msg, parse_mode='Markdown')
    print(alert_msg)

ini_reader = cp.ConfigParser()
# if you are going to run this script on terminal(i.e. contab),
# you should write full-directory of config file
# ex) /root/home/config.ini
ini_reader.read('config.ini', encoding='utf-8-sig')

openapi_station_name = parse.quote(ini_reader.get('API', 'station_name'))
openapi_service_key = str(ini_reader.get('API', 'service_key', raw=True))

url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?stationName='+ openapi_station_name + '&dataTerm=daily&pageNo=1&numOfRows=5&ServiceKey='+ openapi_service_key +'&ver=1.3&_returnType=json'
pm_urldata = request.urlopen(url).read()
pm_jsondata = json.loads(pm_urldata.decode('utf-8'))['list']

pm_grade, pm_value = {}, {}
data_time = [pm_jsondata[i][str('dataTime')] for i in range(2)]

for word in ['pm25', 'pm10','khai']:
    pm_grade[word] = [0,0]
    pm_value[word] = [0,0]
    for i in [0, 1]:
        if word == 'khai':
            pm_grade[word][i] = int(pm_jsondata[i][str(word + 'Grade')])
        else:
            pm_grade[word][i] = int(pm_jsondata[i][str(word + 'Grade1h')])
        pm_value[word][i] = int(pm_jsondata[i][str(word + 'Value')])

if sum([a>2 for a in pm_grade['pm10']+pm_grade['pm25']]):
    telegram_alert(data_time, pm_grade, pm_value)
