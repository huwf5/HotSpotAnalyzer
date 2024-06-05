import requests
from urllib.parse import urlencode
import time
import random
from pyquery import PyQuery as pq

import pymysql

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
def get_single_page(page, keyword):
    # 请求参数
    # params = {
    #     'containerid': f'100103type=1&q=#{keyword}#',  # 
    #     'page_type': 'searchall',
    #     'page': page
    # }
    params = {
        'containerid': f'100103type=1&q=#{keyword}#',  # keyword左右有 '#' 意味着爬取的是话题的内容，而不是单纯输入关键词的内容
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


def parse_page(json_data):
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
                if item.get('isLongText') is False:  # 不是长文本
                    data = {
                        'wid': item.get('id'),
                        'user_name': item.get('user').get('screen_name'),
                        'user_id': item.get('user').get('id'),
                        'gender': item.get('user').get('gender'),
                        'publish_time': time_formater(item.get('created_at')),
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
                        'publish_time': time_formater(item.get('created_at')),
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

# 批量保存帖子数据到数据库
# def batch_save_to_db(data_list, keyword):
#     connection = connect_db()
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT id FROM keywords WHERE keyword=%s", (keyword,))
#             result = cursor.fetchone()
#             keyword_id = result['id'] if result else None
#             if keyword_id:
#                 sql = '''
#                     INSERT INTO posts (wid, keyword_id, user_name, user_id, gender, publish_time, text, like_count, comment_count, forward_count)
#                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 '''
#                 for data in data_list:
#                     cursor.execute(sql, (data['wid'], keyword_id, data['user_name'], data['user_id'], data['gender'],
#                                          data['publish_time'], data['text'], data['like_count'],
#                                          data['comment_count'], data['forward_count']))
#         connection.commit()
#     finally:
#         connection.close()
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


def crawler_post(keyword):
    temp_data = []
    empty_times = 0
    max_retries = 5
    retry_delay = 30
    for page in range(1, 50000):  # 瀑布流下拉式，加载
        retry_count = 0

        while retry_count <= max_retries:
            try:
                print(f'page: {page}')
                json_data = get_single_page(page, keyword)
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
                
                # for result in parse_page(json_data):  # 需要存入的字段
                #     temp_data.append(result)
                
                try:
                    for result in parse_page(json_data):
                        temp_data.append(result)
                except Exception as e:
                    print(f"An error occurred while processing results: {e}")
                    return

                if page % save_per_n_page == 0:
                    # with open(result_file, mode='a+', encoding='utf-8-sig', newline='') as f:
                    #     writer = csv.writer(f)
                    #     for d in temp_data:
                    #         writer.writerow(
                    #             [d['wid'], d['user_name'], d['user_id'], d['gender'],
                    #              d['publish_time'], d['text'], d['like_count'], d['comment_count'],
                    #              d['forward_count']])
                    batch_save_to_db(temp_data, keyword)
                    # print(f'\n\n------cur turn write {len(temp_data)} rows to csv------\n\n')
                    print(f'\n\n------cur turn write {len(temp_data)} rows to mysql------\n\n')
                    temp_data = []
                break  # Exit the retry loop on successful processing
            except requests.exceptions.ConnectionError as e:
                retry_count += 1
                print(f"Connection error on page {page}: {e}, retrying ({retry_count}/{max_retries})")
                retry_delay *= 2
                time.sleep(retry_delay)
        time.sleep(random.randint(2, 6))  # 爬取时间间隔
    # except requests.exceptions.ConnectionError as e:
    #     print(f"Attempt {retries+1}: Connection reset by peer on page {page} for keyword '{keyword}'. Retrying in {retry_delay} seconds...")
    #     time.sleep(retry_delay)  # 等待一段时间后重试
    #     retries += 1
    #     retry_delay *= 2  # 指数退避
    #     if retries > max_retries:
    #         print("Max retries reached, moving to next page or stopping.")
    #         break  # 如果重试次数超过最大值，跳出循环

import os, csv
if __name__ == '__main__':
    # keyword = '北京疫情'
    keyword = '小米联合创始人夫妇向中山大学捐赠1亿元'
    # keyword = '在中山大学共赴宫崎骏的人生之约'
    # insert_keyword("在中山大学共赴宫崎骏的人生之约", "在中山大学共赴宫崎骏的人生之约", "https://s.weibo.com/weibo?q=%23%E5%9C%A8%E4%B8%AD%E5%B1%B1%E5%A4%A7%E5%AD%A6%E5%85%B1%E8%B5%B4%E5%AE%AB%E5%B4%8E%E9%AA%8F%E7%9A%84%E4%BA%BA%E7%94%9F%E4%B9%8B%E7%BA%A6%23", "4677讨论 219.3万阅读")

    csv_file_path = 'sub_topics.csv'

    # 这里可以将爬取的内容存储成csv格式
    # result_file = f'{keyword}.csv'
    # if not os.path.exists(result_file):
    #     with open(result_file, mode='w', encoding='utf-8-sig', newline='') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(['wid', 'user_name', 'user_id', 'gender',
    #                          'publish_time', 'text', 'like_count', 'comment_count',
    #                          'forward_count'])

    # temp_data = []
    create_tables()
    # last_keyword = get_last_keyword()
    last_keyword = get_last_keyword()
    
    start_from_last_keyword = False

    # last_keyword = '中山大学'

    if not last_keyword:
        print("No last keyword found, starting from the first keyword in CSV.")
        start_from_last_keyword = True  # 如果没有最后关键词，从第一个开始

    if not os.path.exists(csv_file_path):
        print("sub_topics.csv does not exist")
    else:
        with open(csv_file_path, mode='r', encoding='utf-8-sig') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                if start_from_last_keyword or row['title'] == last_keyword:
                    
                    start_from_last_keyword = True  # 找到 last_keyword，下一个循环开始处理
                    print(f"Starting or continuing from keyword: {row['title']}")
                    keyword = row['title']
                    insert_keyword(keyword,keyword,row['link'],row['stats'])
                    crawler_post(keyword)
                    print("wait for 1-2 min to crawl the next post")
                    time.sleep(random.randint(120,180))
    
