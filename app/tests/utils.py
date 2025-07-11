import json
import tempfile
from io import BytesIO

def create_test_report_file(report_data):
    """创建测试报告文件"""
    report_json = json.dumps(report_data)
    return (BytesIO(report_json.encode('utf-8')), 'test-report.json')

def create_test_report_data():
    """创建测试报告数据"""
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