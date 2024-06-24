import argparse
import json
from apis import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def read_json_file(file_path):
    """读取JSON文件并返回数据"""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def save_json_file(json_dict, file_path):
    with open(file_path, 'w', encoding='utf-8') as outfile:
        json.dump(json_dict, outfile, ensure_ascii=False, indent=4)


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-source_data_file', type=str, required=True,
                        help='The path to the source data file.')
    parser.add_argument('-clustering_result', type=str, required=True,
                        help='The path to the source clustering result file.')
    parser.add_argument('-target_file', type=str, required=True,
                        help='The path where the analysis results will be saved.')

    args = parser.parse_args()
    source_path = os.path.join(BASE_DIR, 'result', 'weibo_data', args.source_data_file)
    cluster_path = os.path.join(BASE_DIR, 'result', 'cluster_result', args.clustering_result)
    target_path = os.path.join(BASE_DIR, 'result', 'topic_data', args.target_file)

    clusters = read_json_file(cluster_path)
    data = read_json_file(source_path)
    if os.path.exists(target_path):
        target = read_json_file(target_path)
    else:
        target = {}
        save_json_file(target, target_path)

    for label, wids in clusters.items():
        if label == "-1":
            continue

        if label not in target.keys():
            target[label] = {"posts": [], "joy": 0}
            save_json_file(target, target_path)
        text = ""

        for wid in wids:
            dataItem = get_item(wid, data)
            if "text" not in dataItem.keys():
                continue
            text += dataItem["text"]
            if len(text) >= 4096:
                text = text[:4096]
                break
        if "is_news" not in target[label].keys():
            isNews = is_news(text)
            target[label]["is_news"] = isNews
            save_json_file(target, target_path)
        else:
            pass

        target[label]["posts"] = wids.copy()
        if "summary" not in target[label].keys():
            summary = summarize(text)
            target[label]["summary"] = summary
            save_json_file(target, target_path)
        if "title" not in target[label].keys():
            title = generate_title(text)
            target[label]["title"] = title
            save_json_file(target, target_path)



if __name__ == "__main__":
    main()


