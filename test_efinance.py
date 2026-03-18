#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 efinance 库在国内的可用性
作为 akshare 的备用方案
"""

print("=" * 60)
print("efinance 库可用性测试")
print("=" * 60)

# 测试 1：导入库
print("\n[测试 1] 导入库...")
try:
    from efinance import stock, fund, bond
    print("[OK] efinance 导入成功")
except Exception as e:
    print(f"[ERROR] 导入失败：{e}")
    exit(1)

# 测试 2：获取股票实时行情
print("\n[测试 2] 获取股票实时行情（贵州茅台 600519）...")
try:
    df = stock.get_realtime_data('600519')
    print(f"[OK] 获取成功，数据量：{len(df)} 条")
    print(df[['name', 'price', 'change', 'change_percent']].head())
except Exception as e:
    print(f"[ERROR] 失败：{e}")

# 测试 3：获取股票历史数据
print("\n[测试 3] 获取股票历史数据（宁德时代 300750）...")
try:
    df = stock.get_history_data('300750', start='20250101', end='20260318')
    print(f"✅ 获取成功，数据量：{len(df)} 条")
    print(df[['date', 'close', 'change']].head())
except Exception as e:
    print(f"❌ 失败：{e}")

# 测试 4：获取指数数据
print("\n[测试 4] 获取上证指数（000001）...")
try:
    df = stock.get_history_data('000001', start='20250101', end='20260318')
    print(f"✅ 获取成功，数据量：{len(df)} 条")
    print(df[['date', 'close', 'change']].head())
except Exception as e:
    print(f"❌ 失败：{e}")

# 测试 5：获取 ETF 数据
print("\n[测试 5] 获取沪深 300ETF（510300）...")
try:
    df = stock.get_history_data('510300', start='20250101', end='20260318')
    print(f"[OK] 获取成功，数据量：{len(df)} 条")
    print(df[['date', 'close', 'change']].head())
except Exception as e:
    print(f"[ERROR] 失败：{e}")

# 测试 6：获取股票列表
print("\n[测试 6] 获取 A 股股票列表...")
try:
    df = stock.get_stock_list()
    print(f"[OK] 获取成功，股票数量：{len(df)} 只")
    print(df.head())
except Exception as e:
    print(f"[ERROR] 失败：{e}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
