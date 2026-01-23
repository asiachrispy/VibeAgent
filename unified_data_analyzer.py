#!/usr/bin/env python3
"""
Unified Data Analyzer - Comprehensive analysis platform
Integrates Amazon products, YouTube/TikTok videos, and strategic insights
"""

import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UnifiedDataAnalyzer:
    def __init__(self):
        self.analysis_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def analyze_all_data(self) -> str:
        """Generate comprehensive analysis of all available data"""
        analysis = f"""
# 🎯 Comprehensive Market & Content Intelligence Report
**Generated on**: {self.analysis_date}
**Analysis Scope**: Amazon Products + Video Content Analysis

---

"""
        
        # Load and analyze Amazon data
        amazon_analysis = self._analyze_amazon_data()
        if amazon_analysis:
            analysis += amazon_analysis + "\n\n"
        
        # Load and analyze video data
        video_analysis = self._analyze_video_data()
        if video_analysis:
            analysis += video_analysis + "\n\n"
        
        # Generate cross-platform insights
        cross_platform_insights = self._generate_cross_platform_insights()
        if cross_platform_insights:
            analysis += cross_platform_insights
        
        # Generate strategic recommendations
        strategy = self._generate_comprehensive_strategy()
        if strategy:
            analysis += strategy
        
        return analysis
    
    def _analyze_amazon_data(self) -> Optional[str]:
        """Analyze Amazon product data"""
        try:
            with open("amazon_products.json", "r", encoding="utf-8") as f:
                amazon_data = json.load(f)
        except FileNotFoundError:
            logger.info("No Amazon data found")
            return None
        except json.JSONDecodeError:
            logger.error("Invalid Amazon data file")
            return None
        
        if not amazon_data:
            return None
        
        analysis = "## 🛒 Amazon Market Analysis\n\n"
        
        # Filter valid products
        valid_products = [p for p in amazon_data if not p.get('error')]
        
        if not valid_products:
            analysis += "⚠️ No valid Amazon product data available.\n\n"
            return analysis
        
        analysis += f"**Products Analyzed**: {len(valid_products)}\n\n"
        
        # Price analysis
        prices = []
        ratings = []
        review_counts = []
        brands = {}
        
        for product in valid_products:
            # Extract price
            price_str = product.get('price', '0')
            try:
                if isinstance(price_str, str):
                    price_num = float(price_str.replace('$', '').replace(',', ''))
                    prices.append(price_num)
            except (ValueError, AttributeError):
                continue
            
            # Extract rating
            rating = product.get('rating')
            if isinstance(rating, (int, float)):
                ratings.append(rating)
            
            # Extract review count
            reviews = product.get('reviews_count', '0')
            try:
                if isinstance(reviews, str):
                    reviews_num = int(reviews.replace(',', '').replace('(', '').replace(')', ''))
                    review_counts.append(reviews_num)
                elif isinstance(reviews, int):
                    review_counts.append(reviews)
            except (ValueError, AttributeError):
                continue
            
            # Track brands
            brand = product.get('brand', 'Unknown')
            brands[brand] = brands.get(brand, 0) + 1
        
        # Price insights
        if prices:
            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)
            
            analysis += f"""### 💰 Price Analysis
- **Average Price**: ${avg_price:.2f}
- **Price Range**: ${min_price:.2f} - ${max_price:.2f}
- **Price Segments**:
"""
            # Price segments
            budget = len([p for p in prices if p < 25])
            mid_range = len([p for p in prices if 25 <= p < 75])
            premium = len([p for p in prices if p >= 75])
            
            analysis += f"  - Budget (<$25): {budget} products ({budget/len(prices)*100:.1f}%)\n"
            analysis += f"  - Mid-Range ($25-$75): {mid_range} products ({mid_range/len(prices)*100:.1f}%)\n"
            analysis += f"  - Premium (>$75): {premium} products ({premium/len(prices)*100:.1f}%)\n\n"
        
        # Quality analysis
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            high_rated = len([r for r in ratings if r >= 4.5])
            
            analysis += f"""### ⭐ Quality Analysis  
- **Average Rating**: {avg_rating:.2f}/5.0
- **High-Quality Products** (≥4.5★): {high_rated}/{len(ratings)} ({high_rated/len(ratings)*100:.1f}%)
"""
            
            if avg_rating >= 4.3:
                analysis += "- **Excellent product quality** in this market\n"
            elif avg_rating >= 4.0:
                analysis += "- **Good product quality** with room for improvement\n"
            else:
                analysis += "- **Quality concerns** - Opportunity for differentiation\n"
        
        # Brand analysis
        if brands:
            top_brands = sorted(brands.items(), key=lambda x: x[1], reverse=True)[:5]
            analysis += "\n### 🏷️ Top Brands\n"
            for brand, count in top_brands:
                if brand != 'Unknown':
                    analysis += f"- **{brand}**: {count} products\n"
        
        # Market opportunities
        analysis += "\n### 💡 Amazon Market Opportunities\n"
        
        if prices and avg_price < 30:
            analysis += "- **Premium segment opportunity** - Few high-priced products\n"
        elif prices and avg_price > 100:
            analysis += "- **Budget segment opportunity** - Room for affordable options\n"
        
        if ratings and avg_rating < 4.2:
            analysis += "- **Quality differentiation opportunity** - Focus on superior products\n"
        
        if review_counts:
            avg_reviews = sum(review_counts) / len(review_counts)
            if avg_reviews < 1000:
                analysis += "- **New product opportunity** - Low review count indicates emerging market\n"
        
        return analysis
    
    def _analyze_video_data(self) -> Optional[str]:
        """Analyze video data from multiple platforms"""
        try:
            with open("youtube_results.json", "r", encoding="utf-8") as f:
                video_data = json.load(f)
        except FileNotFoundError:
            logger.info("No video data found")
            return None
        except json.JSONDecodeError:
            logger.error("Invalid video data file")
            return None
        
        if not video_data:
            return None
        
        analysis = "## 📺 Video Content Analysis\n\n"
        
        # Filter valid videos
        valid_videos = [v for v in video_data if not v.get('error') and v.get('title')]
        
        if not valid_videos:
            analysis += "⚠️ No valid video data available.\n\n"
            return analysis
        
        analysis += f"**Videos Analyzed**: {len(valid_videos)}\n\n"
        
        # Extract metrics
        total_views = 0
        total_likes = 0
        total_comments = 0
        content_themes = {}
        
        for video in valid_videos:
            # Parse metrics
            views = self._parse_count(video.get('viewCount', '0'))
            likes = self._parse_count(video.get('likes', '0'))
            comments = self._parse_count(video.get('commentsCount', '0'))
            
            total_views += views
            total_likes += likes
            total_comments += comments
            
            # Extract themes from titles
            title = video.get('title', '').lower()
            
            if any(keyword in title for keyword in ['fitness', 'workout', 'gym', 'exercise']):
                content_themes['fitness'] = content_themes.get('fitness', 0) + 1
            if any(keyword in title for keyword in ['tutorial', 'how to', 'guide']):
                content_themes['tutorial'] = content_themes.get('tutorial', 0) + 1
            if any(keyword in title for keyword in ['review', 'test', 'unboxing']):
                content_themes['review'] = content_themes.get('review', 0) + 1
            if any(keyword in title for keyword in ['vlog', 'daily', 'life']):
                content_themes['vlog'] = content_themes.get('vlog', 0) + 1
        
        # Performance summary
        analysis += "### 📊 Performance Summary\n"
        analysis += f"- **Total Views**: {total_views:,}\n"
        analysis += f"- **Total Likes**: {total_likes:,}\n"
        analysis += f"- **Total Comments**: {total_comments:,}\n"
        
        if total_views > 0:
            avg_engagement = ((total_likes + total_comments) / total_views) * 100
            analysis += f"- **Average Engagement Rate**: {avg_engagement:.2f}%\n"
        
        # Content themes
        if content_themes:
            analysis += "\n### 🎬 Content Themes\n"
            for theme, count in sorted(content_themes.items(), key=lambda x: x[1], reverse=True):
                analysis += f"- **{theme.title()}**: {count} videos\n"
        
        # Content strategy insights
        analysis += "\n### 💡 Content Strategy Insights\n"
        
        if content_themes.get('fitness', 0) > len(valid_videos) * 0.5:
            analysis += "- **Fitness-focused content** dominates - Strong niche positioning\n"
        
        if content_themes.get('tutorial', 0) > 0:
            analysis += "- **Educational content** present - Value-driven approach\n"
        
        if total_views > 0 and avg_engagement > 3:
            analysis += "- **Strong audience engagement** - Content resonates well\n"
        elif total_views > 0 and avg_engagement < 1:
            analysis += "- **Engagement improvement needed** - Focus on community building\n"
        
        return analysis
    
    def _generate_cross_platform_insights(self) -> str:
        """Generate insights connecting Amazon and video data"""
        insights = "## 🔗 Cross-Platform Intelligence\n\n"
        
        insights += """### 📈 Content-to-Commerce Opportunities

**Affiliate Marketing Potential**:
- High-engagement video content → Product recommendation opportunities
- Tutorial videos → Equipment/product showcase potential
- Review content → Direct affiliate link integration

**Content Strategy Based on Market Gaps**:
- Identify underserved niches in Amazon market
- Create video content addressing pain points of existing products
- Develop comparison content for high-demand categories

**Audience Monetization Strategies**:
- Merchandise opportunities based on content themes
- Sponsored content partnerships with relevant brands
- Digital products complementing physical products

### 🎯 Strategic Positioning

**Content-Product Alignment**:
```
        
        # Try to identify connections between content themes and product categories
        insights += """
1. **Fitness Content + Workout Equipment**: Natural synergy
2. **Tutorial Content + Educational Products**: Learning resources  
3. **Review Content + Affiliate Products**: Commission opportunities
4. **Lifestyle Content + Lifestyle Products**: Brand partnerships

**Market Entry Strategies**:
- Analyze successful content themes for product ideas
- Identify price points from video audience demographics
- Use video engagement to validate product concepts
"""
        
        return insights
    
    def _generate_comprehensive_strategy(self) -> str:
        """Generate overall strategic recommendations"""
        strategy = "## 🚀 Comprehensive Strategy Recommendations\n\n"
        
        strategy += """### 📋 Immediate Actions (Next 30 Days)

**Content Optimization**:
- [ ] Analyze top-performing video patterns
- [ ] Create content calendar based on successful themes
- [ ] Optimize video SEO (titles, descriptions, tags)
- [ ] Implement consistent branding across platforms

**Market Research**:
- [ ] Identify product opportunities from content gaps
- [ ] Analyze competitor pricing and positioning
- [ ] Validate demand through content engagement metrics
- [ ] Research affiliate program opportunities

**Technical Implementation**:
- [ ] Set up automated data collection pipeline
- [ ] Create performance tracking dashboard
- [ ] Implement A/B testing for content and products
- [ ] Establish regular reporting schedule

### 📈 Growth Strategy (Next 90 Days)

**Platform Expansion**:
- Expand video content to multiple platforms (YouTube, TikTok, Instagram)
- Develop platform-specific content strategies
- Cross-promote content to maximize reach
- Build community engagement across platforms

**Revenue Diversification**:
- Implement affiliate marketing strategy
- Develop digital products based on content expertise
- Explore sponsored content opportunities
- Create merchandise based on brand identity

**Audience Development**:
- Focus on community building and engagement
- Develop email marketing funnels
- Create exclusive content for loyal followers
- Host live events or Q&A sessions

### 🎯 Long-term Vision (6-12 Months)

**Brand Development**:
- Establish authority in chosen niche
- Develop recognizable brand identity
- Create premium product offerings
- Build strategic partnerships

**Business Scaling**:
- Outsource content production while maintaining quality
- Develop team for customer service and support
- Invest in advanced analytics and automation
- Explore international market opportunities

### 📊 Success Metrics

**Content Performance**:
- Video view growth rate: Target 20% month-over-month
- Engagement rate: Target >3% average
- Subscriber growth: Target 15% month-over-month

**Revenue Metrics**:
- Affiliate income: Target $1,000+ monthly within 6 months
- Product sales: Generate consistent revenue stream
- Diversified income: Multiple revenue sources established

**Market Position**:
- Authority recognition: Become go-to source in niche
- Competitive advantage: Unique value proposition
- Brand loyalty: High repeat engagement rates
"""
        
        return strategy
    
    def _parse_count(self, count_str: str) -> int:
        """Parse count string to integer"""
        if not count_str or isinstance(count_str, int):
            return int(count_str or 0)
        
        count_str = str(count_str).upper().replace(',', '')
        
        if 'K' in count_str:
            return int(float(count_str.replace('K', '')) * 1000)
        elif 'M' in count_str:
            return int(float(count_str.replace('M', '')) * 1000000)
        elif 'B' in count_str:
            return int(float(count_str.replace('B', '')) * 1000000000)
        else:
            return int(count_str or 0)
    
    def save_comprehensive_report(self, analysis: str):
        """Save the comprehensive analysis report"""
        filename = f"comprehensive_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(analysis)
        logger.info(f"Comprehensive analysis saved to: {filename}")
        return filename

def main():
    """Main execution function"""
    logger.info("Starting unified data analysis...")
    
    analyzer = UnifiedDataAnalyzer()
    
    # Generate comprehensive analysis
    analysis = analyzer.analyze_all_data()
    
    # Save report
    report_file = analyzer.save_comprehensive_report(analysis)
    
    # Display results
    print("=" * 80)
    print("🎯 COMPREHENSIVE MARKET & CONTENT INTELLIGENCE REPORT")
    print("=" * 80)
    print(analysis)
    print("=" * 80)
    print(f"✅ Full report saved to: {report_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()
