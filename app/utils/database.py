import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

def get_db_connection():
    """获取数据库连接"""
    return psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASS
    )

def get_db_cursor(connection, dict_cursor=False):
    """获取数据库游标"""
    if dict_cursor:
        return connection.cursor(cursor_factory=RealDictCursor)
    return connection.cursor() 