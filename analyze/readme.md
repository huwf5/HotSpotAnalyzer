## makefile

### 介绍

##### makefile结构

- 第一部分：analyze不同功能的文件夹的路径

- 第二部分：设置数据结果文件的名称、存放路径

- 第三部分：读取config.yaml配置文件。
  
  ```shell
  config.yaml文件用于设置一些参数，
  比如爬虫可以选择：大规模爬取、爬取最新数据。
  然后脚本运行的输出被重定向到与脚本同目录的.log文件，如果要保留log文件来debug，则将remain_outputs设置为true第四部分：定义make的目标target
  ```

- 介绍：
  
  ```shell
  整个流程：
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
在analyze目录下的pypeoject.toml定义虚拟环境

其他：
# yq (https://github.com/mikefarah/yq/) version v4.44.1 ; 用于读取yaml文件
snap install yq
```

---

## makefile命令详细介绍

### 1、爬虫

##### [介绍](crawler/weibo_crawler/README.md)

----

### 2、事件图谱

##### [介绍](cluster_and_event_graph/README.md)

---

### 3、情感分析和关键词词频分析

##### [情感分析介绍](sentiment/README.md)

##### [关键词词频分析介绍](wordcount/README.md)

---

## 在服务器测试部署

#### 修改makefile和config.yaml

1. 将`config.yaml`中的`.crawler.target`修改为`latest`，可以进行最新数据的爬取。目前不要使用大规模爬取（爬取历史数据）“`large_batch`”，可能会破坏数据库。
   
   进行latest爬虫测试的时候可以前往analyze/crwaler/weibo_crawler/post.log文件查看运行输出（需要等待一会儿）(同理可以前往对应脚本路径查看其他脚本文件的输出)，输出没问题的话可以停止makefile爬取（已经爬取过了），把config.yaml中的.crawler.target修改为test（只要不是latest或者large_batch就好），以便makefile运行时跳过爬虫`crawler`这一部分。

2. 将makefile中的目标“`get_data`”的命令`@cd $(crawler_dir) && poetry run python convert_to_json_OneMonth.py -target_file $(month_data_file)`去掉（放到目标外面并注释），先不要运行。这个命令的功能是从数据库中导出最近一个月的最新数据，但是由于cpu服务器上不能运行聚类分析`gen_cluster`，因此这个数据在CPU服务器无法分析。采取的弥补做法是预先准备好“假数据”，也就是上一个月的旧数据（在第3步）。此外，将目标“gen_cluster”的命令`@cd $(event_dir) && poetry run python cluster.py -source_file $(date_json_file) -target_file $(date_json_file) > cluster.log 2>&1`和“sentiment_and_wordcount”的第一条命令`@cd $(senti_dir) && poetry run python post_senti.py......`去掉（这两个命令需要用到gpu环境），并预先准备好这些命令的输出结果数据（第3步）。

3. 将Desktop/hyj/old_data目录下的`result`文件夹复制到analyze所在的同级目录。result文件夹保存了4.27～5.27的爬虫和使用到gpu部分的分析过程的结果。

4. 将result文件夹复制后，修改其中的所有文件的文件名为当天日期，如`2024-06-29.json`

5. 对于产生的所有log文件，可以在`config.yaml`中修改`remain_outputs`为false，下一次make时就能删除。