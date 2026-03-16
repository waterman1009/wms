# 库存总和显示功能

## 功能说明

在库存列表页面的表格底部显示所有库存的总和（不仅仅是当前页）。

## 实现内容

### 后端更新

1. **数据库方法**
   - 在 `database.py` 中添加了 `get_total_quantity()` 方法
   - 支持按产品类型筛选（配件/成品）
   - 支持按搜索关键词筛选
   - 使用 SQL 的 `SUM()` 函数高效计算

2. **API接口**
   - 修改 `/api/products` 接口
   - 在返回数据中添加 `total_quantity` 字段
   - 根据筛选条件返回对应的库存总和

### 前端更新

1. **表格汇总行**
   - 在表格底部添加了 `summary` 插槽
   - 使用 Ant Design Vue 的 `a-table-summary` 组件
   - 显示"库存总和"标签和总数量

2. **数据获取**
   - 从后端API获取 `total_quantity` 数据
   - 存储在 `totalQuantity` ref 变量中
   - 每次加载数据时自动更新

3. **样式优化**
   - 汇总行使用浅灰色背景 (#fafafa)
   - 顶部添加2px边框以区分数据行
   - 数量使用蓝色高亮显示 (#1890ff)
   - 字体加粗，字号16px

## 显示效果

```
┌─────┬──────────┬──────┬────────┬──────┬──────┬────────┐
│ ID  │ 产品名称 │ 类型 │  库存  │ 单位 │ 描述 │  操作  │
├─────┼──────────┼──────┼────────┼──────┼──────┼────────┤
│ 1   │ 配件A    │ 配件 │   100  │  个  │  -   │ [操作] │
│ 2   │ 配件B    │ 配件 │   200  │  个  │  -   │ [操作] │
│ 3   │ 成品C    │ 成品 │    50  │  个  │  -   │ [操作] │
├─────┴──────────┴──────┴────────┴──────┴──────┴────────┤
│ 第 1-3 条，共 150 条                                   │
╞═════════════════════════════════════════════════════════╡
│     库存总和                │  5,280  │                │
└─────────────────────────────┴─────────┴────────────────┘
```

## 特性

- ✓ 显示所有库存的总和（不受分页限制）
- ✓ 支持筛选（配件/成品），显示筛选后的总和
- ✓ 支持搜索，显示搜索结果的总和
- ✓ 数据为空时不显示汇总行
- ✓ 后端计算，性能优异
- ✓ 响应式设计，适配移动端

## 使用场景

1. **查看总库存**
   - 无论有多少页数据，都能看到总库存量
   - 快速了解整体库存情况

2. **分类统计**
   - 点击"配件"按钮，查看所有配件的总库存
   - 点击"成品"按钮，查看所有成品的总库存

3. **搜索结果统计**
   - 搜索特定产品后，查看匹配结果的总库存
   - 例如：搜索"F12"，显示所有F12系列产品的总库存

## 技术实现

### 数据库方法
```python
def get_total_quantity(self, product_type=None, search=None):
    """获取库存总和（支持筛选和搜索）"""
    conn = self.get_connection()
    cursor = conn.cursor()
    
    # 构建查询条件
    conditions = []
    params = []
    
    if product_type:
        conditions.append('product_type = ?')
        params.append(product_type)
    
    if search:
        conditions.append('name LIKE ?')
        params.append(f'%{search}%')
    
    where_clause = ' AND '.join(conditions) if conditions else '1=1'
    
    # 查询库存总和
    query = f'SELECT COALESCE(SUM(quantity), 0) FROM products WHERE {where_clause}'
    cursor.execute(query, params)
    total_quantity = cursor.fetchone()[0]
    conn.close()
    
    return total_quantity
```

### API接口
```python
@app.route('/api/products', methods=['GET'])
@login_required
def get_products():
    # ... 获取产品列表 ...
    
    # 获取库存总和
    total_quantity = db.get_total_quantity(
        product_type=product_type,
        search=search
    )
    
    return jsonify({
        'success': True,
        'data': [...],
        'pagination': {...},
        'total_quantity': total_quantity  # 新增字段
    })
```

### 前端代码
```javascript
const totalQuantity = ref(0)  // 所有库存总和

const loadInventory = async (type, page = 1, pageSize = 20) => {
  // ...
  const { data } = await api.getProducts(params)
  products.value = data.data
  pagination.value = data.pagination
  totalQuantity.value = data.total_quantity || 0  // 获取库存总和
}
```

## 注意事项

1. **全局统计**
   - 显示的是所有符合条件的产品库存总和
   - 不受分页影响，始终显示完整统计

2. **筛选和搜索**
   - 筛选配件/成品时，只统计对应类型的库存
   - 搜索时，只统计匹配的产品库存

3. **性能优化**
   - 使用数据库的 SUM() 函数，性能优异
   - 即使有数万条产品，也能快速计算

4. **数据准确性**
   - 每次加载数据时重新计算
   - 与数据库实时同步

## 测试方法

1. 访问 http://localhost:3000
2. 登录系统
3. 进入"当前库存"页面
4. 查看表格底部的"库存总和"
5. 测试不同场景：
   - 切换分页（总和不变）
   - 筛选配件/成品（总和变化）
   - 搜索产品（总和变化）
   - 修改库存数量（总和更新）

## 更新日期

2026-03-16

