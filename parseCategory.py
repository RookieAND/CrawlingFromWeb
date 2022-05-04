from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from parsebook import get_book_info


# 각 분야 별 베스트 셀러 목록을 조사하고, 총 20개 (1~20등까지) 의 책 정보를 크롤링하는 과정.
def inspect_category(cate_func, cate_name):
        crawl_result = []

        wd = webdriver.Chrome('./chromedriver.exe')
        wd.get("http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?range=1&orderClick=DAA")
        wd.execute_script(cate_func)

        # 베스트 셀러 페이지 자체로는 원활한 크롤링이 어려우므로, 해당 책의 바코드를 list로 먼저 담음.
        # 책의 바코드를 통해 해당 책의 상세 구매 페이지로 넘어갈 수 있으며, 그곳에서 최종 크롤링을 진행할 예정.
        html = wd.page_source
        soup_bestseller = bs(html, 'html.parser')
        barcodes_list = [input_tag.get('value') for input_tag in soup_bestseller.find_all(attrs={"name": "barcode"})]

        # 각 항목 별 베스트셀러의 경우 1등부터 20등까지 나열됨 (20위까지만 크롤링 -> 더 찾을 수 있지만 우선 여기까지)
        # 해당 책들의 바코드 값을 넘겨, 상세 페이지로부터 얻은 값들을 하나의 list로 묶어서 처리함.
        for barcode in barcodes_list[:2]:
            if barcode is not None:
                crawl_result.append(get_book_info(cate_name, barcode))
        wd.quit()
        return crawl_result
