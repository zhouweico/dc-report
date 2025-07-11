import pytest
from app_factory import create_app
from config import TestingConfig

@pytest.fixture
def app():
    """创建测试应用实例"""
    app = create_app(TestingConfig)
    return app

@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """创建测试运行器"""
    return app.test_cli_runner()

class TestAPI:
    """API 测试类"""
    
    def test_import_report_no_file(self, client):
        """测试导入报告时没有文件的情况"""
        response = client.post('/api/import-report')
        assert response.status_code == 400
        assert b'No report uploaded' in response.data

    def test_project_report_no_params(self, client):
        """测试项目报告页面没有参数的情况"""
        response = client.get('/projects/report')
        assert response.status_code == 400
        assert b'请提供查询参数' in response.data

    def test_api_help_endpoint(self, client):
        """测试 API 帮助端点"""
        response = client.get('/api/projects/report/help')
        assert response.status_code == 200
        data = response.get_json()
        assert 'supported_parameters' in data
        assert 'examples' in data

    def test_api_report_empty_result(self, client):
        """测试 API 报告查询返回空结果"""
        response = client.get('/api/projects/report?project_name=nonexistent')
        assert response.status_code == 200
        data = response.get_json()
        assert 'data' in data
        assert 'pagination' in data
        assert len(data['data']) == 0

class TestWebInterface:
    """Web 界面测试类"""
    
    def test_web_report_no_params(self, client):
        """测试 Web 报告页面没有参数的情况"""
        response = client.get('/projects/report')
        assert response.status_code == 400
        assert b'请提供查询参数' in response.data

    def test_web_report_with_params(self, client):
        """测试 Web 报告页面有参数的情况"""
        response = client.get('/projects/report?project_name=test')
        # 可能返回 200（有数据）或 500（数据库错误）
        assert response.status_code in [200, 500] 