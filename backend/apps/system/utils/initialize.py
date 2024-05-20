import os
import json
from django.apps import apps


class BaseInitialize:
    def __init__(self, app=None):
        self.app = app or ""

    def init_from_json(self, Serializer, unique_fields=None):
        model = Serializer.Meta.model
        file_path = os.path.join(
            apps.get_app_config(self.app.split(".")[-1]).path,
            "fixtures",
            f"init_{Serializer.Meta.model._meta.model_name}.json",
        )
        if not os.path.exists(file_path):
            print("File not found, skipping initialization")
            return
        with open(file_path, encoding="utf-8") as f:
            for data in json.load(f):
                filter_data = {}
                if unique_fields:
                    for field in unique_fields:
                        if field in data:
                            filter_data[field] = data[field]
                else:
                    for key, value in data.items():
                        if isinstance(value, list) or value == None or value == "":
                            continue
                        filter_data[key] = value
                instance = model.objects.filter(**filter_data).first()
                serializer = Serializer(instance, data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        print(f"[{self.app}][{model._meta.model_name}] initialization completed")

    def init_from_list(self, Serializer, data_list):
        model = Serializer.Meta.model
        for obj_data in data_list:
            filter_data = {}
            for key, value in obj_data.items():
                if isinstance(value, list) or value == None or value == "":
                    continue
                filter_data[key] = value
            instance = model.objects.filter(**filter_data).first()
            serializer = Serializer(instance, data=obj_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        print(f"[{self.app}][{model._meta.model_name}] initialization completed")

    def run(self):
        raise NotImplementedError(".run() must be implemented")
