"""
TradeForge AaaS - Example Trading Strategy: SMA Crossover
Author: Ary HH
Email: cateryatechnology@proton.me
GitHub: https://github.com/cateryatechnology
© 2026

Simple Moving Average (SMA) Crossover Strategy

Strategy Logic:
- BUY when fast SMA crosses above slow SMA (Golden Cross)
- SELL when fast SMA crosses below slow SMA (Death Cross)

This is a basic example strategy for educational purposes.
Always backtest thoroughly before using in live trading.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SMACrossoverStrategy:
    """
    Simple Moving Average (SMA) Crossover Trading Strategy.
    
    Parameters:
        fast_period: Period for fast SMA (default: 20)
        slow_period: Period for slow SMA (default: 50)
        stop_loss_pct: Stop loss percentage (default: 2.0)
        take_profit_pct: Take profit percentage (default: 5.0)
    """
    
    def __init__(
        self,
        fast_period: int = 20,
        slow_period: int = 50,
        stop_loss_pct: float = 2.0,
        take_profit_pct: float = 5.0,
        position_size_pct: float = 100.0,
    ):
        """Initialize strategy parameters."""
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.position_size_pct = position_size_pct
        
        # Validate parameters
        if fast_period >= slow_period:
            raise ValueError("Fast period must be less than slow period")
        
        logger.info(
            f"Initialized SMA Crossover Strategy: "
            f"fast={fast_period}, slow={slow_period}, "
            f"SL={stop_loss_pct}%, TP={take_profit_pct}%"
        )
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate technical indicators.
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            DataFrame with added indicator columns
        """
        df = df.copy()
        
        # Calculate SMAs
        df['SMA_fast'] = df['close'].rolling(window=self.fast_period).mean()
        df['SMA_slow'] = df['close'].rolling(window=self.slow_period).mean()
        
        # Calculate crossover signals
        df['signal'] = 0
        df.loc[df['SMA_fast'] > df['SMA_slow'], 'signal'] = 1  # Bullish
        df.loc[df['SMA_fast'] < df['SMA_slow'], 'signal'] = -1  # Bearish
        
        # Detect crossover points
        df['position'] = df['signal'].diff()
        
        return df
    
    def generate_signals(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Generate trading signals from price data.
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            List of signal dictionaries
        """
        df = self.calculate_indicators(df)
        
        signals = []
        
        for i in range(len(df)):
            row = df.iloc[i]
            
            # Golden Cross (bullish signal)
            if row['position'] == 2:
                signal = {
                    'timestamp': row.name if isinstance(row.name, datetime) else df.index[i],
                    'type': 'BUY',
                    'price': row['close'],
                    'reason': 'Golden Cross (Fast SMA crossed above Slow SMA)',
                    'stop_loss': row['close'] * (1 - self.stop_loss_pct / 100),
                    'take_profit': row['close'] * (1 + self.take_profit_pct / 100),
                    'position_size': self.position_size_pct,
                    'indicators': {
                        'fast_sma': row['SMA_fast'],
                        'slow_sma': row['SMA_slow'],
                    }
                }
                signals.append(signal)
                logger.info(f"BUY signal at {row['close']}")
            
            # Death Cross (bearish signal)
            elif row['position'] == -2:
                signal = {
                    'timestamp': row.name if isinstance(row.name, datetime) else df.index[i],
                    'type': 'SELL',
                    'price': row['close'],
                    'reason': 'Death Cross (Fast SMA crossed below Slow SMA)',
                    'indicators': {
                        'fast_sma': row['SMA_fast'],
                        'slow_sma': row['SMA_slow'],
                    }
                }
                signals.append(signal)
                logger.info(f"SELL signal at {row['close']}")
        
        return signals
    
    def backtest(
        self,
        df: pd.DataFrame,
        initial_capital: float = 10000.0,
        commission: float = 0.001
    ) -> Dict[str, Any]:
        """
        Backtest the strategy.
        
        Args:
            df: DataFrame with OHLCV data
            initial_capital: Starting capital
            commission: Commission per trade (0.001 = 0.1%)
        
        Returns:
            Dictionary with backtest results
        """
        df = self.calculate_indicators(df)
        
        # Initialize portfolio
        capital = initial_capital
        position = 0
        entry_price = 0
        trades = []
        equity_curve = [initial_capital]
        
        for i in range(self.slow_period, len(df)):
            row = df.iloc[i]
            
            # Check for BUY signal
            if row['position'] == 2 and position == 0:
                # Calculate position size
                position_value = capital * (self.position_size_pct / 100)
                shares = position_value / row['close']
                cost = shares * row['close'] * (1 + commission)
                
                if cost <= capital:
                    position = shares
                    entry_price = row['close']
                    capital -= cost
                    
                    trades.append({
                        'date': row.name,
                        'type': 'BUY',
                        'price': row['close'],
                        'shares': shares,
                        'capital': capital,
                    })
            
            # Check for SELL signal
            elif row['position'] == -2 and position > 0:
                proceeds = position * row['close'] * (1 - commission)
                capital += proceeds
                
                pnl = proceeds - (position * entry_price)
                pnl_pct = (pnl / (position * entry_price)) * 100
                
                trades.append({
                    'date': row.name,
                    'type': 'SELL',
                    'price': row['close'],
                    'shares': position,
                    'capital': capital,
                    'pnl': pnl,
                    'pnl_pct': pnl_pct,
                })
                
                position = 0
                entry_price = 0
            
            # Update equity curve
            portfolio_value = capital + (position * row['close'] if position > 0 else 0)
            equity_curve.append(portfolio_value)
        
        # Calculate metrics
        final_capital = capital + (position * df.iloc[-1]['close'] if position > 0 else 0)
        total_return = ((final_capital - initial_capital) / initial_capital) * 100
        
        # Calculate winning trades
        winning_trades = [t for t in trades if t.get('pnl', 0) > 0]
        win_rate = (len(winning_trades) / len([t for t in trades if 'pnl' in t])) * 100 if trades else 0
        
        # Calculate max drawdown
        equity_series = pd.Series(equity_curve)
        running_max = equity_series.expanding().max()
        drawdown = (equity_series - running_max) / running_max * 100
        max_drawdown = drawdown.min()
        
        # Calculate Sharpe ratio (simplified)
        returns = equity_series.pct_change().dropna()
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252) if len(returns) > 0 else 0
        
        results = {
            'initial_capital': initial_capital,
            'final_capital': final_capital,
            'total_return': total_return,
            'total_trades': len(trades),
            'winning_trades': len(winning_trades),
            'win_rate': win_rate,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'trades': trades,
            'equity_curve': equity_curve,
        }
        
        logger.info(f"Backtest complete: Return={total_return:.2f}%, Win Rate={win_rate:.2f}%")
        
        return results
    
    def get_current_signal(self, df: pd.DataFrame) -> Optional[str]:
        """
        Get current signal based on latest data.
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            'BUY', 'SELL', or None
        """
        df = self.calculate_indicators(df)
        latest = df.iloc[-1]
        
        if latest['position'] == 2:
            return 'BUY'
        elif latest['position'] == -2:
            return 'SELL'
        else:
            return None


# Example usage
if __name__ == "__main__":
    # Generate sample data
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='1D')
    prices = 100 + np.cumsum(np.random.randn(len(dates)) * 2)
    
    df = pd.DataFrame({
        'open': prices,
        'high': prices * 1.02,
        'low': prices * 0.98,
        'close': prices,
        'volume': np.random.randint(1000, 10000, len(dates))
    }, index=dates)
    
    # Initialize strategy
    strategy = SMArossoverStrategy(fast_period=20, slow_period=50)
    
    # Run backtest
    results = strategy.backtest(df, initial_capital=10000)
    
    print("\n" + "="*60)
    print("BACKTEST RESULTS")
    print("="*60)
    print(f"Initial Capital:  ${results['initial_capital']:,.2f}")
    print(f"Final Capital:    ${results['final_capital']:,.2f}")
    print(f"Total Return:     {results['total_return']:.2f}%")
    print(f"Total Trades:     {results['total_trades']}")
    print(f"Win Rate:         {results['win_rate']:.2f}%")
    print(f"Max Drawdown:     {results['max_drawdown']:.2f}%")
    print(f"Sharpe Ratio:     {results['sharpe_ratio']:.2f}")
    print("="*60 + "\n")
