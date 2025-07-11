from utils.database import get_db_connection, get_db_cursor
from utils.helpers import build_pagination_info
import logging

logger = logging.getLogger(__name__)

class ReportService:
    """报告查询服务"""
    
    @staticmethod
    def get_report_data(filters, page=1, page_size=20):
        """获取报告数据"""
        try:
            # 构建基础 SQL
            sql = '''
                SELECT
                    p.name AS project_name,
                    p.report_date,
                    p.import_date,
                    d.file_path,
                    d.sha1,
                    sv.cve,
                    sv.cvss_score AS scan_score,
                    v.v3BaseScore,
                    v.v3BaseSeverity,
                    v.v3AttackVector,
                    v.v3AttackComplexity,
                    v.v3PrivilegesRequired,
                    v.v3UserInteraction,
                    v.v3Scope,
                    v.v3ExploitabilityScore,
                    v.v3ImpactScore,
                    v.v4baseScore,
                    v.v4baseSeverity,
                    v.v4attackVector,
                    v.v4exploitMaturity,
                    v.v4environmentalSeverity,
                    k.cveID IS NOT NULL AS is_known_exploited,
                    COALESCE(sv.description, v.description) AS description,
                    (
                        SELECT json_agg(json_build_object(
                            'versionStartIncluding', s.versionStartIncluding,
                            'versionEndIncluding', s.versionEndIncluding,
                            'versionStartExcluding', s.versionStartExcluding,
                            'versionEndExcluding', s.versionEndExcluding
                        ))
                        FROM software s
                        JOIN vulnerability v2 ON s.cveid = v2.id
                        WHERE v2.cve = sv.cve
                          AND (
                            s.versionStartIncluding IS NOT NULL OR
                            s.versionEndIncluding IS NOT NULL OR
                            s.versionStartExcluding IS NOT NULL OR
                            s.versionEndExcluding IS NOT NULL
                          )
                    ) AS safe_versions
                FROM
                    scan_project p
                JOIN scan_dependency d ON d.project_id = p.id
                JOIN scan_vulnerability sv ON sv.dependency_id = d.id
                LEFT JOIN vulnerability v ON sv.cve = v.cve
                LEFT JOIN knownExploited k ON sv.cve = k.cveID
                WHERE 1=1
            '''
            
            params = []
            
            # 添加过滤条件
            if filters.get('project_id'):
                sql += ' AND p.id = %s'
                params.append(filters['project_id'])
            if filters.get('project_name'):
                sql += ' AND p.name ILIKE %s'
                params.append(f'%{filters["project_name"]}%')
            if filters.get('file_path'):
                sql += ' AND d.file_path ILIKE %s'
                params.append(f'%{filters["file_path"]}%')
            if filters.get('cve'):
                sql += ' AND sv.cve = %s'
                params.append(filters['cve'])
            if filters.get('sha1'):
                sql += ' AND d.sha1 = %s'
                params.append(filters['sha1'])
            if filters.get('severity'):
                sql += ' AND (sv.severity = %s OR v.v3BaseSeverity = %s OR v.v4baseSeverity = %s)'
                params.extend([filters['severity'], filters['severity'], filters['severity']])
            
            sql += ' ORDER BY v.v3BaseScore DESC NULLS LAST'

            # 统计总数
            count_sql = 'SELECT COUNT(*) FROM (' + sql + ') AS subquery'
            conn = get_db_connection()
            cur = get_db_cursor(conn, dict_cursor=True)
            
            logger.info(f"执行查询: {count_sql} 参数: {params}")
            cur.execute(count_sql, params)
            total = cur.fetchone()['count']
            logger.info(f"查询结果总数: {total}")

            # 分页查询
            offset = (page - 1) * page_size
            sql += ' LIMIT %s OFFSET %s'
            params.extend([page_size, offset])
            cur.execute(sql, params)
            rows = cur.fetchall()
            cur.close()
            conn.close()

            logger.info(f"返回数据条数: {len(rows)}")

            return {
                'data': rows,
                'pagination': build_pagination_info(page, page_size, total)
            }
            
        except Exception as e:
            logger.error(f"查询报告数据失败: {str(e)}")
            raise Exception(f"数据库查询失败: {str(e)}") 