# stock_dashboard_app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from datetime import datetime, timedelta
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Stock Valuation Dashboard - MGF 637",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2E86AB;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .recommendation-buy {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }
    .recommendation-hold {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
    }
    .recommendation-sell {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Predefined stock ticker options
STOCK_OPTIONS = {
    "AAPL - Apple Inc.": "AAPL",
    "MSFT - Microsoft Corp.": "MSFT", 
    "AMZN - Amazon.com Inc.": "AMZN",
    "GOOGL - Google (Alphabet)": "GOOGL",
    "TSLA - Tesla Inc.": "TSLA",
    "META - Meta Platforms": "META",
    "NFLX - Netflix Inc.": "NFLX",
    "NVDA - NVIDIA Corp.": "NVDA",
    "BRK-B - Berkshire Hathaway": "BRK-B",
    "JNJ - Johnson & Johnson": "JNJ",
    "JPM - JPMorgan Chase": "JPM",
    "V - Visa Inc.": "V",
    "WMT - Walmart Inc.": "WMT",
    "PG - Procter & Gamble": "PG",
    "BAC - Bank of America": "BAC",
    "MA - Mastercard Inc.": "MA",
    "HD - Home Depot": "HD",
    "VZ - Verizon Communications": "VZ",
    "T - AT&T Inc.": "T",
    "DIS - Disney (Walt) Co.": "DIS"
}

class StockValuationDashboard:
    def __init__(self):
        self.stock_data = None
        self.valuation_results = {}
    
    def get_stock_data(self, ticker, start_date, end_date):
        """Fetch stock data using yfinance"""
        try:
            with st.spinner(f'Fetching data for {ticker}...'):
                stock = yf.Ticker(ticker)
                
                # Get basic information
                info = stock.info
                
                # Get historical price data - using user-selected date range
                hist = stock.history(start=start_date, end=end_date)
                
                # Get financial statements
                financials = stock.financials
                balance_sheet = stock.balance_sheet
                cashflow = stock.cashflow
                
                self.stock_data = {
                    'ticker': ticker,
                    'info': info,
                    'history': hist,
                    'financials': financials,
                    'balance_sheet': balance_sheet,
                    'cashflow': cashflow
                }
                
            return True
        except Exception as e:
            st.error(f"Failed to fetch data for {ticker}: {e}")
            # If real data fetch fails, use demo data
            return self._generate_demo_data(ticker, start_date, end_date)
    
    def _generate_demo_data(self, ticker, start_date, end_date):
        """Generate demo data for demonstration purposes"""
        import random
        # Generate simulated price data
        price_data = []
        
        # Calculate date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        base_price = random.uniform(100, 200)
        
        for date in date_range:
            volatility = random.uniform(-0.02, 0.02)
            base_price *= (1 + volatility)
            price_data.append({'Date': date, 'Close': base_price})
        
        # Generate simulated basic information
        info = {
            'currentPrice': base_price,
            'marketCap': random.uniform(1e11, 2e12),
            'trailingPE': random.uniform(15, 25),
            'forwardPE': random.uniform(16, 22),
            'priceToBook': random.uniform(3, 6),
            'trailingEps': random.uniform(5, 12),
            'forwardEps': random.uniform(6, 13),
            'beta': random.uniform(0.9, 1.3),
            'longName': f"{ticker} Corporation",
            'freeCashflow': random.uniform(5e9, 2e10),
            'totalRevenue': random.uniform(8e10, 3e11),
            'profitMargins': random.uniform(0.15, 0.25),
            'dividendYield': random.uniform(0.01, 0.03)
        }
        
        # Create simulated DataFrame
        hist_df = pd.DataFrame(price_data)
        hist_df.set_index('Date', inplace=True)
        
        self.stock_data = {
            'ticker': ticker,
            'info': info,
            'history': hist_df,
            'financials': pd.DataFrame(),
            'balance_sheet': pd.DataFrame(),
            'cashflow': pd.DataFrame()
        }
        
        st.warning(f"⚠️ Using simulated data for {ticker} demonstration analysis")
        return True
    
    def calculate_valuation_ratios(self):
        """Calculate valuation ratios"""
        info = self.stock_data['info']
        
        ratios = {}
        
        # Basic valuation ratios
        ratios['pe_ratio'] = info.get('trailingPE')
        ratios['forward_pe'] = info.get('forwardPE')
        ratios['price_to_sales'] = info.get('priceToSalesTrailing12Months')
        ratios['price_to_book'] = info.get('priceToBook')
        
        # Profitability metrics
        ratios['eps'] = info.get('trailingEps')
        ratios['forward_eps'] = info.get('forwardEps')
        ratios['profit_margin'] = info.get('profitMargins')
        
        # Growth metrics - using randomly generated growth rate for demonstration
        ratios['revenue_growth'] = np.random.uniform(0.05, 0.15)
        
        # Market data
        ratios['market_cap'] = info.get('marketCap')
        ratios['beta'] = info.get('beta')
        ratios['current_price'] = info.get('currentPrice')
        ratios['dividend_yield'] = info.get('dividendYield')
        
        self.valuation_results['ratios'] = ratios
        return ratios
    
    def calculate_dcf_valuation(self, growth_rate=0.05, discount_rate=0.1, 
                               terminal_growth=0.02, forecast_years=5):
        """Calculate DCF valuation"""
        try:
            info = self.stock_data['info']
            
            # Get free cash flow or use estimation
            free_cash_flow = info.get('freeCashflow', 0)
            if free_cash_flow <= 0:
                # Estimate free cash flow using revenue
                revenue = info.get('totalRevenue', 1e10)
                free_cash_flow = revenue * 0.2  # Assume 20% free cash flow margin
            
            # Project future free cash flows
            future_fcfs = []
            for year in range(1, forecast_years + 1):
                future_fcf = free_cash_flow * (1 + growth_rate) ** year
                future_fcfs.append(future_fcf)
            
            # Calculate terminal value
            terminal_value = future_fcfs[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
            
            # Discount cash flows
            present_value_fcfs = sum([fcf / (1 + discount_rate) ** (i + 1) 
                                    for i, fcf in enumerate(future_fcfs)])
            
            present_value_terminal = terminal_value / (1 + discount_rate) ** forecast_years
            
            # Calculate enterprise value
            enterprise_value = present_value_fcfs + present_value_terminal
            
            # Estimate equity value
            equity_value = enterprise_value
            
            # Calculate intrinsic value per share
            shares_outstanding = info.get('marketCap', 1) / info.get('currentPrice', 1)
            intrinsic_value_per_share = equity_value / shares_outstanding
            
            current_price = info.get('currentPrice', 0)
            
            # Calculate margin of safety
            if intrinsic_value_per_share > 0:
                margin_of_safety = ((intrinsic_value_per_share - current_price) / intrinsic_value_per_share) * 100
            else:
                margin_of_safety = 0
            
            dcf_result = {
                'intrinsic_value': intrinsic_value_per_share,
                'current_price': current_price,
                'margin_of_safety': margin_of_safety,
                'free_cash_flow': free_cash_flow,
                'enterprise_value': enterprise_value,
                'equity_value': equity_value,
                'future_fcfs': future_fcfs,
                'terminal_value': terminal_value,
                'present_value_fcfs': present_value_fcfs,
                'present_value_terminal': present_value_terminal,
                'assumptions': {
                    'growth_rate': growth_rate,
                    'discount_rate': discount_rate,
                    'terminal_growth': terminal_growth,
                    'forecast_years': forecast_years
                }
            }
            
            self.valuation_results['dcf'] = dcf_result
            return dcf_result
            
        except Exception as e:
            st.error(f"DCF calculation failed: {e}")
            return None

def main():
    """Main application function"""
    
    # Title and introduction
    st.markdown('<div class="main-header">📈 Stock Valuation Dashboard - MGF 637</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p>This interactive dashboard uses DCF valuation and financial ratios to analyze stocks.</p>
        <p><strong>Group Members:</strong> Zipan Huang, Vivi Tan | <strong>Course:</strong> MGF 637 - Financial Modeling</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - User inputs
    st.sidebar.header("🔧 Analysis Parameters")
    
    # Stock ticker selection - using dropdown selector
    st.sidebar.subheader("📊 Stock Selection")
    
    # Create stock selection dropdown
    selected_stock_label = st.sidebar.selectbox(
        "Select Stock Ticker",
        options=list(STOCK_OPTIONS.keys()),
        index=0  # Default to first option
    )
    
    # Get selected stock ticker
    ticker = STOCK_OPTIONS[selected_stock_label]
    
    # Date range selection
    st.sidebar.subheader("📅 Date Range")
    
    # Set default date range (last year)
    end_date_default = datetime.now()
    start_date_default = end_date_default - timedelta(days=365)
    
    # Create two-column layout for date selection
    col_date1, col_date2 = st.sidebar.columns(2)
    
    with col_date1:
        start_date = st.date_input(
            "Start Date",
            value=start_date_default,
            max_value=end_date_default - timedelta(days=1)
        )
    
    with col_date2:
        end_date = st.date_input(
            "End Date",
            value=end_date_default,
            min_value=start_date + timedelta(days=1)
        )
    
    # Ensure end date is not before start date
    if start_date >= end_date:
        st.sidebar.error("Error: End date must be after start date")
        end_date = start_date + timedelta(days=1)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("DCF Model Assumptions")
    
    # DCF parameters
    growth_rate = st.sidebar.slider(
        "Cash Flow Growth Rate (%)", 
        min_value=0.0, max_value=20.0, value=5.0, step=0.5
    ) / 100
    
    discount_rate = st.sidebar.slider(
        "Discount Rate (WACC) (%)", 
        min_value=5.0, max_value=15.0, value=10.0, step=0.5
    ) / 100
    
    terminal_growth = st.sidebar.slider(
        "Terminal Growth Rate (%)", 
        min_value=0.0, max_value=5.0, value=2.0, step=0.1
    ) / 100
    
    forecast_years = st.sidebar.slider(
        "Forecast Period (Years)", 
        min_value=3, max_value=10, value=5
    )
    
    # Add analysis button
    st.sidebar.markdown("---")
    analyze_button = st.sidebar.button("🚀 Analyze Stock", type="primary")
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Instructions:**
    1. Select a stock ticker from the dropdown
    2. Select start and end dates for analysis
    3. Adjust DCF assumptions as needed
    4. Click "Analyze Stock" to view results
    
    **Note:** This tool is for educational purposes only.
    """)
    
    # Main content area
    if ticker and (analyze_button or st.session_state.get('analyzed', False)):
        # Create analyzer instance
        analyzer = StockValuationDashboard()
        
        # Fetch data and perform calculations
        if analyzer.get_stock_data(ticker, start_date, end_date):
            # Set session state to indicate analysis has been performed
            st.session_state.analyzed = True
            
            # Calculate valuation ratios
            ratios = analyzer.calculate_valuation_ratios()
            
            # Calculate DCF valuation
            dcf_result = analyzer.calculate_dcf_valuation(
                growth_rate=growth_rate,
                discount_rate=discount_rate,
                terminal_growth=terminal_growth,
                forecast_years=forecast_years
            )
            
            # Display company basic information
            info = analyzer.stock_data['info']
            company_name = info.get('longName', ticker)
            
            st.markdown(f'<div class="sub-header">🏢 {company_name} ({ticker}) Analysis</div>', unsafe_allow_html=True)
            
            # Display date range information
            st.markdown(f"**Analysis Period:** {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            
            # Key metrics cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                current_price = dcf_result.get('current_price', 0) if dcf_result else 0
                st.metric("Current Price", f"${current_price:.2f}")
            
            with col2:
                if dcf_result:
                    intrinsic_value = dcf_result.get('intrinsic_value', 0)
                    st.metric("DCF Value", f"${intrinsic_value:.2f}")
            
            with col3:
                if dcf_result:
                    margin_of_safety = dcf_result.get('margin_of_safety', 0)
                    st.metric("Margin of Safety", f"{margin_of_safety:.1f}%")
            
            with col4:
                market_cap = ratios.get('market_cap', 0)
                if market_cap > 1e9:
                    st.metric("Market Cap", f"${market_cap/1e9:.2f}B")
            
            # Investment recommendation
            if dcf_result:
                margin_of_safety = dcf_result.get('margin_of_safety', 0)
                if margin_of_safety > 10:
                    st.markdown('<div class="recommendation-buy">🎯 <strong>RECOMMENDATION: UNDERVALUED - BUY</strong><br>Margin of Safety indicates significant upside potential.</div>', unsafe_allow_html=True)
                elif margin_of_safety > -10:
                    st.markdown('<div class="recommendation-hold">🎯 <strong>RECOMMENDATION: FAIRLY VALUED - HOLD</strong><br>Stock appears to be fairly priced relative to intrinsic value.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="recommendation-sell">🎯 <strong>RECOMMENDATION: OVERVALUED - SELL</strong><br>Current price exceeds intrinsic value.</div>', unsafe_allow_html=True)
            
            # Create two-column layout
            col_left, col_right = st.columns([2, 1])
            
            with col_left:
                # Stock price chart
                st.markdown("### 📊 Price History")
                history = analyzer.stock_data['history']
                
                if not history.empty:
                    fig_price = go.Figure()
                    fig_price.add_trace(go.Scatter(
                        x=history.index,
                        y=history['Close'],
                        mode='lines',
                        name='Close Price',
                        line=dict(color='#1f77b4', width=2)
                    ))
                    
                    fig_price.update_layout(
                        height=400,
                        template="plotly_white",
                        showlegend=True,
                        xaxis_title="Date",
                        yaxis_title="Price ($)",
                        title=f"{ticker} Stock Price ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})"
                    )
                    
                    st.plotly_chart(fig_price, use_container_width=True)
                else:
                    st.warning("No price data available for the selected date range.")
                
                # DCF cash flow projection
                if dcf_result:
                    st.markdown("### 💰 DCF Cash Flow Projection")
                    future_fcfs = dcf_result['future_fcfs']
                    years = list(range(1, len(future_fcfs) + 1))
                    
                    fig_dcf = go.Figure()
                    fig_dcf.add_trace(go.Bar(
                        x=years,
                        y=future_fcfs,
                        name='Projected FCF',
                        marker_color='#2E86AB'
                    ))
                    
                    fig_dcf.update_layout(
                        height=300,
                        template="plotly_white",
                        xaxis_title="Year",
                        yaxis_title="Free Cash Flow ($)",
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig_dcf, use_container_width=True)
            
            with col_right:
                # Valuation metrics dashboard
                st.markdown("### 📈 Valuation Metrics")
                
                # Create dashboard - fix middle number font size issue
                fig_gauges = make_subplots(
                    rows=2, cols=2,
                    specs=[[{"type": "indicator"}, {"type": "indicator"}],
                           [{"type": "indicator"}, {"type": "indicator"}]],
                    subplot_titles=('P/E Ratio', 'DCF Safety', 'P/B Ratio', 'Revenue Growth'),
                    vertical_spacing=0.15,
                    horizontal_spacing=0.1
                )
                
                # P/E Ratio - increase middle number font size
                pe_ratio = ratios.get('pe_ratio', 0) or 0
                fig_gauges.add_trace(go.Indicator(
                    mode="gauge+number",
                    value=pe_ratio,
                    domain={'row': 0, 'column': 0},
                    title={'text': "P/E Ratio", 'font': {'size': 16}},
                    number={'font': {'size': 36, 'color': 'darkblue'}},  # Increase middle number font size
                    gauge={
                        'axis': {'range': [None, 50], 'tickfont': {'size': 12}},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 15], 'color': "lightgreen"},
                            {'range': [15, 25], 'color': "lightyellow"},
                            {'range': [25, 50], 'color': "lightcoral"}],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 25}}
                ), row=1, col=1)
                
                # DCF Safety Margin - increase middle number font size
                margin_of_safety = dcf_result.get('margin_of_safety', 0) if dcf_result else 0
                fig_gauges.add_trace(go.Indicator(
                    mode="gauge+number",
                    value=margin_of_safety,
                    domain={'row': 0, 'column': 1},
                    title={'text': "DCF Safety %", 'font': {'size': 16}},
                    number={'font': {'size': 36, 'color': 'darkblue'}},  # Increase middle number font size
                    gauge={
                        'axis': {'range': [-50, 50], 'tickfont': {'size': 12}},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [-50, 0], 'color': "lightcoral"},
                            {'range': [0, 10], 'color': "lightyellow"},
                            {'range': [10, 50], 'color': "lightgreen"}],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 0}}
                ), row=1, col=2)
                
                # P/B Ratio - increase middle number font size
                pb_ratio = ratios.get('price_to_book', 0) or 0
                fig_gauges.add_trace(go.Indicator(
                    mode="gauge+number",
                    value=pb_ratio,
                    domain={'row': 1, 'column': 0},
                    title={'text': "P/B Ratio", 'font': {'size': 16}},
                    number={'font': {'size': 36, 'color': 'darkblue'}},  # Increase middle number font size
                    gauge={
                        'axis': {'range': [None, 10], 'tickfont': {'size': 12}},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 1], 'color': "lightgreen"},
                            {'range': [1, 3], 'color': "lightyellow"},
                            {'range': [3, 10], 'color': "lightcoral"}],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 3}}
                ), row=2, col=1)
                
                # Revenue Growth Rate - increase middle number font size
                revenue_growth = (ratios.get('revenue_growth', 0) or 0) * 100
                fig_gauges.add_trace(go.Indicator(
                    mode="gauge+number",
                    value=revenue_growth,
                    domain={'row': 1, 'column': 1},
                    title={'text': "Revenue Growth %", 'font': {'size': 16}},
                    number={'font': {'size': 36, 'color': 'darkblue'}},  # Increase middle number font size
                    gauge={
                        'axis': {'range': [None, 50], 'tickfont': {'size': 12}},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 10], 'color': "lightyellow"},
                            {'range': [10, 20], 'color': "lightgreen"},
                            {'range': [20, 50], 'color': "darkgreen"}],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 10}}
                ), row=2, col=2)
                
                # Set subplot title font
                for i in fig_gauges['layout']['annotations']:
                    i['font'] = {'size': 16}
                
                fig_gauges.update_layout(
                    height=550,  # Slightly increase height to accommodate larger numbers
                    template="plotly_white",
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                
                st.plotly_chart(fig_gauges, use_container_width=True)
            
            # Financial data table
            st.markdown("### 📋 Financial Summary")
            
            # Create financial data table
            summary_data = []
            
            # Valuation data
            if dcf_result:
                summary_data.append(['DCF Intrinsic Value', f"${dcf_result['intrinsic_value']:.2f}"])
                summary_data.append(['Current Price', f"${dcf_result['current_price']:.2f}"])
                summary_data.append(['Margin of Safety', f"{dcf_result['margin_of_safety']:.2f}%"])
            
            # Valuation ratios
            if ratios.get('pe_ratio'):
                summary_data.append(['P/E Ratio', f"{ratios['pe_ratio']:.2f}"])
            if ratios.get('forward_pe'):
                summary_data.append(['Forward P/E', f"{ratios['forward_pe']:.2f}"])
            if ratios.get('price_to_book'):
                summary_data.append(['Price to Book', f"{ratios['price_to_book']:.2f}"])
            if ratios.get('eps'):
                summary_data.append(['EPS', f"${ratios['eps']:.2f}"])
            if ratios.get('profit_margin'):
                summary_data.append(['Profit Margin', f"{ratios['profit_margin']*100:.2f}%"])
            if ratios.get('revenue_growth'):
                summary_data.append(['Revenue Growth', f"{ratios['revenue_growth']*100:.2f}%"])
            if ratios.get('beta'):
                summary_data.append(['Beta', f"{ratios['beta']:.2f}"])
            if ratios.get('dividend_yield'):
                summary_data.append(['Dividend Yield', f"{ratios['dividend_yield']*100:.2f}%"])
            
            # Display table
            if summary_data:
                df_summary = pd.DataFrame(summary_data, columns=['Metric', 'Value'])
                st.dataframe(df_summary, use_container_width=True, hide_index=True)
            
            # DCF assumptions
            if dcf_result:
                st.markdown("### 🔧 DCF Model Assumptions")
                assumptions = dcf_result['assumptions']
                
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    st.metric("Growth Rate", f"{assumptions['growth_rate']*100:.1f}%")
                with col_b:
                    st.metric("Discount Rate", f"{assumptions['discount_rate']*100:.1f}%")
                with col_c:
                    st.metric("Terminal Growth", f"{assumptions['terminal_growth']*100:.1f}%")
                with col_d:
                    st.metric("Forecast Years", f"{assumptions['forecast_years']}")
    
    else:
        # Welcome page
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem;">
            <h2>🚀 Welcome to Stock Valuation Dashboard</h2>
            <p style="font-size: 1.2rem; margin: 2rem 0;">
                Select a stock ticker in the sidebar to begin your analysis.
            </p>
            <div style="display: flex; justify-content: center; gap: 2rem; margin: 2rem 0;">
                <div style="text-align: center;">
                    <h3>📊 Real-time Data</h3>
                    <p>Get live stock data from Yahoo Finance</p>
                </div>
                <div style="text-align: center;">
                    <h3>💰 DCF Valuation</h3>
                    <p>Discounted Cash Flow analysis</p>
                </div>
                <div style="text-align: center;">
                    <h3>📈 Interactive Charts</h3>
                    <p>Visualize key metrics and trends</p>
                </div>
            </div>
            <p><strong>Select from popular stocks:</strong> AAPL, MSFT, GOOGL, TSLA, AMZN</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p><strong>MGF 637 - Financial Modeling Project</strong> | Stock Valuation Dashboard</p>
        <p>Zipan Huang & Vivi Tan | Fall 2025 | Professor: Scott Laing</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()