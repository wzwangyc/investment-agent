# 投资学 Agent - 智能投资组合优化系统

## 🎯 项目概述

基于 Claude Code Agent 框架的智能投资分析系统，实现 6 种经典投资策略的自动化分析与优化。

**特点：**
- ✅ 6 种经典投资策略（马科维茨、风险平价、最小方差等）
- ✅ 三重数据源备份（AkShare + eFinance + BaoStock）
- ✅ 数据交叉验证机制
- ✅ 95% 本地化（仅使用国内 API）
- ✅ 一键启动，无需配置

---

## 🚀 快速开始

### 方式 1：一键启动（推荐）

**Windows 用户：**
```bash
run.bat
```

**Mac/Linux 用户：**
```bash
bash run.sh
```

### 方式 2：手动运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行主程序
python src/investment_agent.py
```

---

## 📊 核心功能

### 6 种投资策略

| 策略 | 说明 | 适合人群 |
|------|------|---------|
| **等权重配置** | 平均分配资金 | 新手 |
| **马科维茨最优** | 最大化夏普比率 | 追求收益 |
| **最小方差配置** | 最小化风险 | 保守型 |
| **全天候配置** | 风险平价 | 长期投资 |
| **最大分散化** | 最大化分散比率 | 分散风险 |
| **市场组合** | 市值加权 | 被动投资 |

### 数据源

| 数据源 | 类型 | 状态 |
|--------|------|------|
| **AkShare** | 主力 | ✅ 国内可用 |
| **eFinance** | 备用 1 | ✅ 东方财富 |
| **BaoStock** | 备用 2 | ✅ 稳定可靠 |

---

## 📁 项目结构

```
investment-agent/
├── src/
│   ├── investment_agent.py      # 主程序
│   └── portfolio_strategies.py  # 6 种策略
├── docs/
│   ├── README.md                # 详细文档
│   ├── Pre-PPT.md               # 演示 PPT
│   └── 项目说明.md               # 项目说明
├── run.bat                      # 一键启动（Windows）
├── run.sh                       # 一键启动（Mac/Linux）
├── requirements.txt             # 依赖
└── README.md                    # 本文件
```

---

## 🧪 测试

```bash
# 运行测试
python test_all_data_sources.py
```

---

## 📝 使用示例

### 示例 1：运行主程序

```bash
python src/investment_agent.py
```

**输出：**
```
============================================================
智能投资组合优化与分析 Agent
============================================================

[1/5] 获取股票数据...
[API] akshare - 获取 600519 成功，共 252 条记录

[2/5] 计算收益率与协方差...
收益率数据：251 条记录

[3/5] 优化投资组合...

最优组合:
  权重：{'贵州茅台': 0.35, '宁德时代': 0.25, ...}
  年化收益：18.50%
  年化波动：22.30%
  夏普比率：0.698

[完成] 结果已保存到 outputs/ 目录
```

---

## 🎓 课程要求对应

| 要求 | 完成情况 | 说明 |
|------|---------|------|
| **Claude Code Agent 框架** | ✅ | 主代理 + 子代理架构 |
| **投资学核心功能** | ✅ | 6 种策略 + 数据分析 |
| **数据 API 整合** | ✅ | 3 个数据源 + 交叉验证 |
| **文档完整性** | ✅ | README + PPT + 测试报告 |
| **可运行性** | ✅ | 一键启动，无需配置 |
| **GitHub 仓库** | ✅ | 公开仓库 |

---

## 📊 技术栈

- **编程语言：** Python 3.9+
- **数据处理：** pandas, numpy
- **优化算法：** scipy.optimize
- **可视化：** plotly, matplotlib
- **数据源：** akshare, eFinance, BaoStock

---

## 🔗 相关链接

- **GitHub:** https://github.com/wzwangyc/investment-agent
- **详细文档:** `docs/README.md`
- **PPT:** `docs/Pre-PPT.md`

---

## 💡 常见问题

### Q1: 依赖安装失败？

**解决：**
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: 数据获取失败？

**解决：**
- 检查网络连接
- 程序会自动切换备用数据源
- 查看控制台错误信息

### Q3: 如何修改股票池？

**解决：**
编辑 `src/investment_agent.py`，修改 `A_SHARES` 字典：
```python
A_SHARES = {
    '贵州茅台': '600519',
    '宁德时代': '300750',
    # 添加你的股票...
}
```

---

## 📄 许可证

MIT License

---

## 👤 作者

Yucheng Wang (王煜诚)
- GitHub: github.com/wzwangyc
- Email: wzwangyc@163.com

---

**投资学 Agents 课程项目 | 2026 年 3 月**
