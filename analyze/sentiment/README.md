#### 环境

情感分析过程采用了[ZhipuAI/chatglm3-6b]([魔搭社区](https://www.modelscope.cn/models/ZhipuAI/chatglm3-6b))大模型辅助进行。

使用到的环境依赖已在analyze目录下的poetry虚拟环境依赖文件`pyproject.toml`包含。

目前进行情感分析的python文件中采用cuda加载使用大模型，需要一定的GPU环境。如果需要更改为cpu环境，可以参考[ZhipuAI/chatglm3-6b]([魔搭社区](https://www.modelscope.cn/models/ZhipuAI/chatglm3-6b#%E4%BB%A3%E7%A0%81%E8%B0%83%E7%94%A8))并修改python文件。

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
