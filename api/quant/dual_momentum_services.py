import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)

@dataclass
class BacktestConfig:
    initial_capital: float = 10000
    lookback_months: int = 6

class DualMomentumBacktest:
    def __init__(self, etf_symbols: List[str], duration: str, savings_rate: str, config: BacktestConfig = BacktestConfig()):
        end_date = datetime.today()
        start_date = end_date - timedelta(days=int(duration) * 365)
        self.etf_symbols = etf_symbols
        self.start_date = start_date
        self.end_date = end_date
        self.savings_rate = savings_rate
        self.config = config
        self.monthly_savings_rate = float(savings_rate) / 100 / 12
        self.df = self._fetch_data()
        
    def _fetch_data(self) -> pd.DataFrame:
        """ETF 데이터 가져오기"""
        data = {}
        for symbol in self.etf_symbols:
            try:
                etf_data = yf.download(
                    symbol, 
                    start=self.start_date.strftime('%Y-%m-%d'),
                    end=self.end_date.strftime('%Y-%m-%d')
                )
                data[symbol] = etf_data['Close']
            except Exception as e:
                logger.error(f"Failed to fetch data for {symbol}: {str(e)}")
        return pd.DataFrame(data)

    def _calculate_returns(self, current_date: datetime) -> tuple[pd.Series, pd.Series]:
        """수익률 계산"""
        lookback_date = current_date - timedelta(days=self.config.lookback_months * 30)
        prices = self.df.loc[lookback_date:current_date]
        returns = (prices.iloc[-1] / prices.iloc[0] - 1) * 100
        monthly_returns = (1 + returns / 100) ** (1 / self.config.lookback_months) - 1
        return returns, monthly_returns

    def _process_trading_period(self, date: datetime, capital: float) -> Dict[str, Any]:
        """각 거래 기간 처리"""
        try:
            returns, monthly_returns = self._calculate_returns(date)
            
            if all(monthly_returns <= self.monthly_savings_rate):
                capital *= (1 + self.monthly_savings_rate)
                return {
                    'Date': date,
                    'Best_ETF': 'CASH',
                    '6M_Return': None,
                    'Capital': capital
                }
            
            best_etf = monthly_returns.idxmax()
            capital *= (1 + monthly_returns[best_etf])
            return {
                'Date': date,
                'Best_ETF': best_etf,
                '6M_Return': float(returns[best_etf]),
                'Capital': capital
            }
        except Exception as e:
            logger.error(f"Error processing trading period {date}: {str(e)}")
            return None

    def run_backtest(self) -> Dict[str, Any]:
        """백테스트 실행"""
        capital = self.config.initial_capital
        results = []
        
        for date in pd.date_range(start=self.start_date, end=self.end_date, freq='M'):
            if date - timedelta(days=self.config.lookback_months * 30) < self.df.index[0]:
                continue
                
            result = self._process_trading_period(date, capital)
            if result:
                results.append(result)
                capital = result['Capital']

        results_df = pd.DataFrame(results)
        
        return {
            "data": results_df.to_dict('records'),
            "summary": self._generate_summary(results_df)
        }
    
    def _generate_summary(self, results_df: pd.DataFrame) -> Dict[str, float]:
        """백테스트 결과 요약 생성"""
        if results_df.empty:
            return {
                "initial_capital": self.config.initial_capital,
                "final_capital": self.config.initial_capital,
                "total_return": 0
            }
            
        final_capital = float(results_df['Capital'].iloc[-1])
        return {
            "initial_capital": self.config.initial_capital,
            "final_capital": final_capital,
            "total_return": float((final_capital / self.config.initial_capital - 1) * 100)
        }

def run_dual_momentum_backtest(
    etf_symbols: List[str],
    duration: str,
    savings_rate: float
) -> Dict[str, Any]:
    """백테스트 실행을 위한 편의 함수"""
    backtest = DualMomentumBacktest(etf_symbols, duration, savings_rate)
    return backtest.run_backtest()

# etf_symbols = ['SPY', 'FEZ', 'EWJ', 'EWY']
# end_date = datetime.today()
# start_date = end_date - timedelta(days=10 * 365)
# savings_rate = 3.0

# results = run_dual_momentum_backtest(etf_symbols, 10, savings_rate)
# print(results)
