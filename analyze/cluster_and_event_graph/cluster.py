import json
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
import numpy as np
import argparse  # 导入 argparse 模块
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# 加载数据
def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# 提取有文本的数据
def extract_texts(data):
    texts = []
    for item in data:
        if 'text' in item and item['text']:
            texts.append((item['wid'], item['text']))
    return texts


# 生成文本的嵌入向量
def encode_texts(texts, model_name='aspire/acge_text_embedding'):
    model = SentenceTransformer(model_name)
    embeddings = model.encode([text for _, text in texts], show_progress_bar=True)
    return embeddings


# 应用 DBSCAN 聚类算法
def apply_dbscan(embeddings, eps=0.2, min_samples=5):
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine').fit(embeddings)
    return clustering.labels_


# 保存聚类结果到 JSON 文件
def save_cluster_results_to_json(labels, texts, wids, output_file):
    clusters = {}
    for label, (_, text), wid in zip(labels, texts, wids):
        label = int(label)  # 确保键值格式正确
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(wid)

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(clusters, file, ensure_ascii=False, indent=4)


# 主函数
def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-source_file', type=str, required=True, help='name of the source data file.')
    parser.add_argument('-target_file', type=str, required=True,
                        help='The path where the cluster results will be saved.')
    args = parser.parse_args()
    source_path = os.path.join(BASE_DIR, 'result', 'weibo_data', args.source_file)
    target_path = os.path.join(BASE_DIR, 'result', 'cluster_result', args.target_file)

    # 加载数据
    data = load_data(args.source_file)
    # 提取文本
    items = extract_texts(data)
    # 获取嵌入向量
    embeddings = encode_texts(items)
    # 执行 DBSCAN 聚类
    cluster_labels = apply_dbscan(embeddings)
    # 保存聚类结果到 JSON 文件
    save_cluster_results_to_json(cluster_labels, items, [item[0] for item in items], args.target_file)
    print(f"聚类结果已保存到 {args.target_file} 文件中。")


if __name__ == "__main__":
    main()