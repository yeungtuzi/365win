#!/usr/bin/env python3
# 完整内容爬虫 - 获取网页正文内容

import os
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re
import hashlib

class FullContentCrawler:
    """完整内容爬虫，获取网页正文"""
    
    def __init__(self, storage_dir: str = "data/full_content"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
        # 配置数据源（更可靠的来源）
        self.sources = {
            "foreign": [
                {
                    "name": "BBC News Technology",
                    "url": "https://www.bbc.com/news/technology",
                    "type": "html",
                    "lang": "en",
                    "category": "tech"
                },
                {
                    "name": "Reuters Technology",
                    "url": "https://www.reuters.com/technology/",
                    "type": "html", 
                    "lang": "en",
                    "category": "tech"
                },
                {
                    "name": "AP News Technology",
                    "url": "https://apnews.com/technology",
                    "type": "html",
                    "lang": "en",
                    "category": "tech"
                }
            ],
            "chinese": [
                {
                    "name": "人民网科技",
                    "url": "http://scitech.people.com.cn/",
                    "type": "html",
                    "lang": "zh",
                    "category": "tech"
                },
                {
                    "name": "新华网科技",
                    "url": "http://www.xinhuanet.com/tech/",
                    "type": "html",
                    "lang": "zh",
                    "category": "tech"
                },
                {
                    "name": "央视网科技",
                    "url": "https://news.cctv.com/tech/",
                    "type": "html",
                    "lang": "zh",
                    "category": "tech"
                }
            ]
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        # 请求配置
        self.timeout = 15
        self.max_articles_per_source = 5
    
    def extract_article_links(self, html: str, source: Dict) -> List[str]:
        """从HTML中提取文章链接"""
        links = []
        
        try:
            # 简单的链接提取（避免复杂解析）
            if "bbc.com" in source["url"]:
                # BBC链接模式
                pattern = r'href="(/news/technology-[^"]+)"'
                matches = re.findall(pattern, html)
                links = [f"https://www.bbc.com{match}" for match in matches[:self.max_articles_per_source]]
            
            elif "reuters.com" in source["url"]:
                # Reuters链接模式
                pattern = r'href="(/technology/[^"]+)"'
                matches = re.findall(pattern, html)
                links = [f"https://www.reuters.com{match}" for match in matches[:self.max_articles_per_source]]
            
            elif "apnews.com" in source["url"]:
                # AP News链接模式
                pattern = r'href="(/article/[^"]+)"'
                matches = re.findall(pattern, html)
                links = [f"https://apnews.com{match}" for match in matches[:self.max_articles_per_source]]
            
            elif "people.com.cn" in source["url"]:
                # 人民网链接模式
                pattern = r'href="(http://scitech\.people\.com\.cn/[^"]+)"'
                links = re.findall(pattern, html)[:self.max_articles_per_source]
            
            elif "xinhuanet.com" in source["url"]:
                # 新华网链接模式
                pattern = r'href="(http://www\.xinhuanet\.com/[^"]+)"'
                links = re.findall(pattern, html)[:self.max_articles_per_source]
            
        except Exception as e:
            print(f"提取链接失败 {source['name']}: {e}")
        
        return list(set(links))  # 去重
    
    def extract_article_content(self, html: str, url: str) -> str:
        """提取文章正文内容（简化版）"""
        try:
            # 移除脚本和样式
            html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
            html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
            
            # 提取正文（简单方法）
            # 1. 查找article标签
            article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
            if article_match:
                content = article_match.group(1)
            else:
                # 2. 查找main标签
                main_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL | re.IGNORECASE)
                if main_match:
                    content = main_match.group(1)
                else:
                    # 3. 查找包含大量文本的div
                    div_pattern = r'<div[^>]*>(.{100,}?)</div>'
                    div_matches = re.findall(div_pattern, html, re.DOTALL)
                    if div_matches:
                        # 选择最长的div作为正文
                        content = max(div_matches, key=len)
                    else:
                        content = ""
            
            # 清理HTML标签
            content = re.sub(r'<[^>]+>', ' ', content)
            content = re.sub(r'\s+', ' ', content).strip()
            
            # 限制长度
            if len(content) > 5000:
                content = content[:5000] + "..."
            
            return content
            
        except Exception as e:
            print(f"提取内容失败 {url}: {e}")
            return ""
    
    def fetch_article(self, url: str, source: Dict) -> Optional[Dict]:
        """获取单篇文章"""
        try:
            print(f"  获取文章: {url[:60]}...")
            
            response = requests.get(
                url, 
                headers=self.headers, 
                timeout=self.timeout,
                verify=True
            )
            
            if response.status_code == 200:
                html = response.text
                content = self.extract_article_content(html, url)
                
                if content and len(content) > 100:  # 确保有足够内容
                    # 提取标题
                    title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE)
                    title = title_match.group(1).strip() if title_match else "无标题"
                    
                    # 清理标题
                    title = re.sub(r' - .*$', '', title)  # 移除网站名后缀
                    title = re.sub(r'\s*[|·-].*$', '', title)
                    
                    article = {
                        "url": url,
                        "title": title[:200],
                        "content": content,
                        "source": source["name"],
                        "language": source["lang"],
                        "category": source.get("category", "general"),
                        "crawl_time": datetime.now().isoformat(),
                        "content_hash": hashlib.md5(content.encode()).hexdigest()[:16]
                    }
                    
                    return article
            
            time.sleep(1)  # 礼貌延迟
            
        except requests.exceptions.Timeout:
            print(f"  超时: {url}")
        except Exception as e:
            print(f"  获取失败 {url}: {type(e).__name__}")
        
        return None
    
    def crawl_source(self, source: Dict) -> List[Dict]:
        """爬取单个源"""
        print(f"爬取 {source['name']}...")
        articles = []
        
        try:
            # 1. 获取主页
            response = requests.get(
                source["url"],
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                # 2. 提取文章链接
                links = self.extract_article_links(response.text, source)
                print(f"  找到 {len(links)} 篇文章")
                
                # 3. 获取每篇文章
                for link in links[:3]:  # 限制每源3篇
                    article = self.fetch_article(link, source)
                    if article:
                        articles.append(article)
                    
                    time.sleep(2)  # 避免请求过快
            
            else:
                print(f"  主页请求失败: {response.status_code}")
                
        except Exception as e:
            print(f"  爬取失败: {e}")
        
        print(f"  成功获取 {len(articles)} 篇文章")
        return articles
    
    def daily_crawl(self) -> Dict[str, List[Dict]]:
        """每日爬取任务"""
        print("开始每日爬取任务...")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        all_articles = {"foreign": [], "chinese": []}
        
        # 爬取外文源
        print("\n爬取外文源:")
        for source in self.sources["foreign"]:
            articles = self.crawl_source(source)
            all_articles["foreign"].extend(articles)
            time.sleep(3)  # 源间延迟
        
        # 爬取中文源
        print("\n爬取中文源:")
        for source in self.sources["chinese"]:
            articles = self.crawl_source(source)
            all_articles["chinese"].extend(articles)
            time.sleep(3)
        
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
    
    def get_content_for_processing(self, use_cached: bool = True) -> List[Dict]:
        """获取用于处理的内容"""
        if use_cached:
            articles = self.load_recent_data(days=3)
        else:
            # 强制重新爬取
            crawled = self.daily_crawl()
            articles = []
            for lang in ["foreign", "chinese"]:
                articles.extend(crawled[lang])
        
        # 标记需要翻译的文章
        for article in articles:
            article["needs_translation"] = (article["language"] == "en")
            article["original_language"] = article["language"]
        
        # 混合比例：70%外文，30%中文
        foreign_articles = [a for a in articles if a["language"] == "en"]
        chinese_articles = [a for a in articles if a["language"] == "zh"]
        
        total_needed = min(15, len(articles))
        foreign_target = int(total_needed * 0.7)
        chinese_target = total_needed - foreign_target
        
        selected_foreign = foreign_articles[:min(foreign_target, len(foreign_articles))]
        selected_chinese = chinese_articles[:min(chinese_target, len(chinese_articles))]
        
        result = selected_foreign + selected_chinese
        
        print(f"准备处理: {len(selected_foreign)}外文 + {len(selected_chinese)}中文 = {len(result)}篇")
        
        return result

# 测试函数
if __name__ == "__main__":
    print("测试完整内容爬虫...")
    crawler = FullContentCrawler()
    
    # 测试加载现有数据
    articles = crawler.get_content_for_processing(use_cached=True)
    
    if articles:
        print(f"\n获取到 {len(articles)} 篇文章:")
        for i, article in enumerate(articles[:3]):
            lang = "外文" if article["needs_translation"] else "中文"
            print(f"{i+1}. [{lang}][{article['source']}] {article['title'][:50]}...")
            print(f"   内容长度: {len(article['content'])} 字符")
            print(f"   摘要: {article['content'][:100]}...")
    else:
        print("没有找到数据，需要运行每日爬取")
        
        # 测试爬取（注释掉以避免自动运行）
        # print("\n开始测试爬取...")
        # crawled = crawler.daily_crawl()