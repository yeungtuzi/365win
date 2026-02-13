#!/usr/bin/env python3
# 可靠爬虫 - 使用公开API和RSS源

import os
import json
import time
import requests
import feedparser
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib

class ReliableCrawler:
    """可靠爬虫：使用公开API和RSS源"""
    
    def __init__(self, storage_dir: str = "data/reliable_content"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
        # 使用公开API和RSS源（更可靠）
        self.sources = {
            "foreign": [
                {
                    "name": "Hacker News Top Stories",
                    "url": "https://hacker-news.firebaseio.com/v0/topstories.json",
                    "type": "api",
                    "lang": "en",
                    "category": "tech"
                },
                {
                    "name": "Reddit r/technology Hot",
                    "url": "https://www.reddit.com/r/technology/hot.json",
                    "type": "api",
                    "lang": "en",
                    "category": "tech"
                },
                {
                    "name": "Ars Technica RSS",
                    "url": "https://feeds.arstechnica.com/arstechnica/index",
                    "type": "rss",
                    "lang": "en",
                    "category": "tech"
                }
            ],
            "chinese": [
                {
                    "name": "知乎热榜",
                    "url": "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total",
                    "type": "api",
                    "lang": "zh",
                    "category": "general"
                },
                {
                    "name": "澎湃新闻科技频道",
                    "url": "https://www.thepaper.cn/techChannel",
                    "type": "html",
                    "lang": "zh",
                    "category": "tech"
                },
                {
                    "name": "果壳网科学人",
                    "url": "https://www.guokr.com/scientific/",
                    "type": "html",
                    "lang": "zh",
                    "category": "science"
                }
            ]
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/html, application/xhtml+xml, application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        
        # Reddit需要特定的User-Agent
        self.reddit_headers = {
            'User-Agent': 'MyRedditApp/1.0 by (YourUsername)',
            'Accept': 'application/json'
        }
        
        self.timeout = 10
    
    def fetch_from_api(self, url: str, source: Dict) -> List[Dict]:
        """从API获取数据"""
        articles = []
        
        try:
            print(f"  从API获取: {source['name']}")
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                if "hacker-news" in url:
                    # Hacker News API
                    top_stories = data[:5]  # 前5个故事
                    for story_id in top_stories:
                        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                        story_response = requests.get(story_url, timeout=self.timeout)
                        if story_response.status_code == 200:
                            story = story_response.json()
                            if story.get("title") and story.get("url"):
                                article = {
                                    "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                                    "title": story.get("title", "无标题"),
                                    "content": story.get("text", "") or f"Hacker News story: {story.get('title', '')}",
                                    "source": source["name"],
                                    "language": source["lang"],
                                    "category": source["category"],
                                    "crawl_time": datetime.now().isoformat(),
                                    "content_hash": hashlib.md5(str(story_id).encode()).hexdigest()[:16]
                                }
                                articles.append(article)
                
                elif "reddit.com" in url:
                    # Reddit API - 使用特定的headers
                    try:
                        reddit_response = requests.get(url, headers=self.reddit_headers, timeout=self.timeout)
                        if reddit_response.status_code == 200:
                            reddit_data = reddit_response.json()
                            if "data" in reddit_data and "children" in reddit_data["data"]:
                                for child in reddit_data["data"]["children"][:3]:
                                    post = child.get("data", {})
                                    if post.get("title"):
                                        article = {
                                            "url": f"https://reddit.com{post.get('permalink', '')}",
                                            "title": post.get("title", "无标题"),
                                            "content": post.get("selftext", "")[:500] or f"Reddit post: {post.get('title', '')}",
                                            "source": source["name"],
                                            "language": source["lang"],
                                            "category": source["category"],
                                            "crawl_time": datetime.now().isoformat(),
                                            "content_hash": hashlib.md5(post.get("id", "").encode()).hexdigest()[:16]
                                        }
                                        articles.append(article)
                        else:
                            print(f"  Reddit API请求失败: {reddit_response.status_code}")
                    except Exception as e:
                        print(f"  Reddit API错误: {type(e).__name__}")
                
                elif "zhihu.com" in url:
                    # 知乎API
                    if "data" in data:
                        for item in data["data"][:5]:
                            target = item.get("target", {})
                            if target.get("title") or target.get("question", {}).get("title"):
                                title = target.get("title") or target.get("question", {}).get("title", "无标题")
                                content = target.get("content", "") or target.get("excerpt", "") or ""
                                
                                article = {
                                    "url": f"https://www.zhihu.com/question/{target.get('id', '')}",
                                    "title": title[:200],
                                    "content": content[:2000],
                                    "source": source["name"],
                                    "language": source["lang"],
                                    "category": source["category"],
                                    "crawl_time": datetime.now().isoformat(),
                                    "content_hash": hashlib.md5(str(target.get("id", "")).encode()).hexdigest()[:16]
                                }
                                articles.append(article)
            
            else:
                print(f"  API请求失败: {response.status_code}")
                
        except Exception as e:
            print(f"  API获取失败: {type(e).__name__}")
        
        return articles
    
    def fetch_from_rss(self, url: str, source: Dict) -> List[Dict]:
        """从RSS获取数据"""
        articles = []
        
        try:
            print(f"  从RSS获取: {source['name']}")
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:5]:
                if entry.get("title"):
                    article = {
                        "url": entry.get("link", ""),
                        "title": entry.get("title", "无标题"),
                        "content": entry.get("summary", "") or entry.get("description", "") or "",
                        "source": source["name"],
                        "language": source["lang"],
                        "category": source["category"],
                        "crawl_time": datetime.now().isoformat(),
                        "content_hash": hashlib.md5(entry.get("link", "").encode()).hexdigest()[:16]
                    }
                    articles.append(article)
        
        except Exception as e:
            print(f"  RSS获取失败: {type(e).__name__}")
        
        return articles
    
    def fetch_from_html(self, url: str, source: Dict) -> List[Dict]:
        """从HTML页面获取数据（简化版）"""
        articles = []
        
        try:
            print(f"  从HTML获取: {source['name']}")
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code == 200:
                # 简单提取标题
                import re
                html = response.text
                
                # 提取页面标题
                title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE)
                title = title_match.group(1).strip() if title_match else source["name"]
                
                # 简单内容提取
                content = f"{source['name']}的最新内容。请访问 {url} 查看详情。"
                
                article = {
                    "url": url,
                    "title": title[:200],
                    "content": content,
                    "source": source["name"],
                    "language": source["lang"],
                    "category": source["category"],
                    "crawl_time": datetime.now().isoformat(),
                    "content_hash": hashlib.md5(url.encode()).hexdigest()[:16]
                }
                articles.append(article)
        
        except Exception as e:
            print(f"  HTML获取失败: {type(e).__name__}")
        
        return articles
    
    def crawl_source(self, source: Dict) -> List[Dict]:
        """爬取单个源"""
        print(f"爬取 {source['name']}...")
        
        articles = []
        
        try:
            if source["type"] == "api":
                articles = self.fetch_from_api(source["url"], source)
            elif source["type"] == "rss":
                articles = self.fetch_from_rss(source["url"], source)
            elif source["type"] == "html":
                articles = self.fetch_from_html(source["url"], source)
            
            print(f"  成功获取 {len(articles)} 篇文章")
            
        except Exception as e:
            print(f"  爬取失败: {e}")
        
        return articles
    
    def daily_crawl(self) -> Dict[str, List[Dict]]:
        """每日爬取任务"""
        print("开始可靠爬取任务...")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        all_articles = {"foreign": [], "chinese": []}
        
        # 爬取外文源
        print("\n爬取外文源:")
        for source in self.sources["foreign"]:
            articles = self.crawl_source(source)
            all_articles["foreign"].extend(articles)
            time.sleep(2)  # 礼貌延迟
        
        # 爬取中文源
        print("\n爬取中文源:")
        for source in self.sources["chinese"]:
            articles = self.crawl_source(source)
            all_articles["chinese"].extend(articles)
            time.sleep(2)
        
        # 保存结果
        self.save_daily_crawl(all_articles)
        
        print(f"\n爬取完成: 外文 {len(all_articles['foreign'])} 篇, 中文 {len(all_articles['chinese'])} 篇")
        return all_articles
    
    def save_daily_crawl(self, articles: Dict[str, List[Dict]]):
        """保存每日爬取结果"""
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"{self.storage_dir}/crawl_{date_str}.json"
        
        data = {
            "crawl_date": datetime.now().isoformat(),
            "total_foreign": len(articles["foreign"]),
            "total_chinese": len(articles["chinese"]),
            "articles": articles
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"爬取结果已保存: {filename}")
        
        # 清理旧数据（保留7天）
        self.clean_old_data(days=7)
    
    def clean_old_data(self, days: int = 7):
        """清理旧数据"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for filename in os.listdir(self.storage_dir):
            if filename.startswith("crawl_") and filename.endswith(".json"):
                filepath = os.path.join(self.storage_dir, filename)
                
                # 从文件名提取日期
                try:
                    date_str = filename[6:14]  # crawl_YYYYMMDD.json
                    file_date = datetime.strptime(date_str, "%Y%m%d")
                    
                    if file_date < cutoff_date:
                        os.remove(filepath)
                        print(f"清理旧数据: {filename}")
                except:
                    pass
    
    def load_recent_data(self, days: int = 3) -> List[Dict]:
        """加载最近几天的数据"""
        print(f"加载最近 {days} 天的数据...")
        
        all_articles = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for filename in os.listdir(self.storage_dir):
            if filename.startswith("crawl_") and filename.endswith(".json"):
                filepath = os.path.join(self.storage_dir, filename)
                
                try:
                    # 检查日期
                    date_str = filename[6:14]
                    file_date = datetime.strptime(date_str, "%Y%m%d")
                    
                    if file_date >= cutoff_date:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # 合并文章
                        for lang in ["foreign", "chinese"]:
                            for article in data["articles"].get(lang, []):
                                article["crawl_date"] = data["crawl_date"]
                                all_articles.append(article)
                        
                        print(f"  加载: {filename} ({len(data['articles']['foreign'])}外文, {len(data['articles']['chinese'])}中文)")
                
                except Exception as e:
                    print(f"  加载失败 {filename}: {e}")
        
        print(f"总共加载 {len(all_articles)} 篇文章")
        return all_articles

# 测试函数
if __name__ == "__main__":
    print("测试可靠爬虫...")
    crawler = ReliableCrawler()
    
    # 测试爬取
    result = crawler.daily_crawl()
    
    if result["foreign"] or result["chinese"]:
        print(f"\n爬取结果:")
        print(f"  外文文章: {len(result['foreign'])} 篇")
        print(f"  中文文章: {len(result['chinese'])} 篇")
        
        if result["foreign"]:
            print("\n  外文文章示例:")
            for i, article in enumerate(result["foreign"][:2]):
                print(f"    {i+1}. {article['title'][:50]}...")
                print(f"        来源: {article['source']}")
                print(f"        内容: {article['content'][:80]}...")
        
        if result["chinese"]:
            print("\n  中文文章示例:")
            for i, article in enumerate(result["chinese"][:2]):
                print(f"    {i+1}. {article['title'][:50]}...")
                print(f"        来源: {article['source']}")
                print(f"        内容: {article['content'][:80]}...")
    else:
        print("⚠️ 爬取返回0篇文章")