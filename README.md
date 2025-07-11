# DC-Report

## 项目简介
本项目用于导入和展示 Dependency-Check 扫描报告，支持 PostgreSQL 存储和 Web 展示。

## 依赖安装

```bash
# 安装所有依赖（包括开发依赖）
pip install -r app/requirements.txt

# 或者使用 Makefile
make install-dev
```

## 本地运行

```bash
# 方法1：直接运行
cd app && python run.py

# 方法2：使用 Makefile
make run
```

## 测试

### 运行所有测试
```bash
pytest -c app/pytest.ini
```

### 运行特定测试

```bash
# 运行 API 测试
pytest -c app/pytest.ini app/tests/test_api.py::TestAPI

# 运行 Web 界面测试
pytest -c app/pytest.ini app/tests/test_api.py::TestWebInterface

# 运行特定测试方法
pytest -c app/pytest.ini app/tests/test_api.py::TestAPI::test_import_report_no_file
```

### 生成测试覆盖率报告

```bash
pytest -c app/pytest.ini --cov=app --cov-report=html
```

### 测试标记

```bash
# 运行单元测试
pytest -c app/pytest.ini -m unit

# 运行集成测试
pytest -c app/pytest.ini -m integration

# 运行 API 测试
pytest -c app/pytest.ini -m api
```

### 使用 Makefile 简化命令

```bash
# 运行所有测试
make test

# 运行测试并生成覆盖率报告
make test-cov

# 运行 API 测试
make test-api

# 安装依赖
make install-dev
```

## 生产部署（推荐 Docker compose）

1. 构建镜像：
   ```bash
   # 方法1：直接构建
   docker build -t dc-report ./app
   
   # 方法2：使用 Makefile
   make docker-build
   ```

2. 运行容器：
   ```bash
   # 方法1：直接运行
   docker compose -p dc-report up -d
   
   # 方法2：使用 Makefile
   make docker-run
   ```

3. 查看日志：
   ```bash
   make docker-logs
   ```

4. 停止服务：
   ```bash
   make docker-stop
   ```

## API 说明

### 导入报告
- `POST /api/import-report` - 上传 Dependency-Check JSON 报告

### 查询报告
- `GET /api/projects/report` - JSON 格式的 API 接口
- `GET /projects/report` - HTML 格式的 Web 页面

支持的查询参数：

| 参数         | 说明                 | 示例                |
|--------------|----------------------|---------------------|
| project_name | 项目名称（模糊匹配） | demo                |
| file_path    | 依赖路径（模糊匹配） | log4j / lib/core    |
| cve          | CVE编号              | CVE-2023-1234       |
| sha1         | 依赖SHA1             | 123456abcdef...     |
| severity     | 严重等级             | HIGH                |
| page         | 页码（从1开始）      | 2                   |
| page_size    | 每页数量（默认 20，最大100）  | 50          |

## 开发

### 代码结构说明

- **配置管理** (`app/config.py`): 集中管理所有配置项
- **服务层** (`app/services/`): 业务逻辑处理
- **视图层** (`app/views/`): API 和 Web 路由
- **工具函数** (`app/utils/`): 通用工具和数据库连接
- **应用工厂** (`app/app_factory.py`): Flask 应用创建和配置
- **数据库迁移** (`app/migrations/`): Alembic 迁移文件
- **测试** (`app/tests/`): 单元测试和集成测试
- **Docker 配置** (`app/docker/`): 容器相关配置

### 开发工具

### 依赖管理
```bash
# 安装开发依赖
make install-dev

# 安装生产依赖
make install

# 冻结当前依赖版本
make freeze
```

### 代码质量
```bash
# 清理缓存文件
make clean

# 运行测试
make test

# 生成覆盖率报告
make test-cov

# 格式化代码
make format

# 代码检查
make lint
```

### 测试开发指南

1. **单元测试**：测试独立的函数和方法
2. **集成测试**：测试模块间的交互
3. **API 测试**：测试 API 端点的功能
4. **Web 测试**：测试 Web 界面的功能

### 测试最佳实践

- 每个测试函数只测试一个功能点
- 使用描述性的测试函数名称
- 使用 fixtures 来设置测试数据
- 测试正常情况和异常情况
- 保持测试的独立性

## 环境变量

创建 `.env` 文件并配置以下环境变量：

```env
# 数据库配置
DB_USER=dcuser
DB_PASS=dcpass
DB_HOST=dc-postgres
DB_PORT=5432
DB_NAME=dependencycheck

# Gunicorn 配置
GUNICORN_WORKERS=4
GUNICORN_WORKER_CLASS=gevent
GUNICORN_TIMEOUT=300
GUNICORN_BIND=0.0.0.0:5001

# 其他配置
MIGRATION_ENABLED=true
SECRET_KEY=your-secret-key-here
```

---

## Dependency-Check 漏洞数据

使用 PostgreSQL 持久化存储 Dependency-Check 的漏洞数据，并通过 Docker 执行扫描。操作步骤参考：[dc-db/README.md](dc-db/README.md)