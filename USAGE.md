# 黄金每日复盘系统 - 使用说明

## 快速开始

### 1. 启用GitHub Pages

完成以下步骤以部署您的黄金复盘系统：

#### 配置步骤
1. 打开仓库页面 https://github.com/lyd-666/A
2. 点击 **Settings** (设置)
3. 在左侧菜单中找到 **Pages**
4. 在 **Source** 下拉菜单中选择：
   - **Source**: Deploy from a branch
   - **Branch**: `gh-pages`
   - **Folder**: `/ (root)`
5. 点击 **Save** 保存
6. 等待约1-2分钟，页面会显示部署完成
7. 访问地址: https://lyd-666.github.io/A/

### 2. 手动触发分析

如果您想立即生成最新的分析报告（而不是等到每日18:00），可以手动触发：

#### 手动运行步骤
1. 进入仓库 Actions 页面
2. 在左侧选择 **黄金每日复盘更新** 工作流
3. 点击右上角 **Run workflow** 按钮
4. 在弹出的对话框中点击绿色的 **Run workflow** 确认
5. 等待约2-3分钟，工作流完成后会自动部署最新数据

### 3. 本地开发和测试

如果您想在本地运行和测试系统：

#### 环境准备
```bash
# 克隆仓库
git clone https://github.com/lyd-666/A.git
cd A

# 安装Python依赖
pip install -r requirements.txt
```

#### 运行分析脚本
```bash
# 生成最新分析数据
python analyze_gold.py

# 成功后会生成 data.json 文件
```

#### 本地预览网页
```bash
# 启动本地服务器
python -m http.server 8000

# 在浏览器中访问
# http://localhost:8000
```

## 系统工作流程

### 自动化流程
```
每日北京时间 18:00
    ↓
GitHub Actions 自动触发
    ↓
获取黄金期货数据 (GC=F)
    ↓
计算技术指标
    ↓
生成中文研报分析
    ↓
更新 data.json
    ↓
部署到 GitHub Pages
    ↓
用户访问最新报告
```

### 数据流
```
yfinance API
    → analyze_gold.py
    → data.json
    → GitHub Pages
    → index.html (用户浏览器)
```

## 数据说明

### 技术指标

| 指标 | 说明 | 用途 |
|------|------|------|
| MA5 | 5日移动平均线 | 短期趋势 |
| MA10 | 10日移动平均线 | 短期趋势 |
| MA20 | 20日移动平均线 | 中期趋势 |
| MA60 | 60日移动平均线 | 长期趋势 |
| RSI14 | 14日相对强弱指标 | 超买超卖 |
| MACD | 指数平滑异同移动平均线 | 趋势强度 |
| ATR14 | 14日平均真实波幅 | 波动性 |
| 20日波动率 | 年化波动率 | 风险度量 |

### RSI 判断标准
- **> 70**: 超买区域，可能回调
- **50-70**: 强势区域
- **30-50**: 弱势区域
- **< 30**: 超卖区域，可能反弹

### 置信度评分
- **70-100分**: 高置信度，趋势明确
- **50-69分**: 中等置信度，谨慎观望
- **0-49分**: 低置信度，不建议操作

## 常见问题

### Q1: 数据多久更新一次？
**A**: 系统每日北京时间18:00自动更新。您也可以随时手动触发更新。

### Q2: 数据来源是什么？
**A**: 使用 Yahoo Finance 的 yfinance 库获取 COMEX 黄金期货 (GC=F) 数据。如果 GC=F 不可用，会自动切换到 XAUUSD=X。

### Q3: 如何修改更新时间？
**A**: 编辑 `.github/workflows/update-gold-analysis.yml` 文件中的 cron 表达式：
```yaml
schedule:
  - cron: '0 10 * * *'  # UTC 10:00 = 北京时间 18:00
```

### Q4: 为什么页面显示"数据加载失败"？
**A**: 可能原因：
- GitHub Pages 尚未启用或部署未完成
- data.json 文件未生成
- 网络连接问题

解决方法：
1. 确认 GitHub Pages 已启用
2. 手动运行一次工作流生成数据
3. 检查浏览器控制台的错误信息

### Q5: 可以修改页面样式吗？
**A**: 可以！编辑 `style.css` 文件来自定义样式。修改后提交到仓库，GitHub Actions 会自动部署更新。

### Q6: 如何添加更多技术指标？
**A**: 
1. 在 `analyze_gold.py` 中添加新的计算函数
2. 将结果添加到 `indicators` 字典
3. 在 `index.html` 中添加相应的显示元素
4. 在 `style.css` 中添加样式

### Q7: 系统支持其他金融产品吗？
**A**: 可以修改 `analyze_gold.py` 中的 ticker 代码来分析其他产品，例如：
- 白银: SI=F
- 原油: CL=F
- 标普500: ^GSPC
- 比特币: BTC-USD

## 技术支持

如遇问题，请在 GitHub 仓库提交 Issue:
https://github.com/lyd-666/A/issues

## 免责声明

⚠️ **重要提示**:
- 本系统提供的分析报告仅供参考
- 不构成任何投资建议
- 投资有风险，入市需谨慎
- 请根据自身风险承受能力做出决策

## 许可证

MIT License - 详见 LICENSE 文件

---

**祝您使用愉快！**
