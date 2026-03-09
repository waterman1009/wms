# 仓库管理系统 - Vue 前端

这是使用 Vue 3 + Vite 重构的仓库管理系统前端。

## 项目结构

```
frontend/
├── index.html              # HTML 入口
├── package.json            # 依赖配置
├── vite.config.js          # Vite 配置
└── src/
    ├── main.js             # 应用入口
    ├── App.vue             # 根组件
    ├── api/
    │   └── index.js        # API 接口封装
    ├── assets/
    │   └── styles.css      # 全局样式
    ├── components/         # 可复用组件
    │   ├── AutocompleteInput.vue
    │   ├── CustomerModal.vue
    │   ├── EditProductModal.vue
    │   ├── MessageAlert.vue
    │   ├── ShipmentConfirmModal.vue
    │   ├── Sidebar.vue
    │   └── TopHeader.vue
    ├── layouts/            # 布局组件
    │   └── MainLayout.vue
    ├── router/             # 路由配置
    │   └── index.js
    └── views/              # 页面组件
        ├── AddProductView.vue
        ├── CustomersView.vue
        ├── DefectsView.vue
        ├── HistoryView.vue
        ├── InventoryView.vue
        ├── LoginView.vue
        ├── ShipmentRecordsView.vue
        ├── ShipmentView.vue
        ├── StockInView.vue
        ├── StockOutView.vue
        └── UsersView.vue
```

## 功能模块

### 核心功能
- **登录认证** - 用户登录和权限管理
- **库存管理** - 产品查询、添加、编辑、删除
- **出入库管理** - 配件入库、生产出库、配件损耗
- **销售管理** - 成品发货、发货记录查询
- **统计查询** - 交易历史查询和导出
- **系统管理** - 客户管理、用户管理（管理员）

### 技术特点
- Vue 3 Composition API
- Vue Router 4 路由管理
- Axios HTTP 请求
- 组件化开发
- 响应式设计

## 安装和运行

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 开发模式

```bash
npm run dev
```

访问 http://localhost:3000

### 3. 生产构建

```bash
npm run build
```

构建产物会输出到 `../static` 目录，可直接被 Flask 后端使用。

## 后端集成

### 修改 Flask 后端

需要修改 `app.py` 以支持 Vue 前端：

```python
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
@app.route('/<path:path>')
def serve_spa(path=''):
    """服务 Vue SPA"""
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')
```

### 开发流程

1. **开发阶段**：
   - 后端运行在 `http://localhost:8080`
   - 前端运行在 `http://localhost:3000`
   - Vite 自动代理 `/api` 请求到后端

2. **生产部署**：
   - 运行 `npm run build` 构建前端
   - 构建产物自动输出到 `static/` 目录
   - 只需运行 Flask 后端，访问 `http://localhost:8080`

## API 接口

所有 API 接口都在 `src/api/index.js` 中定义，包括：

- 用户认证：login, logout, getCurrentUser
- 产品管理：getProducts, addProduct, updateProduct, deleteProduct
- 库存操作：stockIn, stockOut, recordDefects
- 发货管理：createShipment, getShipments
- 交易历史：getTransactions, cancelTransaction
- 客户管理：getCustomers, addCustomer, updateCustomer, deleteCustomer
- 用户管理：getUsers, addUser, deleteUser

## 组件说明

### 布局组件
- **MainLayout** - 主布局，包含顶部导航和侧边栏
- **TopHeader** - 顶部导航栏
- **Sidebar** - 左侧导航菜单

### 通用组件
- **MessageAlert** - 消息提示组件
- **AutocompleteInput** - 自动完成输入框
- **EditProductModal** - 产品编辑弹窗
- **CustomerModal** - 客户编辑弹窗
- **ShipmentConfirmModal** - 发货确认弹窗

### 页面组件
每个页面组件对应一个功能模块，采用 Composition API 编写。

## 注意事项

1. 确保后端 API 运行在 `http://localhost:8080`
2. 开发时前后端分离，生产时前端构建到 static 目录
3. 所有 API 请求都会自动处理 401 跳转到登录页
4. 管理员功能需要 ADMIN 或 MANAGER 角色权限

## 浏览器支持

- Chrome (推荐)
- Firefox
- Safari
- Edge

## 许可证

MIT
