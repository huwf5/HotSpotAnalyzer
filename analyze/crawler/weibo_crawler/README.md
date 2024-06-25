# Weibo Data Scraper

## 运行步骤

### 1. 安装对应的依赖
```shell
pip install -r requirements.txt
```
### 2. 安装 Selenium 的 Chrome 浏览器驱动
https://deploy-preview-1382--selenium-dev.netlify.app/zh-cn/documentation/webdriver/getting_started/install_drivers/

### 3. 大批量爬取
#### 3.1 爬取子话题
```bash
python weibo_topic_subtopic.py
```
#### 3.2 爬取话题的帖子数据
##### 3.2.1 修改 connect_db() 部分的 pymysql
```python
def connect_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='huchp6', # 修改密码
        db='weibo_test',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
```
##### 3.2.2 运行脚本
```bash
python WeiboCnTopicSpiderWithoutCookie.py
```

#### 3.3 爬取评论
##### 3.3.1 修改 connect_db()
##### 3.3.2 在 comment_config.json 里修改 cookie,cookie 的获取方式在下方。

##### 3.3.3 运行
```bash
python newWeiboComment.py
```

### 4. 最近一个月的爬取
#### 4.1 爬取最近一个月的 '中山大学' 的帖子数据
##### 4.1.1 修改 connect_db() 部分的 pymysql
```python
def connect_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='huchp6', # 修改密码
        db='weibo_test',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
```
##### 4.1.2 确认 post_monthly_config.json 的配置，设置 isoneMonth 为 true
##### 4.1.3 运行脚本
```bash
python LatestPostSpider_fordaily.py
```

#### 4.2 爬取最近一个月的帖子的评论
##### 4.2.1 修改 connect_db()
##### 4.2.2 修改 limit，limit 是执行爬取评论的帖子上限。
##### 4.2.3 运行
```bash
python LastestCommentSpider_fordaily.py
```

#### 数据转化为 JSON
```bash
python convert_to_json_csv_onlypostAndKeyword.py
python convert_to_json_Allpost_with_comment.py
python convert_to_json_OneMonth.py
```