#!/usr/bin/env python3
"""
Short Video Downloader and Analyzer
Supports downloading YouTube and TikTok videos for analysis
"""

import os
import subprocess
import json
import logging
from typing import List, Optional
from urllib.parse import urlparse
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ShortVideoDownloader:
    def __init__(self, download_dir: str = "downloaded_videos"):
        self.download_dir = download_dir
        self._ensure_download_dir()
        
        # Check if yt-dlp is available
        try:
            subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
            self.yt_dlp_available = True
            logger.info("yt-dlp is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.yt_dlp_available = False
            logger.warning("yt-dlp not found. Video download functionality will be limited.")
    
    def _ensure_download_dir(self):
        """Create download directory if it doesn't exist"""
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            logger.info(f"Created download directory: {self.download_dir}")
    
    def _get_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from various platforms"""
        # YouTube
        youtube_pattern = r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})'
        match = re.search(youtube_pattern, url)
        if match:
            return match.group(1)
        
        # TikTok
        tiktok_pattern = r'tiktok\.com/@[^/]+/video/(\d+)'
        match = re.search(tiktok_pattern, url)
        if match:
            return match.group(1)
        
        return None
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is from supported platforms"""
        supported_domains = ['youtube.com', 'youtu.be', 'tiktok.com', 'www.tiktok.com']
        parsed = urlparse(url)
        return any(domain in parsed.netloc.lower() for domain in supported_domains)
    
    def download_youtube_video(self, url: str, quality: str = "best") -> Optional[str]:
        """Download YouTube video using yt-dlp"""
        if not self.yt_dlp_available:
            logger.error("yt-dlp is not available for YouTube downloads")
            return None
        
        video_id = self._get_video_id(url)
        if not video_id:
            logger.error(f"Invalid YouTube URL: {url}")
            return None
        
        output_template = os.path.join(self.download_dir, f"{video_id}.%(title)s.%(ext)s")
        
        try:
            cmd = [
                'yt-dlp',
                '--format', quality,
                '--output', output_template,
                '--write-info-json',
                '--write-thumbnail',
                '--no-playlist',
                url
            ]
            
            logger.info(f"Downloading YouTube video: {url}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Find the downloaded file
            info_file = os.path.join(self.download_dir, f"{video_id}.info.json")
            if os.path.exists(info_file):
                with open(info_file, 'r', encoding='utf-8') as f:
                    info = json.load(f)
                    title = info.get('title', video_id)
                    
                # Look for video file
                for file in os.listdir(self.download_dir):
                    if video_id in file and file.endswith(('.mp4', '.webm', '.mkv')):
                        video_path = os.path.join(self.download_dir, file)
                        logger.info(f"Successfully downloaded: {video_path}")
                        return video_path
            
            logger.error("Could not find downloaded video file")
            return None
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error downloading video: {e}")
            logger.error(f"yt-dlp stderr: {e.stderr}")
            return None
    
    def download_tiktok_video(self, url: str) -> Optional[str]:
        """Download TikTok video using yt-dlp"""
        if not self.yt_dlp_available:
            logger.error("yt-dlp is not available for TikTok downloads")
            return None
        
        video_id = self._get_video_id(url)
        if not video_id:
            logger.error(f"Invalid TikTok URL: {url}")
            return None
        
        output_template = os.path.join(self.download_dir, f"tiktok_{video_id}.%(ext)s")
        
        try:
            cmd = [
                'yt-dlp',
                '--format', 'best',
                '--output', output_template,
                '--write-info-json',
                '--no-playlist',
                url
            ]
            
            logger.info(f"Downloading TikTok video: {url}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Find the downloaded file
            for file in os.listdir(self.download_dir):
                if f"tiktok_{video_id}" in file:
                    video_path = os.path.join(self.download_dir, file)
                    if file.endswith(('.mp4', '.webm')):
                        logger.info(f"Successfully downloaded: {video_path}")
                        return video_path
                    elif file.endswith('.info.json'):
                        with open(video_path, 'r', encoding='utf-8') as f:
                            info = json.load(f)
                            logger.info(f"TikTok video info: {info.get('title', 'No title')}")
            
            logger.error("Could not find downloaded TikTok video file")
            return None
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error downloading TikTok video: {e}")
            logger.error(f"yt-dlp stderr: {e.stderr}")
            return None
    
    def download_video(self, url: str, quality: str = "best") -> Optional[str]:
        """Download video from supported platforms"""
        if not self._is_valid_url(url):
            logger.error(f"Unsupported URL: {url}")
            return None
        
        if 'youtube.com' in url or 'youtu.be' in url:
            return self.download_youtube_video(url, quality)
        elif 'tiktok.com' in url:
            return self.download_tiktok_video(url)
        else:
            logger.error(f"Platform not supported for: {url}")
            return None
    
    def batch_download(self, urls: List[str], quality: str = "best") -> List[str]:
        """Download multiple videos"""
        downloaded_files = []
        
        for i, url in enumerate(urls, 1):
            logger.info(f"Processing video {i}/{len(urls)}: {url}")
            
            video_path = self.download_video(url, quality)
            if video_path:
                downloaded_files.append(video_path)
            else:
                logger.error(f"Failed to download: {url}")
        
        logger.info(f"Successfully downloaded {len(downloaded_files)}/{len(urls)} videos")
        return downloaded_files
    
    def get_video_info(self, url: str) -> Optional[dict]:
        """Get video information without downloading"""
        if not self.yt_dlp_available:
            return None
        
        try:
            cmd = [
                'yt-dlp',
                '--dump-json',
                '--no-playlist',
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            info = json.loads(result.stdout)
            return info
            
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            logger.error(f"Error getting video info: {e}")
            return None

def install_yt_dlp():
    """Install yt-dlp if not available"""
    try:
        subprocess.run(['pip', 'install', 'yt-dlp'], check=True)
        logger.info("yt-dlp installed successfully")
        return True
    except subprocess.CalledProcessError:
        logger.error("Failed to install yt-dlp")
        return False

def main():
    # Example usage
    downloader = ShortVideoDownloader()
    
    # Test URLs (you can modify these)
    test_urls = [
        "https://www.youtube.com/watch?v=ydTy5doG-4s",
        # Add more URLs as needed
    ]
    
    if not downloader.yt_dlp_available:
        print("yt-dlp is required for video downloads.")
        choice = input("Would you like to install yt-dlp? (y/n): ")
        if choice.lower() == 'y':
            if install_yt_dlp():
                # Reinitialize after installation
                downloader = ShortVideoDownloader()
            else:
                print("Installation failed. Exiting.")
                return
        else:
            print("Cannot download videos without yt-dlp. Exiting.")
            return
    
    # Download videos
    downloaded = downloader.batch_download(test_urls)
    
    print(f"\n📥 Download Summary:")
    print(f"Total URLs: {len(test_urls)}")
    print(f"Successfully downloaded: {len(downloaded)}")
    
    for video_path in downloaded:
        print(f"✅ {video_path}")
    
    print(f"\n📁 All videos saved in: {downloader.download_dir}")

if __name__ == "__main__":
    main()
