.PHONY: test test-cov test-unit test-api clean help

help: ## 显示帮助信息
	@echo "可用的命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test: ## 运行所有测试
	pytest -c app/pytest.ini

test-cov: ## 运行测试并生成覆盖率报告
	pytest -c app/pytest.ini --cov=app --cov-report=html --cov-report=term

test-unit: ## 运行单元测试
	pytest -c app/pytest.ini -m unit

test-api: ## 运行 API 测试
	pytest -c app/pytest.ini -m api

test-web: ## 运行 Web 界面测试
	pytest -c app/pytest.ini -m web

clean: ## 清理测试缓存和临时文件
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete

install-dev: ## 安装开发依赖
	pip install -r app/requirements.txt

run: ## 运行开发服务器
	cd app && python app.py

docker-build: ## 构建 Docker 镜像
	docker build -t dc-report ./app --no-cache

docker-run: ## 运行 Docker 容器
	docker compose -p dc-report up -d

docker-stop: ## 停止 Docker 容器
	docker compose -p dc-report down

docker-logs: ## 查看 Docker 容器日志
	docker compose -p dc-report logs -f

docker-debug: ## 调试 Docker 容器
	docker compose -p dc-report exec dc-report bash

install: ## 安装生产依赖
	pip install -r app/requirements.txt

freeze: ## 冻结当前依赖版本
	pip freeze > app/requirements.txt

format: ## 格式化代码
	black app/

lint: ## 代码检查
	flake8 app/
	mypy app/ 