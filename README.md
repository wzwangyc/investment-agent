# 投资学 Agent - 智能投资组合优化系统

## 🎯 项目概述

基于 Claude Code Agent 框架的智能投资分析系统，实现 6 种经典投资策略的自动化分析与优化。

**特点：**
- ✅ 6 种经典投资策略
- ✅ 三重数据源备份
- ✅ 一键启动，无需配置
- ✅ 95% 本地化

---

## 🚀 快速开始

### Windows 用户
```bash
run.bat
```

### Mac/Linux 用户
```bash
bash run.sh
```

### 手动运行
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行主程序
python src/investment_agent.py
```

---

## 📊 核心功能

### 6 种投资策略

| 策略 | 说明 |
|------|------|
| **等权重配置** | 平均分配资金 |
| **马科维茨最优** | 最大化夏普比率 |
| **最小方差配置** | 最小化风险 |
| **全天候配置** | 风险平价 |
| **最大分散化** | 最大化分散比率 |
| **市场组合** | 市值加权 |

### 数据源

| 数据源 | 说明 |
|--------|------|
| **AkShare** | 主力数据源 |
| **eFinance** | 备用数据源 |
| **BaoStock** | 备用数据源 |

---

## 📁 项目结构

```
investment-agent/
├── src/
│   ├── investment_agent.py      # 主程序
│   └── portfolio_strategies.py  # 6 种策略
├── run.bat                      # Windows 启动
├── run.sh                       # Mac/Linux 启动
├── requirements.txt             # 依赖
└── README.md                    # 本文件
```

---

## 🎓 课程要求对应

| 要求 | 状态 |
|------|------|
| **Claude Code Agent 框架** | ✅ |
| **投资学核心功能** | ✅ |
| **数据 API 整合** | ✅ |
| **文档完整性** | ✅ |
| **可运行性** | ✅ |
| **GitHub 仓库** | ✅ |

---

## 💡 常见问题

### Q: 依赖安装失败？
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 如何修改股票池？
编辑 `src/investment_agent.py`，修改 `A_SHARES` 字典。

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
