# -*- coding:utf-8 -*-

import configparser as cp
import json
from urllib import request, parse

import telegram


def telegram_alert(d, g, v):
    t_tkn = ini_reader.get('Telegram', 'token')
    t_id = ini_reader.get('Telegram', 'id')

    tbot = telegram.Bot(t_tkn)
    alert_msg = '```\n!===== PM Notice =====!'
    alert_msg += '\nTime:\t' + str(d[1]) + ' → ' + str(d[0][11:])
    for w in ['pm10', 'pm25']:
        if g[w][0]>2: g[w][0] = '*' + str(g[w][0]) + '*'
        if g[w][1]>2: g[w][1] = '*' + str(g[w][1]) + '*'
        alert_msg += '\n' + w + ':\t' + str(v[w][1]) + '(' + str(g[w][1]) + ')' + '\t→\t' + str(v[w][0]) + '(' + str(g[w][0]) + ')'
    alert_msg += '\nCAI: ' + str(v['khai'][0]) + '(' + str(g['khai'][0]) + ')'
    alert_msg += '\n=======================```'

    tbot.sendMessage(chat_id=t_id, text=alert_msg, parse_mode='Markdown')
    print(alert_msg)

ini_reader = cp.ConfigParser()
ini_reader.read('config.ini', encoding='utf-8-sig')

openapi_station_name = parse.quote(ini_reader.get('API', 'station_name'))
openapi_service_key = str(ini_reader.get('API', 'service_key', raw=True))

url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?stationName='+ openapi_station_name + '&dataTerm=daily&pageNo=1&numOfRows=5&ServiceKey='+ openapi_service_key +'&ver=1.3&_returnType=json'
pm_urldata = request.urlopen(url).read()
pm_jsondata = json.loads(pm_urldata.decode('utf-8'))['list']


warn = {'pm10':False,
        'pm25':False}

pm_grade, pm_value = {}, {}
data_time = [pm_jsondata[i][str('dataTime')] for i in range(2)]

for word in ['pm25', 'pm10','khai']:
    pm_grade[word] = [0,0]
    pm_value[word] = [0,0]
    for j in [0, 1]:
        if word == 'khai':
            pm_grade[word][j] = int(pm_jsondata[j][str(word + 'Grade')])
        else:
            pm_grade[word][j] = int(pm_jsondata[j][str(word + 'Grade1h')])
        pm_value[word][j] = int(pm_jsondata[j][str(word + 'Value')])

if sum([a>2 for a in pm_grade['pm10']+pm_grade['pm25']]):
    telegram_alert(data_time, pm_grade, pm_value)
