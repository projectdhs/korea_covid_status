파이썬 버전 3.7 이상에서 실행하는 것을 권장합니다.

필요한 패키지 설치 방법:
pip3 install requests lxml

실행방법:
python3 get_covid.py

질병관리청 사이트에 당일 데이터는 9시 30분 ~ 10시 사이에 올라오니, 오전 10시 이후에 코드를 실행해보는 것을 추천드립니다.
http://ncov.mohw.go.kr/ 에 데이터가 올라와있어야 합니다.
크롤링 특성상, 사이트의 구조가 변경되면 개발한 크롤링 코드로 코로나 정보를 불러오지 못할 수도 있습니다.
문제가 있다면 풀리퀘스트나 이슈를 만들어주시면 수정하겠습니다.

업데이트 내역
21-09-30: v0.1 출시
22-06-28: 네이버 크롤링 => 질병관리청 코로나 사이트에서 크롤링해오는 방식으로 변경

![initial]([https://user-images.githubusercontent.com/blahblah~~/.PNG](https://raw.githubusercontent.com/projectdhs/korea_covid_status/main/run_image.png))
