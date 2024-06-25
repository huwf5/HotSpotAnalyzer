# 1、脚本文件路径

# 爬虫部分
crawler_dir := $(CURDIR)/crawler/weibo_crawler
# 大规模爬取数据
weibo_topic := $(crawler_dir)/weibo_topic_subtopic.py # 话题、子话题
crawler := $(crawler_dir)/WeiboCnTopicSpiderWithoutCookie.py
weibo_comments := $(crawler_dir)/newWeiboComment.py
# 最近一个月的爬取 （）
latest_post := $(crawler_dir)/LatestPostSpider_fordaily.py # 先修改数据库配置，并 确认 post_monthly_config.json 的配置，设置 isoneMonth 为 true
lstest_comment := $(crawler_dir)/LastestCommentSpider_fordaily.py # 先修改数据库配置，并 修改 limit，limit 是执行爬取评论的帖子上限。
# 获取数据 (一个月、帖子和所属话题、帖子和帖子评论)
get_1month_data := $(crawler_dir)/convert_to_json_OneMonth.py
get_post_keyword := $(crawler_dir)/convert_to_json_csv_onlypostAndKeyword.py
all_post_comments := $(crawler_dir)/convert_to_json_Allpost_with_comment.py
# 事件处理部分
event_dir := $(CURDIR)/cluster_and_event_graph
cluster := $(event_dir)/cluster.py
topic_analyze := $(event_dir)/analyze.py
build_event_graph := $(event_dir)/build_event_graph.py
convert_knowledge_graph := $(event_dir)/convert_knowledge_graph.py
# 情感分析和词频部分
senti_dir := $(CURDIR)/sentiment
wordcount_dir := $(CURDIR)/wordcount
post_sentiment := $(senti_dir)/post_senti.py
topic_sentiment := $(senti_dir)/analyze_add.py
word_count_jieba := $(wordcount_dir)/title_wordcount_jieba.py


# 2、数据结果文件路径

DIRECTORIES := $(shell dirname $(CURDIR))/result/topic_data \
			$(shell dirname $(CURDIR))/result/cluster_result \
			$(shell dirname $(CURDIR))/result/3d-force-graph \
			$(shell dirname $(CURDIR))/result/graph \
			$(shell dirname $(CURDIR))/result/sentiment/post_sentiment \
			$(shell dirname $(CURDIR))/result/word_cloud/jieba_wordcount \
			$(shell dirname $(CURDIR))/result/weibo_data
# 结果文件名
date_json_file := $(shell date +"%Y-%m-%d.json")
# date_json_file := history.json
# 一个月的json数据的存放路径
month_data_file := $(shell dirname $(CURDIR))/result/weibo_data/$(date_json_file)
# 事件处理部分
# 事件处理：处理源文件、处理结果文件的绝对路径，已经在脚本文件中定义好；文件名统一为 $(date_json_file)
# 情感分析和词频分析结果文件存放路径
# 情感
topic_analyze_result_file := $(shell dirname $(CURDIR))/result/topic_data/$(date_json_file)
post_senti_target_file := $(shell dirname $(CURDIR))/result/sentiment/post_sentiment/$(date_json_file) # 帖子情感
topic_sentiment_target_file := $(shell dirname $(CURDIR))/result/topic_data/$(date_json_file)
# 词频
total_jiebawordcount_target_file := $(shell dirname $(CURDIR))/result/word_cloud/jieba_wordcount/$(date_json_file)
topic_sentiment_wordcount_target_file := $(shell dirname $(CURDIR))/result/topic_data/$(date_json_file)


# 3、读取配置文件

# 读取配置文件，获取爬虫目标target：latest或者large_batch
config := $(CURDIR)/config.yaml
target := $(shell yq eval '.crawler.target' $(config))
# yq (https://github.com/mikefarah/yq/) version v4.44.1 (snap install yq)


# 3、make target

.PHONY: crawler get_data gen_cluster topic_analyze build_event_graph convert_knowledge_graph sentiment_and_wordcount import_data

all: convert_knowledge_graph sentiment_and_wordcount # import_data

# 爬虫，录入数据库
# https://stackoverflow.com/questions/21226905/syntax-error-word-unexpected-expecting 在makefile中ifeq不能用tab缩进。可以用空格
crawler: 
	@echo "创建目录"
	@mkdir -p $(DIRECTORIES)
	@echo "running crawler"	
ifeq ($(target), latest) # 爬虫目标是“latest”，即最新收据
	@echo "爬取最新数据" | sed 's/^/\t/'
	@python $(latest_post)
	@python $(latest_comment)
else 
  ifeq ($(target), large_batch) # 爬虫目标是“large_batch”，即大批量
		@echo "大批量爬取" | sed 's/^/\t/'
		@python $(weibo_topic)
		@python $(WeiboCnTopic)
		@python $(weibo_comments)
  else
		@echo "不存在的爬虫选项：$(target)" | sed 's/^/\t/'
		@echo "模拟爬虫部分" | sed 's/^/\t/'
  endif 
endif


# 生成一个月的数据data，（待修改python文件）
# 实际运行将这个命令替换“模拟”：
# @python $(get_data) $(month_data_file) 2>&1 | sed 's/^/\t/'
get_data: crawler
	@echo "running get_data"
	@if [ ! -d $(month_data_dir) ]; then \
		mkdir -p $(month_data_dir); \
	fi
	@echo "模拟生成一个月数据" | sed 's/^/\t/'


# 聚类分析
# 实际运行将下面命令替换“模拟”
# @python3 $(cluster) -source_file $(date_json_file) -target_file $(date_json_file) 2>&1 | sed 's/^/\t/'
gen_cluster: get_data
	@echo "running gen_cluster"
	@echo "模拟聚类" | sed 's/^/\t/'

 
# 热点topic分析 > log_file/analyze.log
topic_analyze: gen_cluster
	@echo "running topic_analyze"
	@python $(topic_analyze) \
		-source_data_file $(date_json_file) \
		-clustering_result $(date_json_file) \
		-target_file $(date_json_file) \
		2>&1 | sed 's/^/\t/' > log_file/analyze.log


# 事件图谱event_graph
build_event_graph: topic_analyze
	@echo "running build_event_graph"
	@python $(build_event_graph) \
		-source_data_file $(date_json_file) \
		-analyze_result $(date_json_file) \
		-target_file $(date_json_file) \
		2>&1 | sed 's/^/\t/' > log_file/build_event_graph.log

# 将图谱转化为3d-force形式
convert_knowledge_graph: build_event_graph
	@echo "running convert_knowledge_graph"
	@python $(convert_knowledge_graph) \
		-graph_file $(date_json_file) \
		-target_file $(date_json_file) \
		2>&1 | sed 's/^/\t/' > log_file/convert_graph.log


# 情感分析和词频统计（先情感分析再词频统计）
# @if [ ! -d $(post_senti_result_dir) ]; then \
# 	mkdir -p $(post_senti_result_dir); \
# fi
# 实际运行，替换“模拟”：@python $(post_sentiment) -source_data_file $(month_data_file) -post_senti_target_file $(post_senti_target_file) 2>&1 | sed 's/^/\t/'
sentiment_and_wordcount: topic_analyze
	@echo "running sentiment"
	@echo "模拟帖子情感分析" | sed 's/^/\t/'
	@python $(topic_sentiment) \
		-topic_result_file $(topic_analyze_result_file) \
		-post_senti_result_file $(post_senti_target_file) \
		-topic_sentiment_target_file $(topic_sentiment_target_file) \
		2>&1 | sed 's/^/\t/' > log_file/senti.log
	
	@echo "running wordcount"
	@python $(word_count_jieba) \
		-source_data_file $(month_data_file) \
		-topic_sentiment_result_file $(topic_sentiment_target_file) \
		-totalwc_target_file $(total_jiebawordcount_target_file) \
		-topic_senti_wc_target_file $(topic_sentiment_wordcount_target_file) \
		2>&1 | sed 's/^/\t/' > log_file/wordcount.log


import_data: sentiment_and_wordcount
	@echo "importing data"
	@python ../backend/manage.py import ../result/topic_data/$(date_json_file)

.PHONY:
clean:
	find . -name '__pycache__' -type d -exec rm -r {} +




