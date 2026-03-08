import sqlite3
from datetime import datetime
from models import Product, Transaction

class WarehouseDB:
    """仓库数据库管理类"""
    
    def __init__(self, db_name="warehouse.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """初始化数据库表"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 创建用户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                real_name TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建默认管理员账号（密码：admin123）
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                'INSERT INTO users (username, password, real_name, role) VALUES (?, ?, ?, ?)',
                ('admin', 'admin123', '系统管理员', 'ADMIN')
            )
        
        # 创建产品表 (增加产品类型字段)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                product_type TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                unit TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建成品配件关系表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_components (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                finished_product_id INTEGER NOT NULL,
                component_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (finished_product_id) REFERENCES products (product_id),
                FOREIGN KEY (component_id) REFERENCES products (product_id)
            )
        ''')
        
        # 创建交易记录表 (增加分配人员、次品数量和客户名称字段)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                trans_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                trans_type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                operator TEXT NOT NULL,
                assigned_to TEXT,
                customer_name TEXT,
                defect_quantity INTEGER DEFAULT 0,
                trans_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                note TEXT,
                FOREIGN KEY (product_id) REFERENCES products (product_id)
            )
        ''')
        
        # 检查是否需要添加customer_name字段（兼容旧数据库）
        cursor.execute("PRAGMA table_info(transactions)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'customer_name' not in columns:
            cursor.execute('ALTER TABLE transactions ADD COLUMN customer_name TEXT')
        
        # 创建客户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                contact_person TEXT,
                phone TEXT,
                address TEXT,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_product(self, name, product_type, unit, description=""):
        """添加新产品"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO products (name, product_type, quantity, unit, description) VALUES (?, ?, ?, ?, ?)',
                (name, product_type, 0, unit, description)
            )
            conn.commit()
            product_id = cursor.lastrowid
            conn.close()
            return True, "产品添加成功", product_id
        except sqlite3.IntegrityError:
            conn.close()
            return False, "产品名称已存在", None
    
    def add_product_component(self, finished_product_id, component_id, quantity):
        """添加成品配件关系"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO product_components (finished_product_id, component_id, quantity) VALUES (?, ?, ?)',
                (finished_product_id, component_id, quantity)
            )
            conn.commit()
            conn.close()
            return True, "配件关系添加成功"
        except Exception as e:
            conn.close()
            return False, f"添加失败: {str(e)}"
    
    def get_product_components(self, finished_product_id):
        """获取成品所需的配件列表"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.product_id, p.name, pc.quantity, p.quantity as stock
            FROM product_components pc
            JOIN products p ON pc.component_id = p.product_id
            WHERE pc.finished_product_id = ?
        ''', (finished_product_id,))
        components = cursor.fetchall()
        conn.close()
        return components
    
    def stock_in(self, product_name, quantity, operator, note=""):
        """入库操作 (仅配件)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT product_id, quantity, product_type FROM products WHERE name = ?', (product_name,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False, "产品不存在"
        
        product_id, current_quantity, product_type = result
        
        if product_type != 'COMPONENT':
            conn.close()
            return False, "只能对配件进行入库操作"
        
        new_quantity = current_quantity + quantity
        
        cursor.execute('UPDATE products SET quantity = ?, updated_at = ? WHERE product_id = ?',
                      (new_quantity, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), product_id))
        
        cursor.execute(
            'INSERT INTO transactions (product_id, product_name, trans_type, quantity, operator, trans_date, note) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (product_id, product_name, 'IN', quantity, operator, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), note)
        )
        
        conn.commit()
        conn.close()
        return True, f"入库成功，当前库存：{new_quantity}"
    
    def stock_out_batch(self, product_name, assignments, operator, note=""):
        """配件出库（生产成品）- 支持多人员分配，自动完成生产"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT product_id, quantity, product_type FROM products WHERE name = ?', (product_name,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False, "产品不存在"
        
        product_id, current_quantity, product_type = result
        
        if product_type != 'FINISHED':
            conn.close()
            return False, "只能选择成品进行生产"
        
        # 获取成品所需配件
        components = self.get_product_components(product_id)
        
        if not components:
            conn.close()
            return False, "该成品未配置配件关系"
        
        # 计算总生产数量
        total_quantity = sum(a['quantity'] for a in assignments)
        
        # 检查配件库存是否充足
        for comp_id, comp_name, required_qty, stock in components:
            needed = required_qty * total_quantity
            if stock < needed:
                conn.close()
                return False, f"配件 {comp_name} 库存不足，需要 {needed}，当前库存 {stock}"
        
        # 扣减配件库存
        for comp_id, comp_name, required_qty, stock in components:
            needed = required_qty * total_quantity
            new_stock = stock - needed
            cursor.execute('UPDATE products SET quantity = ?, updated_at = ? WHERE product_id = ?',
                          (new_stock, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), comp_id))
            
            # 记录配件出库
            cursor.execute(
                'INSERT INTO transactions (product_id, product_name, trans_type, quantity, operator, trans_date, note) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (comp_id, comp_name, 'OUT', needed, operator, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), f"生产成品: {product_name} x{total_quantity}")
            )
        
        # 为每个人员创建生产记录并直接完成生产
        for assignment in assignments:
            assigned_to = assignment['assigned_to']
            quantity = assignment['quantity']
            
            # 记录生产任务
            cursor.execute(
                'INSERT INTO transactions (product_id, product_name, trans_type, quantity, operator, assigned_to, trans_date, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (product_id, product_name, 'PRODUCTION', quantity, operator, assigned_to, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), note)
            )
            
            # 直接完成生产，成品入库
            cursor.execute('SELECT quantity FROM products WHERE product_id = ?', (product_id,))
            current_stock = cursor.fetchone()[0]
            new_stock = current_stock + quantity
            
            cursor.execute('UPDATE products SET quantity = ?, updated_at = ? WHERE product_id = ?',
                          (new_stock, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), product_id))
            
            # 记录成品入库
            cursor.execute(
                'INSERT INTO transactions (product_id, product_name, trans_type, quantity, operator, assigned_to, trans_date, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (product_id, product_name, 'IN', quantity, operator, assigned_to, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), f"生产完成入库")
            )
        
        conn.commit()
        conn.close()
        
        assignment_summary = ', '.join([f"{a['assigned_to']}({a['quantity']}个)" for a in assignments])
        return True, f"生产完成！配件已出库，成品已入库。分配：{assignment_summary}"
    
    def complete_production(self, trans_id, operator):
        """完成生产，成品全部入库"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 获取生产记录
        cursor.execute('SELECT product_id, product_name, quantity FROM transactions WHERE trans_id = ? AND trans_type = ?',
                      (trans_id, 'PRODUCTION'))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False, "生产记录不存在"
        
        product_id, product_name, production_quantity = result
        
        # 成品全部入库
        cursor.execute('SELECT quantity FROM products WHERE product_id = ?', (product_id,))
        current_stock = cursor.fetchone()[0]
        new_stock = current_stock + production_quantity
        
        cursor.execute('UPDATE products SET quantity = ?, updated_at = ? WHERE product_id = ?',
                      (new_stock, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), product_id))
        
        # 记录成品入库
        cursor.execute(
            'INSERT INTO transactions (product_id, product_name, trans_type, quantity, operator, trans_date, note) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (product_id, product_name, 'IN', production_quantity, operator, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), f"生产完成入库")
        )
        
        conn.commit()
        conn.close()
        
        return True, f"生产完成！成品 {production_quantity} 个已全部入库"
    
    def record_component_defect_batch(self, defects, operator, note=""):
        """批量记录配件损耗/次品"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        results = []
        
        for defect in defects:
            component_name = defect['component_name']
            defect_quantity = defect['quantity']
            
            cursor.execute('SELECT product_id, quantity, product_type FROM products WHERE name = ?', (component_name,))
            result = cursor.fetchone()
            
            if not result:
                conn.rollback()
                conn.close()
                return False, f"配件 {component_name} 不存在"
            
            product_id, current_quantity, product_type = result
            
            if product_type != 'COMPONENT':
                conn.rollback()
                conn.close()
                return False, f"{component_name} 不是配件，只能对配件记录损耗"
            
            if current_quantity < defect_quantity:
                conn.rollback()
                conn.close()
                return False, f"配件 {component_name} 库存不足，当前库存 {current_quantity}，损耗数量 {defect_quantity}"
            
            new_quantity = current_quantity - defect_quantity
            
            cursor.execute('UPDATE products SET quantity = ?, updated_at = ? WHERE product_id = ?',
                          (new_quantity, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), product_id))
            
            cursor.execute(
                'INSERT INTO transactions (product_id, product_name, trans_type, quantity, operator, trans_date, note) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (product_id, component_name, 'DEFECT', defect_quantity, operator, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), note or "配件损耗")
            )
            
            results.append(f"{component_name} 扣减 {defect_quantity}")
        
        conn.commit()
        conn.close()
        
        summary = '，'.join(results)
        return True, f"配件损耗记录成功：{summary}"
    
    def get_all_products(self, product_type=None, search=None, page=1, per_page=20):
        """查询所有产品库存（支持搜索和分页）"""
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
        
        # 查询总数
        count_query = f'SELECT COUNT(*) FROM products WHERE {where_clause}'
        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]
        
        # 查询数据（分页）
        offset = (page - 1) * per_page
        data_query = f'SELECT product_id, name, product_type, quantity, unit, description FROM products WHERE {where_clause} ORDER BY product_type, name LIMIT ? OFFSET ?'
        cursor.execute(data_query, params + [per_page, offset])
        
        products = cursor.fetchall()
        conn.close()
        
        return products, total
    
    def get_transaction_history(self, product_name=None, trans_type=None, start_date=None, end_date=None, limit=50):
        """查询交易历史
        
        Args:
            product_name: 产品名称
            trans_type: 交易类型
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            limit: 返回记录数限制
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT trans_id, product_name, trans_type, quantity, operator, assigned_to, defect_quantity, trans_date, note FROM transactions WHERE 1=1'
        params = []
        
        if product_name:
            query += ' AND product_name = ?'
            params.append(product_name)
        
        if trans_type:
            query += ' AND trans_type = ?'
            params.append(trans_type)
        
        if start_date:
            query += ' AND date(trans_date) >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND date(trans_date) <= ?'
            params.append(end_date)
        
        query += ' ORDER BY trans_date DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        transactions = cursor.fetchall()
        conn.close()
        return transactions

    
    def update_product(self, product_id, name, unit, description, quantity=None):
        """更新产品信息"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if quantity is not None:
                cursor.execute(
                    'UPDATE products SET name = ?, unit = ?, description = ?, quantity = ?, updated_at = ? WHERE product_id = ?',
                    (name, unit, description, quantity, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), product_id)
                )
            else:
                cursor.execute(
                    'UPDATE products SET name = ?, unit = ?, description = ?, updated_at = ? WHERE product_id = ?',
                    (name, unit, description, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), product_id)
                )
            conn.commit()
            conn.close()
            return True, "产品更新成功"
        except sqlite3.IntegrityError:
            conn.close()
            return False, "产品名称已存在"
    
    def delete_product(self, product_id):
        """删除产品"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 检查是否有交易记录
        cursor.execute('SELECT COUNT(*) FROM transactions WHERE product_id = ?', (product_id,))
        trans_count = cursor.fetchone()[0]
        
        if trans_count > 0:
            conn.close()
            return False, "该产品有交易记录，无法删除"
        
        # 检查是否被成品引用
        cursor.execute('SELECT COUNT(*) FROM product_components WHERE component_id = ? OR finished_product_id = ?', 
                      (product_id, product_id))
        comp_count = cursor.fetchone()[0]
        
        if comp_count > 0:
            conn.close()
            return False, "该产品被其他产品引用，无法删除"
        
        cursor.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
        conn.commit()
        conn.close()
        return True, "产品删除成功"
    
    def get_product_by_id(self, product_id):
        """根据ID获取产品信息"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT product_id, name, product_type, quantity, unit, description FROM products WHERE product_id = ?',
                      (product_id,))
        product = cursor.fetchone()
        conn.close()
        return product
    
    def delete_product_components(self, finished_product_id):
        """删除成品的配件关系"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM product_components WHERE finished_product_id = ?', (finished_product_id,))
        conn.commit()
        conn.close()

    
    # 用户管理相关方法
    def login(self, username, password):
        """用户登录"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, username, real_name, role FROM users WHERE username = ? AND password = ?',
                      (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return True, {
                'user_id': user[0],
                'username': user[1],
                'real_name': user[2],
                'role': user[3]
            }
        return False, None
    
    def add_user(self, username, password, real_name, role):
        """添加用户"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (username, password, real_name, role) VALUES (?, ?, ?, ?)',
                (username, password, real_name, role)
            )
            conn.commit()
            conn.close()
            return True, "用户添加成功"
        except sqlite3.IntegrityError:
            conn.close()
            return False, "用户名已存在"
    
    def get_all_users(self, role=None):
        """获取所有用户"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if role:
            cursor.execute('SELECT user_id, username, real_name, role, created_at FROM users WHERE role = ? ORDER BY created_at DESC',
                          (role,))
        else:
            cursor.execute('SELECT user_id, username, real_name, role, created_at FROM users ORDER BY created_at DESC')
        
        users = cursor.fetchall()
        conn.close()
        return users
    
    def update_user(self, user_id, real_name, password=None):
        """更新用户信息"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if password:
            cursor.execute('UPDATE users SET real_name = ?, password = ?, updated_at = ? WHERE user_id = ?',
                          (real_name, password, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        else:
            cursor.execute('UPDATE users SET real_name = ?, updated_at = ? WHERE user_id = ?',
                          (real_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        
        conn.commit()
        conn.close()
        return True, "用户信息更新成功"
    
    def delete_user(self, user_id):
        """删除用户"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 不能删除admin用户
        cursor.execute('SELECT username FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        if result and result[0] == 'admin':
            conn.close()
            return False, "不能删除系统管理员账号"
        
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        return True, "用户删除成功"

    def ship_products(self, shipments, customer_name, operator, note=""):
        """成品发货 - 支持多个成品批量发货
        
        Args:
            shipments: 发货列表 [{'product_name': '成品A', 'quantity': 10}, ...]
            customer_name: 客户名称
            operator: 操作员
            note: 备注
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            for shipment in shipments:
                product_name = shipment['product_name']
                quantity = shipment['quantity']
                
                # 获取产品信息
                cursor.execute('SELECT product_id, quantity, product_type FROM products WHERE name = ?', (product_name,))
                result = cursor.fetchone()
                
                if not result:
                    conn.rollback()
                    conn.close()
                    return False, f"产品 {product_name} 不存在"
                
                product_id, current_quantity, product_type = result
                
                # 只能发货成品
                if product_type != 'FINISHED':
                    conn.rollback()
                    conn.close()
                    return False, f"{product_name} 不是成品，只能发货成品"
                
                # 检查库存
                if current_quantity < quantity:
                    conn.rollback()
                    conn.close()
                    return False, f"成品 {product_name} 库存不足，当前库存 {current_quantity}，发货数量 {quantity}"
                
                # 扣减库存
                new_quantity = current_quantity - quantity
                cursor.execute('UPDATE products SET quantity = ?, updated_at = ? WHERE product_id = ?',
                              (new_quantity, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), product_id))
                
                # 记录发货交易
                cursor.execute(
                    'INSERT INTO transactions (product_id, product_name, trans_type, quantity, operator, customer_name, trans_date, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (product_id, product_name, 'SHIPMENT', quantity, operator, customer_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), note)
                )
            
            conn.commit()
            conn.close()
            
            shipment_summary = ', '.join([f"{s['product_name']}({s['quantity']}个)" for s in shipments])
            return True, f"发货成功！客户：{customer_name}，发货：{shipment_summary}"
            
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, f"发货失败: {str(e)}"
    
    def get_shipment_history(self, customer_name=None, start_date=None, end_date=None, limit=100):
        """获取发货历史记录
        
        Args:
            customer_name: 客户名称
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            limit: 返回记录数限制
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''SELECT trans_id, product_name, quantity, operator, customer_name, trans_date, note 
                   FROM transactions 
                   WHERE trans_type = ?'''
        params = ['SHIPMENT']
        
        if customer_name:
            query += ' AND customer_name = ?'
            params.append(customer_name)
        
        if start_date:
            query += ' AND date(trans_date) >= date(?)'
            params.append(start_date)
        
        if end_date:
            query += ' AND date(trans_date) <= date(?)'
            params.append(end_date)
        
        query += ' ORDER BY trans_date DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        shipments = cursor.fetchall()
        conn.close()
        return shipments

    def cancel_transaction(self, trans_id, operator):
        """取消交易记录并恢复库存
        
        Args:
            trans_id: 交易记录ID
            operator: 操作员
        
        Returns:
            (success, message)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # 获取交易记录
            cursor.execute('''
                SELECT product_id, product_name, trans_type, quantity, assigned_to, customer_name
                FROM transactions 
                WHERE trans_id = ?
            ''', (trans_id,))
            
            result = cursor.fetchone()
            if not result:
                conn.close()
                return False, "交易记录不存在"
            
            product_id, product_name, trans_type, quantity, assigned_to, customer_name = result
            
            # 获取产品当前库存
            cursor.execute('SELECT quantity, product_type FROM products WHERE product_id = ?', (product_id,))
            product_result = cursor.fetchone()
            
            if not product_result:
                conn.close()
                return False, f"产品 {product_name} 不存在"
            
            current_quantity, product_type = product_result
            
            # 根据交易类型恢复库存
            if trans_type == 'IN':
                # 取消入库：扣减库存
                new_quantity = current_quantity - quantity
                if new_quantity < 0:
                    conn.close()
                    return False, f"无法取消入库，当前库存 {current_quantity} 不足以扣减 {quantity}"
                action_desc = f"取消入库，扣减库存 {quantity}"
                
            elif trans_type == 'OUT':
                # 取消配件出库：恢复配件库存
                new_quantity = current_quantity + quantity
                action_desc = f"取消配件出库，恢复库存 {quantity}"
                
            elif trans_type == 'PRODUCTION':
                # 取消生产：扣减成品库存，恢复配件库存
                # 1. 扣减成品库存
                new_quantity = current_quantity - quantity
                if new_quantity < 0:
                    conn.close()
                    return False, f"无法取消生产，成品库存 {current_quantity} 不足以扣减 {quantity}"
                
                # 2. 恢复配件库存
                components = self.get_product_components(product_id)
                for comp_id, comp_name, required_qty, stock in components:
                    needed = required_qty * quantity
                    new_comp_stock = stock + needed
                    cursor.execute('UPDATE products SET quantity = ?, updated_at = ? WHERE product_id = ?',
                                  (new_comp_stock, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), comp_id))
                
                action_desc = f"取消生产，扣减成品 {quantity}，恢复配件库存"
                
            elif trans_type == 'SHIPMENT':
                # 取消发货：恢复成品库存
                new_quantity = current_quantity + quantity
                action_desc = f"取消发货给 {customer_name}，恢复库存 {quantity}"
                
            elif trans_type == 'DEFECT':
                # 取消次品记录：恢复配件库存
                new_quantity = current_quantity + quantity
                action_desc = f"取消次品记录，恢复库存 {quantity}"
                
            else:
                conn.close()
                return False, f"不支持取消的交易类型: {trans_type}"
            
            # 更新产品库存
            cursor.execute('UPDATE products SET quantity = ?, updated_at = ? WHERE product_id = ?',
                          (new_quantity, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), product_id))
            
            # 删除原交易记录
            cursor.execute('DELETE FROM transactions WHERE trans_id = ?', (trans_id,))
            
            # 记录取消操作（作为新的交易记录）
            cancel_note = f"取消交易#{trans_id}: {action_desc}"
            cursor.execute(
                'INSERT INTO transactions (product_id, product_name, trans_type, quantity, operator, trans_date, note) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (product_id, product_name, 'CANCEL', 0, operator, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), cancel_note)
            )
            
            conn.commit()
            conn.close()
            
            return True, f"交易记录已取消。{action_desc}"
            
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, f"取消失败: {str(e)}"
    
    # 客户管理相关方法
    def add_customer(self, name, contact_person="", phone="", address="", note=""):
        """添加客户"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO customers (name, contact_person, phone, address, note) VALUES (?, ?, ?, ?, ?)',
                (name, contact_person, phone, address, note)
            )
            conn.commit()
            customer_id = cursor.lastrowid
            conn.close()
            return True, "客户添加成功", customer_id
        except sqlite3.IntegrityError:
            conn.close()
            return False, "客户名称已存在", None
    
    def get_all_customers(self, search=None):
        """获取所有客户"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if search:
            cursor.execute('''
                SELECT customer_id, name, contact_person, phone, address, note, created_at 
                FROM customers 
                WHERE name LIKE ? OR contact_person LIKE ? OR phone LIKE ?
                ORDER BY name
            ''', (f'%{search}%', f'%{search}%', f'%{search}%'))
        else:
            cursor.execute('''
                SELECT customer_id, name, contact_person, phone, address, note, created_at 
                FROM customers 
                ORDER BY name
            ''')
        
        customers = cursor.fetchall()
        conn.close()
        return customers
    
    def get_customer_by_id(self, customer_id):
        """根据ID获取客户信息"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT customer_id, name, contact_person, phone, address, note 
            FROM customers 
            WHERE customer_id = ?
        ''', (customer_id,))
        customer = cursor.fetchone()
        conn.close()
        return customer
    
    def update_customer(self, customer_id, name, contact_person, phone, address, note):
        """更新客户信息"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE customers 
                SET name = ?, contact_person = ?, phone = ?, address = ?, note = ?, updated_at = ? 
                WHERE customer_id = ?
            ''', (name, contact_person, phone, address, note, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), customer_id))
            conn.commit()
            conn.close()
            return True, "客户信息更新成功"
        except sqlite3.IntegrityError:
            conn.close()
            return False, "客户名称已存在"
    
    def delete_customer(self, customer_id):
        """删除客户"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 检查是否有发货记录
        cursor.execute('SELECT name FROM customers WHERE customer_id = ?', (customer_id,))
        result = cursor.fetchone()
        if not result:
            conn.close()
            return False, "客户不存在"
        
        customer_name = result[0]
        cursor.execute('SELECT COUNT(*) FROM transactions WHERE customer_name = ? AND trans_type = ?', 
                      (customer_name, 'SHIPMENT'))
        shipment_count = cursor.fetchone()[0]
        
        if shipment_count > 0:
            conn.close()
            return False, "该客户有发货记录，无法删除"
        
        cursor.execute('DELETE FROM customers WHERE customer_id = ?', (customer_id,))
        conn.commit()
        conn.close()
        return True, "客户删除成功"
