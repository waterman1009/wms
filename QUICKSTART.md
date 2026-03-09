# 快速开始指南

## 🚀 三步启动

```bash
# 1. 安装依赖（首次使用）
./install.sh

# 2. 启动开发环境
./start.sh dev

# 3. 访问系统
# 打开浏览器访问: http://localhost:3000
```

## 📝 常用命令

| 命令 | 说明 |
|------|------|
| `./install.sh` | 安装所有依赖 |
| `./start.sh dev` | 启动开发环境 |
| `./start.sh prod` | 启动生产环境 |
| `./stop.sh` | 停止所有服务 |
| `./status.sh` | 查看运行状态 |

## 🔐 默认账号

```
用户名: admin
密码: admin123
```

## 🌐 访问地址

### 开发模式
- 前端: http://localhost:3000 ⭐ 推荐
- 后端: http://localhost:8080

### 生产模式
- 访问: http://localhost:8080

## 💡 开发建议

1. **日常开发**: 使用 `./start.sh dev`
2. **测试部署**: 使用 `./start.sh prod`
3. **遇到问题**: 运行 `./status.sh` 查看状态

## 🐛 常见问题

### 端口被占用？
```bash
./stop.sh
```

### 依赖问题？
```bash
rm -rf venv frontend/node_modules
./install.sh
```

### 查看日志？
```bash
tail -f logs/backend_*.log
tail -f logs/frontend_*.log
```

## 📚 更多文档

- [详细脚本说明](SCRIPTS.md)
- [完整 README](README.md)
- [前端开发文档](frontend/README.md)

---

**就这么简单！开始使用吧 🎉**
