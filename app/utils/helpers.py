import json
import hashlib
import datetime

def calculate_report_hash(report):
    """计算报告唯一性哈希"""
    return hashlib.sha256(json.dumps(report, sort_keys=True).encode('utf-8')).hexdigest()

def format_datetime(dt):
    """格式化日期时间"""
    if isinstance(dt, str):
        return dt
    return dt.strftime('%Y-%m-%d %H:%M:%S') if dt else None

def build_pagination_info(page, page_size, total):
    """构建分页信息"""
    return {
        'page': page,
        'page_size': page_size,
        'total': total,
        'total_pages': (total + page_size - 1) // page_size,
        'has_prev': page > 1,
        'has_next': page * page_size < total
    } 