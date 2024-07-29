from chrome.driver import chrome_driver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import time  # 시간 지연
import pandas as pd
from tqdm import tqdm
import random

url = 'https://www.hollys.co.kr/store/korea/korStore2.do'
result_df = pd.DataFrame(columns=['지역', '매장명', '현황', '주소', '전화번호'])
sleep_time = random.uniform(2, 4)
def exam_1():
    driver = chrome_driver()
    url = f"https://www.hollys.co.kr/store/korea/korStore2.do"
    driver.get(url)

    df = pd.DataFrame()
    driver.find_element(By.XPATH, '''//*[@id="contents"]/div[2]/fieldset/fieldset/div[2]/a[1]''').click()
    for i in range(1,10):
        trs = driver.find_elements(By.XPATH, '''//*[@id="contents"]/div[2]/fieldset/fieldset/div[1]/table/tbody/tr''')
        texts = [element.text for element in trs]
        df_new = pd.DataFrame(columns=texts)
        for text in df_new:
            print(text)
        time.sleep(2)
        df = pd.concat([df, df_new])
        driver.find_element(By.XPATH, f'''//*[@id="contents"]/div[2]/fieldset/fieldset/div[2]/a[{i}]''').click()
    print(df)
    path = "data/hollys2.csv"
    df.to_csv(path, encoding='utf-8', index=False)

def exam_2():
    url = 'https://www.coffeebeankorea.com/member/login.asp#loginArea'
    driver = chrome_driver()
    driver.get(url)
    time.sleep(2)

    username = driver.find_element(By.XPATH, '''//*[@id="loginForm"]/fieldset/div/div[1]/div[1]/div/p[1]/input''')
    password = driver.find_element(By.XPATH, '''//*[@id="loginForm"]/fieldset/div/div[1]/div[1]/div/p[2]/input''')
    time.sleep(1)

    username.send_keys("cw3135")
    password.send_keys("qudgns4298!@")
    time.sleep(2)

    driver.find_element(By.XPATH, '''//*[@id="loginForm"]/fieldset/div/div[1]/div[1]/a''').click()
    time.sleep(5)

def exam_3():
    url = 'https://www.hollys.co.kr/store/korea/korStore2.do'

    driver = chrome_driver()
    driver.get(url)

    trs = driver.find_elements(By.XPATH, '''//*[@id="contents"]/div[2]/fieldset/fieldset/div[1]/table/tbody/tr''')
    df = pd.DataFrame(columns=['지역', '매장명', '영업중', '주소', '전환번호'])


    i = 0
    for idx, tr in enumerate(trs):
        data = tr.text
        text_list = data.split(' ')
        legion = ' '.join(text_list[:2])
        name = text_list[2]
        state = text_list[3]
        address = ' '.join(text_list[4:-1])
        phone = text_list[-1]
        df.loc[i] = [legion, name, state, address, phone]
        i += 1

        print(df)
        time.sleep(0.1)

def hollys_crawling(url):
    driver = chrome_driver()
    driver.get(url)
    i = 0
    page = 1
    temp = 10
    while True:
        try:
            trs = driver.find_elements(By.XPATH, '''//*[@id="contents"]/div[2]/fieldset/fieldset/div[1]/table/tbody/tr''')
            for tr in trs:
                data = tr.text
                data_list = data.split(" ")

                region = " ".join(data_list[:2])
                store_name = data_list[2]
                current = data_list[3]
                address = " ".join(data_list[4:-1])
                phone_number = data_list[-1]
                result_df.loc[i] = [region, store_name, current, address, phone_number]
                i += 1
            print(page)
            print(result_df)
            time.sleep(sleep_time)
            if page % temp == 0:
                if temp == 10:
                    driver.find_element(By.XPATH, f'''//*[@id="contents"]/div[2]/fieldset/fieldset/div[2]/a[{temp}]/img''').click()
                    temp += 1
                    page = 2
                else:
                    driver.find_element(By.XPATH, f'''//*[@id="contents"]/div[2]/fieldset/fieldset/div[2]/a[{temp}]/img''').click()
                    page = 2

            else:
                driver.find_element(By.XPATH, f'''//*[@id="contents"]/div[2]/fieldset/fieldset/div[2]/a[{page}]''').click()
                page += 1
        except Exception as e:
            print(e)
            driver.quit()
            break

    return result_df




if __name__ == "__main__":
    result = hollys_crawling(url)
    print(f"결과: {result}")

    path = 'data/hollys2.csv'
    result.to_csv(path, encoding='utf-8-sig', index=False)
    print("save ok!")










