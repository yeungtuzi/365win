#!/usr/bin/env python3
# 网络爬虫模块 - 实时采集中外互联网信息

import os
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import feedparser
from bs4 import BeautifulSoup
import re

class WebCrawler:
    """网络爬虫，采集中外互联网实时信息"""
    
    def __init__(self, cache_dir: str = "cache/raw_data"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        # 配置爬取源
        self.sources = {
            # 外文源 (70%)
            "foreign": {
                "news": [
                    {"name": "BBC News", "url": "http://feeds.bbci.co.uk/news/rss.xml", "lang": "en"},
                    {"name": "Reuters", "url": "http://feeds.reuters.com/reuters/topNews", "lang": "en"},
                    {"name": "AP News", "url": "http://hosted2.ap.org/atom/APDEFAULT/3d281c11a96b4ad082fe88aa0db04305", "lang": "en"},
                ],
                "tech": [
                    {"name": "TechCrunch", "url": "http://feeds.feedburner.com/TechCrunch/", "lang": "en"},
                    {"name": "Wired", "url": "https://www.wired.com/feed/rss", "lang": "en"},
                    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "lang": "en"},
                ],
                "science": [
                    {"name": "arXiv", "url": "http://arxiv.org/rss/cs.AI", "lang": "en"},  # AI类别
                    {"name": "Nature News", "url": "https://www.nature.com/nature.rss", "lang": "en"},
                ]
            },
            # 中文源 (30%)
            "chinese": {
                "news": [
                    {"name": "人民日报", "url": "http://www.people.com.cn/rss/politics.xml", "lang": "zh"},
                    {"name": "新华社", "url": "http://www.xinhuanet.com/rss.xml", "lang": "zh"},
                    {"name": "央视新闻", "url": "http://news.cctv.com/rss/news.xml", "lang": "zh"},
                ],
                "tech": [
                    {"name": "36氪", "url": "https://36kr.com/feed", "lang": "zh"},
                    {"name": "虎嗅", "url": "https://www.huxiu.com/rss/0.xml", "lang": "zh"},
                ],
                "social": [
                    {"name": "微博热搜", "url": "https://s.weibo.com/top/summary", "lang": "zh", "type": "html"},
                    {"name": "知乎热榜", "url": "https://www.zhihu.com/billboard", "lang": "zh", "type": "html"},
                ]
            }
        }
        
        # 用户代理
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_rss_feed(self, feed_url: str, source_name: str) -> List[Dict]:
        """获取RSS订阅内容"""
        items = []
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:10]:  # 每个源取前10条
                item = {
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", entry.get("description", "")),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", datetime.now().isoformat()),
                    "source": source_name,
                    "language": "en" if "bbc" in feed_url.lower() or "reuters" in feed_url.lower() else "zh"
                }
                
                # 清理HTML标签
                if item["summary"]:
                    soup = BeautifulSoup(item["summary"], 'html.parser')
                    item["summary"] = soup.get_text()[:500]  # 限制长度
                
                items.append(item)
        except Exception as e:
            print(f"获取RSS失败 {source_name}: {e}")
        
        return items
    
    def fetch_html_content(self, url: str, source_name: str) -> List[Dict]:
        """获取HTML页面内容（用于微博、知乎等）"""
        items = []
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if "weibo.com" in url:
                # 微博热搜解析
                hot_items = soup.select('.td-02 a')
                for i, item in enumerate(hot_items[:20]):
                    title = item.get_text().strip()
                    if title and not title.startswith("#"):
                        items.append({
                            "title": f"微博热搜: {title}",
                            "summary": f"当前微博热搜第{i+1}位",
                            "link": f"https://s.weibo.com{item.get('href', '')}",
                            "published": datetime.now().isoformat(),
                            "source": "微博热搜",
                            "language": "zh"
                        })
            
            elif "zhihu.com" in url:
                # 知乎热榜解析
                hot_items = soup.select('.HotList-item .HotList-itemTitle')
                for i, item in enumerate(hot_items[:20]):
                    title = item.get_text().strip()
                    items.append({
                        "title": f"知乎热榜: {title}",
                        "summary": f"当前知乎热榜第{i+1}位",
                        "link": f"https://www.zhihu.com{item.get('href', '')}",
                        "published": datetime.now().isoformat(),
                        "source": "知乎热榜",
                        "language": "zh"
                    })
                    
        except Exception as e:
            print(f"获取HTML失败 {source_name}: {e}")
        
        return items
    
    def crawl_all_sources(self, max_items_per_source: int = 5) -> Dict[str, List[Dict]]:
        """爬取所有配置的源"""
        all_items = {"foreign": [], "chinese": []}
        
        print(f"开始爬取互联网实时信息...")
        
        # 爬取外文源 (70%)
        foreign_count = 0
        for category, sources in self.sources["foreign"].items():
            for source in sources:
                if source.get("type") == "html":
                    items = self.fetch_html_content(source["url"], source["name"])
                else:
                    items = self.fetch_rss_feed(source["url"], source["name"])
                
                # 限制每个源的条目数
                items = items[:max_items_per_source]
                all_items["foreign"].extend(items)
                foreign_count += len(items)
                
                print(f"  爬取 {source['name']}: {len(items)} 条")
                time.sleep(1)  # 礼貌延迟
        
        # 爬取中文源 (30%)
        chinese_count = 0
        for category, sources in self.sources["chinese"].items():
            for source in sources:
                if source.get("type") == "html":
                    items = self.fetch_html_content(source["url"], source["name"])
                else:
                    items = self.fetch_rss_feed(source["url"], source["name"])
                
                items = items[:max_items_per_source]
                all_items["chinese"].extend(items)
                chinese_count += len(items)
                
                print(f"  爬取 {source['name']}: {len(items)} 条")
                time.sleep(1)
        
        print(f"爬取完成: 外文 {foreign_count} 条, 中文 {chinese_count} 条")
        
        # 保存到缓存
        self.save_to_cache(all_items)
        
        return all_items
    
    def save_to_cache(self, items: Dict[str, List[Dict]]):
        """保存爬取结果到缓存"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cache_file = os.path.join(self.cache_dir, f"crawled_{timestamp}.json")
        
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "total_foreign": len(items["foreign"]),
            "total_chinese": len(items["chinese"]),
            "items": items
        }
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
        print(f"缓存已保存: {cache_file}")
        
        # 清理3天前的缓存
        self.clean_old_cache(days=3)
    
    def clean_old_cache(self, days: int = 3):
        """清理指定天数前的缓存文件"""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        for filename in os.listdir(self.cache_dir):
            if filename.startswith("crawled_") and filename.endswith(".json"):
                filepath = os.path.join(self.cache_dir, filename)
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                if file_time < cutoff_time:
                    os.remove(filepath)
                    print(f"清理旧缓存: {filename}")
    
    def load_from_cache(self, hours: int = 72) -> Optional[Dict]:
        """从缓存加载数据（默认加载72小时内的）"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        latest_cache = None
        latest_time = None
        
        for filename in os.listdir(self.cache_dir):
            if filename.startswith("crawled_") and filename.endswith(".json"):
                filepath = os.path.join(self.cache_dir, filename)
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                if file_time >= cutoff_time:
                    if latest_time is None or file_time > latest_time:
                        latest_time = file_time
                        latest_cache = filepath
        
        if latest_cache:
            try:
                with open(latest_cache, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"从缓存加载: {os.path.basename(latest_cache)} ({len(data['items']['foreign'])}外文, {len(data['items']['chinese'])}中文)")
                return data
            except Exception as e:
                print(f"加载缓存失败: {e}")
        
        return None
    
    def get_content_for_recommendation(self, use_cached: bool = True) -> List[Dict]:
        """获取用于推荐的内容（混合中外内容，70%外文，30%中文）"""
        data = None
        
        if use_cached:
            data = self.load_from_cache(hours=72)
        
        # 如果没有缓存或强制重新爬取
        if not data:
            print("无有效缓存，开始实时爬取...")
            crawled_data = self.crawl_all_sources()
            data = {
                "timestamp": datetime.now().isoformat(),
                "items": crawled_data
            }
        
        # 混合内容：70%外文，30%中文
        foreign_items = data["items"]["foreign"]
        chinese_items = data["items"]["chinese"]
        
        # 计算目标数量（假设总共需要30条）
        total_needed = 30
        foreign_target = int(total_needed * 0.7)
        chinese_target = total_needed - foreign_target
        
        # 选择内容
        selected_foreign = foreign_items[:min(foreign_target, len(foreign_items))]
        selected_chinese = chinese_items[:min(chinese_target, len(chinese_items))]
        
        # 标记语言
        for item in selected_foreign:
            item["needs_translation"] = True
            item["original_language"] = "en"
        
        for item in selected_chinese:
            item["needs_translation"] = False
            item["original_language"] = "zh"
        
        # 合并
        all_items = selected_foreign + selected_chinese
        
        print(f"准备推荐内容: {len(selected_foreign)}外文 + {len(selected_chinese)}中文 = {len(all_items)}条")
        
        return all_items

# 测试函数
if __name__ == "__main__":
    crawler = WebCrawler()
    
    # 测试爬取
    print("测试爬虫功能...")
    items = crawler.get_content_for_recommendation(use_cached=False)
    
    print(f"\n获取到 {len(items)} 条内容:")
    for i, item in enumerate(items[:3]):  # 显示前3条
        print(f"{i+1}. [{item['source']}] {item['title'][:50]}...")
        print(f"   需要翻译: {item.get('needs_translation', False)}")
        print()