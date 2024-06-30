## 后端文档

[后端文档](backend/README.md)

## 前端文档

[前端文档](web/README.md)

## 项目部署

1. 首先完成[后端文档](backend/README.md)的**前置设置**和[前端文档](web/README.md)的**介绍**--`install`步骤。

2. 然后在项目根目录（当前README所在目录）依次运行以下命令：
   
   1. ##### 初始化数据库
      
      ```shell
      make server_init_db
      ```
   
   2. ##### 运行项目
      
      ```shell
      make run
      ```
   
   3. ##### 进行事件分析过程
      
      在事件分析过程之前，先查看[事件分析介绍](analyze/README.md)。
      
      一定先查看[爬虫文档](crawler/weibocrawler/weibo_crawler/README.md)，需要在代码文件中修改数据库相关配置。
      
      ```shell
      make analyze
      ```
