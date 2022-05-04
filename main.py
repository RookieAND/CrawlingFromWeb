from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd

from parseCategory import inspect_category
import datetime

wd = webdriver.Chrome('./chromedriver.exe')
wd.get("http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?range=1&orderClick=DAA")

# 각 분야 별 이름과 해당 분야 별 베스트 셀러 항목을 로드하기 위한 함수 명을 저장하는 list를 생성.
category_name, category_func = [], []

# 각 분야 별 베스트 셀러 목록을 담은 리스트를 눌러 새로운 창을 띄우게 함.
# a 태그 내의 javascript 함수를 스크랩 하며, 책 분야 별로 함수를 실행시켜 각 분야 별 베스트 셀러 목록으로 넘어가게 한다.
for category_tag in wd.find_elements(by=By.CSS_SELECTOR, value="a[href*='goCateList']"):
    category_func.append(category_tag.get_attribute('href').replace("javascript:", ""))
    category_name.append(category_tag.text.strip())

# 전체 도서 목록을 조금 더 보기 좋게 나누어서 정렬시킴.
print("[!] 교보 문고 전체 도서 분야 목록은 아래와 같습니다...")
print(*category_name[:len(category_name) // 2], sep=', ', end="\n")
print(*category_name[len(category_name) // 2:], sep=', ', end="\n")
user_request = input("\n원하시는 책 분야를 말씀해주세요. 상단의 목록에서만 가능합니다: ").strip()

if user_request in category_name:
    now = datetime.datetime.now()
    nowdate = now.strftime('%Y-%m-%d_%H-%M-%S')

    print(f"{user_request} 분야에 해당되는 주간 베스트셀러 목록을 불러옵니다...")
    print(f"{user_request} 분야 탐색 일자 : {nowdate}")
    book_section = category_name.index(user_request)
    result = inspect_category(category_func[book_section], user_request)

    cb_tbl = pd.DataFrame(result, columns=('cate_name', 'book_title', 'book_author', 'book_publisher', 'book_pubdate'))
    cb_tbl['rank'] = cb_tbl.index + 1
    print(cb_tbl)
    cb_tbl.to_csv(f'./result_{category_name[book_section]}_{nowdate}.csv', encoding='utf-8-sig', mode='w', index=True)
    print(f"성공적으로 분석된 파일이 저장되었습니다. [이름 : result_{category_name[book_section]}_{nowdate}.csv]")
else:
    print(f"입력하신 {user_request} 분야는 존재하지 않는 분야입니다.")
