#!/usr/bin/env python3
"""
Enhanced IPIDEA Scraper with Multiple Platform Support
Supports: YouTube, Amazon, TikTok, Instagram
"""

import requests
import json
import time
import os
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IPIDEAScraper:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://scraper.ipidea.net/builder"
        self.download_url = "https://api.ipidea.net/g/api/web-scraper-api/tasks_download"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.download_headers = {
            "token": api_token,
            "Content-Type": "application/x-www-form-urlencoded"
        }
    
    def scrape_youtube_videos(self, video_urls: List[str]) -> Optional[str]:
        """Scrape YouTube video data"""
        spider_parameters = []
        for url in video_urls:
            spider_parameters.append({
                "num_of_posts": "1",
                "keyword": url
            })
        
        return self._submit_task("youtube.com", "youtube_video-post_by-keyword", 
                             spider_parameters, "{{VideoID}}")
    
    def scrape_amazon_products(self, product_urls: List[str]) -> Optional[str]:
        """Scrape Amazon product data"""
        spider_parameters = []
        for url in product_urls:
            spider_parameters.append({
                "num_of_posts": "1",
                "keyword": url
            })
        
        return self._submit_task("amazon.com", "amazon_product-by-keyword", 
                             spider_parameters, "{{ASIN}}")
    
    def scrape_tiktok_videos(self, video_urls: List[str]) -> Optional[str]:
        """Scrape TikTok video data"""
        spider_parameters = []
        for url in video_urls:
            spider_parameters.append({
                "num_of_posts": "1", 
                "keyword": url
            })
        
        return self._submit_task("tiktok.com", "tiktok_video-post_by-keyword", 
                             spider_parameters, "{{VideoID}}")
    
    def _submit_task(self, spider_name: str, spider_id: str, 
                    spider_parameters: List[Dict], file_name: str) -> Optional[str]:
        """Submit scraping task to IPIDEA"""
        form_data = {
            "spider_name": spider_name,
            "spider_id": spider_id,
            "spider_parameters": json.dumps(spider_parameters),
            "spider_errors": "true",
            "file_name": file_name
        }
        
        try:
            response = requests.post(self.base_url, data=form_data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 200:
                task_id = result.get("data", {}).get("task_id")
                logger.info(f"Task submitted successfully. Task ID: {task_id}")
                return task_id
            else:
                logger.error(f"Task submission failed: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error submitting task: {e}")
            return None
    
    def get_task_result(self, task_id: str, max_wait_time: int = 300) -> Optional[Dict]:
        """Poll for task completion and download results"""
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            try:
                payload = {"tasks_id": task_id, "type": "json"}
                response = requests.post(self.download_url, 
                                    data=payload, headers=self.download_headers)
                response.raise_for_status()
                
                result = response.json()
                
                if result.get("code") == 200:
                    download_url = result.get("ret_data", {}).get("download")
                    if download_url:
                        logger.info(f"Downloading results from: {download_url}")
                        file_response = requests.get(download_url)
                        file_response.raise_for_status()
                        
                        data = file_response.json()
                        logger.info(f"Successfully downloaded {len(data)} records")
                        return data
                    else:
                        logger.info("Task not completed yet, waiting...")
                        time.sleep(10)
                else:
                    logger.error(f"Error checking task: {result}")
                    return None
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Error checking task: {e}")
                time.sleep(5)
                continue
        
        logger.error("Task timed out")
        return None

def main():
    # Configuration
    API_TOKEN = "a81f13858f618cf0b5cd72c4a990e47b"  # Replace with your token
    
    # Initialize scraper
    scraper = IPIDEAScraper(API_TOKEN)
    
    # Example: Scrape YouTube videos
    youtube_urls = [
        "https://www.youtube.com/watch?v=ydTy5doG-4s",
        "https://www.youtube.com/watch?v=cVmdH7yjBj4",
        "https://www.youtube.com/watch?v=jABUkxCK4EY"
    ]
    
    logger.info("Starting YouTube video scraping...")
    task_id = scraper.scrape_youtube_videos(youtube_urls)
    
    if task_id:
        logger.info(f"Waiting for task {task_id} to complete...")
        results = scraper.get_task_result(task_id)
        
        if results:
            # Save results
            with open("youtube_results.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            logger.info("Results saved to youtube_results.json")
        else:
            logger.error("Failed to get results")
    else:
        logger.error("Failed to submit task")

if __name__ == "__main__":
    main()
