#!/bin/bash

# 1. 创建目录结构
mkdir -p .github/workflows
mkdir -p data
mkdir -p logs
mkdir -p src
mkdir -p tests
mkdir -p configs
mkdir -p static/css
mkdir -p static/js

# 2. 创建基础文件
#touch index.html
touch requirements.txt
touch .gitignore.txt
touch .env

# 3. 写入 requirements.txt 默认内容
cat <<EOT > requirements.txt
requests
beautifulsoup4
lxml
feedparser
EOT

# 4. 生成 README.md
cat <<EOT > README.md
# TECHURLS Dashboard

这是一个基于 GitHub Actions 的自动化科技资讯聚合仪表盘。它通过 Python 爬虫定时抓取新闻，使用 SQLite 进行去重持久化，并自动更新前端展示。

## 📂 工程目录说明

| 路径 | 说明 |
| :--- | :--- |
| **.github/workflows/** | 存放 GitHub Actions 自动化配置文件。 |
| **data/data.json** | 前端核心数据源，存放每个来源最新的 50 条新闻。 |
| **index.html** | 仪表盘前端页面，实现 20+10 增量加载及响应式布局。 |
| **crawler.py** | Python 爬虫脚本，负责抓取、入库 (SQLite) 及导出 JSON。 |
| **news.db** | SQLite 数据库文件，用于新闻去重及历史数据持久化。 |
| **requirements.txt** | Python 环境依赖声明（requests, bs4 等）。 |
| **static/** | 存放静态资源文件（CSS/JS/Images）。 |

## 🚀 自动化逻辑描述

1. **触发 (Trigger)**: GitHub Actions 根据 \`update_news.yml\` 设定的定时任务（每小时）启动。
2. **运行 (Runner)**: 在云端 Ubuntu 虚拟环境中安装 Python 并运行 \`crawler.py\`。
3. **持久化 (Persistence)**: 爬虫读取 \`news.db\`，将新内容插入并自动去重，随后导出最新的 50 条到 \`data.json\`。
4. **同步 (Sync)**: Actions 自动执行 Git Commit & Push，将更新后的数据库和 JSON 推送回仓库。
5. **展示 (Display)**: GitHub Pages 自动检测到仓库变化，更新后的内容在前端 \`index.html\` 中实时展现。

## 🔧 部署指南

1. **权限设置**: 仓库 Settings -> Actions -> General -> Workflow permissions 设置为 "Read and write permissions"。
2. **开启 Pages**: 仓库 Settings -> Pages -> Deploy from a branch (main)。
EOT

echo "✅ 工程目录及 README.md 创建成功！"
