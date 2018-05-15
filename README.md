# telegram_pm_notifier
## 개요
미세먼지 수위가 '위험'으로 올라가거나, '위험'에서 내려올 경우 이를 사용자에게 Telegram으로 알려주는 봇

## 준비물
* python-telegram-bot
* [텔레그렘 봇](https://core.telegram.org/bots)
  * 봇 API 키 ([Telegram] - token )
  * 클라이언트 ID ([Telegram] - id)

* 근처 미세먼지 측정소 이름 ([API] - station_name)
* [공공데이터포털](https://www.data.go.kr/) API 키 ([API] - service_key)

참고사항:
* crontab이나 작업 스케쥴러에 등록할것.
* 미세먼지 측정소의 자료 업데이트는 매 정각 15분쯤에 이뤄진다.

## 참고자료
* [나만의 웹 크롤러 만들기](https://beomi.github.io/gb-crawling/posts/2017-04-20-HowToMakeWebCrawler-Notice-with-Telegram.html)

* [crontab](https://zetawiki.com/wiki/%EB%A6%AC%EB%88%85%EC%8A%A4_%EB%B0%98%EB%B3%B5_%EC%98%88%EC%95%BD%EC%9E%91%EC%97%85_cron,_crond,_crontab)