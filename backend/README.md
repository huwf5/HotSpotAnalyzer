## 前置设置
1. 新建一个数据库'HotSpotAnalyzerDB':
    ```mysql
    CREATE DATABASE HotSpotAnalyzerDB;
    ```

2. 修改[配置文件](config/conf.py)
    - 修改数据库连接信息
        - 更改`DATABASES_USER`,`DATABASES_PASSWORD`为数据库用户名和密码
        - 确保`DATABASES_ENGINE`为对应数据库引擎，默认为MySQL，还有对应的`DATABASES_HOST`和`DATABASES_PORT`
    - 修改邮箱设置
        - 更改`EMAIL_HOST`为对应的邮箱服务器，`EMAIL_PORT`为对应的端口
        - 更改`EMAIL_HOST_USER`和`EMAIL_HOST_PASSWORD`为对应的邮箱用户名和密码(请从各邮箱平台中获取授权码)
        - `EMAIL_WHITELIST`为邮箱白名单，只有白名单中的邮箱才能注册账号,若无需限制注册邮箱，请将其设置为['@*'],来允许各种邮箱注册。后续管理员可在web中更改该限制。
    - 设置超级管理员账号
        - 更改其中的`SUPER_ADMIN_EMAIL`,`SUPER_ADMIN_USERNAME`,和`SUPER_ADMIN_PASSWORD`
3. 安全设置
    - 在生产环境中设置`DEBUG`为False，仅在开发环境中设置为True

## 运行程序
   1. `poetry install`下载虚拟环境并启用`poetry shell`
   2. 初始化数据库 `python manage.py makemigrations && python manage.py migrate && python manage.py init`
   3. 打包前端文件 `pnpm run build:pro` 并新建文件夹`mkdir -p static`后收集静态文件 `python manage.py collectstatic --noinput`
   4. 运行后端服务器 `python manage.py runserver`

### 其他功能
1. `python manage.py import [pathtofile.json]`来导入事件消息