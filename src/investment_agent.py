#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智能投资组合优化与分析 Agent
Intelligent Investment Portfolio Optimization & Analysis Agent

课程：投资学 Agents
团队：Leo's Team
日期：2026-03

功能：
1. 数据获取（akshare 为主，efinance 备用）- 仅国内可用 API
2. 投资组合优化计算（马科维茨均值 - 方差模型）
3. 财务指标解读与分析
4. 可视化输出（有效前沿、资产配置饼图、收益对比）
5. 自然语言交互界面

依赖：
pip install akshare efinance pandas numpy matplotlib plotly scipy
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.offline import plot as plotly_plot
from scipy.optimize import minimize
from datetime import datetime, timedelta
import json
import os

# ==================== 配置 ====================

class Config:
    """配置类"""
    # A 股配置（主流蓝筹股）
    A_SHARES = {
        '贵州茅台': '600519',      # 白酒龙头
        '宁德时代': '300750',      # 新能源电池
        '中国平安': '601318',      # 保险龙头
        '招商银行': '600036',      # 银行龙头
        '腾讯控股': '00700',       # 港股互联网
        '五粮液': '000858',        # 白酒
        '美的集团': '000333',      # 家电
        '东方财富': '300059',      # 券商
    }
    
    # ETF 配置（分散风险）
    ETFS = {
        '沪深 300ETF': '510300',
        '中证 500ETF': '510500',
        '创业板 ETF': '159915',
        '科创 50ETF': '588000',
    }
    
    # 无风险利率（年化）- 中国 10 年期国债收益率
    RISK_FREE_RATE = 0.025
    
    # 交易天数
    TRADING_DAYS_PER_YEAR = 252


# ==================== 数据获取模块 ====================

class DataFetcher:
    """多 API 数据获取器"""
    
    def __init__(self):
        self.cache = {}
    
    def fetch_a_share_data(self, stock_code: str, start_date: str = None, end_date: str = None, adjust: str = "qfq") -> pd.DataFrame:
        """
        获取 A 股历史数据（东方财富 API via akshare）
        
        Args:
            stock_code: 股票代码（如'600519'）
            start_date: 开始日期（YYYYMMDD）
            end_date: 结束日期（YYYYMMDD）
            adjust: 复权类型（qfq-前复权，hfq-后复权，空 - 不复权）
        
        Returns:
            DataFrame with columns: date, open, high, low, close, volume
        """
        cache_key = f"a_share_{stock_code}_{start_date}_{end_date}_{adjust}"
        if cache_key in self.cache:
            print(f"[Cache Hit] {stock_code}")
            return self.cache[cache_key]
        
        try:
            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
            
            # 方案 1：akshare（主要）
            try:
                df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    period="daily",
                    start_date=start_date,
                    end_date=end_date,
                    adjust=adjust
                )
                print(f"[API] akshare - 获取 {stock_code} 成功，共 {len(df)} 条记录")
            except Exception as ak_error:
                print(f"[WARNING] akshare 失败：{ak_error}")
                print(f"[INFO] 尝试使用 efinance 作为备用...")
                
                # 方案 2：efinance（备用）
                from efinance import stock
                df = stock.get_quote_history(
                    stock_code,
                    beg=start_date,
                    end=end_date
                )
                # 重命名列以匹配 akshare 格式
                df = df.rename(columns={
                    '日期': 'date',
                    '收盘': 'close',
                    '开盘': 'open',
                    '最高': 'high',
                    '最低': 'low',
                    '成交量': 'volume',
                    '成交额': 'amount'
                })
                print(f"[API] efinance - 获取 {stock_code} 成功，共 {len(df)} 条记录")
            
            # 统一处理
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
            
            self.cache[cache_key] = df
            return df
            
        except Exception as e:
            print(f"[Error] 获取 {stock_code} 失败：{e}")
            return pd.DataFrame()
    
    def fetch_macro_data(self, indicator: str = "CPI") -> pd.DataFrame:
        """
        获取宏观经济指标（东方财富 API）
        
        Args:
            indicator: 指标名称（CPI, PMI, GDP 等）
        
        Returns:
            DataFrame with macroeconomic data
        """
        try:
            if indicator == "CPI":
                df = ak.macro_china_cpi()
            elif indicator == "PMI":
                df = ak.macro_china_pmi()
            elif indicator == "GDP":
                df = ak.macro_china_gdp_yearly()
            elif indicator == "利率":
                df = ak.macro_china_loan_prime_rate()
            else:
                print(f"[Warning] 未知指标：{indicator}")
                return pd.DataFrame()
            
            print(f"[API] 东方财富 - 获取宏观指标 {indicator} 成功")
            return df
            
        except Exception as e:
            print(f"[Error] 获取宏观数据失败：{e}")
            return pd.DataFrame()
    
    def fetch_stock_financials(self, stock_code: str) -> dict:
        """
        获取股票财务指标（多 API 交叉验证）
        
        Args:
            stock_code: 股票代码
        
        Returns:
            Dictionary with financial metrics
        """
        financials = {}
        
        try:
            # API 1: akshare 获取财务指标
            try:
                df = ak.stock_financial_analysis_indicator(symbol=stock_code)
                if not df.empty:
                    latest = df.iloc[0]
                    financials['akshare'] = {
                        'ROE': latest.get('净资产收益率 (%)', 0),
                        '毛利率': latest.get('销售毛利率 (%)', 0),
                        '净利率': latest.get('总资产净利润率 (%)', 0),
                        '负债率': latest.get('资产负债率 (%)', 0),
                    }
            except:
                pass
            
            # API 2: 东方财富获取估值指标
            try:
                df = ak.stock_value_em(symbol=stock_code)
                if not df.empty:
                    latest = df.iloc[0]
                    financials['eastmoney'] = {
                        'PE': latest.get('市盈率 - 动态', 0),
                        'PB': latest.get('市净率', 0),
                        'PS': latest.get('市销率', 0),
                    }
            except:
                pass
            
            print(f"[API] 获取 {stock_code} 财务指标成功")
            return financials
            
        except Exception as e:
            print(f"[Error] 获取财务指标失败：{e}")
            return {}


# ==================== 投资组合优化模块 ====================

class PortfolioOptimizer:
    """投资组合优化器（马科维茨均值 - 方差模型）"""
    
    def __init__(self, risk_free_rate: float = 0.03, trading_days: int = 252):
        self.risk_free_rate = risk_free_rate
        self.trading_days = trading_days
    
    def calculate_returns(self, prices: pd.DataFrame) -> pd.DataFrame:
        """计算对数收益率"""
        returns = np.log(prices / prices.shift(1))
        return returns.dropna()
    
    def portfolio_performance(self, weights: np.ndarray, mean_returns: np.ndarray, cov_matrix: np.ndarray) -> tuple:
        """
        计算投资组合性能
        
        Returns:
            (portfolio_return, portfolio_volatility, sharpe_ratio)
        """
        portfolio_return = np.sum(mean_returns * weights) * self.trading_days
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(self.trading_days)
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
        
        return portfolio_return, portfolio_volatility, sharpe_ratio
    
    def negative_sharpe_ratio(self, weights: np.ndarray, mean_returns: np.ndarray, cov_matrix: np.ndarray) -> float:
        """负夏普比率（用于最小化）"""
        _, _, sharpe = self.portfolio_performance(weights, mean_returns, cov_matrix)
        return -sharpe
    
    def optimize_portfolio(self, prices: pd.DataFrame) -> dict:
        """
        优化投资组合（最大化夏普比率）
        
        Args:
            prices: 价格数据 DataFrame
        
        Returns:
            Dictionary with optimal weights and performance metrics
        """
        # 计算收益率
        returns = self.calculate_returns(prices)
        mean_returns = returns.mean().values
        cov_matrix = returns.cov().values
        
        num_assets = len(prices.columns)
        
        # 约束条件：权重和为 1
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        
        # 边界：每个资产权重 0-1（不允许做空）
        bounds = tuple((0, 1) for _ in range(num_assets))
        
        # 初始猜测：等权重
        initial_weights = num_assets * [1. / num_assets,]
        
        # 优化
        result = minimize(
            self.negative_sharpe_ratio,
            initial_weights,
            args=(mean_returns, cov_matrix),
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        # 计算最优组合性能
        opt_weights = result['x']
        opt_return, opt_vol, opt_sharpe = self.portfolio_performance(opt_weights, mean_returns, cov_matrix)
        
        return {
            'weights': dict(zip(prices.columns, opt_weights)),
            'return': opt_return,
            'volatility': opt_vol,
            'sharpe_ratio': opt_sharpe,
        }
    
    def generate_efficient_frontier(self, prices: pd.DataFrame, num_portfolios: int = 10000) -> dict:
        """
        生成有效前沿
        
        Returns:
            Dictionary with frontier data for plotting
        """
        returns = self.calculate_returns(prices)
        mean_returns = returns.mean().values
        cov_matrix = returns.cov().values
        
        num_assets = len(prices.columns)
        
        results = {
            'returns': [],
            'volatilities': [],
            'sharpe_ratios': [],
            'weights': []
        }
        
        for _ in range(num_portfolios):
            # 随机权重
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            
            portfolio_return, portfolio_vol, sharpe = self.portfolio_performance(
                weights, mean_returns, cov_matrix
            )
            
            results['returns'].append(portfolio_return)
            results['volatilities'].append(portfolio_vol)
            results['sharpe_ratios'].append(sharpe)
            results['weights'].append(weights)
        
        return results


# ==================== 可视化模块 ====================

class Visualizer:
    """可视化生成器"""
    
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_efficient_frontier(self, frontier_data: dict, optimal_portfolio: dict, stock_names: list) -> str:
        """
        绘制有效前沿图
        
        Returns:
            保存的文件路径
        """
        fig = go.Figure()
        
        # 有效前沿散点
        fig.add_trace(go.Scatter(
            x=frontier_data['volatilities'],
            y=frontier_data['returns'],
            mode='markers',
            marker=dict(
                size=3,
                color=frontier_data['sharpe_ratios'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="夏普比率")
            ),
            name='随机组合',
            opacity=0.3
        ))
        
        # 最优组合
        fig.add_trace(go.Scatter(
            x=[optimal_portfolio['volatility']],
            y=[optimal_portfolio['return']],
            mode='markers+text',
            marker=dict(size=15, color='red', symbol='star'),
            text=['最优组合'],
            textposition='top center',
            name='最优组合'
        ))
        
        fig.update_layout(
            title='投资组合有效前沿 (Efficient Frontier)',
            xaxis_title='年化波动率 (风险)',
            yaxis_title='年化收益率',
            hovermode='closest',
            width=800,
            height=600
        )
        
        filename = os.path.join(self.output_dir, 'efficient_frontier.html')
        fig.write_html(filename)
        print(f"[可视化] 已保存：{filename}")
        
        return filename
    
    def plot_asset_allocation(self, weights: dict) -> str:
        """
        绘制资产配置饼图
        
        Returns:
            保存的文件路径
        """
        fig = go.Figure(data=[go.Pie(
            labels=list(weights.keys()),
            values=list(weights.values()),
            hole=0.3,
            textinfo='label+percent',
            hoverinfo='label+value'
        )])
        
        fig.update_layout(
            title='最优资产配置 (Optimal Asset Allocation)',
            width=600,
            height=600
        )
        
        filename = os.path.join(self.output_dir, 'asset_allocation.html')
        fig.write_html(filename)
        print(f"[可视化] 已保存：{filename}")
        
        return filename
    
    def plot_price_comparison(self, prices: pd.DataFrame) -> str:
        """
        绘制价格对比图（归一化）
        
        Returns:
            保存的文件路径
        """
        # 归一化价格
        normalized = prices / prices.iloc[0] * 100
        
        fig = go.Figure()
        
        for col in normalized.columns:
            fig.add_trace(go.Scatter(
                x=normalized.index,
                y=normalized[col],
                mode='lines',
                name=col
            ))
        
        fig.update_layout(
            title='资产价格走势对比 (归一化)',
            xaxis_title='日期',
            yaxis_title='价格指数 (基准=100)',
            hovermode='x unified',
            width=800,
            height=500
        )
        
        filename = os.path.join(self.output_dir, 'price_comparison.html')
        fig.write_html(filename)
        print(f"[可视化] 已保存：{filename}")
        
        return filename
    
    def plot_returns_comparison(self, returns: pd.DataFrame) -> str:
        """
        绘制收益率对比图
        
        Returns:
            保存的文件路径
        """
        cumulative_returns = (1 + returns).cumprod()
        
        fig = go.Figure()
        
        for col in cumulative_returns.columns:
            fig.add_trace(go.Scatter(
                x=cumulative_returns.index,
                y=cumulative_returns[col],
                mode='lines',
                name=col
            ))
        
        fig.update_layout(
            title='累计收益对比',
            xaxis_title='日期',
            yaxis_title='累计收益',
            hovermode='x unified',
            width=800,
            height=500
        )
        
        filename = os.path.join(self.output_dir, 'returns_comparison.html')
        fig.write_html(filename)
        print(f"[可视化] 已保存：{filename}")
        
        return filename


# ==================== 主 Agent 类 ====================

class InvestmentAgent:
    """投资学 Agent 主类"""
    
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.optimizer = PortfolioOptimizer()
        self.visualizer = Visualizer()
        self.results = {}
    
    def run_demo(self, stock_list: list = None, days: int = 252) -> dict:
        """
        运行演示
        
        Args:
            stock_list: 股票列表（中文名称）
            days: 获取天数（默认 252 天=1 年）
        
        Returns:
            完整分析结果
        """
        print("=" * 60)
        print("智能投资组合优化与分析 Agent")
        print("=" * 60)
        
        # 默认股票池（A 股蓝筹）
        if not stock_list:
            stock_list = ['贵州茅台', '宁德时代', '中国平安', '招商银行', '东方财富']
        
        print(f"\n[1/5] 获取股票数据...")
        prices_dict = {}
        
        # 计算日期范围
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
        
        for stock_name in stock_list:
            if stock_name in Config.A_SHARES:
                code = Config.A_SHARES[stock_name]
                df = self.data_fetcher.fetch_a_share_data(code, start_date, end_date)
                if not df.empty:
                    prices_dict[stock_name] = df['close']
            elif stock_name in Config.ETFS:
                code = Config.ETFS[stock_name]
                df = self.data_fetcher.fetch_a_share_data(code, start_date, end_date)
                if not df.empty:
                    prices_dict[stock_name] = df['close']
        
        if not prices_dict:
            print("[Error] 未获取到任何股票数据")
            return {}
        
        prices_df = pd.DataFrame(prices_dict)
        
        print(f"\n[2/5] 计算收益率与协方差...")
        returns = self.optimizer.calculate_returns(prices_df)
        print(f"收益率数据：{len(returns)} 条记录")
        
        print(f"\n[3/5] 优化投资组合...")
        optimal = self.optimizer.optimize_portfolio(prices_df)
        print(f"\n最优组合:")
        print(f"  权重：{optimal['weights']}")
        print(f"  年化收益：{optimal['return']:.2%}")
        print(f"  年化波动：{optimal['volatility']:.2%}")
        print(f"  夏普比率：{optimal['sharpe_ratio']:.3f}")
        
        print(f"\n[4/5] 生成有效前沿...")
        frontier = self.optimizer.generate_efficient_frontier(prices_df, num_portfolios=5000)
        
        print(f"\n[5/5] 生成可视化...")
        self.visualizer.plot_efficient_frontier(frontier, optimal, stock_list)
        self.visualizer.plot_asset_allocation(optimal['weights'])
        self.visualizer.plot_price_comparison(prices_df)
        self.visualizer.plot_returns_comparison(returns)
        
        # 保存结果
        self.results = {
            'stocks': stock_list,
            'optimal_portfolio': optimal,
            'frontier': frontier,
            'returns_stats': {
                'mean': returns.mean().to_dict(),
                'std': returns.std().to_dict(),
                'sharpe': (returns.mean() / returns.std() * np.sqrt(252)).to_dict()
            }
        }
        
        # 保存为 JSON
        results_json = {
            'stocks': stock_list,
            'optimal_portfolio': {
                'weights': {k: float(v) for k, v in optimal['weights'].items()},
                'return': float(optimal['return']),
                'volatility': float(optimal['volatility']),
                'sharpe_ratio': float(optimal['sharpe_ratio'])
            },
            'returns_stats': self.results['returns_stats']
        }
        
        with open(os.path.join(self.visualizer.output_dir, 'results.json'), 'w', encoding='utf-8') as f:
            json.dump(results_json, f, indent=2, ensure_ascii=False)
        
        print(f"\n[完成] 结果已保存到 outputs/ 目录")
        print("=" * 60)
        
        return self.results
    
    def analyze_single_stock(self, stock_code: str) -> dict:
        """
        分析单只股票
        
        Args:
            stock_code: 股票代码
        
        Returns:
            分析结果
        """
        print(f"\n分析股票：{stock_code}")
        
        # 获取数据
        df = self.data_fetcher.fetch_a_share_data(stock_code)
        
        if df.empty:
            return {}
        
        # 计算指标
        df['return'] = df['close'].pct_change()
        df['ma20'] = df['close'].rolling(20).mean()
        df['ma60'] = df['close'].rolling(60).mean()
        
        # 财务指标
        financials = self.data_fetcher.fetch_stock_financials(stock_code)
        
        result = {
            'code': stock_code,
            'latest_price': df['close'].iloc[-1],
            'return_1y': df['close'].pct_change(252).iloc[-1],
            'volatility': df['return'].std() * np.sqrt(252),
            'financials': financials
        }
        
        print(f"最新价：{result['latest_price']:.2f}")
        print(f"年收益：{result['return_1y']:.2%}")
        print(f"波动率：{result['volatility']:.2%}")
        
        return result


# ==================== 命令行接口 ====================

def main():
    """主函数"""
    agent = InvestmentAgent()
    
    # 运行演示
    results = agent.run_demo()
    
    # 分析单只股票示例
    # agent.analyze_single_stock('600519')
    
    return results


if __name__ == "__main__":
    main()
