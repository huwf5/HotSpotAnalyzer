import datetime
import pymysql
import csv
import json
import pymysql
import csv
import json

def connect_db():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='123456',
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
            sql = """
                SELECT p.*, k.keyword, k.title, k.link, k.stats, k.description
                FROM posts p
                JOIN keywords k ON p.keyword_id = k.id;
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            
            # Export to CSV
            with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = results[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in results:
                    writer.writerow(row)
            
            # Export to JSON
            with open('data_onlyPost_And_Keyword.json', 'w', encoding='utf-8') as jsonfile:
                json.dump(results, jsonfile, ensure_ascii=False, indent=4, default=json_serial)
                
    finally:
        connection.close()

if __name__ == '__main__':
    export_data()
