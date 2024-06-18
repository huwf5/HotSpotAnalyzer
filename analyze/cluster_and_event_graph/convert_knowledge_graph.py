import argparse
import json
import networkx as nx
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

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
    # 使用无向图
    G = nx.Graph()
    for node in graph_dict["nodes"]:
        if node["group"] == gid:
            G.add_node(node["id"])
    for link in graph_dict["links"]:
        # 仅添加gid组内的节点
        if G.has_node(link["source"]) and G.has_node(link["target"]):
            G.add_edge(link["source"], link["target"], description=link["description"])

    # 选择主节点，假设第一个节点是主节点
    main_node = next((node["id"] for node in graph_dict["nodes"] if node["group"] == gid), None)

    # 使用无向图的connected_components方法来检查是否所有节点都在同一连通分量中
    if main_node:
        connected_nodes = set(nx.node_connected_component(G, main_node))
        all_nodes = {node["id"] for node in graph_dict["nodes"] if node["group"] == gid}

        # 检查是否所有节点都已连接
        unconnected_nodes = all_nodes - connected_nodes
        if unconnected_nodes:
            # 添加缺失的连接
            for node in unconnected_nodes:
                graph_dict["links"].append({"source": main_node, "target": node, "description": "关联关系"})
            return True  # 有节点未连接，添加了新的边
    return False  # 所有节点已经连接或没有主节点


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-graph_file', type=str, required=True,
                        help='The path to the source graph file.')
    parser.add_argument('-target_file', type=str, required=True,
                        help='The path to the output file.')
    args = parser.parse_args()
    graph_path = os.path.join(BASE_DIR, 'result', 'graph', args.graph_file)
    target_path = os.path.join(BASE_DIR, 'result', '3d-force-graph', args.target_file)
    graphs = read_json_file(graph_path)
    gid = 1
    graph_dict = {"nodes": [{"id": getId("中山大学", gid), "group": gid}], "links": []}
    gid += 1
    for key, graph in graphs.items():
        graph_dict["links"].append({"source": getId("中山大学", 1),
                                    "target": getId(graph["events"][0]["event"], gid),
                                    "description": "关联"})
        for event in graph["events"]:
            if {"id": getId(event["event"], gid), "group": gid} not in graph_dict["nodes"]:
                graph_dict["nodes"].append({"id": getId(event["event"], gid), "group": gid})
            if "attributes" in event.keys():
                for attribute in event["attributes"]:
                    node_id = getId(attribute["value"], gid)
                    if {"id": node_id, "group": gid} not in graph_dict["nodes"]:
                        graph_dict["nodes"].append({"id": node_id, "group": gid})
                    graph_dict["links"].append(
                        {"source": getId(event["event"], gid), "target": node_id, "description": attribute["type"]})
        if "relationships" not in graph.keys():
            continue
        for relation in graph["relationships"]:
            graph_dict["links"].append(
                {"source": getId(find_event_description(graph["events"], relation["source"]), gid),
                 "target": getId(find_event_description(graph["events"], relation["target"]), gid),
                 "description": relation["type"]})
        while (True):
            if not ensure_all_nodes_connected(graph_dict, gid):
                break

        # 确保所有节点都连接到主节点
        save_json_file(graph_dict, target_path)
        gid += 1