## 关键词+词云分析

#### 运行

```shell
cd wordcount
# 示例：
python title_wordcount_jieba.py data_2024-05-27.json analyze_result_0527.json
python title_wordcount_keybert.py data_2024-05-27.json analyze_result_0527.json
```

#### 说明

首先将对应文件放到目录下。

示例中，data_2024-05-27.json 是原始爬虫数据，analyze_result_0527.json 是针对该原始数据的聚类结果。

运行后，将会在目录下创建一个分析结果 title*count_data_2024-05-27*{jieba or keybert}目录，里面是各个聚类标题的关键词+词云分析的结果 csv 文件。

#### 环境

```shell
# jieba
pip install jieba
# keybert
pip install keybert
```

## 情感分析

#### 运行

```shell
cd sentiment
# 示例：
# 首先运行：
python post_senti.py data_2024-05-27.json
# 然后运行：
python analyze_add.py analyze_result_0527.json post_sentiment_counts_data_2024-05-27.json
```

#### 说明

示例中，

1、第一条命令中的 data_2024-05-27.json 是原始爬虫数据，

第一条命令将生成 post_sentiment_counts_data_2024-05-27.json（在命令二用到）。它的内容是每一个帖子各自的情感分析结果。

2、第二条命令中，analyze_result_0527.json 是针对命令一中原始数据的聚类结果，post_sentiment_counts_data_2024-05-27.json 是命令一的产物。

第二条命令在 analyze_result_0527.json 的基础上，添加每个聚类的情感分析结果，并生成新的文件：analyze_result_0527_with_sentiment.json

#### 环境

使用了大模型 chatglm3-6b，可从 modelscope 上下载使用。
