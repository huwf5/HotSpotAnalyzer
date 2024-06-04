import argparse
from apis import *


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-source_data_file', type=str, required=True,
                        help='The path to the source data file.')
    parser.add_argument('-analyze_result', type=str, required=True,
                        help='The path to the source clustering result file.')
    parser.add_argument('-target_file', type=str, required=True,
                        help='The path where the cluster results will be saved.')
    args = parser.parse_args()
    data = read_json_file(args.source_data_file)
    analyze_result = read_json_file(args.analyze_result)
    if os.path.exists(args.target_file):
        target = read_json_file(args.target_file)
    else:
        target = {}
        save_json_file(target, args.target_file)
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
            save_json_file(target, args.target_file)

if __name__ == "__main__":
    main()