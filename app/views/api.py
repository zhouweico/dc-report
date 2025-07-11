from flask import Blueprint, request, jsonify
from services.import_service import ImportService
from services.report_service import ReportService

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/import-report', methods=['POST'])
def import_report():
    """导入扫描报告 API"""
    if 'report' not in request.files:
        return jsonify({'error': 'No report uploaded'}), 400

    try:
        result = ImportService.import_report(request.files['report'])
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({
            'error': 'Invalid report format',
            'detail': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'detail': str(e)
        }), 500

@bp.route('/projects/report', methods=['GET'])
def get_report():
    """获取报告数据 API"""
    # 获取查询参数
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
            return jsonify({
                'message': '没有找到匹配的数据',
                'data': [],
                'pagination': result['pagination'],
                'filters_applied': filters
            }), 200
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'detail': str(e)
        }), 500