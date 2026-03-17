# 智能投资组合优化与分析 Agent - 运行说明

## 📋 项目概述

本项目是一个基于 **Claude Code Agent 能力框架**的投资学 Agent，实现了投资组合的自动化优化与智能化分析。

**核心功能：**
- ✅ 多 API 数据获取（东方财富、akshare、yfinance）
- ✅ 马科维茨均值 - 方差模型优化
- ✅ 有效前沿可视化
- ✅ 财务指标多源交叉验证
- ✅ 自然语言交互界面

---

## 🛠️ 运行环境

### 系统要求
- Python 3.8+
- Windows / macOS / Linux
- 内存：4GB+
- 网络：需要访问 A 股/美股 API

### 核心依赖库

```bash
# 安装所有依赖
pip install akshare yfinance pandas numpy matplotlib plotly scipy

# 可选：Jupyter Notebook 支持
pip install notebook ipywidgets
```

### 依赖说明

| 库 | 版本 | 用途 |
|------|------|------|
| akshare | 1.18.39+ | A 股数据获取 |
| yfinance | 1.2.0+ | 美股数据获取 |
| pandas | 2.0+ | 数据处理 |
| numpy | 1.24+ | 数值计算 |
| matplotlib | 3.7+ | 基础可视化 |
| plotly | 5.15+ | 交互式可视化 |
| scipy | 1.10+ | 优化算法 |

---

## 🚀 快速开始

### 方法 1：直接运行

```bash
# 进入项目目录
cd investment-agent

# 运行主程序
python src/investment_agent.py
```

### 方法 2：Jupyter Notebook

```bash
# 启动 Jupyter
jupyter notebook

# 打开 src/investment_agent_demo.ipynb
# 逐单元格运行
```

### 方法 3：自定义股票池

```python
from investment_agent import InvestmentAgent

agent = InvestmentAgent()

# 自定义股票列表
results = agent.run_demo(stock_list=[
    '贵州茅台',
    '宁德时代',
    '腾讯控股',
    'Apple',
    'NVIDIA'
])
```

---

## 📁 项目结构

```
investment-agent/
├── src/
│   ├── investment_agent.py      # 核心代码
│   └── investment_agent_demo.ipynb  # Notebook 演示
├── outputs/                      # 输出目录（自动生成）
│   ├── efficient_frontier.html   # 有效前沿图
│   ├── asset_allocation.html     # 资产配置饼图
│   ├── price_comparison.html     # 价格对比图
│   ├── returns_comparison.html   # 收益对比图
│   └── results.json              # 分析结果 JSON
├── docs/
│   └── README.md                 # 本文件
├── requirements.txt              # 依赖列表
└── presentation.pptx             # 路演 PPT
```

---

## 📊 输出说明

### 1. 有效前沿图 (efficient_frontier.html)

展示所有可能投资组合的风险 - 收益分布，以及最优夏普比率组合。

**解读：**
- X 轴：年化波动率（风险）
- Y 轴：年化收益率
- 颜色：夏普比率（越黄越高）
- 红星：最优组合

### 2. 资产配置饼图 (asset_allocation.html)

显示最优投资组合中各资产的权重分配。

**解读：**
- 每个扇区代表一个资产
- 百分比表示配置权重
- 总和为 100%

### 3. 价格对比图 (price_comparison.html)

展示各资产归一化后的价格走势。

**解读：**
- 基准：第一天=100
- 可直观比较不同资产的相对表现

### 4. 收益对比图 (returns_comparison.html)

展示各资产累计收益对比。

**解读：**
- Y 轴：累计收益倍数
- 可看出哪个资产长期表现更好

### 5. 结果 JSON (results.json)

包含所有量化分析结果，可用于进一步处理。

```json
{
  "stocks": ["贵州茅台", "宁德时代", "中国平安"],
  "optimal_portfolio": {
    "weights": {"贵州茅台": 0.35, "宁德时代": 0.25, ...},
    "return": 0.1523,
    "volatility": 0.2145,
    "sharpe_ratio": 0.5703
  },
  "returns_stats": {...}
}
```

---

## 🔧 关键指令示例

### 获取 A 股数据

```python
import akshare as ak

# 获取贵州茅台历史数据
df = ak.stock_zh_a_hist(
    symbol="600519",
    period="daily",
    start_date="20230101",
    end_date="20260317",
    adjust="qfq"
)
```

### 获取美股数据

```python
import yfinance as yf

# 获取苹果公司历史数据
apple = yf.Ticker("AAPL")
df = apple.history(period="1y")
```

### 投资组合优化

```python
from scipy.optimize import minimize

# 定义优化目标
def negative_sharpe(weights, returns, cov):
    port_return = np.sum(returns * weights) * 252
    port_vol = np.sqrt(np.dot(weights.T, np.dot(cov, weights))) * np.sqrt(252)
    sharpe = (port_return - 0.03) / port_vol
    return -sharpe

# 执行优化
result = minimize(
    negative_sharpe,
    initial_weights,
    args=(mean_returns, cov_matrix),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)
```

---

## 🎯 核心功能演示

### 功能 1：多 API 数据获取

```python
from investment_agent import DataFetcher

fetcher = DataFetcher()

# A 股
df_a = fetcher.fetch_a_share_data("600519")

# 美股
df_us = fetcher.fetch_us_stock_data("AAPL")

# 宏观数据
df_macro = fetcher.fetch_macro_data("CPI")
```

### 功能 2：财务指标分析

```python
financials = fetcher.fetch_stock_financials("600519")

# 输出：
# {
#   'akshare': {'ROE': 15.2, '毛利率': 92.1, ...},
#   'eastmoney': {'PE': 35.2, 'PB': 12.5, ...}
# }
```

### 功能 3：投资组合优化

```python
from investment_agent import PortfolioOptimizer

optimizer = PortfolioOptimizer()

# 输入：价格数据
# 输出：最优权重、预期收益、风险、夏普比率
optimal = optimizer.optimize_portfolio(prices_df)
```

### 功能 4：可视化生成

```python
from investment_agent import Visualizer

viz = Visualizer(output_dir="outputs")

# 生成有效前沿
viz.plot_efficient_frontier(frontier_data, optimal_portfolio, stock_names)

# 生成资产配置图
viz.plot_asset_allocation(optimal_weights)
```

---

## 📈 示例输出

### 最优投资组合示例

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

### 有效前沿数据

```
随机组合数量：5000
最佳夏普比率：0.698
对应年化收益：18.5%
对应年化风险：22.3%
```

---

## ⚠️ 注意事项

### 1. API 限制
- 东方财富 API：有频率限制，建议添加缓存
- yfinance：延迟 15 分钟数据
- akshare：完全免费，无限制

### 2. 数据质量
- A 股使用前复权数据（`adjust="qfq"`）
- 美股使用 Adjusted Close（考虑分红拆股）
- 建议至少 1 年历史数据

### 3. 模型假设
- 收益率服从正态分布
- 不允许做空（权重 0-1）
- 无交易成本
- 历史数据不代表未来表现

### 4. 风险提示
**本代码仅供教学演示，不构成投资建议！**

---

## 🎓 技术亮点

### 1. 多 API 交叉验证
- 同时调用东方财富、akshare、yfinance
- 财务指标多源对比，确保准确性

### 2. 马科维茨优化
- 使用 SLSQP 算法最大化夏普比率
- 生成 5000+ 随机组合绘制有效前沿

### 3. 交互式可视化
- 使用 Plotly 生成 HTML 交互图表
- 支持缩放、悬停查看数据

### 4. 模块化设计
- DataFetcher：数据获取
- PortfolioOptimizer：组合优化
- Visualizer：可视化
- InvestmentAgent：主协调器

---

## 📞 团队信息

**团队名称：** Leo's Team  
**成员：** （请填写实际成员）  
**课程：** 投资学 Agents  
**日期：** 2026 年 3 月

---

## 🔗 相关资源

- [akshare 文档](https://akshare.akfamily.xyz/)
- [yfinance 文档](https://pypi.org/project/yfinance/)
- [马科维茨投资组合理论](https://www.investopedia.com/terms/m/modernportfoliotheory.asp)
- [Plotly 可视化](https://plotly.com/python/)

---

**最后更新：** 2026-03-17  
**版本：** 1.0.0
