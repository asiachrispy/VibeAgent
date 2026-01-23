#!/usr/bin/env python3
"""
Video Data Analyzer - Comprehensive analysis for YouTube, TikTok videos
Generates strategic insights for content creators and marketers
"""

import json
import os
from typing import List, Dict, Optional
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VideoAnalyzer:
    def __init__(self):
        self.analysis_templates = {
            'performance': self._analyze_performance,
            'content': self._analyze_content,
            'engagement': self._analyze_engagement,
            'strategy': self._generate_strategy
        }
    
    def analyze_videos(self, video_data: List[Dict]) -> str:
        """Comprehensive analysis of video data"""
        if not video_data:
            return "No video data available for analysis."
        
        analysis = "# 📊 Video Content Strategy Analysis Report\n\n"
        analysis += f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        analysis += f"Videos Analyzed: {len(video_data)}\n\n"
        
        # Filter out videos with errors
        valid_videos = [v for v in video_data if not v.get('error')]
        error_videos = [v for v in video_data if v.get('error')]
        
        if error_videos:
            analysis += "## ⚠️ Data Collection Issues\n"
            for video in error_videos:
                analysis += f"- **{video.get('input', 'Unknown URL')}**: {video.get('error', 'Unknown error')}\n"
            analysis += "\n"
        
        if not valid_videos:
            return analysis + "No valid video data collected for analysis."
        
        # Generate analysis sections
        analysis += self._generate_content_overview(valid_videos)
        analysis += self._analyze_performance(valid_videos)
        analysis += self._analyze_content(valid_videos)
        analysis += self._analyze_engagement(valid_videos)
        analysis += self._generate_strategy(valid_videos)
        analysis += self._generate_action_items(valid_videos)
        
        return analysis
    
    def _generate_content_overview(self, videos: List[Dict]) -> str:
        """Generate overview of content types and themes"""
        overview = "## 🎯 Content Overview\n\n"
        
        # Analyze themes from titles and descriptions
        themes = {}
        content_types = {}
        
        for video in videos:
            title = video.get('title', '').lower()
            description = video.get('description', '').lower()
            
            # Extract common themes
            if 'fitness' in title or 'workout' in title or 'gym' in title:
                themes['fitness'] = themes.get('fitness', 0) + 1
            if 'tutorial' in title or 'how to' in title:
                themes['tutorial'] = themes.get('tutorial', 0) + 1
            if 'review' in title or 'test' in title:
                themes['review'] = themes.get('review', 0) + 1
            if 'vlog' in title or 'daily' in title:
                themes['vlog'] = themes.get('vlog', 0) + 1
            
            # Determine content type
            duration = video.get('duration', '')
            if duration:
                if 'PT' in duration:  # ISO 8601 duration format
                    # Simple parsing for PT format
                    if 'H' in duration:
                        content_types['long_form'] = content_types.get('long_form', 0) + 1
                    elif 'M' in duration:
                        minutes = int(duration.split('M')[0].split('T')[-1])
                        if minutes < 5:
                            content_types['short_form'] = content_types.get('short_form', 0) + 1
                        elif minutes < 15:
                            content_types['medium_form'] = content_types.get('medium_form', 0) + 1
                        else:
                            content_types['long_form'] = content_types.get('long_form', 0) + 1
        
        overview += "### Content Themes Identified\n"
        if themes:
            for theme, count in sorted(themes.items(), key=lambda x: x[1], reverse=True):
                overview += f"- **{theme.title()}**: {count} videos\n"
        else:
            overview += "- Diverse content themes detected\n"
        
        overview += "\n### Content Format Distribution\n"
        if content_types:
            for format_type, count in sorted(content_types.items(), key=lambda x: x[1], reverse=True):
                overview += f"- **{format_type.replace('_', ' ').title()}**: {count} videos\n"
        else:
            overview += "- Various video formats detected\n"
        
        return overview + "\n"
    
    def _analyze_performance(self, videos: List[Dict]) -> str:
        """Analyze performance metrics"""
        performance = "## 📈 Performance Analysis\n\n"
        
        total_views = 0
        total_likes = 0
        total_comments = 0
        view_counts = []
        
        for video in videos:
            try:
                views = self._parse_count(video.get('viewCount', '0'))
                likes = self._parse_count(video.get('likes', '0'))
                comments = self._parse_count(video.get('commentsCount', '0'))
                
                total_views += views
                total_likes += likes
                total_comments += comments
                view_counts.append(views)
                
            except (ValueError, AttributeError):
                continue
        
        if view_counts:
            avg_views = total_views // len(videos)
            max_views = max(view_counts)
            min_views = min(view_counts)
            
            performance += f"""### Key Performance Metrics
- **Total Views**: {total_views:,}
- **Average Views per Video**: {avg_views:,}
- **Highest Performing**: {max_views:,} views
- **Lowest Performing**: {min_views:,} views
- **Total Likes**: {total_likes:,}
- **Total Comments**: {total_comments:,}
"""
            
            if total_views > 0:
                engagement_rate = ((total_likes + total_comments) / total_views) * 100
                performance += f"- **Overall Engagement Rate**: {engagement_rate:.2f}%\n"
            
            # Performance insights
            performance += "\n### Performance Insights\n"
            if max_views > avg_views * 3:
                performance += "- **Viral content detected** - One video significantly outperforms others\n"
            if avg_views > 100000:
                performance += "- **Strong channel performance** - Above average viewership\n"
            elif avg_views < 1000:
                performance += "- **Room for growth** - Consider content optimization\n"
            else:
                performance += "- **Steady performance** - Consistent viewership\n"
        
        return performance + "\n"
    
    def _analyze_content(self, videos: List[Dict]) -> str:
        """Analyze content characteristics"""
        content = "## 🎬 Content Analysis\n\n"
        
        title_lengths = []
        description_lengths = []
        
        for video in videos:
            title = video.get('title', '')
            description = video.get('description', '')
            
            if title:
                title_lengths.append(len(title))
            if description:
                description_lengths.append(len(description))
        
        if title_lengths:
            avg_title_length = sum(title_lengths) / len(title_lengths)
            content += f"### Title Optimization\n"
            content += f"- **Average Title Length**: {avg_title_length:.1f} characters\n"
            
            if avg_title_length < 50:
                content += "- **Title optimization needed** - Consider longer, more descriptive titles\n"
            elif avg_title_length > 100:
                content += "- **Titles may be too long** - Risk of truncation in results\n"
            else:
                content += "- **Good title length** - Optimized for search and display\n"
        
        if description_lengths:
            avg_desc_length = sum(description_lengths) / len(description_lengths)
            content += f"\n### Description Strategy\n"
            content += f"- **Average Description Length**: {avg_desc_length:.1f} characters\n"
            
            if avg_desc_length < 500:
                content += "- **Descriptions need more detail** - Add value, links, and keywords\n"
            else:
                content += "- **Good description length** - Adequate detail for SEO and user info\n"
        
        return content + "\n"
    
    def _analyze_engagement(self, videos: List[Dict]) -> str:
        """Analyze engagement patterns"""
        engagement = "## 💬 Engagement Analysis\n\n"
        
        engagement_rates = []
        
        for video in videos:
            try:
                views = self._parse_count(video.get('viewCount', '0'))
                likes = self._parse_count(video.get('likes', '0'))
                comments = self._parse_count(video.get('commentsCount', '0'))
                
                if views > 0:
                    er = ((likes + comments) / views) * 100
                    engagement_rates.append(er)
                    
            except (ValueError, AttributeError):
                continue
        
        if engagement_rates:
            avg_er = sum(engagement_rates) / len(engagement_rates)
            max_er = max(engagement_rates)
            min_er = min(engagement_rates)
            
            engagement += f"""### Engagement Metrics
- **Average Engagement Rate**: {avg_er:.2f}%
- **Highest Engagement**: {max_er:.2f}%
- **Lowest Engagement**: {min_er:.2f}%
"""
            
            # Engagement insights
            engagement += "\n### Engagement Insights\n"
            if avg_er > 5:
                engagement += "- **Excellent engagement** - Strong audience connection\n"
            elif avg_er > 3:
                engagement += "- **Good engagement** - Active and interested audience\n"
            elif avg_er > 1:
                engagement += "- **Moderate engagement** - Room for improvement\n"
            else:
                engagement += "- **Low engagement** - Focus on community building\n"
            
            if max_er > avg_er * 3:
                engagement += "- **Content resonance detected** - Some topics perform significantly better\n"
        
        return engagement + "\n"
    
    def _generate_strategy(self, videos: List[Dict]) -> str:
        """Generate strategic recommendations"""
        strategy = "## 🚀 Content Strategy Recommendations\n\n"
        
        # Analyze top performing videos
        video_data_with_performance = []
        for video in videos:
            try:
                views = self._parse_count(video.get('viewCount', '0'))
                likes = self._parse_count(video.get('likes', '0'))
                comments = self._parse_count(video.get('commentsCount', '0'))
                
                if views > 0:
                    er = ((likes + comments) / views) * 100
                    video_data_with_performance.append({
                        'video': video,
                        'views': views,
                        'engagement_rate': er
                    })
            except (ValueError, AttributeError):
                continue
        
        if video_data_with_performance:
            # Sort by views to find top performers
            top_by_views = sorted(video_data_with_performance, key=lambda x: x['views'], reverse=True)[:3]
            top_by_engagement = sorted(video_data_with_performance, key=lambda x: x['engagement_rate'], reverse=True)[:3]
            
            strategy += "### 🔥 Top Performing Content Patterns\n\n"
            strategy += "**Most Viewed Videos:**\n"
            for i, data in enumerate(top_by_views, 1):
                title = data['video'].get('title', 'Unknown')[:50]
                strategy += f"{i}. {title}... ({data['views']:,} views)\n"
            
            strategy += "\n**Highest Engagement:**\n"
            for i, data in enumerate(top_by_engagement, 1):
                title = data['video'].get('title', 'Unknown')[:50]
                strategy += f"{i}. {title}... ({data['engagement_rate']:.2f}% ER)\n"
            
            strategy += "\n### 📋 Strategic Recommendations\n\n"
            
            # Extract patterns from top performers
            top_titles = [data['video'].get('title', '').lower() for data in top_by_views]
            
            # Common patterns
            if any('how to' in title or 'tutorial' in title for title in top_titles):
                strategy += "1. **Double Down on Educational Content** - 'How-to' formats are resonating\n"
            
            if any('fitness' in title or 'workout' in title for title in top_titles):
                strategy += "2. **Expand Fitness Vertical** - Health and wellness content performs well\n"
            
            if any(len(title.split()) > 8 for title in top_titles):
                strategy += "3. **Use Descriptive Titles** - Longer, keyword-rich titles are working\n"
            else:
                strategy += "3. **Optimize Title Length** - Consider more descriptive, searchable titles\n"
            
            strategy += "\n4. **Content Calendar Optimization**\n"
            strategy += "   - Schedule high-performing content types during peak engagement hours\n"
            strategy += "   - Create series content to build audience anticipation\n"
            strategy += "   - Cross-promote high-engagement videos in descriptions\n"
        
        return strategy + "\n"
    
    def _generate_action_items(self, videos: List[Dict]) -> str:
        """Generate specific action items"""
        actions = "## ✅ Immediate Action Items\n\n"
        
        actions += "### 📊 Content Optimization\n"
        actions += "- [ ] Analyze top 3 performing videos for common elements\n"
        actions += "- [ ] Create content templates based on successful formats\n"
        actions += "- [ ] Optimize video thumbnails to match high-performers\n"
        actions += "- [ ] A/B test title styles and descriptions\n\n"
        
        actions += "### 🎯 Audience Growth\n"
        actions += "- [ ] Identify peak posting times from analytics\n"
        actions += "- [ ] Engage with comments within first 2 hours of posting\n"
        actions += "- [ ] Create call-to-action sequences to boost engagement\n"
        actions += "- [ ] Collaborate with creators in similar niches\n\n"
        
        actions += "### 📈 Performance Tracking\n"
        actions += "- [ ] Set up weekly performance review dashboard\n"
        actions += "- [ ] Track engagement rates by content type\n"
        actions += "- [ ] Monitor competitor content strategies\n"
        actions += "- [ ] Adjust content mix based on monthly performance data\n"
        
        return actions + "\n"
    
    def _parse_count(self, count_str: str) -> int:
        """Parse count string to integer (handles K, M, B suffixes)"""
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

def main():
    # Load video data from previous scraping
    try:
        with open("youtube_results.json", "r", encoding="utf-8") as f:
            video_data = json.load(f)
    except FileNotFoundError:
        print("No video data found. Run enhanced_scraper.py first.")
        return
    except json.JSONDecodeError:
        print("Invalid video data file.")
        return
    
    # Initialize analyzer
    analyzer = VideoAnalyzer()
    
    # Generate analysis
    analysis = analyzer.analyze_videos(video_data)
    
    # Save analysis
    with open("video_analysis.md", "w", encoding="utf-8") as f:
        f.write(analysis)
    
    print("📊 Video Analysis Report")
    print("=" * 50)
    print(analysis)
    print("\n✅ Analysis saved to video_analysis.md")

if __name__ == "__main__":
    main()
