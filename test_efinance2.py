#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 efinance 库 - 正确的 API
"""

print("=" * 60)
print("efinance 库测试 - 正确 API")
print("=" * 60)

# 导入
from efinance import stock
import pandas as pd

# 测试 1：获取股票实时行情
print("\n[测试 1] 贵州茅台实时行情...")
try:
    # 使用正确的 API
    quote = stock.quote('600519')
    print(f"[OK] 获取成功")
    print(quote)
except Exception as e:
    print(f"[ERROR] 失败：{e}")

# 测试 2：获取股票历史数据
print("\n[测试 2] 贵州茅台历史数据...")
try:
    df = stock.get_quote_history('600519', beg='20250101', end='20260318')
    print(f"[OK] 获取成功，数据量：{len(df)} 条")
    print(df[['日期', '收盘价', '涨跌幅']].head())
except Exception as e:
    print(f"[ERROR] 失败：{e}")

# 测试 3：获取股票信息
print("\n[测试 3] 获取股票信息...")
try:
    info = stock.get_stock_info('600519')
    print(f"[OK] 获取成功")
    print(f"股票名称：{info.get('股票名称', 'N/A')}")
    print(f"行业：{info.get('行业', 'N/A')}")
except Exception as e:
    print(f"[ERROR] 失败：{e}")

# 测试 4：获取所有 A 股列表
print("\n[测试 4] 获取 A 股列表...")
try:
    df = stock.get_all_a_stock()
    print(f"[OK] 获取成功，股票数量：{len(df)} 只")
    print(df.head())
except Exception as e:
    print(f"[ERROR] 失败：{e}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
