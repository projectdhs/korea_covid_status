import requests, re, json
from bs4 import BeautifulSoup
import time, random
from datetime import timezone, timedelta, datetime

import time
import json

n_search="https://search.naver.com/search.naver"
n_msearch="https://m.search.naver.com"
timestamp=time.time()
tz = timezone(timedelta(hours=9))
dt_9 = datetime.fromtimestamp(timestamp, tz)

year=dt_9.year
month="{:%m}".format(dt_9)
day="{:%d}".format(dt_9)

title_list = ['확진환자', '격리해제', '사망자', '검사진행']
is_checked = [False, False, False, False]


location_list=['제주', '경남', '경북', '전남', '전북', '충남', '충북', '강원', '경기', '세종', '울산', '대전', '광주', '인천', '대구', '부산', '서울', '검역']


local_list1=["서울","인천","경기"]
hap_name="합계"
gum_name="검역"

hap1=0
hap2=0
hap3=0


hap_death=0
tod_death=0
need_broadcast=0
do_covid=1
error_cnum=0
find_covid=0

u_inspectcount=0
inspectcount=0

mes=''

while do_covid==1:
	if(find_covid>20):
		tel_mes='%s년 %s월 %s일의 코로나 19 감염 현황은 아래의 링크를 통해 확인하여주세요.\n불편을 드려 죄송합니다.\n현재 서비스 정비 중에 있습니다.\n\nhttps://search.naver.com/search.naver?ie=UTF-8&query=코로나19&sm=chr_hty'%(year,month,day)
		
		do_covid=0
		break
	if(error_cnum>=2):
		do_covid=0
	try:
		payload={'where' : 'nexearch', 'sm' : 'tab_etc', 'qvt' : 0, 'query' : '코로나19'}
		s = requests.get(n_search, params=payload, headers={'referer' : 'https://www.naver.com/', 'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36', 'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-encoding' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'})
		
	except Exception as e:
		print(e)
		sleep_t1=random.uniform(25,36)
		time.sleep(sleep_t1)
		error_cnum+=1
		continue
	if(s.status_code!=200):
		print("잠시후 다시 요청합니다.")
		sleep_t2=random.uniform(24,32)
		time.sleep(sleep_t1)
		error_cnum+=1
		continue
	
	try:
		soup = BeautifulSoup(s.text,'html.parser')

		kor_title_name = soup.select('.info_title')
		kor_allcount = soup.select('.info_num')
		kor_todcount = soup.select('.info_variation ')
		for idx, title in enumerate(kor_title_name):
			if(title.text == title_list[0] and is_checked[0] == False):
				hap_covid = re.sub(pattern='[^0-9]', repl='', string=kor_allcount[idx].text)
				hap_today_covid=re.sub(pattern='[^0-9]', repl='', string=kor_todcount[idx].text)
				is_checked[0] = True

			elif(title.text == title_list[1] and is_checked[1] == False):
				hap_clearCovid=re.sub(pattern='[^0-9]', repl='', string=kor_allcount[idx].text)
				tod_clear=re.sub(pattern='[^0-9]', repl='', string=kor_todcount[idx].text)
				is_checked[1] = True

			elif(title.text == title_list[2] and is_checked[2] == False):
				hap_death=re.sub(pattern='[^0-9]', repl='', string=kor_allcount[idx].text)
				tod_death=re.sub(pattern='[^0-9]', repl='', string=kor_todcount[idx].text)
				is_checked[2] = True

			elif(title.text == title_list[3] and is_checked[3] == False):
				inspectcount=re.sub(pattern='[^0-9]', repl='', string=kor_allcount[idx].text)
				u_inspectcount=re.sub(pattern='[^0-9]', repl='', string=kor_todcount[idx].text)
				is_checked[3] = True

			
	except Exception as e:
		print(e)
		sleep_t4=random.uniform(25,38)
		time.sleep(sleep_t4)
		error_cnum+=1
		continue
	payload = {'where' : 'nexearch', 'pkid' : 9005, 'key' : 'diffV2API', '_callback' : '_au_covid19_global_status'}
	req_count = requests.get(n_msearch + '/p/csearch/content/nqapirender.nhn', params = payload, headers={'referer' : 'https://search.naver.com/search.naver?ie=UTF-8&query=%EC%BD%94%EB%A1%9C%EB%82%9819', 'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36', 'accept' : '*/*', 'accept-encoding' : 'gzip, deflate, br', 'accept-language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'})
	jso = json.loads(req_count.text.split("status(")[1].split(");")[0])
	jsoList = jso ['result'] ['list']
	todList = allnum = re.sub(pattern='[^0-9]', repl='', string=jsoList [len(jsoList)-1] ['total'])
	local_hap= re.sub(pattern='[^0-9]', repl='', string=jsoList [len(jsoList)-1] ['local'])
	global_hap = re.sub(pattern='[^0-9]', repl='', string=jsoList [len(jsoList)-1] ['oversea'])
	todDate = jsoList [len(jsoList)-1] ['date']

	reg_name = soup.select('.align_center > .text')
	reg_allcount = soup.select('.align_right > .text')
	reg_todcount = soup.select('.align_right > .confirmed_case')
	

	need_broadcast=1

	for j in range(0, 18):
		
		increase = re.sub(pattern='[^0-9]', repl='', string=reg_todcount[j].text)
		location = reg_name[j].text.strip()
		

		loc_hap = re.sub(pattern='[^0-9]', repl='', string=reg_allcount[j].text)
		print("%s : %s명 (+%s)"%(location,format(int(loc_hap),',d'),format(int(increase),',d')))

		if(location == gum_name):
			hap3=int(increase)
		local_chk=1
		for mylocal in local_list1:
			if(location==mylocal):
				hap1+=int(increase)
				local_chk=0
		if(local_chk!=0 and location!=gum_name):
			hap2+=int(increase)

	do_covid=0



if(need_broadcast==1):
	#mes는 tts용으로 제작해놓은 것입니다.
	mes="안녕하세요. 좋은 아침입니다. 새로운 소식이 도착하였습니다. %s년 %s월 %s일 0시 기준, 코로나 19 국내 확진자는 %s명 이고, 해외 확진자는 %s명으로, 전체 신규 확진자는 %s명입니다. 지역별로 나열해보면 수도권에서 %s명의 확진자가 발생하였고, 비수도권에서 %s명의 확진자가 발생하였습니다."%(year,month,day,local_hap,global_hap,hap_today_covid, str(hap1), str(hap2))

	need_broadcast=0
	
	
	tel_mes_pinit="\n신규 환자: %s명\n%s년 %s월 %s일 코로나19 감염 현황\n\n"%(format(int(hap_today_covid),',d'),year,month,day)
	tel_mes="확진환자: %s명 (%s명 ▲)\n격리해제: %s명 (%s명 ▲)\n사망자: %s명 (%s명 ▲)\n\n"%(format(int(hap_covid),',d'), format(int(hap_today_covid),',d'),format(int(hap_clearCovid),',d'),format(int(tod_clear),',d'),format(int(hap_death),',d'),tod_death)
	tel_mes2="국내발생 신규: %s명\n해외유입 신규: %s명\n(수도권: %s명, 비수도권: %s명)\n\n"%(format(int(local_hap),',d'), global_hap,hap1,hap2)
	
	
	print(tel_mes_pinit+tel_mes+tel_mes2)
