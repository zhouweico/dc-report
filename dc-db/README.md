## Dependency-Check 漏洞数据

使用 PostgreSQL 持久化存储 Dependency-Check 的漏洞数据，并通过 Docker 执行扫描。

### 1. 初始化数据库结构

使用官方提供的初始化脚本（确保版本匹配 12.1.3）：[initialize_postgres.sql](initialize_postgres.sql)

### 2. 配置文件 dependency-check.properties

在项目根目录下创建 [dependency-check.properties](dependency-check.properties)

### 3. 更新数据（updateonly 模式）

```bash
docker run --rm \
  -v "$(pwd)":/src \
  owasp/dependency-check:12.1.3 \
  --updateonly \
  --propertyfile /src/dependency-check-prod.properties
```