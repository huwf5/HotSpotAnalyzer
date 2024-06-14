from modelscope import AutoTokenizer, AutoModel, snapshot_download
import os
import copy
import pandas as pd
import time
from datetime import datetime
import re
import json
import sys
print("loading...")
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2"
model_dir = snapshot_download("ZhipuAI/chatglm3-6b", revision = "v1.0.0")
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
model = AutoModel.from_pretrained(model_dir, trust_remote_code=True).half().cuda()
model = model.eval()
print("finished")


def get_senti_history():
    prompt = '''你是一个分析文本情感倾向的专家，能够很好地分析文本的情感（你只能选择以下其中之一：愤怒、厌恶、害怕、喜悦、悲伤、惊讶、平和、失望）。
    对于给定的文本：“我很喜欢这里，风景如画，空气清新，大家都很友善，这里简直就是个世外桃源。”，你能认真分析文本所表达的情感，并给出这样的格式输出：{"analysis_sentiment": "喜悦"}
    又比如，文本：“分手后心碎和孤独的感觉难以忍受。” 你能输出：{"analysis_sentiment": "悲伤"}
    下面我将给出一段文本，请你不要直接回答文本的问题，而是按照上面的例子回答。
    请确保只返回与上面的"analysis_sentiment"格式一致的json格式的结果，而不是其他文字内容。你准备好了吗？
    '''
    response, his_prompt = model.chat(tokenizer, query=prompt, temperature=0.7, history=None)
    # print(type(his_prompt))
    return copy.deepcopy(his_prompt)


def replace_chinese_keys(chi_senti_counts):
    
    # 定义中英文键名的替换规则
    mapping = {
        "愤怒": "angry",
        "厌恶": "disgusted",
        "害怕": "scared",
        "喜悦": "joyful",
        "悲伤": "sad",
        "惊讶": "surprised",
        "平和": "calm",
        "失望": "disappointed"
    }
    
    # 创建新的JSON对象，将中文键名替换为英文
    eng_senti_counts = {}
    for senti_chi, count in chi_senti_counts.items():
        eng_senti_counts[mapping[senti_chi]] = count
    
    return eng_senti_counts

def get_sentiments_multi(wid_comments, his):
    df = pd.DataFrame(columns=['text', 'sentiment'])
    keywords = ['愤怒', '厌恶', '害怕', '喜悦', '悲伤', '惊讶', '平和', '失望']
    pattern = r'\b(?:' + '|'.join(keywords) + r')\b'

    sentiment_counts = {}

    s_time = time.time()

    for wid, comments in wid_comments.items():
        senti_count = {
            '愤怒': 0,
            '厌恶': 0,
            '害怕': 0,
            '喜悦': 0,
            '悲伤': 0,
            '惊讶': 0,
            '平和': 0,
            '失望': 0
        }

        for text in comments:            
            prompt = '分析以下文本：' + text
            response, hisss = model.chat(tokenizer, query=prompt, temperature=0.4, history=copy.deepcopy(his))
            match = re.search(pattern, response)
            if match:
                sentiment = match.group()
                df.loc[len(df)] = [text, sentiment]
                senti_count[sentiment] += 1
            else:
                print('response is:', response, "///", 'its text is:', text)
                df.loc[len(df)] = [text, None]

        sentiment_counts[wid] = replace_chinese_keys(senti_count)
    
    e_time = time.time()
    
    elapsed_time = "{:.2f}".format(e_time - s_time)
    print("elapsed time:", elapsed_time, "秒")

    return df, sentiment_counts


def get_comments(json_file):
    wid_comments = {}  # 用于存储根据"wid"分组的评论

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
            if 'comments' in json_obj and 'wid' in json_obj:
                comments = json_obj['comments']
                wid = json_obj['wid']

                # 检查comments是否为空
                if comments:
                    # 获取评论文本
                    comment_texts = []
                    for comment in comments:
                        if 'text_raw' in comment:
                            text_raw = comment['text_raw']
                            comment_texts.append(text_raw)
                    # 将wid作为字典的键，评论列表作为值
                    wid_comments[wid] = comment_texts
                else: 
                    wid_comments[wid] = []
    return wid_comments, min_publish_time, max_publish_time

def get_senti_counts(json_file, keyword):
    
    his = get_senti_history()
    w_c, min_time, max_time = get_comments(json_file)
    df, senti_count = get_sentiments_multi(w_c, his)
    # 将情感计数结果写入JSON文件
    output_file = 'post_sentiment_counts'+json_file[:-5]+'.json'
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(senti_count, file, ensure_ascii=False, indent=4)

    return df, senti_count, min_time, max_time

    

if __name__ == '__main__':

    json_file = sys.argv[1] # 'data_2024-05-27.json'
    
    keyword = 1
    
    df, senti_count, min_time, max_time = get_senti_counts(json_file, keyword)
    # print(senti_count)
    # print(min_time, max_time)