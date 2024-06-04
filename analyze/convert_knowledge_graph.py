import argparse
import json
import networkx as nx


def read_json_file(file_path):
    """读取JSON文件并返回数据"""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def save_json_file(json_dict, file_path):
    """将JSON字典保存到文件"""
    with open(file_path, 'w', encoding='utf-8') as outfile:
        json.dump(json_dict, outfile, ensure_ascii=False, indent=4)


def find_event_description(events, id):
    """根据id查找事件描述"""
    for event in events:
        if event["id"] == id:
            return event["event"]


def getId(name, gid):
    """生成和返回带组ID的标识符"""
    return f"{name}-{gid}"


def ensure_all_nodes_connected(graph_dict, gid):
    """确保所有节点都与组内的主节点连接"""
    G = nx.DiGraph()
    for node in graph_dict["nodes"]:
        if node["group"] == gid:
            G.add_node(node["id"])
    for link in graph_dict["links"]:
        if G.has_node(link["source"]) and G.has_node(link["target"]):
            G.add_edge(link["source"], link["target"], description=link["description"])
    main_node = "中山大学-1"
    for node in graph_dict["nodes"]:
        if node["group"] == gid:
            main_node = node["id"]
            break
    connected_nodes = set(nx.descendants(G, main_node)) | {main_node}
    all_nodes = {node["id"] for node in graph_dict["nodes"] if node["group"] == gid}

    if all_nodes - connected_nodes is None:
        return False

    # 添加缺失的连接
    for node in all_nodes - connected_nodes:
        graph_dict["links"].append({"source": main_node, "target": node, "description": "关联关系"})
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-graph_file', type=str, required=True,
                        help='The path to the source graph file.')
    parser.add_argument('-target_file', type=str, required=True,
                        help='The path to the output file.')
    args = parser.parse_args()
    graphs = read_json_file(args.graph_file)
    gid = 1
    graph_dict = {"nodes": [{"id": getId("中山大学", gid), "group": gid}], "links": []}
    gid += 1
    for key, graph in graphs.items():
        graph_dict["links"].append({"source": getId("中山大学", 1),
                                    "target": getId(graph["events"][0]["event"], gid),
                                    "description": "关联"})
        for event in graph["events"]:
            graph_dict["nodes"].append({"id": getId(event["event"], gid), "group": gid})
            for attribute in event["attributes"]:
                node_id = getId(attribute["value"], gid)
                if {"id": node_id, "group": gid} not in graph_dict["nodes"]:
                    graph_dict["nodes"].append({"id": node_id, "group": gid})
                graph_dict["links"].append(
                    {"source": getId(event["event"], gid), "target": node_id, "description": attribute["type"]})
        for relation in graph["relationships"]:
            graph_dict["links"].append(
                {"source": getId(find_event_description(graph["events"], relation["source"]), gid),
                 "target": getId(find_event_description(graph["events"], relation["target"]), gid),
                 "description": relation["type"]})
        while (True):
            if not ensure_all_nodes_connected(graph_dict, gid):
                break

        # 确保所有节点都连接到主节点
        save_json_file(graph_dict, args.target_file)
        gid += 1