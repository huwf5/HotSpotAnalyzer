from django.http import JsonResponse
from django.shortcuts import render
import json
from datetime import datetime
from dateutil import parser
import numpy as np
from django.http import JsonResponse
from django.conf import settings
import json
import os


def find_closest_date_file(directory):
    # 获取当前日期
    current_date = datetime.now().date()

    # 初始化最小差异和目标文件名
    min_diff = float('inf')
    closest_file = None

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        # 假设文件名格式中包含日期，格式为 YYYY-MM-DD
        try:
            # 提取文件名中的日期部分并解析
            file_date_str = filename.split('.')[0]  # 假设日期直接在文件名中，没有其他额外文本
            file_date = parser.parse(file_date_str).date()

            # 计算与当前日期的差异
            diff = abs((file_date - current_date).days)

            # 更新最近的文件
            if diff < min_diff:
                min_diff = diff
                closest_file = filename
        except ValueError:
            # 如果日期解析失败，忽略这个文件
            continue

    return closest_file


def fetch_wordCloud(request):
    date = request.GET.get('date')
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'word_cloud', f'{date}.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return JsonResponse(data)


def fetch_graph(request):
    date = request.GET.get('date')
    print(f"graphDate:{date}")
    # 构建文件的绝对路径
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', '3d-force-graph', f'{date}.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return JsonResponse(data)

def fetch_emotionData(request):
    date = request.GET.get('date')
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'emotion_data', f'{date}.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return JsonResponse(data)


def fetch_chartData(request):
    date = request.GET.get('date')
    print(f"chartDataDate:{date}")
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'chart_data', f"{date}.json")
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return JsonResponse(data)


def fetch_cardList(request):
    try:
        # 构建文件的绝对路径
        file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'weibo_data')
        filename = find_closest_date_file(file_path)
        file_path = os.path.join(file_path, filename)
        print(file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        num_of_posts = len(data)
        like_counts = int(np.sum([dataItem["like_count"] for dataItem in data]))
        comment_counts = int(np.sum(dataItem["comment_count"] for dataItem in data))
        forward_counts = int(np.sum(dataItem["forward_count"] for dataItem in data))

        history_num_of_posts = 0
        history_like_counts = 0
        history_comment_counts = 0
        history_forward_counts = 0
        for filename in os.listdir(os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'weibo_data')):
            path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'weibo_data', filename)
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            history_num_of_posts += len(data)
            history_like_counts += int(np.sum(dataItem["comment_count"] for dataItem in data))
            history_comment_counts += int(np.sum(dataItem["comment_count"] for dataItem in data))
            history_forward_counts += int(np.sum(dataItem["forward_count"] for dataItem in data))

        message = {
            "last_month": {
                "posts": num_of_posts,
                "like_counts": like_counts,
                "comment_counts": comment_counts,
                "forward_counts": forward_counts
            },
            "history": {
                "posts": history_num_of_posts,
                "like_counts": history_like_counts,
                "comment_counts": history_comment_counts,
                "forward_counts": history_forward_counts
            }
        }
        return JsonResponse(message)
    except FileNotFoundError:
        return JsonResponse({'error': 'The specified file was not found.'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Failed to decode JSON from the file.'}, status=500)
    except Exception as e:
        print(e)
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)


def fetch_topicCard(request):
    date = request.GET.get('date')
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'topic_data', f'{date}.json')
    print(os.path.exists(file_path))
    with open(file_path, 'r', encoding='utf-8') as file:
        topic_data = json.load(file)
    source_data_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'weibo_data', f'{date}.json')

    with open(source_data_path, 'r', encoding='utf-8') as file:
        source_data = json.load(file)
    print("ok")
    message = {}
    message["num_of_topics"] = len(topic_data.keys())
    message["num_of_posts"] = len(source_data)
    message["num_of_comments"] = int(np.sum(dataItem["comment_count"] for dataItem in source_data))
    topic_list = [topicItem[1] for topicItem in topic_data.items() if topicItem[1]["is_news"]]

    topic_list = sorted(topic_list, key=lambda topicItem: len(topicItem["posts"]), reverse=True)
    message["topic_list"] = topic_list[:6]
    total_discussion = 0
    for topic in message["topic_list"]:
        for postId in topic["posts"]:
            total_discussion += int(np.sum([dataItem["comment_count"] for dataItem in source_data
                                            if dataItem["wid"] == postId])) + 1

    for topic in message["topic_list"]:
        topic_comment_counts = int(np.sum([dataItem["comment_count"] for dataItem in source_data
                                           if dataItem["wid"] in topic["posts"]]))
        topic["progress"] = (topic_comment_counts + len(topic["posts"])) / total_discussion
        topic["num_of_posts"] = len(topic["posts"])
        topic["date"] = [dataItem["publish_time"] for dataItem in source_data if dataItem["wid"]
                         in topic["posts"]][0].split('T')[0]
    return JsonResponse(message)

def find_event_by_title(title):
    dir = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'topic_data')
    for filename in os.listdir(dir):
        filepath = os.path.join(dir, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            source_data = json.load(file)
        for key, value in source_data.items():
            if value["title"] == title:
                return (value, filename.split(".")[0])
def find_post_by_wid(wid, source):
    for item in source:
        if item["wid"] == wid:
            return item
def fetch_event(request):
    title, date = request.GET.get('title')
    content = find_event_by_title(title)
    filepath = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'weibo_data', f'{date}.json')
    with open(filepath, 'r', encoding='utf-8') as file:
        source_data = json.load(file)
    content["like_count"] = 0
    content["forward_count"] = 0
    content["comment_count"] = 0
    for wid in content["posts"]:
        item = find_post_by_wid(wid, source_data)
        content["like_count"] += item["like_count"]
        content["forward_count"] += item["forward_count"]
        content["comment_count"] += item["comment_count"]
    with open(filepath, 'r', encoding='utf-8') as file:
        content["graph"] = json.load(file)
    return JsonResponse(content)