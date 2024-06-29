import json
import os
import time
import re

import requests


def read_json_file(file_path):
    """读取JSON文件并返回数据"""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def save_json_file(json_dict, file_path):
    with open(file_path, 'w', encoding='utf-8') as outfile:
        json.dump(json_dict, outfile, ensure_ascii=False, indent=4)

def parse_api_response(response):
    print("response:______________________-______________\n",response)
    """
    解析 API 响应字符串，剥去可能存在的 `json` 标注，并返回 JSON 数据。

    :param response: API 响应字符串
    :return: 解析后的 JSON 数据
    :raises: json.JSONDecodeError 如果解析失败
    """
    # 使用正则表达式匹配从第一个 '{' 到最后一个 '}' 的内容
    match = re.search(r'\{.*\}', response, re.DOTALL)

    if match:
        json_str = match.group(0)
        return json.loads(json_str)
    else:
        raise json.JSONDecodeError("No valid JSON object found", response, 0)

def update_dictionary(dict_a, dict_b):
    # 更新或添加事件
    # 创建一个id到事件的映射，便于快速查找
    id_to_event_a = {event['id']: event for event in dict_a['events']}
    for event in dict_b['events']:
        if event['id'] in id_to_event_a:
            # 如果事件已存在，则更新它
            # 更新属性的简单实现：直接覆盖
            id_to_event_a[event['id']] = event
        else:
            # 如果事件不存在，则添加它
            dict_a['events'].append(event)

    # 更新或添加关系
    # 为了避免重复关系，我们需要检查每个关系是否已经存在
    existing_relationships = set((rel['source'], rel['target'], rel['type']) for rel in dict_a['relationships'])
    for relationship in dict_b['relationships']:
        if (relationship['source'], relationship['target'], relationship['type']) not in existing_relationships:
            dict_a['relationships'].append(relationship)
            existing_relationships.add((relationship['source'], relationship['target'], relationship['type']))

    return dict_a

def build_event_graph(text, publish_time):
    # 修改为下面五行（行数不包括注释）：
    # 获取当前脚本所在的目录
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 key.json 文件的路径
    json_file_path = os.path.join(cur_dir, 'documents', 'api_key.json')
    example_file_path = os.path.join(cur_dir, 'documents', 'example.json')
    api_key = read_json_file(json_file_path)["key"]
    example = read_json_file(example_file_path)

    headers = {
        "Authorization": api_key}
    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": publish_time + text,
        "chatbot_global_action": f'''
    请为text中的事件构建事件图谱，详尽描述各个事件的元素，包括人物、组织、成果、特征等，
    事件描述即"event"要尽量简洁，
    要求输出json格式，且内容必须为中文。对于时间属性，需要根据开头的时间推断出具体的年份或月份。
    事件关系可选择的有：因果关系、共指关系、时序关系、包含关系，注意识别这些关系
    source是原因，target是结果，例子如下：
   {example}    
   注意，必须返回json格式！！
    ''',
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 4096,
        "fallback_providers": "gpt-4"
    }

    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)
    print(result)
    print(result['openai']['generated_text'])
    graph = parse_api_response(result['openai']['generated_text'])
    time.sleep(15)
    return graph

def generate_title(text):
    # 修改下面这一行
    # api_key = read_json_file("documents/api_key.json")["key"]
    # 修改为下面三行（行数不包括注释）：
    # 获取当前脚本所在的目录
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 key.json 文件的路径
    json_file_path = os.path.join(cur_dir, 'documents', 'api_key.json')
    api_key = read_json_file(json_file_path)["key"]

    headers = {
        "Authorization": api_key}
    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": text,
        "chatbot_global_action": f'''
        请根据text中文字的内容提取标题,20个字以内
        ''',
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 50,
        "fallback_providers": "gpt-3.5-turbo"
    }

    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)
    title = result['openai']['generated_text']
    print(title)
    time.sleep(15)
    return title


def summarize(text):
    # 修改下面这一行
    # api_key = read_json_file("documents/api_key.json")["key"]
    # 修改为下面三行（行数不包括注释）：
    # 获取当前脚本所在的目录
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 key.json 文件的路径
    json_file_path = os.path.join(cur_dir, 'documents', 'api_key.json')
    api_key = read_json_file(json_file_path)["key"]
    
    headers = {
        "Authorization": api_key}
    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": text,
        "chatbot_global_action": f'''
        请简短总结text中文字的内容，交代事件的来龙去脉，200个字符以内，返回字符串
        ''',
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 200,
        "fallback_providers": "gpt-4"
    }

    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)
    summary = result['openai']['generated_text']
    print(summary)
    time.sleep(15)
    return summary


def select_texts():
    topics = read_json_file("documents/topics.json")
    data = read_json_file("documents/data.json")
    hotspot_texts = {}
    for item in topics.items():
        hotspot_texts[item[0]] = []
        for number in item[1]:
            for dataItem in data:
                if dataItem["keyword_id"] == number:
                    hotspot_texts[item[0]].append(dataItem)
        hotspot_texts[item[0]] = sorted(hotspot_texts[item[0]], key=lambda x: x["like_count"], reverse=True)
    save_json_file(hotspot_texts, "documents/hotspot_texts.json")


def is_news(text):
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWY1NjlkMzUtZjkxYi00MjBhLTkxMjQtOTcxNmVlNGMxZTcyIiwidHlwZSI6ImFwaV90b2tlbiJ9.BfSyYQb4Kj19j0z9GujV65Jq3qLLdL2VcobXfsGiAcE"}
    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": text,
        "chatbot_global_action": f'''
            请判断text中的文字是否为新闻类，即是否包含有价值的、值得报道的信息。
            非新闻类的例子包括：广告、学生写的校园生活帖子、学生发表的自己观点之类
            返回的generated_text只能是true或者false
            如果为新闻类，返回true，如果为非新闻类，返回false
            ''',
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 20,
        "fallback_providers": "meta"
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    print(result['openai']['generated_text'])
    predictions = json.loads(result['openai']['generated_text'])
    print(predictions)
    time.sleep(15)
    return predictions


def get_item(wid, data):
    for dataItem in data:
        if dataItem["wid"] == wid:
            return dataItem


if __name__ == "__main__":
    pass