import json
import datetime
from psycopg2.errors import UniqueViolation
from utils.database import get_db_connection
from utils.helpers import calculate_report_hash

class ImportService:
    """报告导入服务"""
    
    @staticmethod
    def import_report(report_file):
        """导入扫描报告"""
        try:
            # 读取上传报告
            report_data = json.load(report_file)
            report_hash = calculate_report_hash(report_data)
            project_name = report_data.get('projectInfo', {}).get('name', 'Unnamed')
            report_date = report_data.get('projectInfo', {}).get('reportDate')
            import_date = datetime.datetime.now()

            conn = get_db_connection()

            with conn:
                with conn.cursor() as cur:
                    try:
                        # 插入项目记录
                        cur.execute("""
                            INSERT INTO scan_project(name, report_date, import_date, report_hash)
                            VALUES (%s, %s, %s, %s)
                            RETURNING id
                        """, (project_name, report_date, import_date, report_hash))
                        project_id = cur.fetchone()[0]

                    except UniqueViolation:
                        conn.rollback()
                        cur.execute("SELECT name FROM scan_project WHERE report_hash = %s", (report_hash,))
                        row = cur.fetchone()
                        return {'status': 'duplicate', 'project_name': row[0]}

                    # 插入依赖项
                    for dep in report_data.get('dependencies', []):
                        file_path = dep.get('fileName')
                        sha1 = dep.get('sha1')
                        md5 = dep.get('md5')
                        evidence = json.dumps(dep.get('evidenceCollected', {}))

                        cur.execute("""
                            INSERT INTO scan_dependency(project_id, file_path, sha1, md5, evidence)
                            VALUES (%s, %s, %s, %s, %s)
                            RETURNING id
                        """, (project_id, file_path, sha1, md5, evidence))
                        dependency_id = cur.fetchone()[0]

                        # 插入漏洞项
                        for vuln in dep.get('vulnerabilities', []):
                            cur.execute("""
                                INSERT INTO scan_vulnerability(dependency_id, cve, cvss_score, severity, description)
                                VALUES (%s, %s, %s, %s, %s)
                            """, (
                                dependency_id,
                                vuln.get('name'),
                                vuln.get('cvssScore'),
                                vuln.get('severity'),
                                vuln.get('description')
                            ))

            return {'status': 'success', 'project_name': project_name}

        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f'Invalid report format: {str(e)}')
        except Exception as e:
            raise Exception(f'Import failed: {str(e)}') 