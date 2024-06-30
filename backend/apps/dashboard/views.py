from datetime import datetime

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import os
import json
import numpy as np
from django.conf import settings
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from collections import defaultdict
import heapq
from dateutil import parser
from datetime import datetime, timedelta

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

class GraphViewSet(viewsets.ViewSet):
    # 设置权限，只允许经过身份验证的用户访问
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='get',
        operation_summary="Fetch Graph Data",
        operation_description="Fetches and returns graph data for a specific date in JSON format.",
        manual_parameters=[
            openapi.Parameter(
                'date',
                openapi.IN_QUERY,
                description="Date for which to fetch the graph data, formatted as YYYY-MM-DD.",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response('Graph data retrieved successfully'),
            400: 'Invalid date format or missing date',
            404: 'Graph data file not found for the specified date'
        }
    )
    @action(detail=False, methods=['get'])
    def fetch_graph(self, request):
        date = request.GET.get('date')
        if not date:
            return Response({"error": "Date parameter is required."}, status=400)

        try:
            # 构建文件的绝对路径
            file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', '3d-force-graph', f'{date}.json')
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return JsonResponse(data)
        except FileNotFoundError:
            return Response({"error": "Graph data file not found for the specified date."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class WordCloudViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='get',
        operation_summary="Fetch Word Cloud Data",
        operation_description="Fetches and returns the word cloud data for a specific date, showing top 30 words by frequency.",
        manual_parameters=[
            openapi.Parameter(
                'date',
                openapi.IN_QUERY,
                description="Date for which to fetch the word cloud, formatted as YYYY-MM-DD.",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response('Word cloud data retrieved successfully'),
            404: 'File not found',
            500: 'Error processing the JSON data'
        }
    )
    @action(detail=False, methods=['get'])
    def fetch_word_cloud(self, request):
        date = request.query_params.get('date')
        file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'topic_data', f'{date}.json')

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                all_data = json.load(file)

            word_counts = defaultdict(int)
            for item in all_data.values():
                for word_info in item['word_count']:
                    word_counts[word_info['name']] += word_info['value']

            top_words = heapq.nlargest(30, word_counts.items(), key=lambda x: x[1])
            result = {
                "data": [{"name": word, "value": count} for word, count in top_words]
            }

            return Response(result)
        except FileNotFoundError:
            return Response({'error': 'File not found'}, status=404)
        except json.JSONDecodeError:
            return Response({'error': 'Error decoding JSON'}, status=500)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class EmotionViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='get',
        operation_summary="Fetch Emotion Data",
        operation_description="Fetches and returns the emotional data analysis for a specific date, presenting it as percentages of total emotions expressed.",
        manual_parameters=[
            openapi.Parameter(
                'date',
                openapi.IN_QUERY,
                description="Date for which to fetch the emotion data, formatted as YYYY-MM-DD.",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response('Emotion data retrieved successfully'),
            400: 'Invalid date format or missing date',
            404: 'Data file not found',
            500: 'Server error'
        }
    )
    @action(detail=False, methods=['get'])
    def fetch_emotions(self, request):
        date = request.GET.get('date')
        file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'topic_data', f'{date}.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            total_emotions = {
                "joyful": 0,
                "sad": 0,
                "angry": 0,
                "disgusted": 0,
                "scared": 0,
                "surprised": 0,
                "calm": 0,
                "disappointed": 0
            }

            # Accumulate counts from all entries
            for entry in data.values():
                for emotion, count in entry['senti_count'].items():
                    total_emotions[emotion] += count

            # Calculate total counts and percentages
            total_count = sum(total_emotions.values())
            emotion_percentages = []
            for emotion, count in total_emotions.items():
                if total_count > 0:
                    percentage = (count / total_count) * 100
                else:
                    percentage = 0
                emotion_percentages.append({
                    "emotion": emotion.capitalize(),
                    "percentage": round(percentage, 2)
                })

            return JsonResponse({"data": emotion_percentages})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

class CardListViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='get',
        operation_summary="Fetch Weibo Card List Data",
        operation_description="Fetches statistical data about Weibo posts, including counts of likes, comments, and forwards for the last month and historically.",
        responses={
            200: openapi.Response('Data retrieved successfully'),
            404: 'File not found',
            500: 'Internal server error'
        }
    )
    @action(detail=False, methods=['get'])
    def fetch_card_list(self, request):
        try:
            # Construct the absolute path to the data file
            dir_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'weibo_data')
            filename = find_closest_date_file(dir_path)
            file_path = os.path.join(dir_path, filename)
            print(file_path)

            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Current month data
            num_of_posts = len(data)
            like_counts = int(np.sum([dataItem["like_count"] for dataItem in data]))
            comment_counts = int(np.sum(dataItem["comment_count"] for dataItem in data))
            forward_counts = int(np.sum(dataItem["forward_count"] for dataItem in data))

            # Historical data
            history_num_of_posts = 0
            history_like_counts = 0
            history_comment_counts = 0
            history_forward_counts = 0
            for filename in os.listdir(dir_path):
                path = os.path.join(dir_path, filename)
                with open(path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                history_num_of_posts += len(data)
                history_like_counts += int(np.sum(dataItem["like_count"] for dataItem in data))
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
            return Response(message)
        except FileNotFoundError:
            return Response({'error': 'The specified file was not found.'}, status=404)
        except json.JSONDecodeError:
            return Response({'error': 'Failed to decode JSON from the file.'}, status=500)
        except Exception as e:
            print(e)
            return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

class TopicCardViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='get',
        operation_summary="Fetch Topic Card Data",
        operation_description="Fetches data about topics for a given date including the number of topics, posts, and comments.",
        manual_parameters=[
            openapi.Parameter('date', openapi.IN_QUERY, description="Date for which data is requested in YYYY-MM-DD format", type=openapi.TYPE_STRING, required=True)
        ],
        responses={
            200: openapi.Response('Data retrieved successfully'),
            404: 'File not found',
            500: 'Internal server error'
        }
    )
    @action(detail=False, methods=['get'])
    def fetch_topic_card(self, request):
        date = request.GET.get('date')
        file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'topic_data', f'{date}.json')

        # Check if the file exists
        if not os.path.exists(file_path):
            return Response({'error': 'Topic data file not found.'}, status=404)

        # Load topic data
        with open(file_path, 'r', encoding='utf-8') as file:
            topic_data = json.load(file)

        source_data_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'weibo_data', f'{date}.json')
        # Load source data
        with open(source_data_path, 'r', encoding='utf-8') as file:
            source_data = json.load(file)

        message = {
            "num_of_topics": len(topic_data.keys()),
            "num_of_posts": len(source_data),
            "num_of_comments": int(np.sum(dataItem["comment_count"] for dataItem in source_data))
        }

        # Process topics
        topic_list = [topicItem[1] for topicItem in topic_data.items() if topicItem[1]["is_news"]]
        topic_list = sorted(topic_list, key=lambda topicItem: len(topicItem["posts"]), reverse=True)

        message["topic_list"] = topic_list[:6]
        total_discussion = sum(
            int(np.sum([dataItem["comment_count"] for dataItem in source_data if dataItem["wid"] == postId])) + 1
            for topic in message["topic_list"] for postId in topic["posts"]
        )

        for topic in message["topic_list"]:
            topic_comment_counts = int(np.sum([dataItem["comment_count"] for dataItem in source_data
                                               if dataItem["wid"] in topic["posts"]]))
            topic["progress"] = (topic_comment_counts + len(topic["posts"])) / total_discussion
            topic["num_of_posts"] = len(topic["posts"])
            topic["date"] = [dataItem["publish_time"] for dataItem in source_data if dataItem["wid"]
                             in topic["posts"]][0].split('T')[0]

        return Response(message)

def find_event_by_title(title):
    dir = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'topic_data')
    for filename in os.listdir(dir):
        filepath = os.path.join(dir, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            source_data = json.load(file)
        for key, value in source_data.items():
            if value["title"] == title:
                return (key, value, filename.split(".")[0])
    return None, None, None
def find_post_by_wid(wid, source):
    for item in source:
        if item["wid"] == wid:
            return item

class EventViewSet(viewsets.ViewSet):
    """
    ViewSet 处理根据标题获取事件数据的请求。
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='get',
        operation_summary="根据标题获取事件数据",
        operation_description="根据事件标题获取包括点赞数、转发数、评论数等详细信息。",
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, description="事件的标题", type=openapi.TYPE_STRING, required=True)
        ],
        responses={
            200: openapi.Response('成功获取事件数据'),
            400: '请求参数错误',
            404: '未找到数据',
            500: '服务器内部错误'
        }
    )
    @action(detail=False, methods=['get'])
    def fetch_event(self, request):
        try:
            title = request.GET.get('title')
            if not title:
                return Response({"error": "标题参数是必需的。"}, status=400)
            key, value, date = find_event_by_title(title)
            if value is None:
                return Response({'error': f'该标题不存在'}, status=400)
            filepath = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'weibo_data', f'{date}.json')
            with open(filepath, 'r', encoding='utf-8') as file:
                source_data = json.load(file)

            content = {
                "summary": value["summary"],
                "like_count": 0,
                "forward_count": 0,
                "comment_count": 0,
            }

            for wid in value["posts"]:
                item = find_post_by_wid(wid, source_data)
                content["like_count"] += item["like_count"]
                content["forward_count"] += item["forward_count"]
                content["comment_count"] += item["comment_count"]


            graph_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'graph', f'{date}.json')
            with open(graph_path, 'r', encoding='utf-8') as file:
                graphs = json.load(file)
            if key in graphs.keys():
                content["graph"] = graphs[key]
            else:
                content["graph"] = None

            content["word_count"] = value["word_count"]
            content["senti_count"] = value["senti_count"]

            return Response(content)
        except Exception as e:
            return Response({'error': f'发生意外错误：{str(e)}'}, status=500)

class SearchEventViewSet(viewsets.ViewSet):
    """
    ViewSet 获取标题或摘要中含有给定子串的事件。
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='get',
        operation_summary="获取包含给定子串的事件",
        operation_description="获取标题或摘要中含有给定子串的事件，返回标题、摘要、时间",
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, description="搜索的内容", type=openapi.TYPE_STRING, required=True)
        ],
        responses={
            200: openapi.Response('成功获取事件数据'),
            400: '请求参数错误',
            404: '未找到数据',
            500: '服务器内部错误'
        }
    )
    @action(detail=False, methods=['get'])
    def fetch_event(self, request):
        try:
            query = request.GET.get('query')
            if not query:
                return Response({"error": "query参数是必需的。"}, status=400)
            content = {"data": []}

            for topic_file in os.listdir(os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'topic_data')):
                filepath = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'topic_data', topic_file)
                with open(filepath, 'r', encoding='utf-8') as file:
                    topic_data = json.load(file)
                source = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'weibo_data', topic_file)
                with open(source, 'r', encoding='utf-8') as file:
                    source_data = json.load(file)

                for key, value in topic_data.items():
                    if query in value["title"] or query in value["summary"]:
                        new_item = {"title": value["title"], "summary": value["summary"]}
                        for item in source_data:
                            if item["wid"] in value["posts"]:
                                new_item["date"] = item["publish_time"].split('T')[0]
                                break
                        content["data"].append(new_item)
            return Response(content)
        except Exception as e:
            return Response({'error': f'发生意外错误：{str(e)}'}, status=500)

class SentimentByPostViewSet(viewsets.ViewSet):
    """
    ViewSet 处理帖子的情感分析。
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='get',
        operation_summary="获取部分帖子的情感分析",
        operation_description="根据事件标题获取该事件下帖子的各类情感组分",
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, description="事件的标题", type=openapi.TYPE_STRING, required=True)
        ],
        responses={
            200: openapi.Response('成功获取事件数据'),
            400: '请求参数错误',
            404: '未找到数据',
            500: '服务器内部错误'
        }
    )
    @action(detail=False, methods=['get'])
    def fetch_sentiment(self, request):
        try:
            title = request.GET.get('title')
            if not title:
                return Response({"error": "标题参数是必需的。"}, status=400)
            key, value, date = find_event_by_title(title)
            filepath = os.path.join(os.path.dirname(settings.BASE_DIR), 'result',
                                    'sentiment', 'post_sentiment', f'{date}.json')
            with open(filepath, 'r', encoding='utf-8') as file:
                source_data = json.load(file)

            content = {
                "data": []
            }

            key, value, date = find_event_by_title(title)

            for wid in value["posts"]:
                item = source_data[wid]
                senti_sum = int(np.sum([v for v in item.values()]))
                if senti_sum > 0:
                    content["data"].append(item)
            return Response(content)
        except Exception as e:
            return Response({'error': f'发生意外错误：{str(e)}'}, status=500)

class FetchAllEventsViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='get',
        operation_summary="Fetch All Events Data",
        operation_description="Fetches data about every event, including its title and summary.",
        manual_parameters=[
        ],
        responses={
            200: openapi.Response('Data retrieved successfully'),
            404: 'File not found',
            500: 'Internal server error'
        }
    )
    @action(detail=False, methods=['get'])
    def fetch_events(self, request):
        file_dir = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'topic_data')
        content = {"data": []}
        for filename in os.listdir(file_dir):
            file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'topic_data', filename)

            if not os.path.exists(file_path):
                return Response({'error': 'Topic data file not found.'}, status=404)

            with open(file_path, 'r', encoding='utf-8') as file:
                topic_data = json.load(file)
            source = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'weibo_data', filename)

            with open(source, 'r', encoding='utf-8') as file:
                source_data = json.load(file)

            for key, value in topic_data.items():
                for item in source_data:
                    if item["wid"] in value["posts"]:
                        date = item["publish_time"].split('T')[0]
                        content["data"].append({"title": value["title"], "summary": value["summary"],
                                                "date": date})
                        break
        return Response(content)
        # Check if the file exists

class FetchChartDataViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='get',
        operation_summary="Fetch chart data",
        operation_description="Fetches chart data about recent trend.",
        manual_parameters=[openapi.Parameter('date', openapi.IN_QUERY, description="Date for which the chart data is requested in YYYY-MM-DD format.", type=openapi.TYPE_STRING, required=True)
        ],
        responses={
            200: openapi.Response('Data retrieved successfully'),
            404: 'File not found',
            500: 'Internal server error'
        }
    )
    @action(detail=False, methods=['get'])
    def fetch_chart_data(self, request):
        date = request.GET.get('date')
        file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'weibo_data', f'{date}.json')

        with open(file_path, 'r', encoding='utf-8') as file:
            source_data = json.load(file)

        # 获取所有日期并找到最晚的日期
        dates = [item['publish_time'].split('T')[0] for item in source_data]
        latest_date_str = max(dates)
        latest_date = datetime.strptime(latest_date_str, "%Y-%m-%d")

        content = {}

        # 统计每个时间段的文章数、评论数和点赞数总和
        for i in range(6):
            start_date = latest_date - timedelta(days=(i+1) * 5)
            end_date = latest_date - timedelta(days=i * 5)

            article_count = 0
            comment_count = 0
            like_count = 0

            for item in source_data:
                publish_date_str = item['publish_time'].split('T')[0]
                publish_date = datetime.strptime(publish_date_str, "%Y-%m-%d")

                if start_date < publish_date <= end_date:
                    article_count += 1
                    comment_count += item.get('comment_count', 0)
                    like_count += item.get('like_count', 0)

            # 将结果存储到 content 中
            content[start_date.strftime('%Y-%m-%d')] = article_count + comment_count + like_count

        return Response(content)
        # Check if the file exists