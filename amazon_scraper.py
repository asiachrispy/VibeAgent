#!/usr/bin/env python3
"""
Amazon Product Data Scraper using IPIDEA
Specialized for Amazon product analysis and insights
"""

import requests
import json
import time
import os
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AmazonScraper:
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
    
    def scrape_products_by_urls(self, product_urls: List[str]) -> Optional[str]:
        """Scrape Amazon products by their URLs"""
        spider_parameters = []
        for url in product_urls:
            spider_parameters.append({
                "num_of_posts": "1",
                "keyword": url
            })
        
        return self._submit_task("amazon.com", "amazon_product-by-keyword", 
                             spider_parameters, "{{ASIN}}")
    
    def scrape_products_by_keywords(self, keywords: List[str], num_results: int = 10) -> Optional[str]:
        """Scrape Amazon products by keywords"""
        spider_parameters = []
        for keyword in keywords:
            spider_parameters.append({
                "num_of_posts": str(num_results),
                "keyword": keyword
            })
        
        return self._submit_task("amazon.com", "amazon_search-by-keyword", 
                             spider_parameters, "search_results")
    
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
                logger.info(f"Amazon scraping task submitted. Task ID: {task_id}")
                return task_id
            else:
                logger.error(f"Task submission failed: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error submitting Amazon task: {e}")
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
                        logger.info(f"Downloading Amazon results from: {download_url}")
                        file_response = requests.get(download_url)
                        file_response.raise_for_status()
                        
                        data = file_response.json()
                        logger.info(f"Successfully downloaded {len(data)} Amazon products")
                        return data
                    else:
                        logger.info("Amazon task not completed yet, waiting...")
                        time.sleep(15)
                else:
                    logger.error(f"Error checking Amazon task: {result}")
                    return None
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Error checking Amazon task: {e}")
                time.sleep(5)
                continue
        
        logger.error("Amazon task timed out")
        return None

def analyze_amazon_product(product_data: Dict) -> str:
    """Generate comprehensive analysis of Amazon product"""
    
    analysis = f"""
# 📊 Amazon Product Analysis Report

## Product Overview
"""
    
    # Extract basic product information
    if product_data:
        product = product_data[0] if isinstance(product_data, list) else product_data
        
        # Basic info
        title = product.get("title", "N/A")
        asin = product.get("asin", "N/A") 
        brand = product.get("brand", "N/A")
        price = product.get("price", "N/A")
        
        analysis += f"""
**Product Title**: {title}
**ASIN**: {asin}
**Brand**: {brand}
**Price**: {price}
"""
        
        # Sales metrics
        rating = product.get("rating", "N/A")
        reviews_count = product.get("reviews_count", "N/A")
        bought_past_month = product.get("bought_past_month", "N/A")
        
        analysis += f"""
## Sales Performance Metrics
**Rating**: {rating}/5.0
**Reviews Count**: {reviews_count}
**Monthly Sales**: {bought_past_month}
"""
        
        # BSR rankings
        bsr_category = product.get("bsr_category", "N/A")
        bsr_rank = product.get("bsr_rank", "N/A")
        
        analysis += f"""
## Best Sellers Rank (BSR)
**Category**: {bsr_category}
**Rank**: {bsr_rank}
"""
        
        # Product features
        features = product.get("features", [])
        if features:
            analysis += "\n## Key Features\n"
            for i, feature in enumerate(features[:5], 1):
                analysis += f"{i}. {feature}\n"
        
        # Analysis insights
        analysis += """
## Strategic Insights & Recommendations

### Competitive Analysis
"""
        
        # Price analysis
        if price != "N/A" and isinstance(price, str):
            try:
                price_num = float(price.replace('$', '').replace(',', ''))
                if price_num < 20:
                    analysis += "- **Budget-friendly pricing** - Good for volume sales\n"
                elif price_num > 50:
                    analysis += "- **Premium pricing strategy** - Focus on quality and features\n"
                else:
                    analysis += "- **Mid-range pricing** - Competitive positioning\n"
            except:
                analysis += "- **Price analysis unavailable**\n"
        
        # Rating analysis
        if rating != "N/A" and isinstance(rating, (int, float)):
            if rating >= 4.5:
                analysis += "- **Excellent customer satisfaction** - Strong competitive advantage\n"
            elif rating >= 4.0:
                analysis += "- **Good customer satisfaction** - Room for improvement\n"
            else:
                analysis += "- **Moderate customer satisfaction** - Quality improvements needed\n"
        
        # Sales velocity
        if bought_past_month != "N/A":
            if "1K" in bought_past_month or "1000" in bought_past_month:
                analysis += "- **High sales velocity** - Strong product-market fit\n"
            elif "100" in bought_past_month:
                analysis += "- **Moderate sales velocity** - Stable performance\n"
            else:
                analysis += "- **Low sales velocity** - Marketing optimization needed\n"
        
        analysis += """
### Opportunities & Threats
**Opportunities**:
- Expand to related product categories
- Optimize listings with A+ content
- Consider Subscribe & Save program

**Threats**:
- Strong competition in this category
- Price sensitivity in the market
- Potential supply chain disruptions

### Action Items
1. **Monitor competitors** - Track price changes and new entrants
2. **Optimize listing** - Improve images, bullets, and description
3. **Gather more reviews** - Implement review generation strategy
4. **Inventory management** - Ensure adequate stock for sales velocity
"""
    
    return analysis

def main():
    # Configuration
    API_TOKEN = "a81f13858f618cf0b5cd72c4a990e47b"  # Replace with your token
    
    # Initialize Amazon scraper
    scraper = AmazonScraper(API_TOKEN)
    
    # Example: Scrape specific Amazon products
    product_urls = [
        "https://www.amazon.com/Amazon-Basics-Rockets-Decorative-Pillow/dp/B08BD8WKBC",
        # Add more product URLs as needed
    ]
    
    logger.info("Starting Amazon product scraping...")
    task_id = scraper.scrape_products_by_urls(product_urls)
    
    if task_id:
        logger.info(f"Waiting for Amazon task {task_id} to complete...")
        results = scraper.get_task_result(task_id)
        
        if results:
            # Save raw results
            with open("amazon_products.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            logger.info("Raw Amazon data saved to amazon_products.json")
            
            # Generate analysis
            analysis = analyze_amazon_product(results)
            
            # Save analysis
            with open("amazon_analysis.md", "w", encoding="utf-8") as f:
                f.write(analysis)
            logger.info("Amazon analysis saved to amazon_analysis.md")
            
            print(analysis)  # Print to console
        else:
            logger.error("Failed to get Amazon results")
    else:
        logger.error("Failed to submit Amazon task")

if __name__ == "__main__":
    main()
