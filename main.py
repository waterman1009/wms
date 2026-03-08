#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仓库管理系统主程序
"""

from database import WarehouseDB
from tabulate import tabulate

def print_menu():
    """打印主菜单"""
    print("\n" + "="*50)
    print("           仓库管理系统")
    print("="*50)
    print("1. 添加新产品")
    print("2. 入库")
    print("3. 出库")
    print("4. 查看库存")
    print("5. 查看入库历史")
    print("6. 查看出库历史")
    print("7. 查看所有交易历史")
    print("0. 退出系统")
    print("="*50)

def add_product(db):
    """添加产品"""
    print("\n--- 添加新产品 ---")
    name = input("产品名称: ").strip()
    if not name:
        print("产品名称不能为空")
        return
    
    unit = input("单位 (如: 个/箱/kg): ").strip()
    if not unit:
        print("单位不能为空")
        return
    
    description = input("描述 (可选): ").strip()
    
    success, message = db.add_product(name, unit, description)
    print(message)

def stock_in(db):
    """入库操作"""
    print("\n--- 入库操作 ---")
    product_name = input("产品名称: ").strip()
    if not product_name:
        print("产品名称不能为空")
        return
    
    try:
        quantity = int(input("入库数量: "))
        if quantity <= 0:
            print("数量必须大于0")
            return
    except ValueError:
        print("请输入有效的数字")
        return
    
    operator = input("操作员: ").strip()
    if not operator:
        print("操作员不能为空")
        return
    
    note = input("备注 (可选): ").strip()
    
    success, message = db.stock_in(product_name, quantity, operator, note)
    print(message)

def stock_out(db):
    """出库操作"""
    print("\n--- 出库操作 ---")
    product_name = input("产品名称: ").strip()
    if not product_name:
        print("产品名称不能为空")
        return
    
    try:
        quantity = int(input("出库数量: "))
        if quantity <= 0:
            print("数量必须大于0")
            return
    except ValueError:
        print("请输入有效的数字")
        return
    
    operator = input("操作员: ").strip()
    if not operator:
        print("操作员不能为空")
        return
    
    note = input("备注 (可选): ").strip()
    
    success, message = db.stock_out(product_name, quantity, operator, note)
    print(message)


def view_inventory(db):
    """查看库存"""
    print("\n--- 当前库存 ---")
    products = db.get_all_products()
    
    if not products:
        print("暂无产品")
        return
    
    headers = ["产品ID", "产品名称", "库存数量", "单位", "描述"]
    print(tabulate(products, headers=headers, tablefmt="grid"))

def view_in_history(db):
    """查看入库历史"""
    print("\n--- 入库历史 ---")
    transactions = db.get_transaction_history(trans_type='IN')
    
    if not transactions:
        print("暂无入库记录")
        return
    
    headers = ["记录ID", "产品名称", "类型", "数量", "操作员", "时间", "备注"]
    print(tabulate(transactions, headers=headers, tablefmt="grid"))

def view_out_history(db):
    """查看出库历史"""
    print("\n--- 出库历史 ---")
    transactions = db.get_transaction_history(trans_type='OUT')
    
    if not transactions:
        print("暂无出库记录")
        return
    
    headers = ["记录ID", "产品名称", "类型", "数量", "操作员", "时间", "备注"]
    print(tabulate(transactions, headers=headers, tablefmt="grid"))

def view_all_history(db):
    """查看所有交易历史"""
    print("\n--- 所有交易历史 ---")
    transactions = db.get_transaction_history()
    
    if not transactions:
        print("暂无交易记录")
        return
    
    headers = ["记录ID", "产品名称", "类型", "数量", "操作员", "时间", "备注"]
    print(tabulate(transactions, headers=headers, tablefmt="grid"))

def main():
    """主函数"""
    db = WarehouseDB()
    
    while True:
        print_menu()
        choice = input("\n请选择操作 (0-7): ").strip()
        
        if choice == '1':
            add_product(db)
        elif choice == '2':
            stock_in(db)
        elif choice == '3':
            stock_out(db)
        elif choice == '4':
            view_inventory(db)
        elif choice == '5':
            view_in_history(db)
        elif choice == '6':
            view_out_history(db)
        elif choice == '7':
            view_all_history(db)
        elif choice == '0':
            print("\n感谢使用仓库管理系统，再见！")
            break
        else:
            print("\n无效的选择，请重新输入")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()
