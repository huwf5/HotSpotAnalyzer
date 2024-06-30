### 关键词+词云分析

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
