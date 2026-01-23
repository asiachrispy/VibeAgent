#!/usr/bin/env python3
"""
AI Data Analyst Workflow - Complete automation system
Integrates IPIDEA scraping, video downloading, and comprehensive analysis
"""

import os
import json
import logging
import time
from typing import List, Dict, Optional
import argparse
from datetime import datetime

from enhanced_scraper import IPIDEAScraper
from amazon_scraper import AmazonScraper, analyze_amazon_product
from video_analyzer import VideoAnalyzer
from short_video_downloader import ShortVideoDownloader
from unified_data_analyzer import UnifiedDataAnalyzer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AIDataAnalystWorkflow:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.ipidea_scraper = IPIDEAScraper(api_token)
        self.amazon_scraper = AmazonScraper(api_token)
        self.video_analyzer = VideoAnalyzer()
        self.unified_analyzer = UnifiedDataAnalyzer()
        self.video_downloader = ShortVideoDownloader()
        
    def complete_analysis_workflow(self, urls: List[str]) -> str:
        """Execute complete analysis workflow for given URLs"""
        logger.info(f"Starting complete analysis for {len(urls)} URLs")
        
        # Categorize URLs
        amazon_urls = []
        youtube_urls = []
        tiktok_urls = []
        
        for url in urls:
            if 'amazon.' in url:
                amazon_urls.append(url)
            elif 'youtube.' in url or 'youtu.be' in url:
                youtube_urls.append(url)
            elif 'tiktok.' in url:
                tiktok_urls.append(url)
        
        results = {
            'amazon_data': None,
            'video_data': None,
            'amazon_analysis': None,
            'video_analysis': None,
            'comprehensive_analysis': None
        }
        
        # Phase 1: Data Collection
        logger.info("🔍 Phase 1: Data Collection")
        
        if amazon_urls:
            logger.info("Scraping Amazon products...")
            task_id = self.amazon_scraper.scrape_products_by_urls(amazon_urls)
            if task_id:
                results['amazon_data'] = self.amazon_scraper.get_task_result(task_id)
                if results['amazon_data']:
                    with open("amazon_products.json", "w", encoding="utf-8") as f:
                        json.dump(results['amazon_data'], f, indent=2, ensure_ascii=False)
        
        if youtube_urls:
            logger.info("Scraping YouTube videos...")
            task_id = self.ipidea_scraper.scrape_youtube_videos(youtube_urls)
            if task_id:
                results['video_data'] = self.ipidea_scraper.get_task_result(task_id)
                if results['video_data']:
                    with open("youtube_results.json", "w", encoding="utf-8") as f:
                        json.dump(results['video_data'], f, indent=2, ensure_ascii=False)
        
        # Phase 2: Video Download (optional)
        logger.info("📥 Phase 2: Video Download")
        video_urls = youtube_urls + tiktok_urls
        if video_urls:
            logger.info("Downloading videos for local analysis...")
            downloaded_videos = self.video_downloader.batch_download(video_urls)
            logger.info(f"Downloaded {len(downloaded_videos)} videos")
        
        # Phase 3: Analysis Generation
        logger.info("📊 Phase 3: Analysis Generation")
        
        if results['amazon_data']:
            logger.info("Generating Amazon analysis...")
            results['amazon_analysis'] = analyze_amazon_product(results['amazon_data'])
            
            with open("amazon_analysis.md", "w", encoding="utf-8") as f:
                f.write(results['amazon_analysis'])
        
        if results['video_data']:
            logger.info("Generating video analysis...")
            results['video_analysis'] = self.video_analyzer.analyze_videos(results['video_data'])
            
            with open("video_analysis.md", "w", encoding="utf-8") as f:
                f.write(results['video_analysis'])
        
        # Phase 4: Comprehensive Analysis
        logger.info("🎯 Phase 4: Comprehensive Strategic Analysis")
        results['comprehensive_analysis'] = self.unified_analyzer.analyze_all_data()
        
        # Save comprehensive report
        report_file = f"ai_analyst_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(results['comprehensive_analysis'])
        
        return report_file, results
    
    def interactive_mode(self):
        """Interactive mode for user input"""
        print("🤖 AI Data Analyst - Interactive Mode")
        print("=" * 50)
        
        while True:
            print("\n📋 Choose analysis type:")
            print("1. Amazon Product Analysis")
            print("2. YouTube/TikTok Video Analysis") 
            print("3. Complete Multi-Platform Analysis")
            print("4. Analyze Existing Data")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                urls = input("Enter Amazon product URLs (comma-separated): ").strip().split(',')
                urls = [url.strip() for url in urls if url.strip()]
                if urls:
                    self._execute_amazon_analysis(urls)
            
            elif choice == '2':
                urls = input("Enter YouTube/TikTok video URLs (comma-separated): ").strip().split(',')
                urls = [url.strip() for url in urls if url.strip()]
                if urls:
                    self._execute_video_analysis(urls)
            
            elif choice == '3':
                urls = input("Enter all URLs (Amazon, YouTube, TikTok - comma-separated): ").strip().split(',')
                urls = [url.strip() for url in urls if url.strip()]
                if urls:
                    self._execute_complete_analysis(urls)
            
            elif choice == '4':
                self._analyze_existing_data()
            
            elif choice == '5':
                print("👋 Exiting AI Data Analyst. Goodbye!")
                break
            
            else:
                print("❌ Invalid choice. Please try again.")
    
    def _execute_amazon_analysis(self, urls: List[str]):
        """Execute Amazon-specific analysis"""
        print(f"\n🛒 Analyzing {len(urls)} Amazon products...")
        task_id = self.amazon_scraper.scrape_products_by_urls(urls)
        
        if task_id:
            print("⏳ Waiting for data collection...")
            data = self.amazon_scraper.get_task_result(task_id)
            
            if data:
                analysis = analyze_amazon_product(data)
                print("\n📊 Amazon Analysis Results:")
                print("=" * 50)
                print(analysis)
                
                # Save files
                with open("amazon_products.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                with open("amazon_analysis.md", "w", encoding="utf-8") as f:
                    f.write(analysis)
                
                print("\n✅ Analysis saved to amazon_analysis.md")
            else:
                print("❌ Failed to retrieve Amazon data")
        else:
            print("❌ Failed to submit Amazon scraping task")
    
    def _execute_video_analysis(self, urls: List[str]):
        """Execute video-specific analysis"""
        print(f"\n📺 Analyzing {len(urls)} videos...")
        
        # Separate YouTube and TikTok URLs
        youtube_urls = [url for url in urls if 'youtube.' in url or 'youtu.be' in url]
        tiktok_urls = [url for url in urls if 'tiktok.' in url]
        
        if youtube_urls:
            task_id = self.ipidea_scraper.scrape_youtube_videos(youtube_urls)
            if task_id:
                print("⏳ Waiting for YouTube data collection...")
                data = self.ipidea_scraper.get_task_result(task_id)
                
                if data:
                    with open("youtube_results.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    analysis = self.video_analyzer.analyze_videos(data)
                    print("\n📊 Video Analysis Results:")
                    print("=" * 50)
                    print(analysis)
                    
                    with open("video_analysis.md", "w", encoding="utf-8") as f:
                        f.write(analysis)
                    
                    print("\n✅ Analysis saved to video_analysis.md")
        
        if tiktok_urls:
            print("📥 Downloading TikTok videos for analysis...")
            downloaded = self.video_downloader.batch_download(tiktok_urls)
            print(f"Downloaded {len(downloaded)} TikTok videos")
    
    def _execute_complete_analysis(self, urls: List[str]):
        """Execute complete multi-platform analysis"""
        print(f"\n🎯 Executing complete analysis for {len(urls)} URLs...")
        print("This may take several minutes...")
        
        report_file, results = self.complete_analysis_workflow(urls)
        
        print("\n📊 Complete Analysis Results:")
        print("=" * 50)
        print(results['comprehensive_analysis'])
        
        print(f"\n✅ Comprehensive report saved to: {report_file}")
        print("\n📁 Generated files:")
        print("- amazon_products.json" if results['amazon_data'] else "")
        print("- amazon_analysis.md" if results['amazon_analysis'] else "")
        print("- youtube_results.json" if results['video_data'] else "")
        print("- video_analysis.md" if results['video_analysis'] else "")
        print(f"- {report_file}")
    
    def _analyze_existing_data(self):
        """Analyze previously collected data"""
        print("\n📂 Analyzing existing data files...")
        
        analysis = self.unified_analyzer.analyze_all_data()
        
        print("\n📊 Existing Data Analysis:")
        print("=" * 50)
        print(analysis)
        
        # Save analysis
        report_file = self.unified_analyzer.save_comprehensive_report(analysis)
        print(f"\n✅ Analysis saved to: {report_file}")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="AI Data Analyst - Complete automation system")
    parser.add_argument("--token", default="a81f13858f618cf0b5cd72c4a990e47b", 
                       help="IPIDEA API token")
    parser.add_argument("--urls", nargs="*", 
                       help="URLs to analyze (Amazon, YouTube, TikTok)")
    parser.add_argument("--interactive", action="store_true", 
                       help="Run in interactive mode")
    
    args = parser.parse_args()
    
    # Initialize workflow
    workflow = AIDataAnalystWorkflow(args.token)
    
    if args.interactive:
        workflow.interactive_mode()
    elif args.urls:
        workflow._execute_complete_analysis(args.urls)
    else:
        print("🤖 AI Data Analyst")
        print("\nUsage options:")
        print("1. Interactive mode: python ai_analyst_workflow.py --interactive")
        print("2. Direct analysis: python ai_analyst_workflow.py --urls URL1 URL2 URL3")
        print("\nExample:")
        print('python ai_analyst_workflow.py --urls "https://amazon.com/dp/B08BD8WKBC" "https://youtube.com/watch?v=ydTy5doG-4s"')

if __name__ == "__main__":
    main()
