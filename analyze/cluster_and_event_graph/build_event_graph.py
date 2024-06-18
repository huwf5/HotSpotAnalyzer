import argparse
from apis import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-source_data_file', type=str, required=True,
                        help='The path to the source data file.')
    parser.add_argument('-analyze_result', type=str, required=True,
                        help='The path to the source clustering result file.')
    parser.add_argument('-target_file', type=str, required=True,
                        help='The path where the cluster results will be saved.')
    args = parser.parse_args()
    source_path = os.path.join(BASE_DIR, 'result', 'weibo_data', args.source_data_file)
    data = read_json_file(source_path)
    analyze_result_path = os.path.join(BASE_DIR, 'result', 'topic_data', args.analyze_result)
    target_path = os.path.join(BASE_DIR, 'result', 'graph', args.target_file)

    analyze_result = read_json_file(analyze_result_path)
    if os.path.exists(target_path):
        target = read_json_file(target_path)
    else:
        target = {}
        save_json_file(target, target_path)
    for key, value in analyze_result.items():
        if not value["is_news"]:
            continue
        if key not in target.keys():
            text = ""
            publish_time = ""
            for wid in value["posts"]:
                item = get_item(wid, data)
                if "text" not in item.keys():
                    continue
                text += item["text"]
                if len(text) >= 4096:
                    publish_time = item["publish_time"]
                    text = text[:4096]
                    break
            graph = build_event_graph(text, publish_time)
            target[key] = graph
            save_json_file(target, target_path)

if __name__ == "__main__":
    main()