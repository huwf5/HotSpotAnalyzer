from mediacrawler.main import craw
import mediacrawler.config as config

def main():
    # 爬取评论
    config.base_config.ENABLE_GET_COMMENTS = True
    
    # 使用关系数据库保存
    config.base_config.SAVE_DATA_OPTION = "db"
    
    # mysql 属性设置
    config.db_config.RELATION_DB_URL = "127.0.0.1"
    config.db_config.RELATION_DB_PWD = "xxx"
    craw(platform="xhs", login_type="qrcode", crawler_type="search")