# 仓库描述

### 介绍 📖

此处readme仅介绍如何爬取一个月内的对应话题的微博的帖子和评论数据

- **Install：**

你可以根据
```text
poetry install
```
或者是
```text
pip install -r requirements.txt
```
来安装必要的库

- **一些准备：**
1.修改connect_db()，将自己的数据库配置写好。
2.启动浏览器，访问该示例网址：
https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=4467107636950632&is_show_bulletin=2&is_mix=0&count=100&flow=0
然后 f12 找到 访问该网址的cookies，将其复制到  comment_config.json里的cookie字段。


- **Run：**
依次运行脚本：
1.爬取帖子
```text
python LatestPostSpider_fordaily.py
```
2.爬取评论
```text
python LastestCommentSpider_fordaily.py
```
3.数据库导出为json
```text
python convert_to_json_OneMonth.py
```


更多信息，请见文档：
https://xwpk9ejbd1.feishu.cn/docx/RIradHAONot2bBxvdDVcQ05xnxg?from=from_copylink