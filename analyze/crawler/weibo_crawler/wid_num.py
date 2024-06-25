import pymysql

def connect_db():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='123456', # password='huchp6',
                           db='weibo_test',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
def find_wid_position(wid):
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            query = "SELECT COUNT(*) AS Position FROM posts WHERE wid < %s"
            cursor.execute(query, (wid,))
            result = cursor.fetchone()
            if result:
                # 返回位置：计数结果 + 1（因为 SQL 计数是从 1 开始的）
                return result['Position'] + 1
            else:
                return None
    finally:
        conn.close()

# 使用示例
wid = 3478947780280316
position = find_wid_position(wid)
if position:
    print(f"wid {wid} 在数据库中的位置是: {position}")
else:
    print("无法找到指定的 wid")
