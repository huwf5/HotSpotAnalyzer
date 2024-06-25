from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random
# 初始化webdriver
# 这部分用来获取话题下的子话题，来扩大搜索的范围
# 至 2024.4.25的数据的子话题已爬取
# 以便在搜#中山大学#时出现页数限制，也能有更多数据

driver = webdriver.Chrome()
print("请在浏览器中登录微博...")
driver.get("https://login.sina.com.cn/signup/signin.php")
time.sleep(60)  # 这部分时间进行人工登录

def fetch_sub_topics(keyword):
    page_count = 1
    max_pages = 30  # 最多翻页次数
    total_sub_topics = []  # 存储所有页的数据
    while page_count <= max_pages:
        sub_topics = []  # 当前页的子话题数据
        url = f'https://s.weibo.com/topic?q={keyword}&pagetype=topic&topic=1&Refer=weibo_topic&page={page_count}'
        driver.get(url)
        time.sleep(random.randint(6, 8))  # 等待页面加载完毕 
        # cards = driver.find_elements(By.CSS_SELECTOR, 'div.card-wrap')
        
        # 这里可以检查是否到最后一页了
        # # 检查是否有“未找到相关结果”的页面
        # no_results = driver.find_elements(By.CSS_SELECTOR, 'div.card-no-result')
        # if no_results:
        #     print(f"No more results found at page {page_count}. Ending search.")
        #     break
        
        cards = driver.find_elements(By.CSS_SELECTOR, 'div.card-wrap > div.card')
        print(f"Page {page_count} has {len(cards)} cards.")  # 打印卡片数量
        for card in cards:
            try:
                info_div = card.find_element(By.CSS_SELECTOR, 'div.info')
                name_element = info_div.find_element(By.CSS_SELECTOR, 'div a.name')
                link = name_element.get_attribute('href')
                title = name_element.text.strip('#')

                # 获取讨论和阅读数，位于第二个 <p> 标签中
                stats_elements = info_div.find_elements(By.CSS_SELECTOR, 'p')
                if len(stats_elements) > 1:
                    stats_text = stats_elements[1].text
                    sub_topics.append({
                        'title': title,
                        'link': link,
                        'stats': stats_text
                    })
            except Exception as e:
                print(f"Error parsing card: {e}")

        # 保存当前页的数据到DataFrame并追加到CSV文件
        df = pd.DataFrame(sub_topics)
        if page_count == 1:
            df.to_csv('sub_topics.csv', mode='w', index=False, header=True, encoding='utf-8-sig')  # 第一页时创建文件
        else:
            df.to_csv('sub_topics.csv', mode='a', index=False, header=False, encoding='utf-8-sig')  # 后续页追加数据

        print(f"Page {page_count} data saved.")
        total_sub_topics.extend(sub_topics)  # 添加到总列表
        # 下一页
        page_count += 1
    
    return sub_topics

# 执行爬取
keyword = "中山大学"
sub_topics_data = fetch_sub_topics(keyword)

print("数据已保存为CSV文件，驱动正在关闭...")
driver.quit()
