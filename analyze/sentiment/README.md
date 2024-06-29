情感分析

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

命令 1:

- month_data_file 是从数据库提取的源数据文件
- post_senti_target_file 是对每个帖子的评论进行情感分析的结果输出文件

命令 2:

- topic_analyze_result_file 是事件分析部分的热点分析的结果文件
- post_senti_target_file 是命令 1 中的每个帖子的情感分析结果文件
- topic_sentiment_target_file 是热点分析结果+情感分析结果的整合输出文件
