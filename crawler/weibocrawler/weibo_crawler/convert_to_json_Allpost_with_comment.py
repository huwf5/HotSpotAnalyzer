import datetime
import pymysql
import json

def connect_db():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='123456',  # 更新为您的密码
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
            # 查询帖子和关键词
            sql_posts = """
                SELECT p.*, k.keyword, k.title, k.link, k.stats, k.description
                FROM posts p
                JOIN keywords k ON p.keyword_id = k.id;
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
            
            # Export to JSON
            with open('data_Allpost_with_comment.json', 'w', encoding='utf-8') as jsonfile:
                json.dump(posts, jsonfile, ensure_ascii=False, indent=4, default=json_serial)
                
    finally:
        connection.close()

if __name__ == '__main__':
    export_data()
