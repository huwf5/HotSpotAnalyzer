import requests
from urllib.parse import urlencode
import time
import random
from pyquery import PyQuery as pq
import json
import pymysql
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 设置代理等（新浪微博的数据是用ajax异步下拉加载的，network->xhr）
host = 'm.weibo.cn'
base_url = 'https://%s/api/container/getIndex?' % host
user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'

# 设置请求头
headers = {
    'Host': host,
    'keep': 'close',
    # 'Referer': 'https://m.weibo.cn/search?containerid=231522type%3D1%26t%3D10%26q%3D%23%E5%A6%82%E4%BD%95%E7%9C%8B%E5%BE%85%E5%8F%8D%E5%86%85%E5%8D%B7%E7%83%AD%E6%BD%AE%23&extparam=%23%E5%A6%82%E4%BD%95%E7%9C%8B%E5%BE%85%E5%8F%8D%E5%86%85%E5%8D%B7%E7%83%AD%E6%BD%AE%23&luicode=10000011&lfid=100103type%3D38%26q%3D%E5%86%85%E5%8D%B7%26t%3D0',
    'User-Agent': user_agent
}

save_per_n_page = 1

from datetime import datetime


def requests_retry_session(retries=3, backoff_factor=0.5, status_forcelist=(500, 502, 503, 504, 104)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(['GET', 'POST'])  # 默认情况下Retry类不会在POST方法上重试，需要显式允许
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def time_formater(input_time_str):
    input_format = '%a %b %d %H:%M:%S %z %Y'
    output_format = '%Y-%m-%d %H:%M:%S'

    return datetime.strptime(input_time_str, input_format).strftime(output_format)




# 按页数抓取数据
def get_single_page(page, keyword,isoneMonth, isRealTime):
    # 请求参数
    # params = {
    #     'containerid': f'100103type=1&q=#{keyword}#',  # 、、教育内卷、职场内卷、如何看待内卷的社会状态、如何避免婚姻内卷、
    #     'page_type': 'searchall',
    #     'page': page
    # }

    
    params = {
        'containerid': f'100103type=61&q={keyword}',  # 、、教育内卷、职场内卷、如何看待内卷的社会状态、如何避免婚姻内卷、
        'page_type': 'searchall',
        'page': page
    }
    url = base_url + urlencode(params)
    print(url)
    error_times = 0
    while True:
        response = requests.get(url, headers=headers)  # ,proxies=abstract_ip.get_proxy()
        if response.status_code == 200:
            if len(response.json().get('data').get('cards')) > 0:
                return response.json()
        time.sleep(3)
        error_times += 1
        # 连续出错次数超过 3
        if error_times > 3:
            return None


# 长文本爬取代码段
def getLongText(lid):  # lid为长文本对应的id
    # 长文本请求头
    headers_longtext = {
        'Host': host,
        'Referer': 'https://m.weibo.cn/status/' + lid,
        'User-Agent': user_agent
    }
    params = {
        'id': lid
    }
    url = 'https://m.weibo.cn/statuses/extend?' + urlencode(params)
    try:
        response = requests.get(url, headers=headers_longtext)  # proxies=abstract_ip.get_proxy()
        if response.status_code == 200:  # 数据返回成功
            jsondata = response.json()
            tmp = jsondata.get('data')
            return pq(tmp.get("longTextContent")).text()  # 解析返回结构，获取长文本对应内容
    except:
        pass


# 解析页面返回的json数据
count = 0

'''
修改后的页面爬取解析函数
'''


def parse_page(json_data,isoneMonth):
    global count
    items = json_data.get('data').get('cards')

    for index, item in enumerate(items):
        if item.get('card_type') == 7:
            print('导语')
            continue
        elif item.get('card_type') == 8 or (item.get('card_type') == 11 and item.get('card_group') is None):
            continue
        # topic = json_data.get('data').get('cardlistInfo').get('cardlist_head_cards')[0]
        # # 单独的关键词抓取不是超话，会有 topic == null
        # if topic is None or topic.get('head_data', None) is None:
        #     topic = keyword
        # else:
        #     topic = topic.get('head_data').get('title')
        try:
            if item.get('mblog', None):
                item = item.get('mblog')
            else:
                item = item.get('card_group')[0].get('mblog')
            if item:

                publish_time_formatted = time_formater(item.get('created_at'))
                if not isoneMonth or (isoneMonth and is_within_one_month(publish_time_formatted)):
                    if item.get('isLongText') is False:  # 不是长文本
                        data = {
                            'wid': item.get('id'),
                            'user_name': item.get('user').get('screen_name'),
                            'user_id': item.get('user').get('id'),
                            'gender': item.get('user').get('gender'),
                            'publish_time': publish_time_formatted,
                            'text': pq(item.get("text")).text(),  # 仅提取内容中的文本
                            'like_count': item.get('attitudes_count'),  # 点赞数
                            'comment_count': item.get('comments_count'),  # 评论数
                            'forward_count': item.get('reposts_count'),  # 转发数
                        }
                    else:  # 长文本涉及文本的展开
                        tmp = getLongText(item.get('id'))  # 调用函数
                        data = {
                            'wid': item.get('id'),
                            'user_name': item.get('user').get('screen_name'),
                            'user_id': item.get('user').get('id'),
                            'gender': item.get('user').get('gender'),
                            'publish_time': publish_time_formatted,
                            'text': tmp,  # 仅提取内容中的文本
                            'like_count': item.get('attitudes_count'),
                            'comment_count': item.get('comments_count'),
                            'forward_count': item.get('reposts_count'),
                        }
                    count += 1
                    print(f'total count: {count}')
                    yield data
        except Exception as e:
            print(f"Error processing item at index {index}: {e}")
            continue


def connect_db():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='123456', # password='huchp6',
                           db='weibo_test',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


# # 创建关键词表和帖子表
def create_tables():
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            create_keywords_sql = '''
                CREATE TABLE IF NOT EXISTS keywords (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    keyword VARCHAR(255) UNIQUE,
                    title VARCHAR(255),
                    link VARCHAR(255),
                    stats VARCHAR(255),
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            '''
            create_posts_sql = '''
                CREATE TABLE IF NOT EXISTS posts (
                    wid VARCHAR(255) NOT NULL,
                    keyword_id INT,
                    user_name VARCHAR(255),
                    user_id VARCHAR(255),
                    gender CHAR(1),
                    publish_time DATETIME,
                    text TEXT,
                    like_count INT,
                    comment_count INT,
                    forward_count INT,
                    PRIMARY KEY (wid),
                    FOREIGN KEY (keyword_id) REFERENCES keywords(id)
                );
            '''
            cursor.execute(create_keywords_sql)
            cursor.execute(create_posts_sql)
        connection.commit()
    finally:
        connection.close()

# 插入关键词数据
def insert_keyword(keyword, title, link, stats):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = '''
                INSERT INTO keywords (keyword, title, link, stats)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                title=%s, link=%s, stats=%s
            '''
            cursor.execute(sql, (keyword, title, link, stats, title, link, stats))
        connection.commit()
    finally:
        connection.close()

def batch_save_to_db(data_list, keyword):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM keywords WHERE keyword=%s", (keyword,))
            result = cursor.fetchone()
            keyword_id = result['id'] if result else None
            if keyword_id:
                sql = '''
                    INSERT INTO posts (wid, keyword_id, user_name, user_id, gender, publish_time, text, like_count, comment_count, forward_count)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    user_name=VALUES(user_name), user_id=VALUES(user_id), gender=VALUES(gender),
                    publish_time=VALUES(publish_time), text=VALUES(text), like_count=VALUES(like_count),
                    comment_count=VALUES(comment_count), forward_count=VALUES(forward_count)
                '''
                for data in data_list:
                    cursor.execute(sql, (data['wid'], keyword_id, data['user_name'], data['user_id'], data['gender'],
                                         data['publish_time'], data['text'], data['like_count'],
                                         data['comment_count'], data['forward_count']))
        connection.commit()
    finally:
        connection.close()

# 通过关键词检索帖子
def fetch_posts_by_keyword(keyword):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = '''
                SELECT p.* FROM posts p
                JOIN keywords k ON p.keyword_id = k.id
                WHERE k.keyword = %s
            '''
            cursor.execute(sql, (keyword,))
            posts = cursor.fetchall()
            return posts
    finally:
        connection.close()

def get_last_keyword():
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT keyword FROM keywords ORDER BY id DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result['keyword'] if result else None
    finally:
        connection.close()




def crawler_post(keyword,limit,isoneMonth,isRealTime):
    temp_data = []
    empty_times = 0
    max_retries = 5
    retry_delay = 30
    
    noDataPageCount = 0

    for page in range(1, 50000):  # 瀑布流下拉式，加载
        retry_count = 0

        while retry_count <= max_retries:
            try:
                print(f'page: {page}')
                json_data = get_single_page(page, keyword,isoneMonth,isRealTime)
                if json_data == None:
                    print('json is none')
                    return

                if len(json_data.get('data').get('cards')) <= 0:
                    empty_times += 1
                else:
                    empty_times = 0
                if empty_times > 3:
                    print('\n\n consist empty over 3 times \n\n')
                    break
                
                
                try:
                    for result in parse_page(json_data,isoneMonth):
                        temp_data.append(result)
                except Exception as e:
                    print(f"An error occurred while processing results: {e}")
                    return

                if page % save_per_n_page == 0:
                    batch_save_to_db(temp_data, keyword)
                    # print(f'\n\n------cur turn write {len(temp_data)} rows to csv------\n\n')
                    print(f'\n\n------cur turn write {len(temp_data)} rows to mysql------\n\n')
                    temp_data = []
                    if len(temp_data) == 0:
                        noDataPageCount += 1
                    else:
                        noDataPageCount = 0
                    
                if count > limit:
                    break
                if noDataPageCount > 10:
                    break
                break  # Exit the retry loop on successful processing
            except requests.exceptions.ConnectionError as e:
                retry_count += 1
                print(f"Connection error on page {page}: {e}, retrying ({retry_count}/{max_retries})")
                retry_delay *= 2
                time.sleep(retry_delay)
        time.sleep(random.randint(2, 6))  # 爬取时间间隔

def load_config():
    with open('post_monthly_config.json', 'r', encoding='utf-8') as file:  # 指定文件编码为 UTF-8
        return json.load(file)

def is_within_one_month(publish_time_str, date_format='%Y-%m-%d %H:%M:%S'):
    """检查发布时间是否在当前日期的一个月内"""
    publish_time = datetime.strptime(publish_time_str, date_format)
    one_month_ago = datetime.now() - timedelta(days=30)
    return publish_time >= one_month_ago


import os, csv
if __name__ == '__main__':

    config  = load_config()

    keyword = '中山大学'
    keyword = config['keyword']

    isoneMonth = config.get('isoneMonth', False)
    isRealTime = config['isRealTime']
    start_from_last_keyword = True
    limit = config['limit']
    # last_keyword = '中山大学'
    
    last_keyword = keyword
    

    # else:
    #     with open(csv_file_path, mode='r', encoding='utf-8-sig') as f:
    #         csv_reader = csv.DictReader(f)
    #         for row in csv_reader:
    #             if start_from_last_keyword or row['title'] == last_keyword:
    #                 start_from_last_keyword = True  # 找到 last_keyword，下一个循环开始处理
    #                 print(f"Starting or continuing from keyword: {row['title']}")
    #                 keyword = row['title']
    #                 insert_keyword(keyword,keyword,row['link'],row['stats'])
    #                 crawler_post(keyword)
    #                 print("wait for 1-2 min to crawl the next post")
    #                 time.sleep(random.randint(120,180))

    
    insert_keyword(keyword,keyword,"","")
    crawler_post(keyword,limit,isoneMonth,isRealTime)
    
