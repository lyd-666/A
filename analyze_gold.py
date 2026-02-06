#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄金每日复盘分析脚本
使用yfinance获取黄金期货数据，计算技术指标，生成简体中文研报风格分析
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import warnings
warnings.filterwarnings('ignore')


def calculate_ma(data, periods=[5, 10, 20, 60]):
    """计算移动平均线"""
    mas = {}
    for period in periods:
        mas[f'MA{period}'] = data['Close'].rolling(window=period).mean().iloc[-1]
    return mas


def calculate_rsi(data, period=14):
    """计算RSI指标"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]


def calculate_macd(data, fast=12, slow=26, signal=9):
    """计算MACD指标"""
    exp1 = data['Close'].ewm(span=fast, adjust=False).mean()
    exp2 = data['Close'].ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    return {
        'MACD': macd.iloc[-1],
        'Signal': signal_line.iloc[-1],
        'Histogram': histogram.iloc[-1]
    }


def calculate_atr(data, period=14):
    """计算ATR（平均真实波幅）"""
    high = data['High']
    low = data['Low']
    close = data['Close']
    
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr.iloc[-1]


def calculate_volatility(data, period=20):
    """计算20日波动率"""
    returns = data['Close'].pct_change()
    volatility = returns.rolling(window=period).std() * np.sqrt(252) * 100
    return volatility.iloc[-1]


def analyze_trend(data, mas, rsi, macd):
    """趋势判断"""
    close = data['Close'].iloc[-1]
    
    # 均线排列
    ma_trend = ""
    if mas['MA5'] > mas['MA10'] > mas['MA20'] > mas['MA60']:
        ma_trend = "多头排列"
        trend = "强势上涨"
    elif mas['MA5'] < mas['MA10'] < mas['MA20'] < mas['MA60']:
        ma_trend = "空头排列"
        trend = "弱势下跌"
    elif close > mas['MA60']:
        ma_trend = "中期多头"
        trend = "震荡偏多"
    elif close < mas['MA60']:
        ma_trend = "中期空头"
        trend = "震荡偏空"
    else:
        ma_trend = "均线纠缠"
        trend = "区间震荡"
    
    # RSI判断
    if rsi > 70:
        rsi_signal = "超买区域"
    elif rsi < 30:
        rsi_signal = "超卖区域"
    elif rsi > 50:
        rsi_signal = "强势区域"
    else:
        rsi_signal = "弱势区域"
    
    # MACD判断
    if macd['MACD'] > macd['Signal'] and macd['Histogram'] > 0:
        macd_signal = "金叉向上"
    elif macd['MACD'] < macd['Signal'] and macd['Histogram'] < 0:
        macd_signal = "死叉向下"
    elif macd['Histogram'] > 0:
        macd_signal = "多头趋势"
    else:
        macd_signal = "空头趋势"
    
    return {
        'trend': trend,
        'ma_trend': ma_trend,
        'rsi_signal': rsi_signal,
        'macd_signal': macd_signal
    }


def generate_summary(data, indicators, trend_analysis):
    """生成晨会级摘要"""
    close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[-2]
    change = close - prev_close
    change_pct = (change / prev_close) * 100
    
    direction = "上涨" if change > 0 else "下跌"
    
    summary = f"""
【核心观点】截至最新交易日收盘，COMEX黄金期货主力合约报收{close:.2f}美元/盎司，
日内{direction}{abs(change):.2f}美元，涨跌幅{change_pct:+.2f}%。技术面呈现{trend_analysis['trend']}格局，
均线系统{trend_analysis['ma_trend']}，动量指标{trend_analysis['macd_signal']}，
RSI处于{trend_analysis['rsi_signal']}。综合研判，短期金价{trend_analysis['trend']}，
建议关注{indicators['support']:.2f}-{indicators['resistance']:.2f}美元区间运行。
    """.strip()
    
    return summary


def generate_indicator_evidence(mas, rsi, macd, atr, volatility):
    """生成指标证据（研报语言）"""
    evidence = f"""
【均线系统】MA5报{mas['MA5']:.2f}美元，MA10报{mas['MA10']:.2f}美元，
MA20报{mas['MA20']:.2f}美元，MA60报{mas['MA60']:.2f}美元。短期均线
{'上穿' if mas['MA5'] > mas['MA10'] else '下穿'}中期均线，显示{'多头' if mas['MA5'] > mas['MA20'] else '空头'}动能。

【动量指标】RSI14当前读数{rsi:.2f}，处于{'超买' if rsi > 70 else '超卖' if rsi < 30 else '中性'}水平；
MACD快线{macd['MACD']:.2f}，慢线{macd['Signal']:.2f}，柱状图{macd['Histogram']:.2f}，
{'金叉向上' if macd['Histogram'] > 0 else '死叉向下'}，趋势{'偏多' if macd['Histogram'] > 0 else '偏空'}。

【波动率】ATR14日均值{atr:.2f}美元，20日年化波动率{volatility:.2f}%，
市场波动性处于{'较高' if volatility > 15 else '适中' if volatility > 10 else '较低'}水平。
    """.strip()
    
    return evidence


def generate_daily_commentary(data, trend_analysis):
    """生成每日点评"""
    close = data['Close'].iloc[-1]
    high = data['High'].iloc[-1]
    low = data['Low'].iloc[-1]
    volume = data['Volume'].iloc[-1]
    
    intraday_range = high - low
    intraday_range_pct = (intraday_range / close) * 100
    
    commentary = f"""
【盘面特征】本交易日金价于{low:.2f}美元开盘后，日内最高触及{high:.2f}美元，
最低回落至{low:.2f}美元，全天振幅{intraday_range_pct:.2f}%，收盘报{close:.2f}美元。
成交量为{volume:,.0f}手，显示市场交投{'活跃' if volume > data['Volume'].iloc[-5:-1].mean() else '清淡'}。

【技术形态】日K线收{'阳' if data['Close'].iloc[-1] > data['Open'].iloc[-1] else '阴'}线，
实体{'较大' if abs(data['Close'].iloc[-1] - data['Open'].iloc[-1]) > intraday_range * 0.5 else '较小'}，
上下影线{'均衡' if abs((high - max(data['Open'].iloc[-1], data['Close'].iloc[-1])) - (min(data['Open'].iloc[-1], data['Close'].iloc[-1]) - low)) < intraday_range * 0.2 else '不对称'}，
{'多头' if data['Close'].iloc[-1] > data['Open'].iloc[-1] else '空头'}格局明显。
    """.strip()
    
    return commentary


def compare_today_yesterday(data):
    """今日vs昨日复盘对比"""
    today = data.iloc[-1]
    yesterday = data.iloc[-2]
    
    price_change = today['Close'] - yesterday['Close']
    price_change_pct = (price_change / yesterday['Close']) * 100
    volume_change = ((today['Volume'] - yesterday['Volume']) / yesterday['Volume']) * 100
    
    comparison = f"""
【价格对比】较上一交易日{'上涨' if price_change > 0 else '下跌'}{abs(price_change):.2f}美元，
涨跌幅{price_change_pct:+.2f}%，{'延续' if (today['Close'] > today['Open']) == (yesterday['Close'] > yesterday['Open']) else '逆转'}
前日{'涨' if yesterday['Close'] > yesterday['Open'] else '跌'}势。

【成交对比】成交量较前日{'放大' if volume_change > 0 else '萎缩'}{abs(volume_change):.1f}%，
{'量价' if (price_change > 0) == (volume_change > 0) else '量价背离，需警惕'}配合
{'良好' if (price_change > 0) == (volume_change > 0) else '出现背离'}。

【波幅对比】日内振幅{((today['High'] - today['Low']) / today['Close'] * 100):.2f}%，
前日振幅{((yesterday['High'] - yesterday['Low']) / yesterday['Close'] * 100):.2f}%，
市场波动{'加大' if (today['High'] - today['Low']) > (yesterday['High'] - yesterday['Low']) else '收窄'}。
    """.strip()
    
    return comparison


def generate_invalidation_conditions(mas, current_price):
    """判断失效条件"""
    conditions = f"""
【多头失效】若金价有效跌破MA20均线（{mas['MA20']:.2f}美元）支撑位，
且RSI跌破50中轴，则短期多头格局失效，需重新评估趋势方向。

【空头失效】若金价有效突破MA60均线（{mas['MA60']:.2f}美元）压力位，
且MACD金叉向上，则短期空头格局失效，或将开启反弹行情。

【震荡失效】若金价突破近20日区间上沿或下破下沿，
且伴随成交量显著放大，则震荡格局打破，需顺势调整交易策略。
    """.strip()
    
    return conditions


def calculate_confidence_score(data, mas, rsi, macd):
    """置信度评分（0-100分）"""
    score = 50  # 基准分
    
    # 均线系统得分（30分）
    close = data['Close'].iloc[-1]
    if mas['MA5'] > mas['MA10'] > mas['MA20']:
        score += 15
    elif mas['MA5'] < mas['MA10'] < mas['MA20']:
        score -= 15
    
    if close > mas['MA60']:
        score += 15
    elif close < mas['MA60']:
        score -= 15
    
    # RSI得分（20分）
    if 40 <= rsi <= 60:
        score += 10  # 中性区域
    elif rsi > 70 or rsi < 30:
        score -= 10  # 极端区域风险
    
    # MACD得分（20分）
    if macd['Histogram'] > 0:
        score += 10
    else:
        score -= 10
    
    # 趋势一致性得分（10分）
    ma_bullish = mas['MA5'] > mas['MA20']
    rsi_bullish = rsi > 50
    macd_bullish = macd['Histogram'] > 0
    
    consistency = sum([ma_bullish, rsi_bullish, macd_bullish])
    if consistency == 3 or consistency == 0:
        score += 10  # 三者一致
    elif consistency == 2 or consistency == 1:
        score += 5  # 部分一致
    
    score = max(0, min(100, score))  # 限制在0-100范围
    
    return score


def generate_5day_narrative(data):
    """近5日趋势叙事"""
    recent_5 = data.tail(5)
    
    prices = recent_5['Close'].tolist()
    dates = [d.strftime('%m月%d日') for d in recent_5.index]
    
    # 计算趋势
    if prices[-1] > prices[0]:
        overall_trend = "震荡上行"
        direction = "上涨"
    elif prices[-1] < prices[0]:
        overall_trend = "震荡下行"
        direction = "下跌"
    else:
        overall_trend = "窄幅震荡"
        direction = "持平"
    
    total_change = prices[-1] - prices[0]
    total_change_pct = (total_change / prices[0]) * 100
    
    narrative = f"""
【五日回顾】过去5个交易日（{dates[0]}-{dates[-1]}），COMEX黄金期货呈{overall_trend}态势。
起始日收盘{prices[0]:.2f}美元，期间最高{recent_5['High'].max():.2f}美元，
最低{recent_5['Low'].min():.2f}美元，截至最新收盘{prices[-1]:.2f}美元，
累计{direction}{abs(total_change):.2f}美元，区间涨跌幅{total_change_pct:+.2f}%。

【运行特征】五日均价{recent_5['Close'].mean():.2f}美元，
日均波幅{((recent_5['High'] - recent_5['Low']) / recent_5['Close'] * 100).mean():.2f}%，
呈现{'高波动' if ((recent_5['High'] - recent_5['Low']) / recent_5['Close'] * 100).mean() > 1.5 else '低波动'}特征。
价格重心{'上移' if prices[-1] > recent_5['Close'].mean() else '下移'}，
短期趋势{'向上' if prices[-1] > prices[0] else '向下' if prices[-1] < prices[0] else '中性'}。
    """.strip()
    
    return narrative


def fetch_gold_data():
    """获取黄金数据"""
    try:
        print("正在获取COMEX黄金期货数据 (GC=F)...")
        ticker = yf.Ticker("GC=F")
        data = ticker.history(period="2y")
        
        if data.empty:
            print("GC=F数据为空，尝试备选XAUUSD=X...")
            ticker = yf.Ticker("XAUUSD=X")
            data = ticker.history(period="2y")
        
        if data.empty:
            raise ValueError("无法获取黄金数据")
        
        # 确保至少有1年数据
        if len(data) < 250:
            print(f"警告: 仅获取到{len(data)}天数据，少于1年")
        
        print(f"成功获取{len(data)}天数据")
        return data
    
    except Exception as e:
        print(f"获取数据失败: {e}")
        raise


def calculate_support_resistance(data, mas):
    """计算支撑位和阻力位"""
    close = data['Close'].iloc[-1]
    recent_high = data['High'].tail(20).max()
    recent_low = data['Low'].tail(20).min()
    
    # 支撑位：取MA20和近期低点较低者
    support = min(mas['MA20'], recent_low)
    
    # 阻力位：取MA60和近期高点较高者
    resistance = max(mas['MA60'], recent_high)
    
    return support, resistance


def main():
    """主函数"""
    print("=" * 60)
    print("黄金每日复盘分析系统")
    print("=" * 60)
    
    # 1. 获取数据
    data = fetch_gold_data()
    
    # 2. 计算指标
    print("\n计算技术指标...")
    mas = calculate_ma(data)
    rsi = calculate_rsi(data)
    macd = calculate_macd(data)
    atr = calculate_atr(data)
    volatility = calculate_volatility(data)
    
    # 3. 计算支撑阻力位
    support, resistance = calculate_support_resistance(data, mas)
    
    indicators = {
        'MA5': mas['MA5'],
        'MA10': mas['MA10'],
        'MA20': mas['MA20'],
        'MA60': mas['MA60'],
        'RSI14': rsi,
        'MACD': macd['MACD'],
        'MACD_Signal': macd['Signal'],
        'MACD_Histogram': macd['Histogram'],
        'ATR14': atr,
        'Volatility_20d': volatility,
        'support': support,
        'resistance': resistance
    }
    
    # 4. 趋势分析
    print("分析趋势...")
    trend_analysis = analyze_trend(data, mas, rsi, macd)
    
    # 5. 生成各模块内容
    print("生成分析报告...")
    summary = generate_summary(data, indicators, trend_analysis)
    evidence = generate_indicator_evidence(mas, rsi, macd, atr, volatility)
    commentary = generate_daily_commentary(data, trend_analysis)
    comparison = compare_today_yesterday(data)
    invalidation = generate_invalidation_conditions(mas, data['Close'].iloc[-1])
    confidence = calculate_confidence_score(data, mas, rsi, macd)
    narrative_5d = generate_5day_narrative(data)
    
    # 6. 组装完整报告
    current_date = data.index[-1].strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report = {
        'date': current_date,
        'update_time': current_time,
        'price': {
            'current': float(data['Close'].iloc[-1]),
            'change': float(data['Close'].iloc[-1] - data['Close'].iloc[-2]),
            'change_pct': float((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2] * 100),
            'open': float(data['Open'].iloc[-1]),
            'high': float(data['High'].iloc[-1]),
            'low': float(data['Low'].iloc[-1]),
            'volume': int(data['Volume'].iloc[-1])
        },
        'indicators': {k: float(v) for k, v in indicators.items()},
        'analysis': {
            'summary': summary,
            'trend': trend_analysis['trend'],
            'ma_trend': trend_analysis['ma_trend'],
            'rsi_signal': trend_analysis['rsi_signal'],
            'macd_signal': trend_analysis['macd_signal'],
            'evidence': evidence,
            'commentary': commentary,
            'comparison': comparison,
            'invalidation': invalidation,
            'confidence_score': confidence,
            'narrative_5d': narrative_5d
        },
        'historical_5d': [
            {
                'date': d.strftime('%Y-%m-%d'),
                'close': float(data['Close'].iloc[i]),
                'change_pct': float((data['Close'].iloc[i] - data['Close'].iloc[i-1]) / data['Close'].iloc[i-1] * 100) if i > 0 else 0
            }
            for i, d in enumerate(data.index[-5:])
        ]
    }
    
    # 7. 保存JSON
    output_file = 'data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 分析完成，数据已保存至 {output_file}")
    print(f"✓ 最新金价: ${report['price']['current']:.2f}")
    print(f"✓ 涨跌幅: {report['price']['change_pct']:+.2f}%")
    print(f"✓ 趋势判断: {trend_analysis['trend']}")
    print(f"✓ 置信度: {confidence}/100")
    print("=" * 60)
    
    return report


if __name__ == '__main__':
    main()
