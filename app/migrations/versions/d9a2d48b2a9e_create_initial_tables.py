"""create initial tables

Revision ID: d9a2d48b2a9e
Revises: 
Create Date: 2025-07-10 17:55:20.759441

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd9a2d48b2a9e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'scan_project',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Text, nullable=False),
        sa.Column('report_date', sa.TIMESTAMP(timezone=True)),
        sa.Column('import_date', sa.TIMESTAMP, server_default=sa.text('NOW()')),
        sa.Column('report_hash', sa.Text, unique=True),
    )
    op.create_index('idx_scan_project_name', 'scan_project', ['name'])

    op.create_table(
        'scan_dependency',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('scan_project.id', ondelete='CASCADE')),
        sa.Column('file_path', sa.Text),
        sa.Column('sha1', sa.Text),
        sa.Column('md5', sa.Text),
        sa.Column('evidence', sa.Text),
    )
    op.create_index('idx_scan_dependency_file_path', 'scan_dependency', ['file_path'])
    op.create_index('idx_scan_dependency_sha1', 'scan_dependency', ['sha1'])

    op.create_table(
        'scan_vulnerability',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('dependency_id', sa.Integer, sa.ForeignKey('scan_dependency.id', ondelete='CASCADE')),
        sa.Column('cve', sa.Text),
        sa.Column('cvss_score', sa.Numeric),
        sa.Column('severity', sa.Text),
        sa.Column('description', sa.Text),
    )
    op.create_index('idx_scan_vulnerability_cve', 'scan_vulnerability', ['cve'])
    op.create_index('idx_scan_vulnerability_severity', 'scan_vulnerability', ['severity'])


def downgrade():
    op.drop_index('idx_scan_vulnerability_severity', table_name='scan_vulnerability')
    op.drop_index('idx_scan_vulnerability_cve', table_name='scan_vulnerability')
    op.drop_table('scan_vulnerability')

    op.drop_index('idx_scan_dependency_sha1', table_name='scan_dependency')
    op.drop_index('idx_scan_dependency_file_path', table_name='scan_dependency')
    op.drop_table('scan_dependency')

    op.drop_index('idx_scan_project_name', table_name='scan_project')
    op.drop_table('scan_project')