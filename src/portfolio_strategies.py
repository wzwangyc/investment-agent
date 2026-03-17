#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
投资组合策略模板
Portfolio Strategy Templates

包含多种经典投资策略：
1. 等权重配置 (Equal Weight)
2. 马科维茨最优配置 (Markowitz Optimal)
3. 市场组合 (Market Portfolio)
4. 全天候配置 (All Weather / Risk Parity)
5. 最小方差配置 (Minimum Variance)
6. 最大分散化配置 (Maximum Diversification)

数据源：仅使用 akshare
"""

import akshare as ak
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from datetime import datetime, timedelta
import json
import os


# ==================== 配置 ====================

class PortfolioConfig:
    """投资组合配置"""
    
    # A 股股票池（主流蓝筹）
    A_SHARES = {
        '贵州茅台': '600519',      # 白酒/消费
        '宁德时代': '300750',      # 新能源/电池
        '中国平安': '601318',      # 金融/保险
        '招商银行': '600036',      # 金融/银行
        '东方财富': '300059',      # 金融/券商
        '五粮液': '000858',        # 白酒/消费
        '美的集团': '000333',      # 消费/家电
        '恒瑞医药': '600276',      # 医药
        '中信证券': '600030',      # 金融/券商
        '比亚迪': '002594',        # 新能源/汽车
    }
    
    # ETF 股票池（分散风险）
    ETFS = {
        '沪深 300ETF': '510300',    # 大盘股
        '中证 500ETF': '510500',    # 中盘股
        '创业板 ETF': '159915',     # 成长股
        '科创 50ETF': '588000',     # 科技股
        '红利 ETF': '510880',       # 高股息
        '债券 ETF': '511010',       # 债券
    }
    
    # 无风险利率（年化）- 中国 10 年期国债收益率
    RISK_FREE_RATE = 0.025
    
    # 交易天数
    TRADING_DAYS = 252


# ==================== 数据获取 ====================

class DataManager:
    """数据管理器（仅使用 akshare）"""
    
    def __init__(self):
        self.cache = {}
    
    def fetch_stock_data(self, stock_code: str, start_date: str = None, 
                         end_date: str = None, adjust: str = "qfq", retries: int = 3) -> pd.DataFrame:
        """
        获取 A 股历史数据（带重试机制）
        
        Args:
            stock_code: 股票代码
            start_date: 开始日期 YYYYMMDD
            end_date: 结束日期 YYYYMMDD
            adjust: 复权类型 (qfq/hfq/空)
            retries: 重试次数
        
        Returns:
            DataFrame with close prices
        """
        cache_key = f"{stock_code}_{start_date}_{end_date}"
        if cache_key in self.cache:
            print(f"[Cache] {stock_code}")
            return self.cache[cache_key]
        
        if not end_date:
            end_date = datetime.now().strftime("%Y%m%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
        
        # 重试机制
        for attempt in range(retries):
            try:
                import time
                if attempt > 0:
                    print(f"[重试 {attempt}/{retries}] 获取 {stock_code}...")
                    time.sleep(2 ** attempt)  # 指数退避
                
                # 使用 akshare 获取历史行情
                df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    period="daily",
                    start_date=start_date,
                    end_date=end_date,
                    adjust=adjust
                )
                
                df['date'] = pd.to_datetime(df['日期'])
                df = df.set_index('date')
                
                self.cache[cache_key] = df
                print(f"[OK] {stock_code}: {len(df)} 条")
                return df
                
            except Exception as e:
                if attempt == retries - 1:
                    print(f"[Error] {stock_code}: {e}")
                    return pd.DataFrame()
                continue
        
        return pd.DataFrame()
    
    def get_prices(self, stock_dict: dict, days: int = 252) -> pd.DataFrame:
        """
        获取多个股票的价格数据
        
        Args:
            stock_dict: {名称：代码}
            days: 获取天数
        
        Returns:
            DataFrame with close prices for all stocks
        """
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
        
        prices = {}
        for name, code in stock_dict.items():
            df = self.fetch_stock_data(code, start_date, end_date)
            if not df.empty:
                prices[name] = df['收盘']
        
        return pd.DataFrame(prices)
    
    def get_returns(self, prices: pd.DataFrame) -> pd.DataFrame:
        """计算对数收益率"""
        returns = np.log(prices / prices.shift(1))
        return returns.dropna()


# ==================== 投资策略模板 ====================

class PortfolioStrategies:
    """投资策略模板类"""
    
    def __init__(self, prices: pd.DataFrame, risk_free_rate: float = 0.025):
        self.prices = prices
        self.returns = np.log(prices / prices.shift(1)).dropna()
        self.risk_free_rate = risk_free_rate
        self.trading_days = 252
        
        # 预计算
        self.mean_returns = self.returns.mean().values * self.trading_days
        self.cov_matrix = self.returns.cov().values * self.trading_days
        self.n_assets = len(prices.columns)
    
    # ==================== 策略 1: 等权重配置 ====================
    
    def equal_weight(self) -> dict:
        """
        等权重配置 (Equal Weight)
        
        最简单的策略：每个资产分配相同权重
        """
        weights = np.array([1.0 / self.n_assets] * self.n_assets)
        
        return self._calculate_metrics(weights, "等权重配置")
    
    # ==================== 策略 2: 马科维茨最优配置 ====================
    
    def markowitz_optimal(self) -> dict:
        """
        马科维茨最优配置 (Markowitz Optimal)
        
        目标：最大化夏普比率
        约束：权重和为 1，不允许做空
        """
        def negative_sharpe(weights):
            port_return = np.sum(self.mean_returns * weights)
            port_vol = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
            sharpe = (port_return - self.risk_free_rate) / port_vol
            return -sharpe
        
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        initial_weights = [1.0 / self.n_assets] * self.n_assets
        
        result = minimize(
            negative_sharpe,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return self._calculate_metrics(result['x'], "马科维茨最优")
    
    # ==================== 策略 3: 最小方差配置 ====================
    
    def minimum_variance(self) -> dict:
        """
        最小方差配置 (Minimum Variance)
        
        目标：最小化组合波动率
        适合风险厌恶型投资者
        """
        def portfolio_variance(weights):
            return np.dot(weights.T, np.dot(self.cov_matrix, weights))
        
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        initial_weights = [1.0 / self.n_assets] * self.n_assets
        
        result = minimize(
            portfolio_variance,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return self._calculate_metrics(result['x'], "最小方差配置")
    
    # ==================== 策略 4: 全天候配置 (风险平价) ====================
    
    def all_weather(self) -> dict:
        """
        全天候配置 (All Weather / Risk Parity)
        
        目标：每个资产对组合风险的贡献相等
        核心思想：风险平价，而非资金平价
        """
        def risk_parity_objective(weights):
            port_vol = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
            
            # 计算每个资产的边际风险贡献
            marginal_risk = np.dot(self.cov_matrix, weights) / port_vol
            
            # 计算每个资产的风险贡献
            risk_contribution = weights * marginal_risk
            
            # 目标：所有资产风险贡献相等
            target_risk = port_vol / self.n_assets
            error = np.sum((risk_contribution - target_risk) ** 2)
            
            return error
        
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = tuple((0.01, 1) for _ in range(self.n_assets))  # 最小 1%
        initial_weights = [1.0 / self.n_assets] * self.n_assets
        
        result = minimize(
            risk_parity_objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return self._calculate_metrics(result['x'], "全天候配置 (风险平价)")
    
    # ==================== 策略 5: 最大分散化配置 ====================
    
    def maximum_diversification(self) -> dict:
        """
        最大分散化配置 (Maximum Diversification)
        
        目标：最大化分散化比率
        分散化比率 = 加权平均波动率 / 组合波动率
        """
        # 计算单个资产的波动率
        individual_vols = np.sqrt(np.diag(self.cov_matrix))
        
        def negative_diversification_ratio(weights):
            weighted_avg_vol = np.sum(weights * individual_vols)
            port_vol = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
            return -weighted_avg_vol / port_vol
        
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        initial_weights = [1.0 / self.n_assets] * self.n_assets
        
        result = minimize(
            negative_diversification_ratio,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return self._calculate_metrics(result['x'], "最大分散化配置")
    
    # ==================== 策略 6: 市场组合 (市值加权) ====================
    
    def market_portfolio(self, market_caps: dict = None) -> dict:
        """
        市场组合 (Market Portfolio / Cap-Weighted)
        
        目标：按市值加权
        如果没有市值数据，使用等权重作为近似
        
        Args:
            market_caps: {股票名称：市值 (亿元)}
        """
        if market_caps and len(market_caps) == self.n_assets:
            # 按市值加权
            caps = np.array([market_caps.get(name, 1000) for name in self.prices.columns])
            weights = caps / np.sum(caps)
        else:
            # 退化为等权重
            weights = np.array([1.0 / self.n_assets] * self.n_assets)
        
        return self._calculate_metrics(weights, "市场组合 (市值加权)")
    
    # ==================== 辅助函数 ====================
    
    def _calculate_metrics(self, weights: np.ndarray, strategy_name: str) -> dict:
        """计算组合性能指标"""
        port_return = np.sum(self.mean_returns * weights)
        port_vol = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
        sharpe = (port_return - self.risk_free_rate) / port_vol
        
        return {
            'strategy': strategy_name,
            'weights': dict(zip(self.prices.columns, weights)),
            'return': port_return,
            'volatility': port_vol,
            'sharpe_ratio': sharpe,
            'weights_array': weights  # 用于后续分析
        }
    
    def compare_all_strategies(self, market_caps: dict = None) -> pd.DataFrame:
        """
        比较所有策略
        
        Returns:
            DataFrame with all strategy results
        """
        strategies = [
            self.equal_weight(),
            self.markowitz_optimal(),
            self.minimum_variance(),
            self.all_weather(),
            self.maximum_diversification(),
            self.market_portfolio(market_caps)
        ]
        
        # 转换为 DataFrame
        results = []
        for s in strategies:
            results.append({
                '策略': s['strategy'],
                '年化收益': f"{s['return']:.2%}",
                '年化波动': f"{s['volatility']:.2%}",
                '夏普比率': f"{s['sharpe_ratio']:.3f}",
            })
        
        df = pd.DataFrame(results)
        df = df.set_index('策略')
        
        return df


# ==================== 可视化 ====================

class PortfolioVisualizer:
    """投资组合可视化"""
    
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_strategy_comparison(self, strategies_results: list) -> str:
        """
        绘制策略对比图
        
        Returns:
            保存的文件路径
        """
        import plotly.graph_objects as go
        
        fig = go.Figure()
        
        # 散点图：风险 - 收益
        for result in strategies_results:
            weights = result['weights_array']
            fig.add_trace(go.Scatter(
                x=[result['volatility']],
                y=[result['return']],
                mode='markers+text',
                name=result['strategy'],
                marker=dict(size=15),
                text=[result['strategy']],
                textposition='top center'
            ))
        
        fig.update_layout(
            title='投资策略对比 (Strategy Comparison)',
            xaxis_title='年化波动率 (风险)',
            yaxis_title='年化收益率',
            width=800,
            height=600
        )
        
        filename = os.path.join(self.output_dir, 'strategy_comparison.html')
        fig.write_html(filename)
        print(f"[可视化] 已保存：{filename}")
        
        return filename
    
    def plot_weights_heatmap(self, strategies_results: list) -> str:
        """
        绘制权重热力图
        
        Returns:
            保存的文件路径
        """
        import plotly.graph_objects as go
        
        # 构建权重矩阵
        strategies = [r['strategy'] for r in strategies_results]
        assets = list(strategies_results[0]['weights'].keys())
        
        weights_matrix = []
        for result in strategies_results:
            weights_matrix.append([result['weights'][asset] for asset in assets])
        
        fig = go.Figure(data=go.Heatmap(
            z=weights_matrix,
            x=assets,
            y=strategies,
            colorscale='RdYlGn',
            zmin=0,
            zmax=1,
            text=[[f"{v:.1%}" for v in row] for row in weights_matrix],
            texttemplate="%{text}",
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title='投资策略权重对比 (Strategy Weights Heatmap)',
            xaxis_title='资产',
            yaxis_title='策略',
            width=800,
            height=400
        )
        
        filename = os.path.join(self.output_dir, 'weights_heatmap.html')
        fig.write_html(filename)
        print(f"[可视化] 已保存：{filename}")
        
        return filename


# ==================== 主函数 ====================

def main():
    """主函数 - 演示所有投资策略"""
    print("=" * 80)
    print("投资策略模板 - 全天候/等权重/马科维茨/风险平价/最大分散化")
    print("=" * 80)
    
    # 1. 获取数据
    print("\n[1/4] 获取股票数据...")
    dm = DataManager()
    prices = dm.get_prices(PortfolioConfig.A_SHARES, days=252)
    
    if prices.empty:
        print("[Error] 未获取到数据")
        return
    
    print(f"获取到 {len(prices)} 个交易日数据")
    print(f"股票池：{list(prices.columns)}")
    
    # 2. 计算所有策略
    print("\n[2/4] 计算投资策略...")
    ps = PortfolioStrategies(prices, risk_free_rate=PortfolioConfig.RISK_FREE_RATE)
    
    strategies = ps.compare_all_strategies()
    print("\n策略对比结果:")
    print(strategies)
    
    # 3. 获取详细结果
    print("\n[3/4] 详细结果...")
    detailed_results = [
        ps.equal_weight(),
        ps.markowitz_optimal(),
        ps.minimum_variance(),
        ps.all_weather(),
        ps.maximum_diversification()
    ]
    
    for result in detailed_results:
        print(f"\n{result['strategy']}:")
        print(f"  年化收益：{result['return']:.2%}")
        print(f"  年化波动：{result['volatility']:.2%}")
        print(f"  夏普比率：{result['sharpe_ratio']:.3f}")
        print(f"  权重：")
        for asset, weight in result['weights'].items():
            if weight > 0.01:
                print(f"    {asset}: {weight:.1%}")
    
    # 4. 可视化
    print("\n[4/4] 生成可视化...")
    viz = PortfolioVisualizer()
    viz.plot_strategy_comparison(detailed_results)
    viz.plot_weights_heatmap(detailed_results)
    
    # 5. 保存结果
    results_json = []
    for result in detailed_results:
        results_json.append({
            'strategy': result['strategy'],
            'weights': {k: float(v) for k, v in result['weights'].items()},
            'return': float(result['return']),
            'volatility': float(result['volatility']),
            'sharpe_ratio': float(result['sharpe_ratio'])
        })
    
    with open(os.path.join(viz.output_dir, 'strategies_results.json'), 'w', 
              encoding='utf-8') as f:
        json.dump(results_json, f, indent=2, ensure_ascii=False)
    
    print(f"\n[完成] 结果已保存到 {viz.output_dir}/ 目录")
    print("=" * 80)
    
    return strategies


if __name__ == "__main__":
    main()
