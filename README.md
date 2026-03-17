# 智能投资组合优化与分析 Agent
# Investment Portfolio Optimization & Analysis Agent

## 📋 项目概述

基于 **Claude Code Agent 能力框架**的投资学 Agent，实现了投资组合的自动化优化与智能化分析。

**核心功能：**
- ✅ 多 API 数据获取（东方财富、akshare、yfinance）
- ✅ 马科维茨均值 - 方差模型优化
- ✅ 有效前沿可视化
- ✅ 财务指标多源交叉验证
- ✅ 交互式图表输出

**课程：** 投资学 Agents  
**团队：** Leo's Team  
**日期：** 2026 年 3 月

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行演示

```bash
python src/investment_agent.py
```

### 3. 查看结果

输出文件保存在 `outputs/` 目录：
- `efficient_frontier.html` - 有效前沿图
- `asset_allocation.html` - 资产配置饼图
- `price_comparison.html` - 价格对比图
- `returns_comparison.html` - 收益对比图
- `results.json` - 分析结果

---

## 📁 项目结构

```
investment-agent/
├── src/
│   └── investment_agent.py      # 核心代码
├── docs/
│   ├── README.md                 # 运行说明
│   └── PPT_Outline.md            # PPT 大纲
├── outputs/                      # 输出目录
├── requirements.txt              # 依赖列表
└── README.md                     # 本文件
```

---

## 🎯 核心功能

### 功能 1：多 API 数据获取

```python
from src.investment_agent import DataFetcher

fetcher = DataFetcher()

# A 股
df_a = fetcher.fetch_a_share_data("600519")

# 美股
df_us = fetcher.fetch_us_stock_data("AAPL")

# 宏观数据
df_macro = fetcher.fetch_macro_data("CPI")
```

### 功能 2：投资组合优化

```python
from src.investment_agent import PortfolioOptimizer

optimizer = PortfolioOptimizer()
optimal = optimizer.optimize_portfolio(prices_df)

# 输出最优权重、预期收益、风险、夏普比率
```

### 功能 3：可视化

```python
from src.investment_agent import Visualizer

viz = Visualizer()
viz.plot_efficient_frontier(frontier_data, optimal_portfolio, stock_names)
viz.plot_asset_allocation(optimal_weights)
```

---

## 📊 示例输出

### 最优投资组合

```
最优组合:
  权重：{
    '贵州茅台': 0.35,
    '宁德时代': 0.15,
    '中国平安': 0.20,
    '招商银行': 0.20,
    '腾讯控股': 0.10
  }
  年化收益：18.5%
  年化波动：22.3%
  夏普比率：0.698
```

---

## 🎓 技术亮点

1. **多 API 交叉验证** - 确保数据准确性
2. **马科维茨优化** - 经典投资组合理论
3. **交互式可视化** - Plotly HTML 图表
4. **模块化设计** - 易于扩展和维护

---

## 📞 团队信息

**团队名称：** Leo's Team  
**课程：** 投资学 Agents  
**日期：** 2026 年 3 月

---

## 📄 许可证

MIT License

---

## ⚠️ 免责声明

**本代码仅供教学演示，不构成投资建议！**

投资有风险，入市需谨慎。
