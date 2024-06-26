from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GraphViewSet, WordCloudViewSet, EmotionViewSet, \
    CardListViewSet, TopicCardViewSet, ChartDataViewSet, EventViewSet, SentimentByPostViewSet, \
    FetchAllEventsViewSet, SearchEventViewSet

router = DefaultRouter()
router.register(r'graphs', GraphViewSet, basename='graph')
router.register(r'wordcloud', WordCloudViewSet, basename='wordcloud')
router.register(r'emotion', EmotionViewSet, basename='emotion')
router.register(r'cardlist', CardListViewSet, basename='cardlist')
router.register(r'topiccard', TopicCardViewSet, basename='topiccard')
router.register(r'chartdata', ChartDataViewSet, basename='chartdata')
router.register(r'event', EventViewSet, basename='event')
router.register(r'senti', SentimentByPostViewSet, basename='senti')
router.register(r'allEvents', FetchAllEventsViewSet, basename='allEvents')
router.register(r'searchEvents', SearchEventViewSet, basename='searchEvents')
urlpatterns = [
    path('', include(router.urls)),
]