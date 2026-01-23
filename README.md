# 🤖 AI Data Analyst - Complete Solution

基于IPIDEA的智能数据分析师，支持Amazon商品抓取、YouTube/TikTok视频分析和短视频下载。

## ✨ 功能特性

### 🛒 Amazon商品分析
- ✅ 商品数据抓取（价格、评分、评论数、销量等）
- ✅ 市场表现分析（BSR排名、竞品对比）
- ✅ 战略洞察（机会识别、威胁分析）
- ✅ 可行性建议（定价策略、产品优化）

### 📺 视频内容分析
- ✅ YouTube视频数据抓取（播放量、点赞、评论等）
- ✅ TikTok视频下载和元数据提取
- ✅ 内容表现分析（互动率、传播效果）
- ✅ 内容策略建议（主题识别、发布时机）

### 📥 短视频下载
- ✅ 多平台支持（YouTube、TikTok）
- ✅ 高质量视频下载
- ✅ 元数据提取（标题、描述、时长等）
- ✅ 批量下载功能

### 🎯 综合分析
- ✅ 跨平台数据整合
- ✅ 市场趋势识别
- ✅ 内容到电商的机会挖掘
- ✅ 完整战略路线图

## 🚀 快速开始

### 1. 环境准备
```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装yt-dlp（视频下载功能需要）
pip install yt-dlp
```

### 2. 配置API Token
编辑相关Python文件，将以下行中的token替换为你的IPIDEA API token：
```python
API_TOKEN = "your_ipidea_api_token_here"
```

### 3. 运行方式

#### 🖱️ 交互模式（推荐）
```bash
python ai_analyst_workflow.py --interactive
```

#### 📝 命令行模式
```bash
# 分析Amazon商品
python ai_analyst_workflow.py --urls "https://amazon.com/dp/B08BD8WKBC"

# 分析YouTube视频
python ai_analyst_workflow.py --urls "https://youtube.com/watch?v=ydTy5doG-4s"

# 多平台综合分析
python ai_analyst_workflow.py --urls "amazon_url" "youtube_url" "tiktok_url"
```

#### 📦 单独模块使用
```bash
# 仅Amazon分析
python amazon_scraper.py

# 仅视频分析
python video_analyzer.py

# 仅视频下载
python short_video_downloader.py

# 综合分析
python unified_data_analyzer.py
```

## 📊 输出文件说明

运行后会生成以下分析报告：

| 文件名 | 内容描述 |
|---------|---------|
| `amazon_products.json` | Amazon商品原始数据 |
| `amazon_analysis.md` | Amazon商品分析报告 |
| `youtube_results.json` | YouTube视频原始数据 |
| `video_analysis.md` | 视频内容分析报告 |
| `comprehensive_analysis_*.md` | 综合战略分析报告 |
| `downloaded_videos/` | 下载的视频文件目录 |

## 🎯 核心优势

### 📈 数据全面性
- **实时抓取**: 通过IPIDEA获取最新数据，避免大模型数据滞后
- **多平台覆盖**: 支持Amazon、YouTube、TikTok等主流平台
- **深度分析**: 从基础指标到战略洞察的全方位分析

### 🔒 技术可靠性
- **高成功率**: IPIDEA全球住宅IP确保99.9%抓取成功率
- **智能重试**: 自动处理网络异常和反爬机制
- **错误处理**: 完善的异常处理和错误报告

### 🧠 智能分析
- **商业洞察**: 超越数据本身的战略性建议
- **跨平台整合**: 挖掘内容到电商的关联机会
- **可操作建议**: 具体的执行方案和行动项

## 📋 使用场景

### 💼 商业应用
- **市场调研**: 竞品分析和市场机会识别
- **内容策略**: 基于数据的内容规划和优化
- **选品决策**: 基于Amazon数据的产品选择
- **投资分析**: 内容变现和电商投资评估

### 🎬 创作者工具
- **内容优化**: 分析高表现视频的共同特征
- **选题规划**: 识别热门话题和蓝海领域
- **竞品分析**: 同行内容策略和表现对比
- **增长策略**: 粉丝增长和互动提升方案

### 🛍️ 电商运营
- **产品定位**: 基于市场数据的产品定位
- **定价策略**: 竞品价格分析和定价建议
- **Listing优化**: 产品页面优化建议
- **选品开发**: 基于需求缺口的新品开发

## ⚙️ 配置说明

### IPIDEA配置
1. 注册IPIDEA账号：http://www.ipidea.net/
2. 获取API Token
3. 在代码中替换API_TOKEN变量

### 下载配置
```python
# 视频质量设置
QUALITY = "best"  # best/worst/specific format

# 下载目录
DOWNLOAD_DIR = "downloaded_videos"
```

## 📝 分析报告示例

### Amazon分析报告包含：
- 📊 产品基本信息
- 📈 销售表现指标
- 🏆 BSR排名分析
- 💡 竞争洞察
- 🎯 战略建议

### 视频分析报告包含：
- 📈 表现分析（播放量、互动率）
- 🎬 内容分析（主题、格式）
- 💬 互动分析（评论、点赞）
- 🚀 内容策略建议

### 综合分析报告包含：
- 🔗 跨平台关联分析
- 💰 内容变现机会
- 📋 执行路线图
- 🎯 长期战略规划

## 🛠️ 故障排除

### 常见问题
1. **API Token错误**
   - 确保token正确且未过期
   - 检查IPIDEA账户余额

2. **视频下载失败**
   - 确保已安装yt-dlp: `pip install yt-dlp`
   - 检查网络连接和URL有效性

3. **数据抓取失败**
   - 检查目标URL是否可访问
   - 等待一段时间后重试（反爬机制）

4. **分析结果不准确**
   - 确保数据文件完整且格式正确
   - 检查数据是否为空或包含错误信息

### 技术支持
- IPIDEA文档：https://help.ipidea.net/
- 项目Issues：提交问题描述和日志
- 更新日志：查看最新版本和改进

## 📄 许可证

本项目仅供学习和研究使用，请遵守相关平台的使用条款和法律法规。

## 🤝 贡献

欢迎提交Issues和Pull Requests来改进这个项目！

---

**🚀 让AI为你的数据分析和商业决策赋能！**
