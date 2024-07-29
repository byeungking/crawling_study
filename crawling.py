from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm
def crawling(soup):
    table = soup.find('table')
    ths = table.find_all('th')
    columns = []
    for idx, th in enumerate(ths):
        if idx == 4: continue
        columns.append(th.string)
    df = pd.DataFrame(columns=columns)

    trs = table.find_all('tr')
    i = 0
    for jdx, tr in enumerate(trs):
        if jdx == 0: continue
        tds = tr.find_all('td')
        temps = []
        for idx, td in enumerate(tds):
            if idx == 4: continue
            temps.append(td.text)
        df.loc[i] = temps
        i += 1
    return df



if __name__ == "__main__":
    # url = f"https://www.hollys.co.kr/store/korea/korStore2.do?pageNo=1"
    # response = requests.get(url)
    # html = response.text
    # soup = BeautifulSoup(html, 'html.parser')
    # tr = soup.select_one("#contents > div.content > fieldset > fieldset > div.tableType01 > table > tbody > tr:nth-child(1) > td.noline.center_t")
    # print(tr)
    # exit()

    df = pd.DataFrame()
    page = 1
    while tqdm(1):
        try:
            url = f"https://www.hollys.co.kr/store/korea/korStore2.do?pageNo={page}"
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            new_df = crawling(soup)
            page += 1
            print(page)
        except Exception as e:
            print(e)
            break
        else:
            df = pd.concat([df, new_df])
    df.reset_index(inplace=True)
    path = "data/hollys.csv"
    df.to_csv(path)