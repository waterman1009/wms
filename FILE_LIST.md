# 项目文件清单

## 📋 根目录文件

### Python 核心文件
- `app.py` - Flask 后端主程序
- `database.py` - 数据库操作封装
- `models.py` - 数据模型定义
- `import_excel.py` - Excel 导入工具
- `requirements.txt` - Python 依赖列表
- `warehouse.db` - SQLite 数据库文件

### 启动脚本
- `install.sh` - 安装脚本（安装所有依赖）
- `start.sh` - 启动脚本（支持 dev/prod 模式）
- `stop.sh` - 停止脚本（停止所有服务）
- `status.sh` - 状态查看脚本

### 主要文档
- `README.md` - 项目总览和介绍
- `QUICKSTART.md` - 快速开始指南
- `SCRIPTS.md` - 脚本详细使用说明
- `SUMMARY.md` - 项目更新总结
- `PROJECT_STRUCTURE.md` - 项目结构详细说明
- `CLEANUP_SUMMARY.md` - 项目整理总结
- `FILE_LIST.md` - 本文件，文件清单

### 配置文件
- `.gitignore` - Git 忽略配置

## 📂 docs/ 目录

### 文档索引
- `INDEX.md` - 文档索引和导航中心

### 功能文档
- `系统功能总结.md` - 完整的系统功能说明
- `发货二次确认功能说明.md` - 发货确认功能详解
- `客户管理功能说明.md` - 客户管理功能说明
- `界面改版说明.md` - 界面改版记录

### 部署文档
- `DEPLOY.md` - 生产环境部署指南

## 🔧 scripts/ 目录

### 辅助脚本
- `backup.sh` - 数据库备份脚本
- `package.sh` - 项目打包脚本
- `logs.sh` - 日志查看脚本
- `clean-logs.sh` - 清理旧日志脚本

## 📊 data/ 目录

### 数据文件
- `产品配件.xlsx` - 产品配件数据模板

## 🎨 frontend/ 目录

### 前端项目根文件
- `index.html` - HTML 入口文件
- `package.json` - 前端依赖配置
- `package-lock.json` - 依赖锁定文件
- `vite.config.js` - Vite 构建配置
- `README.md` - 前端开发文档

### src/ 源代码目录
- `src/main.js` - 前端入口文件
- `src/App.vue` - 根组件

#### src/api/ API 接口
- `src/api/index.js` - API 接口封装

#### src/assets/ 静态资源
- `src/assets/styles.css` - 全局样式

#### src/components/ 通用组件
- `src/components/TopHeader.vue` - 顶部导航栏
- `src/components/Sidebar.vue` - 侧边栏菜单
- `src/components/MessageAlert.vue` - 消息提示组件
- `src/components/AutocompleteInput.vue` - 自动完成输入框
- `src/components/EditProductModal.vue` - 产品编辑弹窗
- `src/components/CustomerModal.vue` - 客户编辑弹窗
- `src/components/ShipmentConfirmModal.vue` - 发货确认弹窗

#### src/layouts/ 布局组件
- `src/layouts/MainLayout.vue` - 主布局组件

#### src/router/ 路由配置
- `src/router/index.js` - Vue Router 配置

#### src/views/ 页面组件
- `src/views/LoginView.vue` - 登录页面
- `src/views/InventoryView.vue` - 库存查询页面
- `src/views/AddProductView.vue` - 添加产品页面
- `src/views/StockInView.vue` - 配件入库页面
- `src/views/StockOutView.vue` - 生产出库页面
- `src/views/DefectsView.vue` - 配件损耗页面
- `src/views/ShipmentView.vue` - 成品发货页面
- `src/views/ShipmentRecordsView.vue` - 发货记录页面
- `src/views/HistoryView.vue` - 交易历史页面
- `src/views/CustomersView.vue` - 客户管理页面
- `src/views/UsersView.vue` - 用户管理页面

## 📝 logs/ 目录

### 日志文件（自动生成）
- `backend_*.log` - 后端服务日志（开发模式）
- `frontend_*.log` - 前端服务日志（开发模式）
- `app_*.log` - 应用日志（生产模式）
- `backend.pid` - 后端进程 ID 文件
- `frontend.pid` - 前端进程 ID 文件
- `app.pid` - 应用进程 ID 文件

## 🚫 忽略的目录

以下目录不纳入版本控制：

- `venv/` - Python 虚拟环境
- `node_modules/` - Node.js 依赖
- `__pycache__/` - Python 缓存
- `.vscode/` - VS Code 配置
- `.git/` - Git 仓库
- `static/` - 前端构建产物（生产模式）

## 📊 文件统计

### 根目录
- Python 文件: 4 个
- Shell 脚本: 4 个
- Markdown 文档: 7 个
- 配置文件: 2 个

### docs/ 目录
- Markdown 文档: 6 个

### scripts/ 目录
- Shell 脚本: 4 个

### frontend/ 目录
- Vue 组件: 18 个
- JavaScript 文件: 3 个
- 配置文件: 3 个
- 文档: 1 个

### 总计
- Python 文件: 4 个
- Vue 组件: 18 个
- JavaScript 文件: 3 个
- Shell 脚本: 8 个
- Markdown 文档: 14 个
- 配置文件: 5 个

## 🎯 文件用途分类

### 开发文件
- Python 核心文件（4 个）
- Vue 前端文件（21 个）
- 配置文件（5 个）

### 运维文件
- 启动脚本（4 个）
- 辅助脚本（4 个）

### 文档文件
- 根目录文档（7 个）
- docs/ 文档（6 个）
- 前端文档（1 个）

### 数据文件
- 数据库文件（1 个）
- Excel 文件（1 个）

## 📖 重要文件说明

### 必读文档
1. `README.md` - 项目总览
2. `QUICKSTART.md` - 快速开始
3. `SCRIPTS.md` - 脚本使用

### 核心代码
1. `app.py` - 后端主程序
2. `database.py` - 数据库操作
3. `frontend/src/` - 前端源代码

### 关键配置
1. `requirements.txt` - Python 依赖
2. `frontend/package.json` - 前端依赖
3. `frontend/vite.config.js` - 构建配置

---

**文件清单更新日期: 2026-03-09**
