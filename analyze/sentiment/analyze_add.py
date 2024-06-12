import json
import sys
def add_sentiments(analyze_reslut_file, post_senti_file, output_file):
    # 读取文件A
    with open(analyze_reslut_file, 'r', encoding='utf-8') as file:
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
    # 示例用法
    analyze_result = sys.argv[1] # 'analyze_result_0527.json'  
    post_sentiment_counts = sys.argv[2] # 'sentiments_counts_eng.json'  
    output_file = analyze_result[:-5]+'_with_sentiment.json'
    add_sentiments(analyze_result, post_sentiment_counts, output_file)

        