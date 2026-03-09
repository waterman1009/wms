# macOS 部署指南

## 📦 部署包内容

```
仓库管理系统/
├── app.py                    # Flask主程序
├── database.py               # 数据库操作
├── models.py                 # 数据模型
├── main.py                   # 命令行版本（可选）
├── requirements.txt          # Python依赖
├── README.md                 # 项目说明
├── DEPLOY.md                 # 本部署指南
├── install.sh                # 安装脚本
├── start.sh                  # 启动脚本
├── stop.sh                   # 停止脚本
├── backup.sh                 # 备份脚本
├── templates/                # HTML模板
│   ├── index.html
│   └── login.html
├── warehouse.db              # 数据库（首次运行自动创建）
└── 20-12月半成品发料.xlsx   # Excel数据（可选）
```

## 🚀 快速部署（3步完成）

### 1. 解压文件
将压缩包解压到目标目录，例如：
```bash
cd ~/Documents
unzip 仓库管理系统.zip
cd 仓库管理系统
```

### 2. 赋予脚本执行权限
```bash
chmod +x install.sh start.sh stop.sh backup.sh
```

### 3. 运行安装脚本
```bash
./install.sh
```

安装脚本会自动：
- 检查Python环境
- 创建虚拟环境
- 安装所有依赖
- 初始化数据库

### 4. 启动服务
```bash
./start.sh
```

### 5. 访问系统
在浏览器打开：http://localhost:8080

默认账号：
- 用户名：admin
- 密码：admin123

⚠️ **重要**：首次登录后请立即修改密码！

## 📋 系统要求

- macOS 10.15 (Catalina) 或更高版本
- Python 3.8 或更高版本
- 4GB 内存（推荐 8GB）
- 500MB 可用磁盘空间

## 🔧 安装Python（如果未安装）

### 方法1：使用Homebrew（推荐）
```bash
# 安装Homebrew（如果未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装Python
brew install python@3.11
```

### 方法2：官方安装包
访问 https://www.python.org/downloads/macos/ 下载并安装

## 🎯 常用操作

### 启动服务
```bash
./start.sh
```

### 停止服务
按 `Ctrl+C` 或在新终端运行：
```bash
./stop.sh
```

### 数据备份
```bash
./backup.sh
```
备份文件保存在 `backup/` 目录

### 查看日志
服务运行时会在终端显示实时日志

## 🌐 局域网访问

### 1. 获取Mac的IP地址
```bash
ifconfig en0 | grep "inet " | awk '{print $2}'
```

### 2. 配置防火墙
系统偏好设置 → 安全性与隐私 → 防火墙 → 防火墙选项
- 允许 Python 接受传入连接

### 3. 局域网访问
其他设备访问：`http://[你的IP]:8080`

## 🔐 安全建议

1. **修改默认密码** - 首次登录后立即修改
2. **定期备份** - 运行 `./backup.sh` 备份数据
3. **限制访问** - 仅在需要时开放局域网访问
4. **使用强密码** - 为所有用户设置强密码
5. **定期更新** - 保持Python和依赖包最新

## 🐛 故障排除

### 问题1：端口被占用
```bash
# 查看占用8080端口的进程
lsof -i :8080

# 停止进程
kill -9 <PID>
```

### 问题2：Python命令不存在
```bash
# 检查Python安装
which python3
python3 --version

# 如果未安装，使用Homebrew安装
brew install python@3.11
```

### 问题3：权限被拒绝
```bash
# 赋予脚本执行权限
chmod +x *.sh
```

### 问题4：依赖安装失败
```bash
# 激活虚拟环境
source venv/bin/activate

# 使用国内镜像安装
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题5：无法访问网页
- 检查服务是否正常启动
- 检查防火墙设置
- 尝试使用 127.0.0.1:8080 而不是 localhost:8080

## 📊 性能优化

### 生产环境部署
如需在生产环境使用，建议使用 Gunicorn：

```bash
# 激活虚拟环境
source venv/bin/activate

# 安装Gunicorn
pip install gunicorn

# 启动（4个工作进程）
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

### 开机自启动
创建 LaunchAgent 配置文件：

```bash
# 创建plist文件
nano ~/Library/LaunchAgents/com.warehouse.app.plist
```

内容：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.warehouse.app</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/仓库管理系统/start.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/path/to/仓库管理系统</string>
</dict>
</plist>
```

加载服务：
```bash
launchctl load ~/Library/LaunchAgents/com.warehouse.app.plist
```

## 📁 数据管理

### 数据库位置
`warehouse.db` - SQLite数据库文件

### 备份策略
- 每天运行一次 `./backup.sh`
- 备份保留30天
- 重要数据建议额外备份到云存储

### 数据恢复
```bash
# 从备份恢复
cp backup/warehouse_YYYYMMDD_HHMMSS.db warehouse.db

# 重启服务
./stop.sh
./start.sh
```

## 🔄 更新系统

### 更新依赖
```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### 更新代码
替换以下文件后重启服务：
- app.py
- database.py
- models.py
- templates/

## 📞 技术支持

遇到问题请提供：
- macOS版本：`sw_vers`
- Python版本：`python3 --version`
- 错误信息截图
- 操作步骤

## 📝 更新日志

### v1.0.0
- 初始版本
- 支持macOS部署
- 一键安装脚本
- 自动化备份

## 🙏 致谢

感谢使用仓库管理系统！
