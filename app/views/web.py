from flask import Blueprint, request, render_template
from services.report_service import ReportService

bp = Blueprint('web', __name__)

@bp.route('/projects/report')
def project_report():
    """项目报告页面"""
    # 获取查询参数
    if not request.args:
        return '''<div style="margin:40px auto;max-width:600px;font-size:18px;color:#444;line-height:2;">
        <b>请提供查询参数！</b><br>
        支持的参数有：<br>
        <ul>
          <li><b>project_name</b>：项目名称（模糊匹配）</li>
          <li><b>file_path</b>：依赖路径（模糊匹配）</li>
          <li><b>cve</b>：CVE编号</li>
          <li><b>sha1</b>：依赖SHA1</li>
          <li><b>severity</b>：严重等级</li>
          <li><b>page</b>：页码（从1开始）</li>
          <li><b>page_size</b>：每页数量（最大100）</li>
        </ul>
        示例：<br>
        <code>/projects/report?project_name=demo&severity=HIGH</code>
        </div>''', 400

    # 获取过滤条件
    filters = {
        'project_name': request.args.get('project_name'),
        'file_path': request.args.get('file_path'),
        'cve': request.args.get('cve'),
        'sha1': request.args.get('sha1'),
        'severity': request.args.get('severity')
    }
    
    # 移除空值
    filters = {k: v for k, v in filters.items() if v is not None}
    
    # 分页参数
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=20, type=int)
    if page_size > 100:
        page_size = 100

    try:
        result = ReportService.get_report_data(filters, page, page_size)
        
        # 检查是否有数据
        if not result['data']:
            return f'''<div style="margin:40px auto;max-width:600px;font-size:18px;color:#666;line-height:2;">
            <b>没有找到匹配的数据</b><br>
            查询条件：{filters if filters else '无'}<br>
            页码：{page}，每页：{page_size}条<br>
            <a href="/projects/report">返回查询页面</a>
            </div>''', 200
        
        return render_template(
            "project_report.html",
            report=result['data'],
            pagination=result['pagination']
        )
    except Exception as e:
        return f'<div style="margin:40px auto;max-width:600px;color:red;">查询失败: {str(e)}</div>', 500