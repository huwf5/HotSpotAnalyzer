import json
from django.db import transaction
from apps.user.models import Message

class Import:
    def __init__(self,json_file):
        self.json_file = json_file
    
    def import_message(self):
        # Load the JSON file
        with open(self.json_file, "r", encoding='utf-8') as file:
            data = json.load(file)
        
        with transaction.atomic():
            for _ , item in data.items():
                title = item.get("title", "")
                summary = item.get("summary", "")
                is_news = item.get("is_news", False)
                senti_count = item.get("senti_count", 0)
                # calculate the negative sentiment ratio
                negative_sentiment_ratio = sum([
                    senti_count.get('angry', 0),
                    senti_count.get('disgusted', 0),
                    senti_count.get('scared', 0),
                    senti_count.get('sad', 0),
                    senti_count.get('disappointed', 0)
                ]) / sum(senti_count.values()) if sum(senti_count.values()) > 0 else 0

                # create the message object
                Message.objects.create(
                    title=title,
                    summary=summary,
                    negative_sentiment_ratio=negative_sentiment_ratio,
                    is_news=is_news
                )
            
    def run(self):
        self.import_message()

