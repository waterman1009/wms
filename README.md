# 仓库管理系统

一个基于 Flask + Vue 3 的现代化仓库管理系统，支持库存管理、出入库、发货、客户管理等功能。

## ✨ 特性

- 📦 **库存管理** - 产品查询、添加、编辑、删除
- 📥 **配件入库** - 配件入库记录
- 📤 **生产出库** - 成品生产配件出库
- ⚠️ **配件损耗** - 配件损耗登记
- 🚚 **成品发货** - 发货确认和记录
- 📊 **交易历史** - 完整的交易记录查询
- 👥 **客户管理** - 客户信息管理
- 👤 **用户管理** - 多角色用户权限管理
- 📈 **数据导出** - Excel 导出功能

## 🚀 快速开始

### 1. 安装依赖

```bash
./install.sh
```

### 2. 启动服务

**开发模式（推荐用于开发）：**
```bash
./start.sh dev
```
访问：http://localhost:3000

**生产模式（推荐用于部署）：**
```bash
./start.sh prod
```
访问：http://localhost:8080

### 3. 停止服务

```bash
./stop.sh
```

### 4. 查看状态

```bash
./status.sh
```

## 🔐 默认账号

- **用户名：** admin
- **密码：** admin123

⚠️ 首次登录后请立即修改密码！

## 📖 文档

- [快速开始指南](QUICKSTART.md) - 三步启动系统
- [脚本使用说明](SCRIPTS.md) - 详细的脚本使用指南
- [前端开发文档](frontend/README.md) - Vue 前端开发说明
- [系统功能说明](docs/系统功能总结.md) - 完整的功能说明
- [部署文档](docs/DEPLOY.md) - 生产环境部署指南
- [Ant Design 重构总结](ANTD_REFACTOR_SUMMARY.md) - UI 组件库重构说明

## 🛠️ 技术栈

### 后端
- Python 3.8+
- Flask 3.0
- Flask-CORS
- SQLite
- openpyxl

### 前端
- Vue 3
- Vite 5
- Vue Router 4
- Axios

## 📁 项目结构

```
仓库管理系统/
├── app.py                  # Flask 后端主程序
├── database.py             # 数据库操作
├── models.py               # 数据模型
├── requirements.txt        # Python 依赖
├── warehouse.db            # SQLite 数据库
├── frontend/               # Vue 前端项目
│   ├── src/
│   │   ├── api/           # API 接口
│   │   ├── components/    # Vue 组件
│   │   ├── views/         # 页面组件
│   │   └── router/        # 路由配置
│   └── package.json
├── docs/                   # 详细文档
├── scripts/                # 辅助脚本
├── data/                   # 数据文件
├── logs/                   # 日志文件
├── install.sh             # 安装脚本
├── start.sh               # 启动脚本
├── stop.sh                # 停止脚本
└── status.sh              # 状态查看脚本
```

详细说明请查看 [ANTD_REFACTOR_SUMMARY.md](ANTD_REFACTOR_SUMMARY.md)

## 🎯 功能模块

### 库存管理
- 产品列表查询（支持分页和搜索）
- 添加产品（配件/成品）
- 编辑产品信息
- 删除产品
- 成品配件配置

### 出入库管理
- 配件入库
- 生产出库（配件消耗）
- 配件损耗登记

### 销售管理
- 成品发货（带二次确认）
- 发货记录查询
- 客户管理

### 统计查询
- 交易历史查询
- 日期范围筛选
- 类型筛选
- Excel 导出

### 系统管理
- 用户管理（管理员）
- 客户管理（管理员）
- 角色权限控制

## 👥 用户角色

- **系统管理员（ADMIN）** - 完全权限
- **仓库管理员（MANAGER）** - 管理权限
- **生产人员（WORKER）** - 基础操作权限

## 🔧 开发模式 vs 生产模式

### 开发模式
- 前后端分离运行
- 支持热更新
- 前端：http://localhost:3000
- 后端：http://localhost:8080
- 适合开发调试

### 生产模式
- 前端构建为静态文件
- 单一服务运行
- 访问：http://localhost:8080
- 性能优化
- 适合生产部署

## 📝 常用命令

```bash
# 安装依赖
./install.sh

# 启动开发环境
./start.sh dev

# 启动生产环境
./start.sh prod

# 停止服务
./stop.sh

# 查看状态
./status.sh

# 查看日志
./logs.sh

# 查看实时日志
tail -f logs/backend_*.log
tail -f logs/frontend_*.log
```

## 🐛 故障排除

### 端口被占用
```bash
./stop.sh
# 或
lsof -ti:8080 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

### 依赖问题
```bash
# 重新安装
rm -rf venv frontend/node_modules
./install.sh
```

### 查看错误日志
```bash
tail -f logs/backend_*.log
tail -f logs/frontend_*.log
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题，请提交 Issue。
