from bs4 import BeautifulSoup as bs
from selenium import webdriver


# 해당 책의 정보가 담긴 페이지에서 유의미한 정보를 추출하는 함수
def get_book_info(cate_name, barcode):
    wd = webdriver.Chrome('./chromedriver.exe')
    book_url = "http://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&barcode=%s" % barcode

    wd.get(book_url)
    html = wd.page_source

    soupBook = bs(html, 'html.parser')
    book_title = soupBook.select("div.box_detail_point > h1.title > strong")[0].text.strip()
    book_author = soupBook.select("div.author > span.name > a")[0].text.strip()
    book_publisher = soupBook.select("div.author > span[title=출판사] > a")[0].text.strip()
    book_pubdate = soupBook.select("div.author > span.date")[0].text.strip()[:13]

    # book_org_price = soupBook.select("ul.list_detail_price > li:nth-of-type(1) > span.org_price")
    # book_sell_price = soupBook.select("ul.list_detail_price > li:nth-of-type(1) > span.sell_price")
    wd.quit()
    print("{0:^4} | {1:<80} | {2:<10} | {3:<10} | {4}".format(
        cate_name, book_title, book_author, book_publisher, book_pubdate))
    return [cate_name] + [book_title] + [book_author] + [book_publisher] + [book_pubdate]