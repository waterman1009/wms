from datetime import datetime

class Product:
    """产品模型"""
    def __init__(self, product_id, name, quantity, unit, description=""):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.description = description

class Transaction:
    """交易记录模型"""
    def __init__(self, trans_id, product_id, product_name, trans_type, quantity, 
                 operator, trans_date, note=""):
        self.trans_id = trans_id
        self.product_id = product_id
        self.product_name = product_name
        self.trans_type = trans_type  # 'IN' 或 'OUT'
        self.quantity = quantity
        self.operator = operator
        self.trans_date = trans_date
        self.note = note
