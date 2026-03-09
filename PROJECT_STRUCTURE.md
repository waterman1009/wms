# 项目结构说明

## 📁 目录结构

```
仓库管理系统/
│
├── 📄 核心文件
│   ├── app.py                  # Flask 后端主程序
│   ├── database.py             # 数据库操作封装
│   ├── models.py               # 数据模型定义
│   ├── import_excel.py         # Excel 导入工具
│   ├── requirements.txt        # Python 依赖
│   └── warehouse.db            # SQLite 数据库
│
├── 🚀 启动脚本
│   ├── install.sh              # 安装脚本（安装所有依赖）
│   ├── start.sh                # 启动脚本（dev/prod 模式）
│   ├── stop.sh                 # 停止脚本
│   └── status.sh               # 状态查看脚本
│
├── 📚 文档
│   ├── README.md               # 项目总览（主文档）
│   ├── QUICKSTART.md           # 快速开始指南
│   ├── SCRIPTS.md              # 脚本使用说明
│   ├── SUMMARY.md              # 更新总结
│   └── PROJECT_STRUCTURE.md    # 本文件
│
├── 📂 docs/                    # 详细文档目录
│   ├── 系统功能总结.md         # 系统功能说明
│   ├── 发货二次确认功能说明.md # 发货功能说明
│   ├── 界面改版说明.md         # 界面改版记录
│   ├── 客户管理功能说明.md     # 客户管理说明
│   └── DEPLOY.md               # 部署文档
│
├── 🎨 frontend/                # Vue 3 前端项目
│   ├── src/
│   │   ├── api/                # API 接口封装
│   │   ├── assets/             # 静态资源
│   │   ├── components/         # 通用组件
│   │   ├── layouts/            # 布局组件
│   │   ├── router/             # 路由配置
│   │   ├── views/              # 页面组件
│   │   ├── App.vue             # 根组件
│   │   └── main.js             # 入口文件
│   ├── index.html              # HTML 模板
│   ├── package.json            # 前端依赖
│   ├── vite.config.js          # Vite 配置
│   └── README.md               # 前端开发文档
│
├── 🔧 scripts/                 # 辅助脚本目录
│   ├── backup.sh               # 数据库备份脚本
│   ├── package.sh              # 打包脚本
│   └── logs.sh                 # 日志查看脚本
│
├── 📊 data/                    # 数据文件目录
│   └── 产品配件.xlsx           # 产品配件数据
│
├── 📝 logs/                    # 日志目录
│   ├── backend_*.log           # 后端日志
│   ├── frontend_*.log          # 前端日志
│   ├── app_*.log               # 应用日志
│   ├── backend.pid             # 后端进程 ID
│   └── frontend.pid            # 前端进程 ID
│
└── 🔒 其他
    ├── .gitignore              # Git 忽略配置
    ├── .vscode/                # VS Code 配置
    ├── venv/                   # Python 虚拟环境
    └── __pycache__/            # Python 缓存
```

## 📖 文件说明

### 核心 Python 文件

| 文件 | 说明 |
|------|------|
| `app.py` | Flask 后端主程序，包含所有 API 路由 |
| `database.py` | 数据库操作封装，提供增删改查接口 |
| `models.py` | 数据模型定义 |
| `import_excel.py` | Excel 数据导入工具 |

### 启动脚本

| 脚本 | 说明 | 用法 |
|------|------|------|
| `install.sh` | 安装所有依赖 | `./install.sh` |
| `start.sh` | 启动服务 | `./start.sh dev` 或 `./start.sh prod` |
| `stop.sh` | 停止所有服务 | `./stop.sh` |
| `status.sh` | 查看运行状态 | `./status.sh` |

### 文档文件

| 文档 | 说明 | 适合人群 |
|------|------|----------|
| `README.md` | 项目总览 | 所有人 |
| `QUICKSTART.md` | 快速开始 | 新用户 |
| `SCRIPTS.md` | 脚本详细说明 | 开发者 |
| `SUMMARY.md` | 更新总结 | 维护者 |
| `PROJECT_STRUCTURE.md` | 项目结构 | 开发者 |

### 辅助脚本（scripts/）

| 脚本 | 说明 | 用法 |
|------|------|------|
| `backup.sh` | 数据库备份 | `./scripts/backup.sh` |
| `package.sh` | 项目打包 | `./scripts/package.sh` |
| `logs.sh` | 查看日志 | `./scripts/logs.sh` |

## 🎯 快速导航

### 我想...

- **开始使用** → 阅读 [QUICKSTART.md](QUICKSTART.md)
- **了解项目** → 阅读 [README.md](README.md)
- **学习脚本** → 阅读 [SCRIPTS.md](SCRIPTS.md)
- **查看功能** → 阅读 [docs/系统功能总结.md](docs/系统功能总结.md)
- **前端开发** → 阅读 [frontend/README.md](frontend/README.md)
- **部署项目** → 阅读 [docs/DEPLOY.md](docs/DEPLOY.md)

## 📦 依赖文件

### Python 依赖（requirements.txt）
- Flask 3.0 - Web 框架
- flask-cors - CORS 支持
- openpyxl - Excel 操作
- tabulate - 表格格式化

### 前端依赖（frontend/package.json）
- Vue 3 - 前端框架
- Vite 5 - 构建工具
- Vue Router 4 - 路由管理
- Axios - HTTP 客户端

## 🗂️ 数据文件

### 数据库（warehouse.db）
SQLite 数据库，包含以下表：
- users - 用户表
- products - 产品表
- product_components - 产品配件关系表
- transactions - 交易记录表
- customers - 客户表

### Excel 文件（data/产品配件.xlsx）
产品配件数据模板，用于批量导入

## 📝 日志文件

### 日志类型
- `backend_*.log` - 后端服务日志（开发模式）
- `frontend_*.log` - 前端服务日志（开发模式）
- `app_*.log` - 应用日志（生产模式）

### 日志命名规则
格式：`类型_YYYYMMDD_HHMMSS.log`
示例：`backend_20260309_143210.log`

## 🔧 配置文件

### Git 配置（.gitignore）
忽略以下文件：
- Python 缓存和虚拟环境
- 数据库文件
- 日志文件
- IDE 配置
- Node 模块
- 构建产物

### Vite 配置（frontend/vite.config.js）
- 开发服务器端口：3000
- API 代理：/api → http://127.0.0.1:8080
- 构建输出：../static

## 🚫 已删除的文件

以下文件已被删除或移动：

| 文件 | 原因 | 替代方案 |
|------|------|----------|
| `templates/` | 已用 Vue 替代 | `frontend/src/views/` |
| `test_shipment.html` | 测试文件 | 已集成到系统 |
| `main.py` | 重复文件 | 使用 `app.py` |
| `start-dev.sh` | 已合并 | 使用 `start.sh dev` |
| `stop-dev.sh` | 已合并 | 使用 `stop.sh` |
| `start-prod.sh` | 已合并 | 使用 `start.sh prod` |

## 💡 最佳实践

### 开发时
1. 使用 `./start.sh dev` 启动开发环境
2. 前端代码在 `frontend/src/` 修改
3. 后端代码在根目录修改
4. 使用 `./status.sh` 检查状态

### 部署时
1. 使用 `./start.sh prod` 启动生产环境
2. 前端会自动构建到 `static/`
3. 只需访问一个端口（8080）

### 备份时
1. 使用 `./scripts/backup.sh` 备份数据库
2. 备份文件保存在 `backups/` 目录

## 🔗 相关链接

- [快速开始](QUICKSTART.md)
- [完整文档](README.md)
- [脚本说明](SCRIPTS.md)
- [前端文档](frontend/README.md)
- [系统功能](docs/系统功能总结.md)
