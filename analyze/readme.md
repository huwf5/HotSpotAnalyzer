## makefile

##### 文件结构大致划分为以下四部分

- 第一部分：列出anlyze的所有脚本文件的具体路径

- 第二部分：设置数据结果文件的名称、存放路径

- 第三部分：读取config.yaml配置文件。
  
  ```shell
  config.yaml文件用于设置一些参数，比如爬虫可以选择：大规模爬取、爬取最新数据。
  通过设置不同的参数，可以在makefile中运行不同的脚本文件。
  ```

- 第四部分：定义make的目标target
  
  介绍：
  
  ```shell
  整个流程是：
  首先进行爬虫部分
  1、将爬到的数据读入数据库
  2、然后从数据库中读取数据，输出为json文件，以供后续分析使用
  然后进行事件分析部分
  1、分别进行：聚类分析、热点分析、事件图谱构建、将图谱转化为3d-force-graph可接受的形式
  再进行情感分析、关键词的词频分析
  1、情感分析完成后，将分析结果与热点分析的结果整合
  2、词频分析，完成后，将分析结果整合到情感分析、热点分析的整合结果
  最后进行结果文件录入数据库
  1、将热点分析、情感分析、词云分析的结果录入数据库
  ```

##### makefile中用到的环境

```shell
# yq (https://github.com/mikefarah/yq/) version v4.44.1 ; 用于读取yaml文件
snap install yq
```

## makefile命令详细介绍

### 1、爬虫

[HotSpotAnalyzer/crawler/README.md at main · huwf5/HotSpotAnalyzer · GitHub](https://github.com/huwf5/HotSpotAnalyzer/blob/main/crawler/README.md)

### 2、事件图谱

[HotSpotAnalyzer/analyze/README.md at event_analysis · huwf5/HotSpotAnalyzer · GitHub](https://github.com/huwf5/HotSpotAnalyzer/blob/event_analysis/analyze/README.md)

---

### 3、情感分析

#### 单独运行

```shell
cd sentiment

# 示例：

# 首先运行：
# 命令1
python post_senti.py \
    -source_data_file $(month_data_file) \
    -post_senti_target_file $(post_senti_target_file)

# 然后运行：
# 命令2
python analyze_add.py \
    -topic_result_file $(topic_analyze_result_file) \
    -post_senti_result_file $(post_senti_target_file) \
    -topic_sentiment_target_file $(topic_sentiment_target_file)
```

#### 说明

示例中，将$(xxx_file)替换为实际文件

命令1:

- month_data_file 是从数据库提取的源数据文件

- post_senti_target_file 是对每个帖子的评论进行情感分析的结果输出文件

命令2:

- topic_analyze_result_file 是事件分析部分的热点分析的结果文件

- post_senti_target_file 是命令1中的每个帖子的情感分析结果文件

- topic_sentiment_target_file 是热点分析结果+情感分析结果的整合输出文件

#### 环境

使用了大模型chatglm3-6b，可从modelscope下载部署。

---

### 4、关键词+词云分析

#### 单独运行

```shell
cd wordcount

# 示例：
# jieba关键词分析 + 词频统计
python title_wordcount_jieba.py
    -source_data_file $(month_data_file) \
    -topic_sentiment_result_file $(topic_sentiment_target_file) \
    -totalwc_target_file $(total_jiebawordcount_target_file) \
    -topic_senti_wc_target_file $(topic_sentiment_wordcount_target_file)
# keybert关键词分析 + 词频统计 （命令待完善）
python title_wordcount_keybert.py data_2024-05-27.json analyze_result_0527.json
```

#### 说明

示例中，将$(xxx_file)替换为实际文件：

- month_data_file 是从数据库提取的源数据文件

- topic_sentiment_target_file 是热点分析结果+情感分析结果的整合文件

- total_jiebawordcount_target_file 是总词频结果的输出目标文件

- topic_sentiment_wordcount_target_file 是热点分析结果+情感分析结果+词频结果的整合结果的输出目标文件

#### 环境

```shell
# jieba

pip install jieba

# keybert

pip install keybert
```

---