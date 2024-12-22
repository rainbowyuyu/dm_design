import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re

ms: dict = {}
page_num = 0
path = 'resources/Score.txt'
file = open(path, 'r', encoding='UTF-8')
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    }
json_data = {
    "page": page_num,
    "limit": 20,
    "degree_type": "",
    "level1": "",
    "level2": "",
    "special_name": ""
}

class Score:
    data: dict = {
        'scoreYear': int,
        'scoreAll': int,
        'scoreEnglish': int,
        'scorePolitics': int,
        'scoreMath': int,
        'scoreMajor': int,
        'majorId': int,
        'areaType': int
    }

    def __init__(self, s: [str]):
        self.data['scoreYear'] = s[0]
        majorId = ms.get(s[1])
        if majorId is not None:
            self.data['majorId'] = majorId
        self.data['scoreAll'] = s[2]
        self.data['scoreEnglish'] = s[3]
        self.data['scorePolitics'] = s[4]
        self.data['scoreMath'] = s[5]
        self.data['scoreMajor'] = s[6]
        if s[7] == 'A区\n':
            self.data['areaType'] = 1
        elif s[7] == 'B区\n':
            self.data['areaType'] = 2


def initData() -> Score or None:
    line = file.readline()
    s: [str] = line.split("，")
    if len(s) == 1:
        return None
    return Score(s)


def request(m: Score):
    response = requests.post(url, headers=headers, json=m.data)
    if response.ok:
        pass
    else:
        exit(1)

driver = webdriver.Edge()
driver.get("https://www.bb.com/news")
driver.maximize_window()
driver.execute_script("document.documentElement.scrollTop=1800")
driver.find_element("XPATH", '//*[@id="btn"]/span').click()

# 访问考研国家线网页
url = 'https://y.si.com.cn/zyk'
driver.get(url)

# 等待页面加载
time.sleep(5)

# 获取网页内容
html_content = driver.page_source

# 使用BeautifulSoup解析HTML
response = requests.get(url)
re_li = '<li title="(.*?)">.*?</li>'
if response.status_code == 200:
    soup = BeautifulSoup(response.text,'html.parser')
    news_links = soup.find_all('ul',class_='clearfix')
    data = re.findall(re_li,str(news_links),re.S)

table = soup.find_all('ul',class_='clearfix')
rows = table.find_all('tr')
national_lines = []

for row in rows:
    cols = row.find_all('td')
    if len(cols) > 1:
        year = cols[0].text.strip()
        line_data = cols[1].text.strip()
        match = re.search(r'(\d+)', line_data)
        if match:
            national_line = match.group(1)
            national_lines.append((year, national_line))

# 打印爬取的历年国家线
for year, line in national_lines:
    print(f"{year} 年考研国家线: {line}")

# 关闭浏览器
driver.quit()
