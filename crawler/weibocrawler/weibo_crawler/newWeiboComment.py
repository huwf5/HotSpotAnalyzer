import requests, os, csv, traceback
from datetime import datetime
from collections import deque
from time import sleep
# import pandas as pd
import pymysql
import random
per_request_sleep_sec = 5
request_timeout = 10
limit_page = 300
# import execjs

# def mid2id(id):
#     jspython = 'str62keys = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";\n    /**\n    * 62进制值转换为10进制\n    * @param {String} str62 62进制值\n    * @return {String} 10进制值\n    */\n    function str62to10(str62) {\n        var i10 = 0;\n        for (var i = 0; i < str62.length; i++) {\n                var n = str62.length - i - 1;\n                var s = str62.substr(i, 1);  // str62[i]; 字符串用数组方式获取，IE下不支持为“undefined”\n                i10 += parseInt(str62keys.indexOf(s)) * Math.pow(62, n);\n        }\n        return i10;\n    }\n    /**\n    * mid转换为id\n    * @param {String} mid 微博mid，如 "wr4mOFqpbO"\n    * @return {String} 微博id，如 "201110410216293360"\n    */\n    function mid2id(mid) {\n        var id = \'\';\n        for (var i = mid.length - 4; i > -4; i = i - 4) //从最后往前以4字节为一组读取mid字符\n        {\n                var offset1 = i < 0 ? 0 : i;\n                var len = i < 0 ? parseInt(mid.length % 4) : 4;\n                var str = mid.substr(offset1, len);\n                str = str62to10(str).toString();\n                if (offset1 > 0) //若不是第一组，则不足7位补0\n                {\n                        while (str.length < 7) {\n                                str = \'0\' + str;\n                        }\n                }\n                id = str + id;\n        }\n        return id;\n    }'
#     ctx = execjs.compile(jspython)
#     return ctx.call("mid2id", id)

# print(mid2id(5005818583846182))

class WeiboCommentSpider(object):
    url = 'https://weibo.com/ajax/statuses/buildComments'
    headers = {
     'authority': '"weibo.com"', 
     'sec-ch-ua': '\'"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"\'', 
     'accept': '"application/json, text/plain, */*"', 
     'x-xsrf-token': '"-OsgXanv8IeYF0Sc1UdtiBB7"', 
     'x-requested-with': '"XMLHttpRequest"', 
     'traceparent': '"00-e5b530ae9b5a4f289194c266b198bc0b-49c92543eb3e163f-00"', 
     'sec-ch-ua-mobile': '"?0"', 
     'user-agent': '"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"', 
     'sec-fetch-site': '"same-origin"', 
     'sec-fetch-mode': '"cors"', 
     'sec-fetch-dest': '"empty"', 
     'referer': '"https://weibo.com/1689653470/O9wCzfNhI?refer_flag=1001030103_&type=comment"', 
     'accept-language': '"zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7,es-MX;q=0.6,es;q=0.5"', 
     'cookie': '"SINAGLOBAL=4459335575214.156.1626924756119; UOR=,,weibo.cn; ALF=1717593326; SUB=_2A25LPKe9DeRhGeBO6FsS9yvLyD2IHXVoM6V1rDV8PUJbkNAGLVL2kW1NSh6UAJwsirO8H6LrIfvDiVYCAJHCmcJp; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5XhRK9ulpf3LgIZlO6oeHW5JpX5KMhUgL.Foq7e0.0S0-Ne022dJLoI77LxKqL1heLBKWudPnt; ULV=1715494985048:10:5:1:2206838522078.456.1715494985019:1715177313572; WBPSESS=MsEAi1ogr81xvjZtzwKzpt4WF_MYyFwDTrMomAeuIG_1InxUA1p7nvCVPiSgzK1QwTfI5n_PQ8CpB_VVb_3DQgT2tvWaAgtWl5yKsV3SpBi2l7pTGw4PULTgpl82xkkZlBp-htPjs83KFYwt_bPoRw==; XSRF-TOKEN=iCmmywOnObEtPI8yDik0hELI"'}

    params = {
        'is_reload': '1', 
        'id': '5005818583846182', 
        'is_show_bulletin': '2', 
        'is_mix': '0', 
        'count': '100', 
        # 'uid': '6623758877',
        # 'max_id':'140242976300206',
        'flow': '0'
    }

    limit = 100000

    # 从数据库中提取到 wid 
    def __init__(self, id=None, limit=None, cookie=None, child_max_page=5):
        # 直接使用 wid 作为 id 即可
        # 上述的uid是weibo.com的搜索标识，目前已经获取了wid(id)，所以不需要uid，自然不需要将uid转换成wid了
        self.got_comments = []
        self.got_comments_num = 0
        self.has_written_comments_num = 0
        self.comment_queue = deque()
        self.wid = id
        self.limit = limit
        self.headers["cookie"] = cookie
        self.params["id"] = id
        self.child_max_page = child_max_page

    def display(self):
        print("------      this is self.got_comments    ---------")
        print(self.got_comments)

    def parse_json(self,res_json):
        if res_json.get('ok') != 1:
            return None
        max_id = res_json.get('max_id',0)
        # post_total_number = res_json.get('total_number',0)
        for comment in res_json.get('data',[]):
            comment_data = {
                'comment_time': comment.get('created_at'),
                'comment_id': comment.get('id'),
                'parent_comment_id': comment.get('rootid'),
                'comment_user_id': comment.get('user', {}).get('id'),
                'comment_user_name': comment.get('user', {}).get('screen_name'),
                'comment_user_location': comment.get('user', {}).get('location'),
                'comment_floor_number': comment.get('floor_number'),
                # 'max_id': comment.get('max_id'),
                'total_number': comment.get('total_number'),
                'like_counts': comment.get('like_counts'),
                'text_raw': comment.get('text_raw')
                # 'isLikedByMblogAuthor': comment.get('isLikedByMblogAuthor')
            }
            # for key, value in comment_data.items():
            #     print(f"{key}: {type(value)}")


            self.got_comments.append(comment_data)
            self.got_comments_num += 1
            if comment.get('total_number',0) > 0:
                self.comment_queue.append(comment_data) 
        return max_id

    def parse_child_json(self,res_json,root_comment_id):
        if res_json.get('ok') != 1:
            return None
        max_id = res_json.get('max_id',0)
        # post_total_number = res_json.get('total_number',0)
        for comment in res_json.get('data',[]):
            comment_data = {
                'comment_time': comment.get('created_at'),
                'comment_id': comment.get('id'),
                'parent_comment_id': comment.get('rootid'),
                'comment_user_id': comment.get('user', {}).get('id'),
                'comment_user_name': comment.get('user', {}).get('screen_name'),
                'comment_user_location': comment.get('user', {}).get('location'),
                'comment_floor_number': comment.get('floor_number'),
                # 'max_id': comment.get('max_id'),
                'total_number': comment.get('total_number',0),
                'like_counts': comment.get('like_counts'),
                'text_raw': comment.get('text_raw')
                # 'isLikedByMblogAuthor': comment.get('isLikedByMblogAuthor')
            }
            self.got_comments.append(comment_data)
            self.got_comments_num += 1
            # if comment.get('total',0) > 0:
                # self.comment_queue.append(comment_data) 
        return max_id

    def parseChild(self, root_comment_id):
        print(f"............爬取: {root_comment_id}的子评论 .........")
        # child_params = {
        #  'is_reload': '"1"', 
        #  'id': '"4663893136511324"', 
        #  'is_show_bulletin': '"2"', 
        #  'is_mix': '"0"', 
        #  'count': '"20"', 
        # #  'uid': '"6882947163"', 
        #  'fetch_level': '"1"', 
        #  'flow': '"0"'}
        child_params = {
            'is_reload': '1', 
            'id': '5006355417010657', 
            'is_show_bulletin': '2', 
            'is_mix': '0', 
            'count': '20', 
        #  'uid': '"6882947163"', 
            'fetch_level': '1', 
            'flow': '0'
        }
        child_params["id"] = root_comment_id
        page = 1
        child_max_page = self.child_max_page
        while True:
            if page > child_max_page:
                print(f"child page up to max_page_limit == {child_max_page}")
                break
            print(f"............ {root_comment_id} child page: {page} .........")
            try:
                response = requests.get("https://weibo.com/ajax/statuses/buildComments", headers=(self.headers), params=child_params,
                  timeout=request_timeout)
            except:
                print(traceback.format_exc())
                break

            res_json = response.json()
            max_id = self.parse_child_json(res_json, root_comment_id)
            if not max_id:
                break
            child_params["max_id"] = max_id
            sleep(random.randint(1, per_request_sleep_sec))
            page += 1
        
        # self.got_comments.clear()
    def write_to_mysql(self):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                for comment in self.got_comments:
                    self.has_written_comments_num += 1
                    comment_time = datetime.strptime(comment['comment_time'], '%a %b %d %H:%M:%S +0800 %Y')
                    parent_comment_id = None if comment['parent_comment_id'] == comment['comment_id'] else comment['parent_comment_id']
                    
                    sql = """
                        INSERT IGNORE INTO comments (comment_id, comment_time, parent_comment_id, comment_user_id, comment_user_name,
                                              comment_user_location, comment_floor_number, total_number, like_counts, text_raw, wid)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        str(comment['comment_id']), 
                        comment_time, 
                        str(parent_comment_id), 
                        str(comment['comment_user_id']), 
                        comment['comment_user_name'], 
                        comment['comment_user_location'], 
                        comment['comment_floor_number'], 
                        comment['total_number'], 
                        comment['like_counts'], 
                        comment['text_raw'],
                        str(self.wid)
                    ))
            conn.commit()
            print("%d 条评论写入csv文件完毕:" % self.got_comments_num)
            print("累计写入 %d 条评论" % self.has_written_comments_num)
        finally:
            conn.close()


    def crawler(self):
        page = 1
        page_without_write_count = 0
        while page<= limit_page:
            print(f"............page: {page} .........")
            try:
                response = requests.get("https://weibo.com/ajax/statuses/buildComments", headers=(self.headers), params=(self.params),
                  timeout=request_timeout)
                # print(self.headers)
                # print(self.params)
                # response = requests.get(self.url, headers=(self.headers), params=(self.params))
                # print("------------- this is the response ----------\n")
                # print(response)
                # print("------------- this is the response text !!!----------")
                # print(response.text)
            except:
                print(traceback.format_exc())
                break
            
            res_json = response.json()

            try:
                max_id = self.parse_json(res_json)
            except:
                print(res_json["data"])
                print(traceback.format_exc())
                break
            
            self.params["max_id"] = max_id

            while self.comment_queue:
                comment = self.comment_queue.popleft()
                rootid = comment["comment_id"]
                self.parseChild(rootid)
            
            if page % 3 == 0:
                # if self.got_comments_num > self.has_written_comments_num:
                if self.got_comments_num != 0:
                    self.write_to_mysql()
                    self.got_comments.clear()
                    self.got_comments_num = 0
                    page_without_write_count = 0
                if not self.got_comments_num:
                    page_without_write_count += 1
                if self.has_written_comments_num >= self.limit:
                    break
                sleep(per_request_sleep_sec)

            if not max_id:
                self.write_to_mysql()
                self.got_comments.clear()
                self.got_comments_num = 0
                # sleep(per_request_sleep_sec)
                break
            if page_without_write_count >= 15:
                break
            # self.display()
            page += 1
            # print("------------- this is the response json !!!----------")
            # print(res_json)
            
import json
config_json = None
config_path = "comment_config.json"

def loadConfig():
    if not os.path.exists(config_path):
        raise Exception(f"没有配置文件 {config_path}")
    with open(config_path, "r", encoding="utf-8-sig") as f:
        config_json = json.loads(f.read())
    return config_json

def connect_db():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='123456', # password='huchp6',
                           db='weibo_test',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
def get_last_wid():
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # 查询最新的 wid，按 cid 递减排序确保获取最后一个记录的 wid
            cursor.execute("SELECT wid FROM comments ORDER BY cid DESC LIMIT 1")
            result = cursor.fetchone()
            if result:
                return result['wid']
            else:
                return None  # 返回 None 或默认值，如果表为空
    finally:
        conn.close()

# def create_comment_table():
#     conn = connect_db()
#     try:
#         with conn.cursor() as cursor:
#             # Drop table if it already exists
#             cursor.execute("DROP TABLE IF EXISTS comments;")
#             # Create new table with updated column types
#             cursor.execute("""
#                 CREATE TABLE comments (
#                     comment_id VARCHAR(255) PRIMARY KEY,
#                     comment_time DATETIME,
#                     parent_comment_id VARCHAR(255),
#                     comment_user_id VARCHAR(255),
#                     comment_user_name VARCHAR(255),
#                     comment_user_location VARCHAR(255),
#                     comment_floor_number INT,
#                     total_number INT,
#                     like_counts INT,
#                     text_raw TEXT,
#                     wid VARCHAR(255) NOT NULL,
#                     FOREIGN KEY (wid) REFERENCES posts(wid)
#                 );
#             """)
#         conn.commit()
#     finally:
#         conn.close()
def create_comment_table():
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # Drop table if it already exists
            # cursor.execute("DROP TABLE IF EXISTS comments;")
            # Create new table with updated column types and new auto-increment ID
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS comments (
                    cid INT AUTO_INCREMENT PRIMARY KEY,
                    comment_id VARCHAR(255) NOT NULL,
                    comment_time DATETIME,
                    parent_comment_id VARCHAR(255),
                    comment_user_id VARCHAR(255),
                    comment_user_name VARCHAR(255),
                    comment_user_location VARCHAR(255),
                    comment_floor_number INT,
                    total_number INT,
                    like_counts INT,
                    text_raw TEXT,
                    wid VARCHAR(255) NOT NULL,
                    FOREIGN KEY (wid) REFERENCES posts(wid),
                    UNIQUE KEY (comment_id)
                );
            """)
        conn.commit()
    finally:
        conn.close()

# def load_set_config():
#     try:
#         with open('set_config.json', 'r') as file:
#             return json.load(file)
#     except FileNotFoundError:
#         return {}

# def update_set_config(data):
#     with open('set_config.json', 'w') as file:
#         json.dump(data, file, indent=4)


# 记录之前的wid
global_last_wid = "4649213911111848"

def main(id=None):
    # global config_json
    # config_json = loadConfig()

    # cookie = config_json["cookie"]
    # child_max_page = config_json.get("child_max_page", 5)
    # for comment in config_json["comments"]:
    #     id = comment["id"]
    #     limit = comment.get("limit", 1000000)
    #     print(f"-------- 开始爬取 id = {id} --------")

    #     spider = WeiboCommentSpider(cookie=cookie, id=id, limit=limit, child_max_page=child_max_page)
    #     spider.crawler()

    global config_json
    global global_last_wid
    config_json = loadConfig()

    cookie = config_json["cookie"]
    child_max_page = config_json.get("child_max_page", 5)
    
    create_comment_table()

    last_wid = get_last_wid()
    last_wid = config_json["start_id"] if config_json["start_id"] else last_wid
    global_last_wid = config_json["start_id"] if config_json["start_id"] else last_wid

    
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # set_config = load_set_config()
            # set_last_wid = set_config.get('last_wid',None)
            # last_wid = get_last_wid()
            last_wid = global_last_wid if global_last_wid else last_wid


            while True:
                # last_wid = load_set_config().get('last_wid')
                # last_wid = global_last_wid
                if last_wid is not None:
                    query = "SELECT wid FROM posts WHERE wid > %s ORDER BY wid ASC LIMIT 20"
                    cursor.execute(query, (last_wid,))
                else:
                    query = "SELECT wid FROM posts ORDER BY wid ASC"
                    cursor.execute(query)

                posts = cursor.fetchall()
                posts_size = len(posts)

                for post in posts:
                    wid = post['wid']
                    print(f"-------- 开始爬取 wid = {wid} --------")
                    spider = WeiboCommentSpider(cookie=cookie, id=wid, limit=10000, child_max_page=child_max_page)
                    spider.crawler()
                    time_per_wid = 2
                    sleep(time_per_wid)
                    # 更新配置文件，存储正在爬取的 wid
                    global_last_wid = wid
                    # update_set_config({'last_wid': current_wid})
                
                if posts_size == 0:
                    print("没有更多的帖子需要爬取，现在退出。")
                    break

    finally:
        conn.close()

if __name__ == "__main__":
    while True:
        try:
            main()
            print("完成所有爬取任务，现在退出。")
            break  # 如果没有异常发生，退出循环
        except Exception as e:
            print(f"在运行过程中遇到错误: {e}")
            print("等待 60 秒后重试...")
            sleep(60)  # 发生异常时等待一分钟

