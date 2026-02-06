# 黄金每日复盘系统

[![黄金每日复盘更新](https://github.com/lyd-666/A/actions/workflows/update-gold-analysis.yml/badge.svg)](https://github.com/lyd-666/A/actions/workflows/update-gold-analysis.yml)

## 项目简介

这是一个自动化的黄金市场每日复盘分析系统，采用卖方研报风格，使用简体中文输出专业的技术分析报告。

## 功能特点

- 📊 **数据来源**: 使用 yfinance 获取 COMEX 黄金期货 (GC=F) 数据，备选 XAUUSD=X
- 📈 **技术指标**: MA5/10/20/60、RSI14、MACD、ATR、20日波动率
- 📝 **研报风格**: 卖方研报专业语言，全中文输出
- 🤖 **自动更新**: GitHub Actions 每日北京时间18:00自动更新
- 🌐 **静态部署**: GitHub Pages 静态网页展示

## 报告模块

1. **晨会级摘要** - 核心观点快速概览
2. **趋势判断** - 整体趋势、均线形态、RSI状态、MACD状态
3. **技术指标证据** - 详细指标数据与研判
4. **每日盘面点评** - 当日交易特征分析
5. **今日vs昨日复盘** - 价格、成交量、波幅对比
6. **近五日趋势叙事** - 短期走势回顾
7. **判断失效条件** - 多空失效临界点
8. **置信度评分** - 0-100分量化评估

## 在线访问

🔗 [查看每日复盘报告](https://lyd-666.github.io/A/)

## 本地运行

### 环境要求

- Python 3.8+
- pip

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行分析脚本

```bash
python analyze_gold.py
```

脚本会生成 `data.json` 文件，包含完整的分析数据。

### 本地预览网页

```bash
# 使用 Python 内置服务器
python -m http.server 8000
```

然后访问 http://localhost:8000

## 项目结构

```
.
├── analyze_gold.py              # 黄金数据分析脚本
├── data.json                    # 生成的分析数据（自动更新）
├── index.html                   # 前端展示页面
├── style.css                    # 样式文件（研报风格）
├── requirements.txt             # Python依赖
├── .github/
│   └── workflows/
│       └── update-gold-analysis.yml  # GitHub Actions工作流
└── README.md                    # 说明文档
```

## GitHub Actions 自动化

系统通过 GitHub Actions 实现自动化：

- ⏰ 每日北京时间18:00（UTC 10:00）自动执行
- 📥 获取最新黄金数据
- 🧮 计算技术指标
- 📊 生成分析报告
- 🚀 自动部署到 GitHub Pages

也可以手动触发工作流：进入 Actions 页面，选择 "黄金每日复盘更新"，点击 "Run workflow"。

## 技术栈

- **后端**: Python 3.11
  - yfinance - 金融数据获取
  - pandas - 数据处理
  - numpy - 数值计算
- **前端**: HTML5 + CSS3 + JavaScript (原生)
- **CI/CD**: GitHub Actions
- **部署**: GitHub Pages

## 指标说明

### 移动平均线 (MA)
- MA5: 5日均线
- MA10: 10日均线
- MA20: 20日均线
- MA60: 60日均线

### 相对强弱指标 (RSI14)
- > 70: 超买区域
- 30-70: 正常区域
- < 30: 超卖区域

### MACD
- 快线: 12日EMA
- 慢线: 26日EMA
- 信号线: 9日EMA

### ATR14
- 14日平均真实波幅，衡量市场波动性

### 20日波动率
- 基于20日收益率的年化波动率

## 免责声明

本报告仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。

## 许可证

MIT License

---

**更新频率**: 每日自动更新

**数据延迟**: 取决于 Yahoo Finance 数据更新时间

**问题反馈**: 请提交 Issue