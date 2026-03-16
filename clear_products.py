#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理数据库中的所有产品和配件数据
"""

import sqlite3
from datetime import datetime

def clear_products(db_name="warehouse.db"):
    """清空所有产品和配件数据（保留用户和客户数据）"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("仓库管理系统 - 数据清理工具")
    print("=" * 60)
    print()
    
    # 获取当前数据统计
    cursor.execute('SELECT COUNT(*) FROM products WHERE product_type = "COMPONENT"')
    component_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM products WHERE product_type = "FINISHED"')
    finished_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM product_components')
    relation_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM transactions')
    transaction_count = cursor.fetchone()[0]
    
    print("当前数据统计:")
    print(f"  配件数量: {component_count}")
    print(f"  成品数量: {finished_count}")
    print(f"  配件关系: {relation_count}")
    print(f"  交易记录: {transaction_count}")
    print()
    
    if component_count == 0 and finished_count == 0 and transaction_count == 0:
        print("✓ 数据库已经是空的，无需清理")
        conn.close()
        return
    
    # 确认清理
    print("⚠️  警告: 此操作将清空以下数据:")
    print("  - 所有产品（配件和成品）")
    print("  - 所有配件关系")
    print("  - 所有交易记录（入库、出库、发货等）")
    print()
    print("✓ 保留的数据:")
    print("  - 用户账号")
    print("  - 客户信息")
    print()
    
    confirm = input("确定要清空数据吗？(输入 yes 确认): ")
    
    if confirm.lower() != 'yes':
        print("\n❌ 操作已取消")
        conn.close()
        return
    
    print("\n正在清理数据...")
    
    try:
        # 清空交易记录
        cursor.execute('DELETE FROM transactions')
        print("✓ 清空交易记录")
        
        # 清空配件关系
        cursor.execute('DELETE FROM product_components')
        print("✓ 清空配件关系")
        
        # 清空产品
        cursor.execute('DELETE FROM products')
        print("✓ 清空产品数据")
        
        # 重置自增ID
        cursor.execute('DELETE FROM sqlite_sequence WHERE name IN ("products", "product_components", "transactions")')
        print("✓ 重置自增ID")
        
        conn.commit()
        
        print()
        print("=" * 60)
        print("✅ 数据清理完成！")
        print("=" * 60)
        print()
        print("现在可以:")
        print("  1. 通过Excel导入新的产品数据")
        print("  2. 手动添加产品")
        print()
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ 清理失败: {e}")
    finally:
        conn.close()

def main():
    """主函数"""
    clear_products()

if __name__ == '__main__':
    main()
