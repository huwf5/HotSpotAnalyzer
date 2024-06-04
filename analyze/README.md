## 运行说明
在该目录的三个文件中，apis.py定义了调用Open AI语言模型的接口，实现了各种函数，包括摘要、提取标题、判断内容性质、构建事件图谱

为了完成聚类分析，用户需要准备数据文件，该文件读入内存后应该为一个列表，
其中每个元素是一条微博帖子信息，包括wid，text，publish_time等字段
运行命令如下，需要指明数据文件的地址和输出文件的地址
```shell
python cluster.py -source_file your_source_file_path -target_file your_output_path
```

完成聚类分析后，需要为每个聚类判断是否为热点事件，并为热点事件提取标题和摘要
运行时，需要指明数据文件和刚才分析的聚类结果文件
```shell
python analyze.py -source_data_file your_data_file -clustering_result your_clustering_result -target_file your_target_file
```

如果需要进一步构建事件图谱，则运行build_event_graph.py，提供源数据文件，上一步的分析结果，以及输出文件地址
```shell
python build_event_graph.py -source_data_file your_data_file -analyze_result your_result -target_file your_data_file
```

构建完事件图谱后，将事件图谱转化为3d-force-graph可以接受的格式：
```shell
python convert_knowledge_graph.py -graph_file your_graph_file -target_file your_target_file
```