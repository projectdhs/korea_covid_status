from lxml import html
import requests
import re
from datetime import timezone, timedelta, datetime
import time

local_list1=["서울","인천","경기"]
location_list=['제주', '경남', '경북', '전남', '전북', '충남', '충북', '강원', '경기', '세종', '울산', '대전', '광주', '인천', '대구', '부산', '서울', '검역']

hap1 = 0 #수도권 확진자 수
hap2 = 0 #비수도권 확진자 수
hap3=0
timestamp=time.time()
tz = timezone(timedelta(hours=9))
dt_9 = datetime.fromtimestamp(timestamp, tz)

year=dt_9.year
month="{:%m}".format(dt_9)
day="{:%d}".format(dt_9)

today=str(year)+str(month)+str(day)

http_header = {"referer" : "http://ncov.mohw.go.kr/bdBoardList.do?brdId=1&brdGubun=13",
               "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
               "accept-encoding" : "gzip, deflate",
               "accept-language" : "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"}

page = requests.get('http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=', headers=http_header)
page.encoding = 'utf-8'
tree = html.fromstring(page.text)

covid_date = tree.xpath('//*[@id="content"]/div/div[2]/p/span/text()')[0]
if(covid_date.split(' ')[1] == month + '.' + day + '.'):
    print("코로나 정보를 가져오는 중입니다.\n")
else:
    print("틀림")
    exit()

hap_today_covid = tree.xpath('//*[@id="content"]/div/div[5]/table/tbody/tr[1]/td[1]/text()')[0]
hap_covid = tree.xpath('//*[@id="mapAll"]/div/ul/li[5]/div[2]/span/text()')[0]
hap_death = tree.xpath('//*[@id="mapAll"]/div/ul/li[1]/div[2]/span/text()')[0]
tod_death = tree.xpath('//*[@id="mapAll"]/div/ul/li[2]/div[2]/span/text()')[0]
local_hap = tree.xpath('//*[@id="content"]/div/div[5]/table/tbody/tr[1]/td[2]/text()')[0]
global_hap = tree.xpath('//*[@id="content"]/div/div[5]/table/tbody/tr[1]/td[3]/text()')[0]

locationName_html = tree.xpath('//*[@id="main_maplayout"]/button/span[1]/text()')
locationHap_html = tree.xpath('//*[@id="main_maplayout"]/button/span[2]/text()')
locationToday_html = tree.xpath('//*[@id="main_maplayout"]/button/span[3]/text()')


#print(tod_death)
#print(len(tod_death))
hap_today_covid = re.sub(r'[^0-9]', '', hap_today_covid)
hap_covid = re.sub(r'[^0-9]', '', hap_covid)
hap_death = re.sub(r'[^0-9]', '', hap_death)
tod_death = re.sub(r'[^0-9]', '', tod_death)
local_hap = re.sub(r'[^0-9]', '', local_hap)
global_hap = re.sub(r'[^0-9]', '', global_hap)
need_broadcast = 1
# print(hap_today_covid)
# print(hap_covid)
# print(hap_death)
# print(tod_death)
# print(local_hap)
# print(global_hap)

for myI in range(0,len(locationName_html)):
    location = locationName_html[myI]
    loc_hap = re.sub(r'[^0-9]', '',locationHap_html[myI])
    increase = re.sub(r'[^0-9]', '', locationToday_html[myI])

    local_chk = 0
    for mylocal in local_list1:
        if(location == mylocal):
            hap1 += int(increase)
            local_chk = 1
    if(local_chk == 0 and location != '검역'):
        hap2 += int(increase)





if(need_broadcast == 1):
    # mes="%s년 %s월 %s일 0시 기준, 코로나 19 국내 확진자는 %s명 이고, 해외 확진자는 %s명으로, 전체 신규 확진자는 %s명입니다. 국내 확진자를 지역별로 나열해보면 수도권에서 %s명의 확진자가 발생하였고, 비수도권에서 %s명의 확진자가 발생하였습니다. 종료하시려면 종료라고 말씀해주세요."%(year,month,day,local_hap,global_hap,hap_today_covid, str(hap1), str(hap2))
    # print(mes) ## tts용으로 필요하면 사용하세요.
    tel_mes = ''
    tel_mes_pinit="신규 환자: %s명\n%s년 %s월 %s일 코로나19 감염 현황\n\n"%(format(int(hap_today_covid),',d'),year,month,day)
    tel_mes += "확진환자: %s명 (%s명 ▲)\n"%(format(int(hap_covid),',d'), format(int(hap_today_covid),',d'))
    tel_mes += "사망자: %s명 (%s명 ▲)\n"%(format(int(hap_death),',d'),tod_death)
    tel_mes2="\n국내발생 신규: %s명\n해외유입 신규: %s명\n(수도권: %s명, 비수도권: %s명)\n\n"%(format(int(local_hap),',d'), format(int(global_hap),',d'),format(int(hap1),',d'),format(int(hap2),',d'))
    print(tel_mes_pinit+tel_mes+tel_mes2)
    exit()


## 변수 목록 (참고용)
hap_today_covid = '신규확진자'
hap_covid = '누적 확진 환자'
hap_death = "누적 사망자"
tod_death = '오늘 사망자'
local_hap = '국내발생 신규'
global_hap = '해외발생 신규'
hap1 = '수도권 발생 총합'
hap2 = '비수도권 발생 총합'

##for문
loc_hap = '지역발생 총합'
increase = '지역발생 증가'
