import jieba
from jieba import analyse
from collections import Counter
import json
import pandas as pd
from datetime import datetime
import time
import sys
import os
from pathlib import Path
import argparse

def get_main_texts(json_file):
    wid_texts = {}  # 用于存储根据"wid"分组的评论

    min_publish_time = datetime.max
    max_publish_time = datetime.min
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

        # 遍历每个JSON对象
        for json_obj in data:

            # 最早和最晚时间
            publish_time = datetime.fromisoformat(json_obj['publish_time'])
            if publish_time < min_publish_time:
                min_publish_time = publish_time
            if publish_time > max_publish_time:
                max_publish_time = publish_time

            # 检查JSON对象中是否有"comments"和"wgid"字段
            if 'text' in json_obj and 'wid' in json_obj:
                text = json_obj['text']
                wid = json_obj['wid']
                if text:
                    wid_texts[wid] = text
    # print(wid_texts)
    return wid_texts, min_publish_time, max_publish_time

def group_texts_by_title(analyze_file, wid_texts, output_file):
    # 读取文件A
    with open(analyze_file, 'r', encoding='utf-8') as file:
        data_analyze = json.load(file)
    # 根据titleid将文件C中的JSON对象进行分组
    grouped_texts = {}
    # print(len(wid_texts.items()))
    for wid, text in wid_texts.items():
        for title_id, value in data_analyze.items():
            # print(key_a,value_a)
            posts = value.get("posts", [])
            if wid in posts:
                # title = value_a.get("title")
                if title_id in grouped_texts:
                    grouped_texts[title_id].append(text)
                else:
                    grouped_texts[title_id] = [text] 

    # print(grouped_texts)

    # 构建最终的JSON集合
    json_collection = []
    for title_id, value in data_analyze.items():
        json_obj = {
            "id": title_id,
            "title": value.get("title"),
            "texts": grouped_texts.get(title_id, [])
        }
        json_collection.append(json_obj)
        # print(grouped_texts.get(value_a.get("title"), []))

    # 将最终的JSON集合写入新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(json_collection, file, ensure_ascii=False, indent=4)


def jieba_e_result(texts, top_n = 20):

    stop_words = set()
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        for line in file:
            stop_words.add(line.strip())

    keyword_freq = Counter() 
    # 遍历文本列表
    for text in texts:
        # 使用jieba进行分词
        seg_list = jieba.cut(text)
        seg_text = " ".join(seg_list)
        # 使用jieba.analyse.extract_tags方法进行关键词提取
        keywords = jieba.analyse.extract_tags(seg_text, topK=5)
        
        words = jieba.lcut(text)
        # 停用词过滤
        words = [word for word in words if word not in stop_words]
        # 关键词过滤
        key_words = [word for word in words if word in keywords]
        # 统计关键词的词频
        keyword_freq.update(key_words)
        
    # return keyword_freq.most_common(top_n)
    result = []
    for word, freq in keyword_freq.most_common(top_n):
        result.append({"name": word, "value": freq})

    return result

def title_word_count(grouped_json_file, total_count_output_file):
    title_wordcount = {}
    total_count = Counter()
    with open(grouped_json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for json_obj in data:
            title_id = json_obj['id']
            title = json_obj['title']
            texts = json_obj['texts']
            result = jieba_e_result(texts)
            title_wordcount[title_id] = result
            # df = pd.DataFrame(result, columns=['Keyword', 'Count'])
            # 获取当前脚本文件的路径
            # current_file = os.path.abspath(__file__)
            # # 获取当前文件所在目录的路径
            # current_dir = os.path.dirname(current_file)
            # # 创建结果文件夹路径
            # result_dir = os.path.join(current_dir, output_dir)
            # # 检查结果文件夹是否存在，如果不存在则创建
            # if not os.path.exists(result_dir):
            #     os.makedirs(result_dir)

            # output_file = ""
            # if title_id is not None and title is not None:
            #     output_file = os.path.join(result_dir, f"{title_id}_{title}_wordcount.json")
            # else:
            #     # 提供一个默认的文件名
            #     output_file = os.path.join(result_dir, f"{title_id}_no_title_default_wordcount.json")

            # # df.to_csv(output_file, index=False)
            # with open(output_file, 'w', encoding='utf-8') as outfile:
            #     json.dump(result, outfile, ensure_ascii=False, indent=2)
            # print("结果已保存到", output_file)

    for result in title_wordcount.values():
        for item in result:
            word = item['name']
            freq = item['value']
            total_count[word] += freq

    total_json = []
    for word, freq in total_count.most_common(50):
        total_json.append({"name": word, "value": freq})
    with open(total_count_output_file, 'w', encoding='utf-8') as outfile:
        json.dump({"data": total_json}, outfile, ensure_ascii=False, indent=2)

    # 删除grouped_json_file文件
    os.remove(grouped_json_file)
    print("已生成总词频文件：" + total_count_output_file)
    return title_wordcount

def merge(title_word_count, analyse_result_file, output_file):
    with open(analyse_result_file, 'r', encoding='utf-8') as file:
        analyze_data = json.load(file)
    for key, value in analyze_data.items():
        if title_word_count[key]:
            value["word_count"] = title_word_count[key]
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(analyze_data, file, ensure_ascii=False, indent=4)
    print("...单事件词频已合并到：" + output_file)

def do_process(json_file, analyse_result_file, grouped_output_file,total_count_output_file, output_file):
    s_t = time.time()
    wid_texts, min_time, max_time = get_main_texts(json_file)
    group_texts_by_title(analyse_result_file, wid_texts, grouped_output_file)
    title_wordcount = title_word_count(grouped_output_file, total_count_output_file)
    merge(title_wordcount, analyse_result_file, output_file)

    e_t = time.time()
    elapsed_time = "{:.2f}".format(e_t - s_t)
    print(elapsed_time)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-source_data_file', type=str, required=True,
    help='源数据文件的路径。')
    parser.add_argument('-topic_sentiment_result_file', type=str, required=True,
    help='结合了情感分析后的topic分析结果文件的路径。')
    parser.add_argument('-totalwc_target_file', type=str, required=True,
    help='总词频的保存路径。')
    parser.add_argument('-topic_senti_wc_target_file', type=str, required=True,
    help='单事件词频集成到topic+情感结果文件的保存路径。')

    args = parser.parse_args()
    json_file = args.source_data_file
    topic_sentiment_result_file = args.topic_sentiment_result_file # "analyze_result_0527.json"
    total_count_output_file = args.totalwc_target_file # 总词频
    output_file = args.topic_senti_wc_target_file # 单事件词频集成到结果文件
    
    stopwords_file = os.path.join(Path(__file__).resolve().parent, 'stopwords.txt')

    # 获取当前的日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间为字符串
    formatted_datetime = current_datetime.strftime("%m%d%H%M%S")

    grouped_output_file = total_count_output_file[:-5] + "can_delete_title_group_texts"+ "_" + formatted_datetime + ".json"
    # output_dir = "title_count_"+json_file[:-5]+"_jieba"

    do_process(json_file, topic_sentiment_result_file, grouped_output_file, total_count_output_file, output_file)

