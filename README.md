# 仓库管理系统

一个基于Flask的现代化仓库管理系统，用于管理配件和成品的库存、生产和交易记录。

## ✨ 功能特点

### 核心功能
- 📦 **库存管理** - 实时查看配件和成品库存
- ➕ **产品管理** - 添加、编辑、删除产品
- 📥 **配件入库** - 配件入库操作，自动更新库存
- 📤 **生产出库** - 选择成品生产，自动扣减配件库存
- ⚠️ **配件损耗** - 记录配件损耗，支持批量登记
- 📊 **交易历史** - 完整的交易记录，支持筛选和导出
- 📥 **Excel导出** - 一键导出交易记录到Excel
- 🔍 **智能搜索** - 配件选择支持自动完成搜索
- 👥 **用户管理** - 多角色用户管理（管理员、仓库管理员、生产人员）
- 🔐 **权限控制** - 基于角色的访问控制

### 技术特点
- 🚀 轻量级设计，易于部署
- 💾 SQLite数据库，无需额外配置
- 🎨 现代化UI设计，响应式布局
- 🔒 Session会话管理，安全可靠
- 📱 支持移动端访问

## 🖥️ 系统要求

### Windows系统
- Windows 10/11 或 Windows Server 2016+
- Python 3.8 或更高版本
- 4GB内存（推荐8GB）
- 500MB可用磁盘空间

### macOS/Linux系统
- macOS 10.15+ 或 Linux（Ubuntu 20.04+）
- Python 3.8 或更高版本
- 4GB内存
- 500MB可用磁盘空间

## 🚀 快速开始

### Windows系统

#### 方法1：一键安装（推荐）
1. 双击运行 `install.bat`
2. 双击运行 `start.bat`
3. 访问 http://localhost:8080
4. 使用 admin / admin123 登录

#### 方法2：手动安装
```cmd
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动应用
python app.py
```

### macOS/Linux系统

```bash
# 1. 创建虚拟环境
python3 -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动应用
python app.py
```

## 📖 详细文档

### Windows用户
- [快速开始指南](快速开始.md) - 5分钟快速部署
- [Windows部署指南](Windows部署指南.md) - 完整部署说明
- [导出功能测试指南](导出功能测试指南.md) - 测试导出功能

### 功能说明
- [交易历史导出功能说明](交易历史导出功能说明.md)
- [配件搜索功能说明](配件搜索功能说明.md)
- [编辑产品弹窗优化说明](编辑产品弹窗优化说明.md)

### 数据管理
- [F16导入结果](F16导入结果.md)
- [库存更新记录](库存更新记录.md)

## 🛠️ 管理脚本（Windows）

### 安装和启动
- `install.bat` - 一键安装脚本
- `start.bat` - 启动应用（开发模式）
- `start_production.bat` - 启动应用（生产模式）
- `stop.bat` - 停止应用

### 维护工具
- `check.bat` - 环境检查
- `backup.bat` - 数据备份
- `install_service.bat` - 安装为Windows服务

## 👤 默认账号

- **用户名**: admin
- **密码**: admin123
- **角色**: 系统管理员

⚠️ **重要**: 首次登录后请立即修改密码！

## 📊 系统架构

```
仓库管理系统/
├── app.py                 # Flask应用主程序
├── database.py            # 数据库操作
├── models.py              # 数据模型
├── requirements.txt       # Python依赖
├── warehouse.db          # SQLite数据库（自动生成）
├── templates/            # HTML模板
│   ├── index.html       # 主页面
│   └── login.html       # 登录页面
├── backup/              # 备份目录（自动创建）
└── venv/                # 虚拟环境（自动创建）
```

## 🔐 安全建议

1. **修改默认密码** - 首次登录后立即修改
2. **定期备份** - 运行 `backup.bat` 备份数据
3. **限制访问** - 仅在需要时开放局域网访问
4. **使用强密码** - 为所有用户设置强密码
5. **定期更新** - 保持Python和依赖包最新

## 🌐 局域网访问

### 1. 配置防火墙
允许8080端口的入站连接

### 2. 获取IP地址
```cmd
ipconfig          # Windows
ifconfig          # macOS/Linux
```

### 3. 访问
局域网内其他设备访问：`http://[你的IP]:8080`

## 📦 依赖包

- Flask==3.0.0 - Web框架
- tabulate==0.9.0 - 表格格式化
- openpyxl==3.1.2 - Excel文件操作

## 🔄 数据备份

### 自动备份（Windows）
运行 `backup.bat`，会自动：
- 备份数据库文件
- 备份Excel文件
- 备份配置文件
- 清理30天前的旧备份

### 手动备份
复制以下文件：
- `warehouse.db` - 数据库
- `20-12月半成品发料.xlsx` - Excel数据

## 🐛 故障排除

### 端口被占用
```cmd
# Windows
netstat -ano | findstr :8080
taskkill /PID <进程ID> /F

# macOS/Linux
lsof -i :8080
kill -9 <进程ID>
```

### Python命令不存在
- 确保Python已安装
- 确保已添加到PATH环境变量
- 重启命令提示符

### 依赖安装失败
```cmd
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 📈 性能优化

1. **使用SSD** - 将数据库放在SSD上
2. **增加内存** - 推荐8GB以上
3. **定期清理** - 清理旧的交易记录
4. **生产服务器** - 使用waitress替代Flask内置服务器

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 📞 技术支持

如遇到问题，请提供：
- 操作系统版本
- Python版本
- 错误信息截图
- 操作步骤

## 🎉 更新日志

### v1.0.0 (2024-01-17)
- ✨ 初始版本发布
- ✨ 基础库存管理功能
- ✨ 用户权限管理
- ✨ 交易历史记录
- ✨ Excel导出功能
- ✨ 配件搜索功能
- ✨ Windows一键部署脚本

## 🙏 致谢

感谢所有使用和支持本项目的用户！
