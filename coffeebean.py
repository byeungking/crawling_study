from chrome.driver import chrome_driver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import time  # 시간 지연
import pandas as pd
from tqdm import tqdm
import random
from bs4 import BeautifulSoup
import re

random_time = random.uniform(1, 3)
df = pd.DataFrame(columns=['이름', '설명', '칼로리', '포화지방', '나트륨', '탄수화물', '당', '카페인', '단백질'])


def coffeebean_crawling():
    url2 = 'https://www.coffeebeankorea.com/member/login.asp#loginArea'
    driver = chrome_driver()
    driver.get(url2)
    driver.maximize_window()
    time.sleep(random_time)
    # login
    username = driver.find_element(By.XPATH, '''//*[@id="loginForm"]/fieldset/div/div[1]/div[1]/div/p[1]/input''')
    password = driver.find_element(By.XPATH, '''//*[@id="loginForm"]/fieldset/div/div[1]/div[1]/div/p[2]/input''')
    time.sleep(random_time)

    username.send_keys("cw3135")
    time.sleep(random_time)
    password.send_keys("qudgns4298!@")
    time.sleep(random_time)
    # button click
    driver.find_element(By.XPATH, '''//*[@id="loginForm"]/fieldset/div/div[1]/div[1]/a''').click()
    time.sleep(random_time)
    # menu click
    driver.find_element(By.XPATH, '''//*[@id="gnb"]/ul/li[3]/a''').click()
    time.sleep(random_time)
    # 정적 크롤링


    jdx = 0
    page = 4
    while True:
        try:
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            ul = soup.select_one('''#contents > div > div > ul''')
            lis = ul.find_all('li')
            for i, li in enumerate(lis):
                menu = li.select_one(f'''#contents > div > div > ul > li:nth-child({i+1}) > dl > dt > span.kor''').text
                des = li.select_one(f'''#contents > div > div > ul > li:nth-child({i+1}) > dl > dd''').text.strip()
                dls = li.find_all('dl')
                temp_list = [menu, des]
                for idx, dl in enumerate(dls):
                    if idx == 0: continue
                    numbers = re.sub(r'[^0-9]', '', dl.text)
                    temp_list.append(numbers)

                df.loc[jdx] = temp_list
                jdx += 1
            if page == 4:
                driver.find_element(By.XPATH, f'''//*[@id="contents"]/div/div/div/a[{page}]''').click()
                page += 1
                time.sleep(random_time)
            else:
                driver.find_element(By.XPATH, f'''//*[@id="contents"]/div/div/div/a[{page}]''').click()
                time.sleep(random_time)
        except Exception as e:
            print(e)
            break


    time.sleep(3)
    driver.quit()

    return df
if __name__ == "__main__":
    result = coffeebean_crawling()
    print(result)
    df.to_csv("data/coffeebean.csv", encoding='utf-8-sig', index=False)
    print("save")