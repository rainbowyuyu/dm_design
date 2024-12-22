import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re

# 设置Chrome驱动路径
driver_path = 'path_to_your_chromedriver'

# 初始化Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式
driver = webdriver.Chrome(executable_path=driver_path, options=options)

# 访问考研国家线网页
url = 'https://www.example.com/kaoyan-guojiaxian'  # 替换为实际的页面URL
driver.get(url)

# 等待页面加载
time.sleep(5)

# 获取网页内容
html_content = driver.page_source

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 假设国家线数据存放在一个特定的表格中，找到该表格
table = soup.find('table', {'class': 'national-line-table'})  # 替换为实际的table class名

# 获取所有行数据
rows = table.find_all('tr')

# 使用正则表达式从每一行中提取年份和对应的国家线
national_lines = []

for row in rows:
    cols = row.find_all('td')
    if len(cols) > 1:
        # 获取年份和国家线数据
        year = cols[0].text.strip()
        line_data = cols[1].text.strip()

        # 使用正则表达式提取国家线的数字
        match = re.search(r'(\d+)', line_data)
        if match:
            national_line = match.group(1)
            national_lines.append((year, national_line))

# 打印爬取的历年国家线
for year, line in national_lines:
    print(f"{year} 年考研国家线: {line}")

# 关闭浏览器
driver.quit()
