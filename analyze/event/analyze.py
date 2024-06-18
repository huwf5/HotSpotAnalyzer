import argparse
import json
from apis import *


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
                        help='The path where the cluster results will be saved.')
    args = parser.parse_args()
    analyze_result = {}
    clusters = read_json_file(args.clustering_result)
    data = read_json_file(args.source_data_file)
    if os.path.exists(args.target_file):
        target = read_json_file(args.target_file)
    else:
        target = {}
        save_json_file(target, args.target_file)

    for label, wids in clusters.items():
        if label == "-1":
            continue

        if label not in target.keys():
            target[label] = {"posts": [], "joy": 0}
            save_json_file(target, args.target_file)
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
            save_json_file(target, args.target_file)
        else:
            pass

        target[label]["posts"] = wids.copy()
        if "summary" not in target[label].keys():
            summary = summarize(text)
            target[label]["summary"] = summary
            save_json_file(target, args.target_file)
        if "title" not in target[label].keys():
            title = generate_title(text)
            target[label]["title"] = title
            save_json_file(target, args.target_file)



if __name__ == "__main__":
    main()