import pytest
import tempfile
import os
from app_factory import create_app
from config import TestingConfig

@pytest.fixture
def app():
    """创建测试应用实例"""
    app = create_app(TestingConfig)
    
    # 创建临时数据库文件（如果使用 SQLite）
    with tempfile.NamedTemporaryFile() as f:
        app.config['DATABASE'] = f.name
        yield app

@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """创建测试运行器"""
    return app.test_cli_runner()

@pytest.fixture
def sample_report_data():
    """示例报告数据"""
    return {
        "projectInfo": {
            "name": "test-project",
            "reportDate": "2024-01-01T00:00:00Z"
        },
        "dependencies": [
            {
                "fileName": "test.jar",
                "sha1": "test-sha1",
                "md5": "test-md5",
                "evidenceCollected": {},
                "vulnerabilities": [
                    {
                        "name": "CVE-2023-1234",
                        "cvssScore": 7.5,
                        "severity": "HIGH",
                        "description": "Test vulnerability"
                    }
                ]
            }
        ]
    } 