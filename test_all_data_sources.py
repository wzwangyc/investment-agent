#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A 股数据库对比测试
测试 5 个主流金融数据库的可用性和数据准确度
"""

import pandas as pd
from datetime import datetime

print("=" * 80)
print("A 股数据库对比测试 - 5 大主流库")
print("=" * 80)

# 测试参数
STOCK_CODE = '600519'  # 贵州茅台
START_DATE = '20260101'
END_DATE = '20260318'

results = {}

# ==================== 1. AkShare ====================
print("\n" + "=" * 80)
print("[1/5] 测试 AkShare")
print("=" * 80)

try:
    import akshare as ak
    
    df_ak = ak.stock_zh_a_hist(
        symbol=STOCK_CODE,
        period="daily",
        start_date=START_DATE,
        end_date=END_DATE,
        adjust="qfq"
    )
    
    print(f"[OK] AkShare 获取成功")
    print(f"数据量：{len(df_ak)} 条")
    print(f"列名：{df_ak.columns.tolist()}")
    print(f"最新收盘价：{df_ak.iloc[-1]['收盘']}")
    
    results['akshare'] = {
        'status': 'OK',
        'count': len(df_ak),
        'close': df_ak.iloc[-1]['收盘']
    }
except Exception as e:
    print(f"[ERROR] AkShare 失败：{e}")
    results['akshare'] = {'status': 'ERROR', 'error': str(e)}

# ==================== 2. eFinance ====================
print("\n" + "=" * 80)
print("[2/5] 测试 eFinance")
print("=" * 80)

try:
    from efinance import stock
    
    df_ef = stock.get_quote_history(
        STOCK_CODE,
        beg=START_DATE,
        end=END_DATE
    )
    
    print(f"[OK] eFinance 获取成功")
    print(f"数据量：{len(df_ef)} 条")
    print(f"列名：{df_ef.columns.tolist()}")
    print(f"最新收盘价：{df_ef.iloc[-1]['收盘']}")
    
    results['efinance'] = {
        'status': 'OK',
        'count': len(df_ef),
        'close': df_ef.iloc[-1]['收盘']
    }
except Exception as e:
    print(f"[ERROR] eFinance 失败：{e}")
    results['efinance'] = {'status': 'ERROR', 'error': str(e)}

# ==================== 3. FinShare ====================
print("\n" + "=" * 80)
print("[3/5] 测试 FinShare")
print("=" * 80)

try:
    import finshare as fs
    
    # 测试历史数据
    df_fs = fs.get_hist_data(STOCK_CODE, start=START_DATE, end=END_DATE)
    
    print(f"[OK] FinShare 获取成功")
    print(f"数据量：{len(df_fs)} 条")
    print(f"列名：{df_fs.columns.tolist()}")
    if 'close' in df_fs.columns:
        print(f"最新收盘价：{df_fs.iloc[-1]['close']}")
    
    results['finshare'] = {
        'status': 'OK',
        'count': len(df_fs),
        'close': df_fs.iloc[-1].get('close', 'N/A')
    }
except Exception as e:
    print(f"[ERROR] FinShare 失败：{e}")
    results['finshare'] = {'status': 'ERROR', 'error': str(e)}

# ==================== 4. qstock ====================
print("\n" + "=" * 80)
print("[4/5] 测试 qstock")
print("=" * 80)

try:
    import qstock as qs
    
    # 测试历史数据
    df_qs = qs.get_data(STOCK_CODE, start_date=START_DATE, end_date=END_DATE)
    
    print(f"[OK] qstock 获取成功")
    print(f"数据量：{len(df_qs)} 条")
    print(f"列名：{df_qs.columns.tolist()}")
    if 'close' in df_qs.columns:
        print(f"最新收盘价：{df_qs.iloc[-1]['close']}")
    
    results['qstock'] = {
        'status': 'OK',
        'count': len(df_qs),
        'close': df_qs.iloc[-1].get('close', 'N/A')
    }
except Exception as e:
    print(f"[ERROR] qstock 失败：{e}")
    results['qstock'] = {'status': 'ERROR', 'error': str(e)}

# ==================== 5. BaoStock ====================
print("\n" + "=" * 80)
print("[5/5] 测试 BaoStock")
print("=" * 80)

try:
    import baostock as bs
    
    # 登录
    bs.login()
    
    # 获取历史数据
    rs = bs.query_history_k_data_plus(
        f"sh.{STOCK_CODE}",
        "date,code,open,high,low,close,volume",
        start_date=START_DATE,
        end_date=END_DATE,
        frequency="d",
        adjustflag="3"  # 前复权
    )
    
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    
    df_bs = pd.DataFrame(data_list, columns=rs.fields)
    
    print(f"[OK] BaoStock 获取成功")
    print(f"数据量：{len(df_bs)} 条")
    print(f"列名：{df_bs.columns.tolist()}")
    if 'close' in df_bs.columns:
        print(f"最新收盘价：{df_bs.iloc[-1]['close']}")
    
    # 登出
    bs.logout()
    
    results['baostock'] = {
        'status': 'OK',
        'count': len(df_bs),
        'close': df_bs.iloc[-1].get('close', 'N/A')
    }
except Exception as e:
    print(f"[ERROR] BaoStock 失败：{e}")
    results['baostock'] = {'status': 'ERROR', 'error': str(e)}

# ==================== 总结 ====================
print("\n" + "=" * 80)
print("测试结果总结")
print("=" * 80)

print(f"\n测试股票：{STOCK_CODE} (贵州茅台)")
print(f"测试时间：{START_DATE} 至 {END_DATE}")
print("\n" + "-" * 80)
print(f"{'数据库':<15} {'状态':<10} {'数据量':<10} {'最新收盘价':<15}")
print("-" * 80)

for lib, result in results.items():
    status = result.get('status', 'ERROR')
    count = result.get('count', 'N/A')
    close = result.get('close', 'N/A')
    print(f"{lib:<15} {status:<10} {count:<10} {close:<15}")

print("-" * 80)

# 交叉验证
print("\n数据交叉验证:")
valid_closes = [r['close'] for r in results.values() 
                if r['status'] == 'OK' and isinstance(r.get('close'), (int, float))]

if len(valid_closes) >= 2:
    max_diff = max(valid_closes) - min(valid_closes)
    print(f"最高价：{max(valid_closes)}")
    print(f"最低价：{min(valid_closes)}")
    print(f"差异：{max_diff} ({max_diff/min(valid_closes)*100:.2f}%)")
    
    if max_diff < 0.1:
        print("[OK] 数据一致性良好")
    else:
        print("[WARNING] 数据存在差异，需要进一步验证")
else:
    print("[WARNING] 可用数据不足，无法交叉验证")

print("\n" + "=" * 80)
print("测试完成！")
print("=" * 80)
