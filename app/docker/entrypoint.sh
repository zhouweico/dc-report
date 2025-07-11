#!/bin/bash
set -e

# 是否跳过数据库升级（通过环境变量控制）
if [[ "${MIGRATION_ENABLED}" == "true" ]]; then
  echo "[Entrypoint] 正在执行数据库升级 (alembic upgrade head) ..."
  alembic -c migrations/alembic.ini upgrade head || { echo "数据库升级失败，退出"; exit 1; }
fi

echo "[Entrypoint] 启动 Gunicorn ..."
exec gunicorn \
  -w ${GUNICORN_WORKERS:-4} \
  -k ${GUNICORN_WORKER_CLASS:-gevent} \
  --timeout ${GUNICORN_TIMEOUT:-300} \
  --capture-output \
  -b ${GUNICORN_BIND:-0.0.0.0:5001} \
  app:app