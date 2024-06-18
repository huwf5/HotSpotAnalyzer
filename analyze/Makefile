# 1、脚本文件路径

# 爬虫部分
crawler_dir := crawler/WeiboCrawler
crawler := $(crawler_dir)/WeiboCnTopicSpiderWithoutCookie.py
get_data := $(crawler_dir)/convert_to_json_OneMonth.py
# 事件处理部分
event_dir := event
cluster := $(event_dir)/cluster.py
event_analyze := $(event_dir)/analyze.py
event_graph := $(event_dir)/build_event_graph.py
convert_knowledge_graph := $(event_dir)/convert_knowledge_graph.py
# 情感分析和词频部分
senti_dir := sentiment
wordcount_dir := word_cloud
post_sentiment := $(senti_dir)/post_senti.py
topic_sentiment := $(senti_dir)/analyze_add.py
word_count_jieba := $(wordcount_dir)/title_wordcount_jieba.py
stopwords := $(wordcount_dir)/stopwords.txt

# 2、数据文件目录

# 策略：功能目录+时间目录，如graph/2024-06-06
# 当前时间戳（设想是makefile运行的当前时间，用于数据、结果文件夹的子目录命名）
# current_time := $(shell date +"%Y-%m-%d")
file_name_by_date := $(shell date +"%Y-%m-%d.json")
# 一个月的json数据的存放目录
month_data_dir := ../result/weibo_data
data_file_name := $(file_name_by_date)
cluster_source_file := $(month_data_dir)/$(data_file_name)
# 聚类结果存放路径
cluster_dir := ../result/cluster_result
cluster_target_file := $(cluster_dir)/$(file_name_by_date)
# 热点分析结果存放路径
event_analyze_dir := ../result/topic_data
event_analyze_target_file := $(event_analyze_dir)/$(file_name_by_date)
# 事件图谱结果文件存放路径
event_graph_dir := ../result/graph
event_graph_target_file := $(event_graph_dir)/$(file_name_by_date)
# 3d-force-graph图谱结果路径
convert_knowledge_graph_dir := $(event_graph_dir)
convert_knowledge_graph_file := $(event_graph_target_file)
# 情感分析和词频分析结果文件存放路径
post_senti_result_dir := ../result/sentiment/post_sentiment
post_senti_target_file := $(post_senti_result_dir)/$(file_name_by_date)
topic_sentiment_result_dir := $(event_analyze_dir)
topic_sentiment_target_file := $(topic_sentiment_result_dir)/$(file_name_by_date)
wordcount_total_result_jieba_dir := ../result/word_cloud/jieba_wordcount
wordcount_total_result_jieba_file := $(wordcount_total_result_jieba_dir)/$(file_name_by_date)
topic_sentiment_wordcount_target_file := $(topic_sentiment_result_dir)/$(file_name_by_date)

# log目录(简陋版)
# log_dir := log

# 3、target
.PHONY: crawler get_data gen_cluster event_analyze event_graph convert_knowledge_graph sentiment_and_wordcount

all: convert_knowledge_graph sentiment_and_wordcount

# 爬虫，录入数据库
# 下面的@python $(crawler)命令中的if __name__ == '__main__'部分代码被注释
crawler: 
	@echo "running crawler"	
	@python $(crawler) 2>&1 | sed 's/^/\t/'

# 生成一个月的数据data
# 实际运行将这个命令替换“模拟”：
# @python $(get_data) $(month_data_dir) $(data_file_name) 2>&1 | sed 's/^/\t/'
get_data: crawler
	@echo "running get_data"
	@if [ ! -d $(month_data_dir) ]; then \
		mkdir -p $(month_data_dir); \
	fi
	@echo "模拟生成一个月数据" | sed 's/^/\t/'

# 聚类分析
# 实际运行将下面命令替换“模拟”
# @python3 $(cluster) -source_file $(cluster_source_file) -target_file $(cluster_target_file) 2>&1 | sed 's/^/\t/'
gen_cluster: get_data
	@echo "running gen_cluster"
	@if [ ! -d $(cluster_dir) ]; then \
		mkdir -p $(cluster_dir); \
	fi
	@echo "模拟聚类" | sed 's/^/\t/'
	
# 热点topic分析
event_analyze: gen_cluster
	@echo "running event_analyze_topic"
	@if [ ! -d $(event_analyze_dir) ]; then \
		mkdir -p $(event_analyze_dir); \
	fi
	@python $(event_analyze) \
		-source_data_file $(cluster_source_file) \
		-clustering_result $(cluster_target_file) \
		-target_file $(event_analyze_target_file) \
		2>&1 | sed 's/^/\t/' > log_file/analyze.log

# 事件图谱event_graph
event_graph: event_analyze
	@echo "running build_event_graph"
	@if [ ! -d $(event_graph_dir) ]; then \
		mkdir -p $(event_graph_dir); \
	fi
	@python $(event_graph) \
		-source_data_file $(cluster_source_file) \
		-analyze_result $(event_analyze_target_file) \
		-target_file $(event_graph_target_file) \
		2>&1 | sed 's/^/\t/' > log_file/build_event_graph.log

# 将图谱转化为3d-force形式
convert_knowledge_graph: event_graph
	@echo "running convert_knowledge_graph"
	@if [ ! -d $(convert_knowledge_graph_dir) ]; then \
		mkdir -p $(convert_knowledge_graph_dir); \
	fi
	@python $(convert_knowledge_graph) \
		-graph_file $(event_analyze_target_file) \
		-target_file $(convert_knowledge_graph_file) \
		2>&1 | sed 's/^/\t/' > log_file/convert_graph.log


# 情感分析和词频统计（先情感分析再词频统计）
# 实际运行，替换“模拟”：@python $(post_sentiment) $(cluster_source_file) $(post_senti_target_file) 2>&1 | sed 's/^/\t/'
sentiment_and_wordcount: event_analyze
	@echo "running sentiment"
	@if [ ! -d $(post_senti_result_dir) ]; then \
		mkdir -p $(post_senti_result_dir); \
	fi
	@echo "模拟帖子情感分析" | sed 's/^/\t/'
	@python $(topic_sentiment) $(event_analyze_target_file) $(post_senti_target_file) $(topic_sentiment_target_file) 2>&1 | sed 's/^/\t/' > log_file/senti.log
	@echo "running wordcount"
	@if [ ! -d $(wordcount_total_result_jieba_dir) ]; then \
		mkdir -p $(wordcount_total_result_jieba_dir); \
	fi
	@python $(word_count_jieba) $(cluster_source_file) $(topic_sentiment_target_file) $(wordcount_total_result_jieba_file) $(topic_sentiment_wordcount_target_file) $(stopwords) 2>&1 | sed 's/^/\t/' > log_file/wordcount.log

.PHONY:
clean:
	find . -name '__pycache__' -type d -exec rm -r {} +

