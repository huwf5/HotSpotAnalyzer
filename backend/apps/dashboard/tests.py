from rest_framework.throttling import BaseThrottle
import os
import json
from django.urls import reverse
from django.conf import settings
from apps.user.models import User, Role
from django.test import TestCase, Client
from unittest.mock import patch, MagicMock
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

# Create your tests here.
class NoThrottle(BaseThrottle):
    def allow_request(self, request, view):
        return True

# 定义一个不进行限流的类
class GraphViewSetTests(TestCase):
    def setUp(self):
        # 创建一个用户并生成JWT token
        self.role_user = Role.objects.create(role="User")
        self.user = User.objects._create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword",
            role=self.role_user,
        )
        self.client = Client()
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + self.token

    @patch("apps.dashboard.views.GraphViewSet.throttle_classes", [NoThrottle])
    def test_fetch_graph_success(self):
        # 创建一个日期文件
        test_date = '2023-01-01'
        file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', '3d-force-graph', f'{test_date}.json')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        test_data = {"graph": "data"}
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(test_data, file)

        url = reverse('graphs')  # 根据你的URL配置，这个可能需要调整
        response = self.client.get(url, {'date': test_date})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), test_data)

    @patch("apps.dashboard.views.GraphViewSet.throttle_classes", [NoThrottle])
    def test_fetch_graph_missing_date(self):
        url = reverse('graphs')  # 根据你的URL配置，这个可能需要调整
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Date parameter is required.'})

    @patch("apps.dashboard.views.GraphViewSet.throttle_classes", [NoThrottle])
    def test_fetch_graph_file_not_found(self):
        test_date = '2023-01-02'
        url = reverse('graphs')  # 根据你的URL配置，这个可能需要调整
        response = self.client.get(url, {'date': test_date})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"error": "Graph data file not found for the specified date."})

    @patch("apps.dashboard.views.GraphViewSet.throttle_classes", [NoThrottle])
    def test_fetch_graph_invalid_date_format(self):
        test_date = 'invalid-date'
        url = reverse('graphs')  # 根据你的URL配置，这个可能需要调整
        response = self.client.get(url, {'date': test_date})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # 这里假设你的视图会返回一个特定的错误消息，如果不是，请相应调整
        self.assertIn("error", response.json())

    def tearDown(self):
        # 清理创建的测试文件
        test_date = '2023-01-01'
        file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', '3d-force-graph', f'{test_date}.json')
        if os.path.exists(file_path):
            os.remove(file_path)

class WordCloudViewSetTests(TestCase):
    def setUp(self):
        # 创建一个用户并生成JWT token
        self.role_user = Role.objects.create(role="User")
        self.user = User.objects._create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword",
            role=self.role_user,
        )
        self.client = Client()
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + self.token

    @patch("apps.dashboard.views.WordCloudViewSet.throttle_classes", [NoThrottle])
    def test_fetch_word_cloud_success(self):
        # 创建一个日期文件
        test_date = '2023-01-01'
        file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'topic_data', f'{test_date}.json')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        test_data = {
            "some_id": {
                "word_count": [{"name": "test", "value": 50}, {"name": "word", "value": 30}]
            }
        }
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(test_data, file)

        url = reverse('wordcloud')  # 根据你的URL配置，这个可能需要调整
        response = self.client.get(url, {'date': test_date})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "data": [{"name": "test", "value": 50}, {"name": "word", "value": 30}]
        }
        self.assertEqual(response.json(), expected_data)

    @patch("apps.dashboard.views.WordCloudViewSet.throttle_classes", [NoThrottle])
    def test_fetch_word_cloud_missing_date(self):
        url = reverse('wordcloud')  # 根据你的URL配置，这个可能需要调整
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'error': 'File not found'})

    @patch("apps.dashboard.views.WordCloudViewSet.throttle_classes", [NoThrottle])
    def test_fetch_word_cloud_file_not_found(self):
        test_date = '2023-01-02'
        url = reverse('wordcloud')  # 根据你的URL配置，这个可能需要调整
        response = self.client.get(url, {'date': test_date})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"error": "File not found"})

    @patch("apps.dashboard.views.WordCloudViewSet.throttle_classes", [NoThrottle])
    def test_fetch_word_cloud_invalid_date_format(self):
        test_date = 'invalid-date'
        url = reverse('wordcloud')  # 根据你的URL配置，这个可能需要调整
        response = self.client.get(url, {'date': test_date})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # 这里假设你的视图会返回一个特定的错误消息，如果不是，请相应调整
        self.assertIn("error", response.json())

    def tearDown(self):
        # 清理创建的测试文件
        test_date = '2023-01-01'
        file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'topic_data', f'{test_date}.json')
        if os.path.exists(file_path):
            os.remove(file_path)

class TopicCardViewSetTests(TestCase):
    def setUp(self):
        # 创建角色和用户，并生成JWT token
        self.role_user = Role.objects.create(role="User")
        self.user = User.objects._create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword",
            role=self.role_user,
        )
        self.client = Client()
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + self.token

    @patch("apps.dashboard.views.TopicCardViewSet.throttle_classes", [NoThrottle])
    def test_fetch_topic_card_success(self):
        # 创建测试数据文件
        date = '2023-01-01'
        topic_data_dir = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'topic_data')
        weibo_data_dir = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'weibo_data')
        os.makedirs(topic_data_dir, exist_ok=True)
        os.makedirs(weibo_data_dir, exist_ok=True)

        topic_data = {
            "topic1": {"is_news": True, "posts": ["post1", "post2"]},
            "topic2": {"is_news": True, "posts": ["post3"]},
            "topic3": {"is_news": False, "posts": ["post4"]}
        }
        weibo_data = [
            {"wid": "post1", "comment_count": 5, "publish_time": "2023-01-01T10:00:00"},
            {"wid": "post2", "comment_count": 10, "publish_time": "2023-01-01T11:00:00"},
            {"wid": "post3", "comment_count": 2, "publish_time": "2023-01-01T12:00:00"},
            {"wid": "post4", "comment_count": 3, "publish_time": "2023-01-01T13:00:00"}
        ]

        with open(os.path.join(topic_data_dir, f'{date}.json'), 'w', encoding='utf-8') as file:
            json.dump(topic_data, file)

        with open(os.path.join(weibo_data_dir, f'{date}.json'), 'w', encoding='utf-8') as file:
            json.dump(weibo_data, file)

        url = reverse('topiccard')  # 修改为你的URL名称
        response = self.client.get(url, {'date': date})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "num_of_topics": 3,
            "num_of_posts": 4,
            "num_of_comments": 20,
            "topic_list": [
                {
                    "is_news": True,
                    "posts": ["post1", "post2"],
                    "progress": 0.85,
                    "num_of_posts": 2,
                    "date": "2023-01-01"
                },
                {
                    "is_news": True,
                    "posts": ["post3"],
                    "progress": 0.15,
                    "num_of_posts": 1,
                    "date": "2023-01-01"
                }
            ]
        }
        self.assertEqual(response.json(), expected_data)

    @patch("apps.dashboard.views.TopicCardViewSet.throttle_classes", [NoThrottle])
    def test_fetch_topic_card_file_not_found(self):
        date = '2023-01-01'
        url = reverse('topiccard')  # 修改为你的URL名称
        response = self.client.get(url, {'date': date})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'error': 'Topic data file not found.'})

    @patch("apps.dashboard.views.TopicCardViewSet.throttle_classes", [NoThrottle])
    def test_fetch_topic_card_json_decode_error(self):
        # 创建一个格式错误的JSON文件
        date = '2023-01-01'
        topic_data_dir = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'topic_data')
        os.makedirs(topic_data_dir, exist_ok=True)

        with open(os.path.join(topic_data_dir, f'{date}.json'), 'w', encoding='utf-8') as file:
            file.write('{"topic1": {"is_news": True, "posts": ["post1", "post2"]')  # 缺少右括号

        url = reverse('topiccard')  # 修改为你的URL名称
        response = self.client.get(url, {'date': date})

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventViewSetTests(TestCase):
    def setUp(self):
        self.role_user = Role.objects.create(role="User")
        self.user = User.objects._create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword",
            role=self.role_user,
        )
        self.client = Client()
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + self.token

    @patch("apps.dashboard.views.EventViewSet.throttle_classes", [NoThrottle])
    def test_fetch_event_missing_title(self):
        url = reverse('event')  # 修改为你的URL名称
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"error": "标题参数是必需的。"})

    @patch("apps.dashboard.views.EventViewSet.throttle_classes", [NoThrottle])
    @patch("apps.dashboard.views.find_event_by_title")
    def test_fetch_event_file_not_found(self, mock_find_event_by_title):
        title = 'Test Event'
        date = '2023-01-01'
        key = 'event_key'
        value = {
            "is_news": True,
            "posts": ["post1", "post2"],
            "word_count": 100,
            "senti_count": 20
        }
        mock_find_event_by_title.return_value = (key, value, date)

        url = reverse('event')  # 修改为你的URL名称
        response = self.client.get(url, {'title': title})

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.json())

    @patch("apps.dashboard.views.find_post_by_wid")
    @patch("apps.dashboard.views.find_event_by_title")
    def test_fetch_event_internal_error(self, mock_find_post_by_wid, mock_find_event_by_title):
        title = 'Test Event'
        date = '2023-01-01'
        key = 'event_key'
        value = {
            "is_news": True,
            "posts": ["post1", "post2"],
            "word_count": 100,
            "senti_count": 20
        }
        mock_find_event_by_title.return_value = (key, value, date)

        source_data = [
            {"wid": "post1", "like_count": 5, "forward_count": 10, "comment_count": 15},
            {"wid": "post2", "like_count": 3, "forward_count": 6, "comment_count": 9}
        ]
        mock_find_post_by_wid.side_effect = lambda wid, data: next(item for item in data if item["wid"] == wid)

        weibo_data_dir = os.path.join(os.path.dirname(settings.BASE_DIR), 'result', 'weibo_data')
        os.makedirs(weibo_data_dir, exist_ok=True)
        with open(os.path.join(weibo_data_dir, f'{date}.json'), 'w', encoding='utf-8') as file:
            json.dump(source_data, file)

        # Simulate an internal error by raising an exception when opening the graph file
        def raise_exception(*args, **kwargs):
            raise IOError("Simulated IOError")

        with patch("builtins.open", side_effect=raise_exception):
            url = reverse('event-fetch-event')  # 修改为你的URL名称
            response = self.client.get(url, {'title': title})

            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertIn('error', response.json())
            self.assertTrue(response.json()['error'].startswith('发生意外错误：'))