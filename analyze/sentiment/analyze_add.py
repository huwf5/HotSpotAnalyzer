import json
import sys
from pathlib import Path
import argparse


def add_sentiments(analyze_result_file, post_senti_file, output_file):
    # 读取文件A
    with open(analyze_result_file, 'r', encoding='utf-8') as file:
        analyze_data = json.load(file)

    # 读取文件B
    with open(post_senti_file, 'r', encoding='utf-8') as file:
        post_senti = json.load(file)

    # 遍历文件A中的每个JSON对象
    for key, value in analyze_data.items():
        posts = value.get("posts", [])

        # 统计senti_count的总计数
        senti_count_total = {}
        for post in posts:
            senti_count = post_senti.get(post)
            for senti, count in senti_count.items():
                senti_count_total[senti] = senti_count_total.get(senti, 0) + count

        # 将总计数添加到文件A中的每个JSON对象中，并删除"joy"字段
        value["senti_count"] = senti_count_total
        value.pop("joy", None)

    # 将更新后的数据写入新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(analyze_data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-topic_result_file', type=str, required=True,
    help='热点topic分析结果文件的路径。')
    parser.add_argument('-post_senti_result_file', type=str, required=True,
    help='帖子情感分析结果文件路径')
    parser.add_argument('-topic_sentiment_target_file', type=str, required=True,
    help='topic+情感结果文件的保存路径。')

    args = parser.parse_args()
    topic_result = args.topic_result_file 
    post_sentiment_counts = args.post_senti_result_file 
    output_file = args.topic_sentiment_target_file

    add_sentiments(topic_result, post_sentiment_counts, output_file)

        