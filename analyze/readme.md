## makefile

三部分，第一部分是脚本文件的存放路径，第二部分是数据结果文件的存放路径，第三部分是make target部分。由于没有整合环境配置，makefile中有一些脚本文件没有实际运行，或者在代码中被注释掉了关键部分，在第三部分都有注释说明。
同时由于某些步骤没有实际运行，对于第二部分定义的结果存放路径“result”，现阶段需要先将一个月的数据、针对该数据的聚类分析结果、帖子情感分析结果事先放在result中的相应目录下。

## makefile命令详细介绍

### 1、爬虫

[HotSpotAnalyzer/crawler/README.md at main · huwf5/HotSpotAnalyzer · GitHub](https://github.com/huwf5/HotSpotAnalyzer/blob/main/crawler/README.md)

### 2、事件图谱

[HotSpotAnalyzer/analyze/README.md at event_analysis · huwf5/HotSpotAnalyzer · GitHub](https://github.com/huwf5/HotSpotAnalyzer/blob/event_analysis/analyze/README.md)

### 3、关键词+词云分析

#### 运行

```shell
cd wordcount
# 示例：
python title_wordcount_jieba.py data_2024-05-27.json analyze_result_0527.json
python title_wordcount_keybert.py data_2024-05-27.json analyze_result_0527.json
```

#### 说明

首先将对应文件放到目录下。

示例中，data_2024-05-27.json是原始爬虫数据，analyze_result_0527.json是针对该原始数据的聚类结果。

运行后，将会在目录下创建一个分析结果title_count_data_2024-05-27_{jieba or keybert}目录，里面是各个聚类标题的关键词+词云分析的结果csv文件。

#### 环境

```shell
# jieba
pip install jieba
# keybert
pip install keybert
```

---

### 4、情感分析

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

1、第一条命令中的data_2024-05-27.json是原始爬虫数据，

第一条命令将生成post_sentiment_counts_data_2024-05-27.json（在命令二用到）。它的内容是每一个帖子各自的情感分析结果。

2、第二条命令中，analyze_result_0527.json是针对命令一中原始数据的聚类结果，post_sentiment_counts_data_2024-05-27.json是命令一的产物。

第二条命令在analyze_result_0527.json的基础上，添加每个聚类的情感分析结果，并生成新的文件：analyze_result_0527_with_sentiment.json

#### 环境

使用了大模型chatglm3-6b，可从modelscope上下载使用。