import datetime
import pymysql
import json
import os  # 添加 os 模块来处理文件路径

def connect_db():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='huchp6',  # 更新为您的密码
                           db='weibo_test',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def export_data():
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # 只查询最近一个月的帖子和关键词
            sql_posts = """
                SELECT p.*, k.keyword, k.title, k.link, k.stats, k.description
                FROM posts p
                JOIN keywords k ON p.keyword_id = k.id
                WHERE p.publish_time >= CURDATE() - INTERVAL 1 MONTH;
            """
            cursor.execute(sql_posts)
            posts = cursor.fetchall()

            # 对每个帖子查询评论
            for post in posts:
                sql_comments = """
                    SELECT *
                    FROM comments
                    WHERE wid = %s;
                """
                cursor.execute(sql_comments, (post['wid'],))
                comments = cursor.fetchall()
                post['comments'] = comments  # 将评论列表直接添加到帖子字典中

            # 确保 data 目录存在
            if not os.path.exists('data'):
                os.makedirs('data')

            # 使用当前日期命名 JSON 文件
            today_date = datetime.datetime.now().strftime("%Y-%m-%d")
            filename = f"data/data_{today_date}.json"
            
            # 导出到 JSON 文件
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(posts, jsonfile, ensure_ascii=False, indent=4, default=json_serial)
                
    finally:
        connection.close()

if __name__ == '__main__':
    export_data()
