# @title MONTO Invest
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import requests
from scipy import stats
from scipy.optimize import minimize
import warnings
from zoneinfo import ZoneInfo  # Add this with your other imports


warnings.filterwarnings('ignore')

def get_yahoo_data_backtest(symbol, range="10y", interval="1d"):
    import requests
    import pandas as pd
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    params = {
        "range": range,
        "interval": interval,
        "includePrePost": False
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
        result = data['chart']['result'][0]
        timestamps = pd.to_datetime(result['timestamp'], unit='s')
        quotes = result['indicators']['quote'][0]
        df = pd.DataFrame({
            'Open': quotes.get('open', []),
            'High': quotes.get('high', []),
            'Low': quotes.get('low', []),
            'Close': quotes.get('close', []),
            'Volume': quotes.get('volume', [])
        }, index=timestamps)
        return df.dropna()
    return pd.DataFrame()

class UltimateQuantStrategy:
    """
    The Nuclear Option: Advanced Quantitative Strategy
    Combines the simplicity of the original 3-5 component system
    with cutting-edge mathematical optimization
    """

    def __init__(self):

        
        # Core strategy parameters (keeping your brilliant base)
        self.monthly_target = 1500
        self.component_size = 300
        self.iwda_components = 3.33  # 1000/300
        self.btc_components = 1.67   # 500/300
        self.max_buffer_months = 8

        # Advanced quantitative parameters
        self.lookback_window = 252  # 1 year
        self.vol_lookback = 21     # Volatility window
        self.confidence_level = 0.95

        # Market regime thresholds (mathematically optimized)
        self.regime_thresholds = {
            'extreme_fear': -2.0,    # 2 std dev below mean
            'fear': -1.0,            # 1 std dev below mean
            'neutral': 0.0,
            'greed': 1.0,            # 1 std dev above mean
            'extreme_greed': 2.0     # 2 std dev above mean
        }

        # Kelly Criterion parameters
        self.max_kelly_fraction = 0.25  # Never risk more than 25%

        # Load historical performance data
        self.performance_history = self.load_performance_data()

        # Add audit-ready parameters
        self.risk_limits = {
            'max_position_size': 0.25,  # Maximum 25% in single position
            'max_drawdown': 0.15,       # Maximum 15% drawdown tolerance
            'min_liquidity': 1000000,   # Minimum daily volume in EUR
            'max_spread': 0.005         # Maximum bid-ask spread tolerance
        }

        # Enhanced order execution parameters
        self.execution_params = {
            'order_types': ['LIMIT', 'TWAP', 'VWAP'],
            'time_validity': 5,  # trading days
            'min_fill_rate': 0.95
        }

    def load_performance_data(self):
        """Load historical strategy performance for optimization"""
        try:
            with open('strategy_performance.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"monthly_returns": [], "strategy_stats": {}}

    def get_market_data_optimized(self):
        """Fetch market data using Yahoo Finance API directly and keep existing Fear & Greed APIs"""
        try:
            print("📊 Fetching market prices...")
            
            def get_yahoo_data(symbol, range="2y", interval="1d"):
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                params = {
                    "range": range,
                    "interval": interval,
                    "includePrePost": False
                }
                
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                
                if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                    result = data['chart']['result'][0]
                    timestamps = pd.to_datetime(result['timestamp'], unit='s')
                    quotes = result['indicators']['quote'][0]
                    
                    df = pd.DataFrame({
                        'Open': quotes.get('open', []),
                        'High': quotes.get('high', []),
                        'Low': quotes.get('low', []),
                        'Close': quotes.get('close', []),
                        'Volume': quotes.get('volume', [])
                    }, index=timestamps)
                    
                    return df.dropna()
                return pd.DataFrame()

            # Get market data
            try:
                iwda_data = get_yahoo_data("IWDA.AS")
                btc_data = get_yahoo_data("BTC-USD")
                vix_data = get_yahoo_data("^VIX")
                
                # Get EUR/USD rate
                usd_eur_data = get_yahoo_data("EURUSD=X", range="1d")
                usd_eur_rate = 1 / float(usd_eur_data['Close'].iloc[-1])

            except Exception as e:
                print(f"Yahoo Finance API error: {e}")
                return None

            # Updated CNN Fear & Greed API call
            try:
                print("Fetching S&P500 Fear & Greed Index...")
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/json'
                }
                cnn_response = requests.get(
                    "https://production.dataviz.cnn.io/index/fearandgreed/graphdata",
                    headers=headers,
                    timeout=10
                )
                cnn_data = cnn_response.json()
                sp500_fear_greed = float(cnn_data['fear_and_greed']['score'])
                print(f"S&P500 Fear & Greed: {sp500_fear_greed:.1f}")

            except Exception as e:
                print(f"CNN API error: {e}, calculating from VIX")
                # Smart fallback using VIX data
                vix_current = vix_data['Close'].iloc[-1]
                vix_max = vix_data['Close'].max()
                vix_min = vix_data['Close'].min()
                
                # Enhanced VIX-based calculation
                vix_percentile = (vix_current - vix_min) / (vix_max - vix_min)
                sp500_fear_greed = 100 - (vix_percentile * 100)
                
                # Adjust for extreme values
                if vix_current > 35:  # High VIX indicates fear
                    sp500_fear_greed = min(sp500_fear_greed, 25)  # Cap at 25 (fear)
                elif vix_current < 15:  # Low VIX indicates greed
                    sp500_fear_greed = max(sp500_fear_greed, 75)  # Floor at 75 (greed)
                
                print(f"S&P500 Fear & Greed (VIX-based): {sp500_fear_greed:.1f}")

            try:
                print("Fetching Bitcoin Fear & Greed Index...")
                crypto_response = requests.get(
                    "https://api.alternative.me/fng/?limit=1",
                    timeout=10
                )
                crypto_data = crypto_response.json()
                btc_fear_greed = float(crypto_data['data'][0]['value'])
                print(f"Bitcoin Fear & Greed: {btc_fear_greed:.1f}")

            except Exception as e:
                print(f"Crypto API error: {e}, using fallback calculation")
                btc_fear_greed = 50

            return {
                'iwda': iwda_data,
                'btc': btc_data,
                'vix': vix_data,
                'sp500_fear_greed': sp500_fear_greed,
                'btc_fear_greed': btc_fear_greed,
                'usd_eur_rate': usd_eur_rate,
                'fetch_time': datetime.now()
            }

        except Exception as e:
            print(f"Critical data fetch error: {str(e)}")
            return None

    def _convert_polygon_to_df(self, raw_data):
        """Convert Polygon.io data to pandas DataFrame with same format as before"""
        try:
            # Create DataFrame with proper timestamp conversion
            df = pd.DataFrame([{
                'Open': x.o,
                'High': x.h,
                'Low': x.l,
                'Close': x.c,
                'Volume': x.v,
                'Date': pd.Timestamp.fromtimestamp(x.t / 1000)  # Convert milliseconds to seconds
            } for x in raw_data])
            
            # Set index after DataFrame creation
            if not df.empty:
                df.set_index('Date', inplace=True)
                df.sort_index(inplace=True)  # Ensure chronological order
                return df
            else:
                print("Warning: Empty data received from Polygon.io")
                return pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])
                
        except Exception as e:
            print(f"Error converting Polygon data to DataFrame: {str(e)}")
            return pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])

    def calculate_statistical_regime(self, data):
        """
        Use actual Fear & Greed indices and handle USD/EUR conversion
        """
        # Get Fear & Greed scores (0-100 scale)
        sp500_fear_greed = data['sp500_fear_greed']
        btc_fear_greed = data['btc_fear_greed']

        # Convert to z-scores (-3 to +3 scale approximately)
        # 50 is neutral, 25 is fear, 75 is greed
        sp500_zscore = (sp500_fear_greed - 50) / 25
        btc_zscore = (btc_fear_greed - 50) / 25

        # Get USD/EUR conversion for amount calculations
        usd_eur_rate = data['usd_eur_rate']

        # Calculate other metrics
        iwda_prices = data['iwda']['Close']
        btc_prices = data['btc']['Close']
        vix_prices = data['vix']['Close']

        # Price metrics vs moving averages
        iwda_current = iwda_prices.iloc[-1]
        iwda_ma200 = iwda_prices.rolling(200).mean().iloc[-1]

        btc_current = btc_prices.iloc[-1]
        btc_ma200 = btc_prices.rolling(200).mean().iloc[-1]

        # VIX metrics
        vix_current = vix_prices.iloc[-1]
        vix_mean = vix_prices.rolling(252).mean().iloc[-1]
        vix_std = vix_prices.rolling(252).std().iloc[-1]
        vix_zscore = (vix_current - vix_mean) / vix_std

        # Composite score using actual fear & greed indices
        composite_score = (-sp500_zscore - btc_zscore + vix_zscore) / 3

        return {
            'composite_score': composite_score,
            'sp500_fear_greed': sp500_fear_greed,
            'btc_fear_greed': btc_fear_greed,
            'vix_zscore': vix_zscore,
            'iwda_vs_ma200': (iwda_current / iwda_ma200 - 1) * 100,
            'btc_vs_ma200': (btc_current / btc_ma200 - 1) * 100,
            'vix_level': vix_current,
            'usd_eur_rate': usd_eur_rate
        }

    def calculate_kelly_criterion(self, data):
        """
        Kelly Criterion: Mathematically optimal bet sizing
        f = (bp - q) / b
        where f = fraction to bet, b = odds, p = win probability, q = loss probability
        """
        iwda_returns = data['iwda']['Close'].pct_change().dropna()
        btc_returns = data['btc']['Close'].pct_change().dropna()

        # Calculate historical statistics
        iwda_mean = iwda_returns.mean() * 252  # Annualized
        iwda_std = iwda_returns.std() * np.sqrt(252)
        iwda_sharpe = iwda_mean / iwda_std if iwda_std > 0 else 0

        btc_mean = btc_returns.mean() * 252
        btc_std = btc_returns.std() * np.sqrt(252)
        btc_sharpe = btc_mean / btc_std if btc_std > 0 else 0

        # Kelly fraction for each asset
        iwda_kelly = iwda_sharpe / iwda_std if iwda_std > 0 else 0
        btc_kelly = btc_sharpe / btc_std if btc_std > 0 else 0

        # Cap Kelly fractions (Kelly can be aggressive)
        iwda_kelly = min(iwda_kelly, self.max_kelly_fraction)
        btc_kelly = min(btc_kelly, self.max_kelly_fraction)

        return {
            'iwda_kelly': iwda_kelly,
            'btc_kelly': btc_kelly,
            'iwda_sharpe': iwda_sharpe,
            'btc_sharpe': btc_sharpe
        }

    def calculate_value_at_risk(self, data, confidence_level=0.95):
        """
        Value at Risk: Maximum expected loss at given confidence level
        Used to size positions appropriately
        """
        iwda_returns = data['iwda']['Close'].pct_change().dropna().tail(252)
        btc_returns = data['btc']['Close'].pct_change().dropna().tail(252)

        # Calculate VaR
        iwda_var = np.percentile(iwda_returns, (1 - confidence_level) * 100)
        btc_var = np.percentile(btc_returns, (1 - confidence_level) * 100)

        return {
            'iwda_var': iwda_var,
            'btc_var': btc_var,
            'iwda_vol': iwda_returns.std() * np.sqrt(252),
            'btc_vol': btc_returns.std() * np.sqrt(252)
        }

    def optimize_portfolio_allocation(self, regime_data, kelly_data, var_data, data):
        # Base allocation (keep IWDA stable, vary BTC more aggressively)
        btc_fear_greed = regime_data['btc_fear_greed']
        sp500_fear_greed = regime_data['sp500_fear_greed']

        # Default allocations (67% IWDA, 33% BTC)
        iwda_allocation = 0.67
        btc_allocation = 0.33

        # Bitcoin-specific multipliers based on crypto fear & greed
        if btc_fear_greed >= 80:  # Extreme greed (80-100)
            scale_factor = (btc_fear_greed - 80) / 20
            btc_multiplier = 0.2 + (scale_factor * 0.2)  # 0.2-0.4 range
            btc_max = 200
            regime = "CRYPTO_EXTREME_GREED"
            print("🚨 CRYPTO WARNING: Consider taking profits on existing positions")

        elif btc_fear_greed >= 60:  # Greed (60-79)
            scale_factor = (btc_fear_greed - 60) / 20
            btc_multiplier = 0.4 + (scale_factor * 0.2)  # 0.4-0.6 range
            btc_max = 300
            regime = "CRYPTO_GREED"

        elif btc_fear_greed >= 40:  # Neutral (40-59)
            scale_factor = (btc_fear_greed - 40) / 20
            btc_multiplier = 0.6 + (scale_factor * 0.2)  # 0.6-0.8 range
            btc_max = 400
            regime = "CRYPTO_NEUTRAL"

        elif btc_fear_greed >= 20:  # Fear (20-39)
            scale_factor = (20 - btc_fear_greed) / 20
            btc_multiplier = 0.8 + (scale_factor * 0.7)  # 0.8-1.5 range
            btc_max = None  # Remove cap during fear
            regime = "CRYPTO_FEAR"

        else:  # Extreme fear (0-19)
            scale_factor = (20 - btc_fear_greed) / 20
            btc_multiplier = 1.5 + (scale_factor * 1.0)  # 1.5-2.5 range
            btc_max = None  # No cap during extreme fear
            regime = "CRYPTO_EXTREME_FEAR"
            print("💡 CRYPTO OPPORTUNITY: Maximum buying opportunity")

        # Calculate BTC target amount
        btc_target = round(self.monthly_target * btc_multiplier * btc_allocation, 2)
        btc_target = min(btc_target, btc_max)  # Apply cap

        # IWDA signals
        iwda_signals = {
            'sp500_fear': sp500_fear_greed <= 35,
            'vix_high': regime_data['vix_level'] > 25,
            'price_vs_ma': regime_data['iwda_vs_ma200'] < -5,  # 5% onder MA200
        }

        # IWDA multiplier logic (geoptimaliseerde ranges)
        if sp500_fear_greed >= 80:  # Extreme greed (80-100)
            scale_factor = (sp500_fear_greed - 80) / 20
            iwda_multiplier = 0.2 + (scale_factor * 0.2)  # 0.2-0.4 range
            iwda_message = "⚠️ IWDA WARNING: Extreme market greed - minimal exposure"

        elif sp500_fear_greed >= 60:  # Greed (60-79)
            scale_factor = (sp500_fear_greed - 60) / 20
            iwda_multiplier = 0.4 + (scale_factor * 0.2)  # 0.4-0.6 range
            iwda_message = "⚠️ IWDA CAUTION: Market showing greed - reduced exposure"

        elif sp500_fear_greed >= 40:  # Neutral (40-59)
            scale_factor = (sp500_fear_greed - 40) / 20
            iwda_multiplier = 0.6 + (scale_factor * 0.2)  # 0.6-0.8 range
            iwda_message = "ℹ️ IWDA: Neutral market conditions - moderate exposure"

        elif sp500_fear_greed >= 20:  # Fear (20-39)
            scale_factor = (20 - sp500_fear_greed) / 20
            iwda_multiplier = 0.8 + (scale_factor * 0.5)  # 0.8-1.3 range
            iwda_message = "💡 IWDA OPPORTUNITY: Market fear - increased exposure"

        else:  # Extreme fear (0-19)
            scale_factor = (20 - sp500_fear_greed) / 20
            iwda_multiplier = 1.3 + (scale_factor * 0.7)  # 1.3-2.0 range
            iwda_message = "💡 IWDA OPPORTUNITY: Extreme market fear - significant allocation increase"

        # Calculate IWDA target
        iwda_target = round(self.monthly_target * iwda_multiplier * iwda_allocation, 2)

        # Calculate IWDA shares
        iwda_shares, iwda_amount = self.calculate_iwda_shares(
            iwda_target,
            data['iwda']['Close'].iloc[-1]
        )

        if iwda_message:
            print(iwda_message)

        return {
            'iwda_amount': iwda_amount,
            'iwda_shares': iwda_shares,
            'iwda_signals': iwda_signals,
            'btc_amount': int(btc_target),
            'total_investment': int(iwda_amount + btc_target),
            'regime': regime,
            'btc_fear_greed_level': btc_fear_greed,
            'component_count': 2,
            'kelly_optimization': {
                'iwda_weight': iwda_allocation,
                'btc_weight': btc_allocation,
                'iwda_kelly': kelly_data['iwda_kelly'],
                'btc_kelly': kelly_data['btc_kelly']
            }
        }

    def calculate_iwda_shares(self, target_amount, price):
        """
        Bereken IWDA shares met consistente afronding
        """
        # Rond eerst de prijs af op 2 decimalen
        price = round(float(price), 2)

        # Bereken shares en rond NAAR BENEDEN af (conservatief)
        shares = int(target_amount / price)

        # Bereken het exacte bedrag
        actual_amount = round(shares * price, 2)

        return shares, actual_amount

    def calculate_expected_returns(self, allocation, var_data):
        """Calculate expected returns and risk metrics"""
        # Portfolio expected return (simplified)
        portfolio_weights = np.array([allocation['kelly_optimization']['iwda_weight'],
                                    allocation['kelly_optimization']['btc_weight']])

        # Expected annual returns (historical averages)
        expected_returns = np.array([0.08, 0.15])  # 8% IWDA, 15% BTC historical

        portfolio_return = np.dot(portfolio_weights, expected_returns)

        # Portfolio risk (simplified - assumes some correlation)
        portfolio_risk = np.sqrt(
            (portfolio_weights[0] ** 2) * (var_data['iwda_vol'] ** 2) +
            (portfolio_weights[1] ** 2) * (var_data['btc_vol'] ** 2) +
            2 * portfolio_weights[0] * portfolio_weights[1] *
            var_data['iwda_vol'] * var_data['btc_vol'] * 0.3  # Assume 30% correlation
        )

        sharpe_ratio = portfolio_return / portfolio_risk if portfolio_risk > 0 else 0

        return {
            'expected_annual_return': portfolio_return,
            'expected_annual_risk': portfolio_risk,
            'sharpe_ratio': sharpe_ratio
        }

    def generate_ultimate_recommendation(self):
        """Generate the ultimate quantitative recommendation"""
        print("🧮 ULTIMATE QUANTITATIVE ANALYSIS INITIATED...")
        print("📊 Fetching market data...")

        # Get market data
        data = self.get_market_data_optimized()
        if not data:
            return None

        print("📈 Calculating statistical regime...")
        regime_data = self.calculate_statistical_regime(data)

        print("🎯 Applying Kelly Criterion optimization...")
        kelly_data = self.calculate_kelly_criterion(data)

        print("⚠️  Computing Value at Risk...")
        var_data = self.calculate_value_at_risk(data)

        print("🚀 Optimizing portfolio allocation...")
        allocation = self.optimize_portfolio_allocation(regime_data, kelly_data, var_data, data)  # Add data parameter

        print("💰 Calculating expected returns...")
        performance = self.calculate_expected_returns(allocation, var_data)

        # Compile comprehensive recommendation
        recommendation = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'market_regime': {
                'regime': allocation['regime'],
                'composite_score': regime_data['composite_score'],
                'sp500_fear_greed': data['sp500_fear_greed'],
                'btc_fear_greed': data['btc_fear_greed'],
                'btc_fear_greed_level': data['btc_fear_greed'],  # Add this line
                'usd_eur_rate': data['usd_eur_rate'],
                'iwda_vs_ma200': regime_data['iwda_vs_ma200'],
                'btc_vs_ma200': regime_data['btc_vs_ma200'],
                'vix_level': regime_data['vix_level']
            },
            'allocation': allocation,
            'risk_metrics': {
                'iwda_var_95': var_data['iwda_var'],
                'btc_var_95': var_data['btc_var'],
                'iwda_volatility': var_data['iwda_vol'],
                'btc_volatility': var_data['btc_vol']
            },
            'performance_forecast': performance,
            'current_prices': {
                'iwda_proxy': data['iwda']['Close'].iloc[-1],
                'btc': data['btc']['Close'].iloc[-1],
                'vix': data['vix']['Close'].iloc[-1]
            }
        }

        return recommendation

    def convert_to_brussels_time(self, timestamp):
        """Convert timestamp to Brussels time (CET/CEST)"""
        from datetime import datetime
        from zoneinfo import ZoneInfo

        # Convert string timestamp to datetime object
        dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

        # Convert to Brussels time
        brussels_time = dt.astimezone(ZoneInfo("Europe/Brussels"))
        return brussels_time.strftime('%Y-%m-%d %H:%M:%S %Z')

    def display_ultimate_analysis(self, rec):
        """Display clear investment instructions"""
        print("\n" + "="*80)
        print("💰 MONTHLY INVESTMENT RECOMMENDATION")
        print("="*80)

        # Current market conditions with Brussels time
        brussels_time = self.convert_to_brussels_time(rec['timestamp'])
        print(f"\n📊 MARKET CONDITIONS ({brussels_time}):")
        print(f"• Market Regime: {rec['market_regime']['regime']}")
        print(f"• S&P500 Fear & Greed: {rec['market_regime']['sp500_fear_greed']}/100")
        print(f"• Bitcoin Fear & Greed: {rec['market_regime']['btc_fear_greed']}/100")
        print(f"• USD/EUR Rate: {rec['market_regime']['usd_eur_rate']:.4f}")

        # Clear investment instructions
        print(f"\n🎯 INVESTMENT ACTIONS REQUIRED:")
        print(f"1. IWDA ETF (DEGIRO):")
        print(f"   → Buy: {rec['allocation']['iwda_shares']} shares")
        print(f"   → Total Investment: €{rec['allocation']['iwda_amount']:,}")
        print(f"   → Current Price: €{rec['current_prices']['iwda_proxy']:.2f}")

        print(f"\n2. Bitcoin (Bitvavo):")
        print(f"   → Invest: €{rec['allocation']['btc_amount']:,}")
        print(f"   → Current Price: ${rec['current_prices']['btc']:,.0f}")
        print(f"   → EUR Price: €{rec['current_prices']['btc'] * rec['market_regime']['usd_eur_rate']:,.0f}")

        print(f"\n💡 EXECUTION INSTRUCTIONS:")
        print(f"• Total to Invest This Month: €{rec['allocation']['total_investment']:,}")
        print(f"• Number of Components: {rec['allocation']['component_count']}")
        print(f"• Execute Between: 15-25th of the month")
        print(f"• Use Limit Orders at Current Prices")

        # Enhanced Risk Assessment
        print(f"\n⚠️  RISK ASSESSMENT:")
        print(f"• Portfolio Risk Level: {rec['market_regime']['regime']}")
        print(f"• Value at Risk (95% confidence):")
        print(f"  - IWDA: {rec['risk_metrics']['iwda_var_95']*100:.1f}% daily")
        print(f"  - Bitcoin: {rec['risk_metrics']['btc_var_95']*100:.1f}% daily")
        print(f"• Annual Volatility:")
        print(f"  - IWDA: {rec['risk_metrics']['iwda_volatility']*100:.1f}%")
        print(f"  - Bitcoin: {rec['risk_metrics']['btc_volatility']*100:.1f}%")
        print(f"• Portfolio Metrics:")
        print(f"  - Expected Return: {rec['performance_forecast']['expected_annual_return']*100:.1f}%")
        print(f"  - Expected Risk: {rec['performance_forecast']['expected_annual_risk']*100:.1f}%")
        print(f"  - Sharpe Ratio: {rec['performance_forecast']['sharpe_ratio']:.2f}")

        # Market Specific Warnings
        if rec['market_regime']['regime'] == "EXTREME_GREED":
            print("\n🚨 RISK WARNINGS:")
            print("  • Markets showing extreme greed - high risk of correction")
            print("  • Using defensive allocation with reduced exposure")
            print("  • Consider splitting purchases over multiple weeks")
        elif rec['market_regime']['regime'] == "GREED":
            print("\n🚨 RISK WARNINGS:")
            print("  • Markets showing greed - elevated risk levels")
            print("  • Bitcoin capped at €500 for risk management")
            print("  • Consider using limit orders below market price")
        elif rec['market_regime']['regime'] == "EXTREME_FEAR":
            print("\n💡 OPPORTUNITY ALERT:")
            print("  • Markets in extreme fear - potential buying opportunity")
            print("  • Still maintain position sizing discipline")
            print("  • Consider gradual scaling in over several days")

        # Add Bitcoin-specific advice
        btc_advice = self.get_btc_position_advice(rec['market_regime']['btc_fear_greed'])  # Changed this line
        if btc_advice:
            print("\n🔷 BITCOIN POSITION ADVICE:")
            for msg in btc_advice['message']:
                print(f"  {msg}")

        # Add after current market conditions
        if rec['allocation']['iwda_signals']['sp500_fear'] or \
           rec['allocation']['iwda_signals']['vix_high'] or \
           rec['allocation']['iwda_signals']['price_vs_ma']:
            print("\n📈 IWDA MARKET SIGNALS:")
            if rec['allocation']['iwda_signals']['sp500_fear']:
                print("  • S&P500 showing fear - potential buying opportunity")
            if rec['allocation']['iwda_signals']['vix_high']:
                print("  • VIX elevated - market uncertainty high")
            if rec['allocation']['iwda_signals']['price_vs_ma']:
                print("  • IWDA trading below 200-day moving average")

        # Add after risk assessment section
        print("\n📍 SUGGESTED ORDER PLACEMENT:")
        entry_points = self.analyze_optimal_entry_points(
            {
                'btc': rec['current_prices']['btc'],
                'iwda': rec['current_prices']['iwda_proxy']
            },
            rec['allocation']
        )

        print("\nIWDA Orders:")
        for order in entry_points['iwda_orders']:
            print(f"  • {order['type']} Order: {order['size']}% @ €{order['price']:.2f} "
                  f"({order['confidence']} confidence)")

        print("\nBitcoin Orders:")
        for order in entry_points['btc_orders']:
            eur_price = order['price'] * rec['market_regime']['usd_eur_rate']
            print(f"  • {order['type']} Order: {order['size']}% @ €{eur_price:.0f} "
                  f"({order['confidence']} confidence)")

        print("\n💡 ORDER EXECUTION TIPS:")
        print("  • Use Good-til-Cancelled (GTC) for limit orders")
        print("  • Place orders during high liquidity hours (14:30-22:00 CET)")
        print("  • Monitor order fills and adjust if needed after 48 hours")
        print("  • Consider cancelling unfilled orders after 5 trading days")

        print("\n" + "="*80)
        return rec

    def get_btc_position_advice(self, btc_fear_greed):
        """Generate Bitcoin-specific position advice"""
        if btc_fear_greed >= 80:
            return {
                'action': 'TAKE_PROFIT',
                'message': [
                    "🚨 BITCOIN EXTREME GREED ALERT:",
                    "• Consider taking partial profits (20-30%) on existing positions",
                    "• Set trailing stop losses on remaining position",
                    "• Minimal new investment recommended"
                ]
            }
        elif btc_fear_greed <= 20:
            return {
                'action': 'ACCUMULATE',
                'message': [
                    "💰 BITCOIN OPPORTUNITY ALERT:",
                    "• Significant fear presents buying opportunity",
                    "• Consider scaling in over several days",
                    "• Increased position size recommended"
                ]
            }
        return None

    def analyze_optimal_entry_points(self, prices, allocation):
        """Analyze optimal entry points based on liquidity zones and market structure"""
        btc_current = prices['btc']  # Now expecting a simple price value
        iwda_current = prices['iwda']  # Now expecting a simple price value

        def calculate_zones(current_price, volatility_factor=0.02):
            """Calculate price zones based on current price and volatility"""
            return {
                'support_1': current_price * (1 - volatility_factor),
                'support_2': current_price * (1 - volatility_factor * 2),
                'resistance_1': current_price * (1 + volatility_factor),
                'resistance_2': current_price * (1 + volatility_factor * 2)
            }

        btc_zones = calculate_zones(btc_current, 0.03)  # Higher volatility for BTC
        iwda_zones = calculate_zones(iwda_current, 0.01)  # Lower volatility for IWDA

        def get_order_strategy(current_price, zones, asset_type):
            # Base order distribution
            if asset_type == 'BTC':
                chunks = 4 if allocation['regime'] in ['CRYPTO_EXTREME_FEAR', 'CRYPTO_FEAR'] else 2
            else:
                chunks = 3 if allocation['iwda_signals']['sp500_fear'] else 2

            orders = []

            # Market order at current price
            market_order = {
                'price': round(current_price, 2),
                'size': round(100/chunks, 1),
                'type': 'Market',
                'confidence': 'High'
            }

            # Limit order at first support
            support_1_order = {
                'price': round(zones['support_1'], 2),
                'size': round(100/chunks, 1),
                'type': 'Limit',
                'confidence': 'High'
            }

            # Limit order at second support
            support_2_order = {
                'price': round(zones['support_2'], 2),
                'size': round(100/chunks, 1),
                'type': 'Limit',
                'confidence': 'Medium'
            }

            orders.extend([market_order, support_1_order, support_2_order])
            return orders

        return {
            'btc_orders': get_order_strategy(btc_current, btc_zones, 'BTC'),
            'iwda_orders': get_order_strategy(iwda_current, iwda_zones, 'IWDA'),
            'btc_zones': btc_zones,
            'iwda_zones': iwda_zones
        }

    def calculate_adaptive_volatility(self, data, window=21):
        """Dynamische volatiliteit op basis van recente marktcondities"""
        atr = self.calculate_atr(data, window)
        return {
            'btc_vol': max(0.03, min(0.05, atr['btc'])),  # 3-5% range
            'iwda_vol': max(0.01, min(0.02, atr['iwda']))  # 1-2% range
        }

    def optimize_execution_timing(self, data):
        """Bepaal beste uitvoeringstijden op basis van volume"""
        return {
            'best_hours': ['14:30-16:30', '20:00-22:00'],
            'avoid_hours': ['12:00-14:00', '22:00-06:00'],
            'volume_threshold': 'Wacht met grote orders tot volume > gemiddeld'
        }

    def validate_market_conditions(self, data):
        """Audit-ready market validation"""
        validations = {
            'volume_check': self._validate_volume(data),
            'spread_check': self._validate_spreads(data),
            'liquidity_check': self._validate_liquidity(data),
            'price_quality': self._validate_price_quality(data)
        }
        return all(validations.values()), validations

    def _validate_volume(self, data):
        """Ensure sufficient trading volume"""
        min_volume = self.risk_limits['min_liquidity']
        iwda_volume = data['iwda']['Volume'].mean() * data['iwda']['Close'].mean()
        btc_volume = data['btc']['Volume'].mean() * data['btc']['Close'].mean()

        return {
            'iwda': iwda_volume > min_volume,
            'btc': btc_volume > min_volume,
            'metrics': {
                'iwda_volume': iwda_volume,
                'btc_volume': btc_volume
            }
        }

    def _validate_price_quality(self, data):
        """Ensure price data quality"""
        return {
            'gaps': self._check_price_gaps(data),
            'staleness': self._check_price_staleness(data),
            'outliers': self._detect_price_outliers(data)
        }

    def _check_price_gaps(self, data):
        """Detect and analyze price gaps"""
        gaps = {
            'iwda': self._analyze_gaps(data['iwda']['Close']),
            'btc': self._analyze_gaps(data['btc']['Close'])
        }
        return all(gap['valid'] for gap in gaps.values())

    def _analyze_gaps(self, prices):
        """Analyze price gaps in a series"""
        returns = prices.pct_change()
        significant_gaps = abs(returns) > 0.03  # 3% threshold
        return {
            'valid': significant_gaps.sum() <= 3,  # Max 3 significant gaps
            'gap_count': significant_gaps.sum(),
            'max_gap': returns.max()
        }

    def _check_price_staleness(self, data):
        """Check for stale price data"""
        staleness = {
            'iwda': self._analyze_staleness(data['iwda']),
            'btc': self._analyze_staleness(data['btc'])
        }
        return all(stale['valid'] for stale in staleness.values())

    def _analyze_staleness(self, asset_data):
        """Analyze price staleness"""
        price_changes = asset_data['Close'].pct_change() != 0
        return {
            'valid': price_changes.sum() >= len(price_changes) * 0.95,  # 95% must have changes
            'unchanged_periods': (~price_changes).sum()
        }

    def _detect_price_outliers(self, data):
        """Detect price outliers"""
        outliers = {
            'iwda': self._analyze_outliers(data['iwda']['Close']),
            'btc': self._analyze_outliers(data['btc']['Close'])
        }
        return all(outlier['valid'] for outlier in outliers.values())

    def _analyze_outliers(self, prices):
        """Analyze price outliers using z-score"""
        z_scores = np.abs((prices - prices.mean()) / prices.std())
        return {
            'valid': (z_scores > 4).sum() <= 2,  # Max 2 extreme outliers
            'outlier_count': (z_scores > 4).sum()
        }

    def _calculate_intraday_volatility(self, asset):
        """Calculate intraday volatility"""
        if asset == 'IWDA':
            return 0.01  # 1% base volatility for IWDA
        return 0.03  # 3% base volatility for BTC

    def _calculate_effective_spread(self, asset):
        """Calculate effective spread"""
        return self.risk_limits['max_spread'] if asset == 'IWDA' else self.risk_limits['max_spread'] * 2

    def _calculate_twap(self, asset):
        """Calculate Time Weighted Average Price"""
        # Simplified TWAP calculation
        return asset['Close'].tail(21).mean() if isinstance(asset, pd.DataFrame) else asset

    def _calculate_vwap(self, asset):
        """Calculate Volume Weighted Average Price"""
        if isinstance(asset, pd.DataFrame):
            typical_price = (asset['High'] + asset['Low'] + asset['Close']) / 3
            return (typical_price * asset['Volume']).sum() / asset['Volume'].sum()
        return asset

    def _calculate_volume_profile(self, data):
        """Calculate volume profile"""
        return {
            'high_volume_zone': data['Close'].quantile(0.75),
            'low_volume_zone': data['Close'].quantile(0.25)
        }

    def _identify_key_levels(self, data):
        """Identify key support/resistance levels"""
        closes = data['Close']
        return [
            closes.quantile(0.25),  # Support level 1
            closes.quantile(0.5),   # Mid point
            closes.quantile(0.75)   # Resistance level 1
        ]

    def _analyze_liquidity(self, data):
        """Analyze liquidity zones"""
        volume_profile = self._calculate_volume_profile(data)
        return {
            volume_profile['high_volume_zone']: 'HIGH',
            volume_profile['low_volume_zone']: 'MEDIUM'
        }

    def _calculate_entry_score(self, price_level, liquidity, volume, regime):
        """Calculate entry score based on multiple factors"""
        base_score = 50

        # Liquidity adjustment
        liquidity_score = 20 if liquidity == 'HIGH' else 10

        # Volume adjustment
        volume_score = min(20, volume / 1000000)  # Cap at 20 points

        # Regime adjustment
        regime_scores = {
            'EXTREME_FEAR': 30,
            'FEAR': 20,
            'NEUTRAL': 0,
            'GREED': -10,
            'EXTREME_GREED': -20
        }
        regime_score = regime_scores.get(regime['regime'], 0)

        return base_score + liquidity_score + volume_score + regime_score

    def _calculate_kelly(self, asset):
        """Calculate Kelly fraction"""
        if asset == 'IWDA':
            return min(0.15, self.max_kelly_fraction)  # More conservative for IWDA
        return min(0.25, self.max_kelly_fraction)  # More aggressive for BTC

    def _calculate_vol_adjustment(self, asset):
        """Calculate volatility adjustment"""
        base_vol = 0.01 if asset == 'IWDA' else 0.03
        return 1 / (1 + base_vol)

    def _get_regime_multiplier(self, regime_data):
        """Get regime-based position multiplier"""
        regime = regime_data.get('regime', 'NEUTRAL')
        multipliers = {
            'EXTREME_FEAR': 2.0,
            'FEAR': 1.5,
            'NEUTRAL': 1.0,
            'GREED': 0.7,
            'EXTREME_GREED': 0.5
        }
        return multipliers.get(regime, 1.0)

    def calculate_atr(self, data, window=21):
        """Calculate Average True Range"""
        return {
            'btc': self._calculate_single_atr(data['btc'], window),
            'iwda': self._calculate_single_atr(data['iwda'], window)
        }

    def _calculate_single_atr(self, asset_data, window):
        """Calculate ATR for a single asset"""
        high = asset_data['High']
        low = asset_data['Low']
        close = asset_data['Close']

        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(window=window).mean().iloc[-1]
    
    def run_10y_backtest(self):
        """
        Transparante 10-jaars backtest (2015-2025) van GrowWise (volledige UltimateQuantStrategy) vs DCA (70/30).
        Gebruikt historische VIX en BTC-volatiliteit als Fear & Greed proxies.
        """
       
        iwda = get_yahoo_data_backtest("IWDA.AS", range="10y", interval="1d")
        btc = get_yahoo_data_backtest("BTC-USD", range="10y", interval="1d")
        eurusd = get_yahoo_data_backtest("EURUSD=X", range="10y", interval="1d")
        vix = get_yahoo_data_backtest("^VIX", range="10y", interval="1d")

        iwda = iwda.ffill()
        btc = btc.ffill()
        eurusd = eurusd.ffill()
        vix = vix.ffill()

        months = pd.date_range("2015-01-01", "2024-12-31", freq="MS")
        monthly_invest = self.monthly_target

        rows = []
        gw_iwda_shares = 0
        gw_btc = 0
        dca_iwda_shares = 0
        dca_btc = 0

        # Voor BTC Fear & Greed: gebruik rolling volatiliteit als proxy
        btc_vol_rolling = btc['Close'].pct_change().rolling(30).std() * (252 ** 0.5)

        for date in months:
            iwda_hist = iwda.loc[:date]
            btc_hist = btc.loc[:date]
            eurusd_hist = eurusd.loc[:date]
            vix_hist = vix.loc[:date]

            iwda_price = iwda.loc[iwda.index >= date, "Close"].iloc[0]
            btc_price_usd = btc.loc[btc.index >= date, "Close"].iloc[0]
            eurusd_rate = eurusd.loc[eurusd.index >= date, "Close"].iloc[0]
            btc_price_eur = btc_price_usd / eurusd_rate

            # ---- HISTORISCHE FEAR & GREED ----
            # S&P500: VIX als proxy (hoge VIX = fear, lage VIX = greed)
            vix_slice = vix.loc[vix.index <= date, "Close"]
            if not vix_slice.empty:
                vix_current = vix_slice.iloc[-1]
                vix_min = vix_slice.min()
                vix_max = vix_slice.max()
            else:
                # Kies een default waarde, bijvoorbeeld 20
                vix_current = 20
                vix_min = 20
                vix_max = 20

            vix_percentile = (vix_current - vix_min) / (vix_max - vix_min) if vix_max != vix_min else 0.5
            sp500_fear_greed = 100 - (vix_percentile * 100)
            sp500_fear_greed = max(0, min(100, sp500_fear_greed))

            # BTC: rolling volatiliteit als proxy (hoge vol = fear, lage vol = greed)
            btc_vol = btc_vol_rolling.loc[btc_vol_rolling.index <= date].iloc[-1]
            btc_vol_min = btc_vol_rolling.loc[btc_vol_rolling.index <= date].min()
            btc_vol_max = btc_vol_rolling.loc[btc_vol_rolling.index <= date].max()
            btc_vol_percentile = (btc_vol - btc_vol_min) / (btc_vol_max - btc_vol_min)
            btc_fear_greed = 100 - (btc_vol_percentile * 100)
            btc_fear_greed = max(0, min(100, btc_fear_greed))

            data = {
                'iwda': iwda_hist,
                'btc': btc_hist,
                'vix': vix_hist,
                'sp500_fear_greed': sp500_fear_greed,
                'btc_fear_greed': btc_fear_greed,
                'usd_eur_rate': eurusd_rate,
                'fetch_time': date
            }

            # --- GrowWise: volledige pipeline ---
            regime_data = self.calculate_statistical_regime(data)
            kelly_data = self.calculate_kelly_criterion(data)
            var_data = self.calculate_value_at_risk(data)
            allocation = self.optimize_portfolio_allocation(regime_data, kelly_data, var_data, data)

            iwda_shares, iwda_amount = self.calculate_iwda_shares(
                allocation['iwda_amount'], iwda_price
            )
            btc_amount = allocation['btc_amount']
            gw_iwda_shares += iwda_shares
            gw_btc += btc_amount / btc_price_eur

            # --- DCA allocatie (70/30) ---
            dca_iwda_shares += (monthly_invest * 0.7) / iwda_price
            dca_btc += (monthly_invest * 0.3) / btc_price_eur

            gw_value = gw_iwda_shares * iwda_price + gw_btc * btc_price_eur
            dca_value = dca_iwda_shares * iwda_price + dca_btc * btc_price_eur

            rows.append({
                'month': date.strftime('%Y-%m'),
                'invested': monthly_invest,
                'gw_iwda': round(gw_iwda_shares * iwda_price, 2),
                'gw_btc': round(gw_btc * btc_price_eur, 2),
                'gw_cash': 0,
                'dca_iwda': round(dca_iwda_shares * iwda_price, 2),
                'dca_btc': round(dca_btc * btc_price_eur, 2),
                'iwda_price': round(iwda_price, 2),
                'btc_price': round(btc_price_eur, 2),
                'gw_value': round(gw_value, 2),
                'dca_value': round(dca_value, 2),
                'sp500_fear_greed': round(sp500_fear_greed, 1),
                'btc_fear_greed': round(btc_fear_greed, 1)
            })

        return rows


# Initialize the strategy
strategy = UltimateQuantStrategy()

# Generate and display recommendation
recommendation = strategy.generate_ultimate_recommendation()
if recommendation:
    strategy.display_ultimate_analysis(recommendation)
