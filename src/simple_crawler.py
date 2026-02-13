#!/usr/bin/env python3
# 简化版爬虫 - 使用API和简单HTML解析

import os
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re

class SimpleWebCrawler:
    """简化版网络爬虫，避免复杂依赖"""
    
    def __init__(self, cache_dir: str = "cache/raw_data"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        # 使用更简单的数据源
        self.sources = {
            # 外文源 - 使用NewsAPI等简单API
            "foreign": [
                {
                    "name": "NewsAPI头条",
                    "url": "https://newsapi.org/v2/top-headlines?country=us&apiKey=demo",  # 示例，实际需要API密钥
                    "type": "api",
                    "lang": "en"
                },
                {
                    "name": "Hacker News",
                    "url": "https://hacker-news.firebaseio.com/v0/topstories.json",
                    "type": "api",
                    "lang": "en"
                }
            ],
            # 中文源 - 使用简单的RSS或API
            "chinese": [
                {
                    "name": "知乎热榜API",
                    "url": "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total",
                    "type": "api",
                    "lang": "zh"
                },
                {
                    "name": "百度热搜",
                    "url": "https://top.baidu.com/board?tab=realtime",
                    "type": "html",
                    "lang": "zh"
                }
            ]
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_api_data(self, url: str, source_name: str) -> List[Dict]:
        """获取API数据"""
        items = []
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if "hacker-news" in url:
                # Hacker News API
                story_ids = response.json()[:10]  # 前10个故事ID
                for story_id in story_ids[:5]:  # 只取前5个，避免太多请求
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    story_resp = requests.get(story_url, timeout=5)
                    if story_resp.status_code == 200:
                        story = story_resp.json()
                        items.append({
                            "title": story.get("title", ""),
                            "summary": story.get("text", f"Hacker News story with score {story.get('score', 0)}"),
                            "link": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                            "published": datetime.fromtimestamp(story.get("time", time.time())).isoformat(),
                            "source": "Hacker News",
                            "language": "en"
                        })
                    time.sleep(0.1)  # 避免请求过快
            
            elif "zhihu.com" in url:
                # 知乎热榜API
                data = response.json()
                for item in data.get("data", [])[:10]:
                    target = item.get("target", {})
                    items.append({
                        "title": target.get("title", target.get("question", {}).get("title", "")),
                        "summary": f"热度: {item.get('detail_text', '')}",
                        "link": f"https://www.zhihu.com/question/{target.get('id', '')}",
                        "published": datetime.now().isoformat(),
                        "source": "知乎热榜",
                        "language": "zh"
                    })
            
            else:
                # 通用API处理
                data = response.json()
                if "articles" in data:
                    for article in data["articles"][:10]:
                        items.append({
                            "title": article.get("title", ""),
                            "summary": article.get("description", article.get("title", "")),
                            "link": article.get("url", ""),
                            "published": article.get("publishedAt", datetime.now().isoformat()),
                            "source": article.get("source", {}).get("name", source_name),
                            "language": "en"
                        })
            
        except Exception as e:
            print(f"API获取失败 {source_name}: {e}")
        
        return items
    
    def fetch_html_simple(self, url: str, source_name: str) -> List[Dict]:
        """简单HTML解析（不使用BeautifulSoup）"""
        items = []
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            text = response.text
            
            if "baidu.com" in url:
                # 简单解析百度热搜
                # 查找热搜标题
                import re
                pattern = r'class="c-single-text-ellipsis">([^<]+)</div>'
                titles = re.findall(pattern, text)[:20]
                
                for i, title in enumerate(titles):
                    items.append({
                        "title": f"百度热搜: {title.strip()}",
                        "summary": f"百度实时热搜第{i+1}位",
                        "link": "https://top.baidu.com",
                        "published": datetime.now().isoformat(),
                        "source": "百度热搜",
                        "language": "zh"
                    })
            
        except Exception as e:
            print(f"HTML获取失败 {source_name}: {e}")
        
        return items
    
    def get_mock_data(self) -> Dict[str, List[Dict]]:
        """获取模拟数据（当真实爬取失败时使用）"""
        print("使用模拟数据（真实爬取失败）")
        
        current_time = datetime.now().isoformat()
        
        return {
            "foreign": [
                {
                    "title": "AI Breakthrough: New Model Achieves Human-Level Reasoning in Scientific Research",
                    "summary": "Researchers at leading universities announce a breakthrough in artificial intelligence with new models demonstrating human-like reasoning capabilities in complex scientific problems. The technology could accelerate discoveries in medicine, materials science, and climate research.",
                    "link": "https://example.com/ai-breakthrough",
                    "published": current_time,
                    "source": "Tech News International",
                    "language": "en"
                },
                {
                    "title": "Global Economic Recovery Accelerates as Major Economies Show Strong Growth Indicators",
                    "summary": "Latest economic data from international organizations suggest the global economy is entering a phase of sustained recovery. Manufacturing indices, trade volumes, and consumer confidence all show positive trends across major economies.",
                    "link": "https://example.com/economy-recovery",
                    "published": current_time,
                    "source": "Global Financial Review",
                    "language": "en"
                },
                {
                    "title": "International Space Agencies Announce Ambitious Joint Mission to Explore Mars in Unprecedented Detail",
                    "summary": "NASA, ESA, and other space agencies have announced a collaborative mission to conduct the most comprehensive exploration of Mars to date. The mission will deploy advanced rovers and orbital instruments to search for signs of past life and prepare for future human exploration.",
                    "link": "https://example.com/mars-mission",
                    "published": current_time,
                    "source": "Space Exploration Journal",
                    "language": "en"
                }
            ],
            "chinese": [
                {
                    "title": "中国科技创新取得系列重大突破，人工智能量子计算等领域引领全球发展",
                    "summary": "我国科研人员在人工智能、量子计算、生物技术等领域取得一系列重要进展，多项核心技术实现自主可控。最新发布的科技统计数据显示，中国在全球创新指数排名持续上升，科技创新对经济增长贡献率超过60%。",
                    "link": "https://example.com/china-tech",
                    "published": current_time,
                    "source": "科技日报",
                    "language": "zh"
                },
                {
                    "title": "中国经济展现强大韧性，高质量发展取得新成效市场信心持续增强",
                    "summary": "国家统计局最新数据显示，我国经济在复杂国际环境下保持稳定增长，消费、投资、出口三大需求协同发力。上半年GDP同比增长6.3%，高技术制造业投资增长15.2%，经济结构持续优化，高质量发展根基更加稳固。",
                    "link": "https://example.com/china-economy",
                    "published": current_time,
                    "source": "人民日报",
                    "language": "zh"
                },
                {
                    "title": "数字技术助力传统文化保护传承，文化自信在现代社会焕发新生",
                    "summary": "借助人工智能、虚拟现实、区块链等数字技术，我国传统文化保护传承工作进入新阶段。故宫博物院、国家博物馆等文化机构推出数字化展览和互动体验项目，让文物活起来，让历史说话，优秀传统文化在新时代绽放出更加绚丽的光彩。",
                    "link": "https://example.com/china-culture",
                    "published": current_time,
                    "source": "光明日报",
                    "language": "zh"
                }
            ]
        }
    
    def crawl_all_sources(self, use_mock_if_failed: bool = True) -> Dict[str, List[Dict]]:
        """爬取所有源"""
        print("开始简化爬取...")
        
        all_items = {"foreign": [], "chinese": []}
        success = False
        
        try:
            # 尝试爬取外文源
            for source in self.sources["foreign"]:
                if source["type"] == "api":
                    items = self.fetch_api_data(source["url"], source["name"])
                else:
                    items = self.fetch_html_simple(source["url"], source["name"])
                
                all_items["foreign"].extend(items)
                print(f"  爬取 {source['name']}: {len(items)} 条")
                time.sleep(1)
            
            # 尝试爬取中文源
            for source in self.sources["chinese"]:
                if source["type"] == "api":
                    items = self.fetch_api_data(source["url"], source["name"])
                else:
                    items = self.fetch_html_simple(source["url"], source["name"])
                
                all_items["chinese"].extend(items)
                print(f"  爬取 {source['name']}: {len(items)} 条")
                time.sleep(1)
            
            success = True
            
        except Exception as e:
            print(f"爬取过程出错: {e}")
        
        # 如果爬取失败且允许使用模拟数据
        if not success and use_mock_if_failed:
            all_items = self.get_mock_data()
            success = True
        
        if success:
            # 保存到缓存
            self.save_to_cache(all_items)
            print(f"爬取完成: 外文 {len(all_items['foreign'])} 条, 中文 {len(all_items['chinese'])} 条")
        else:
            print("爬取失败")
        
        return all_items
    
    def save_to_cache(self, items: Dict[str, List[Dict]]):
        """保存到缓存"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cache_file = os.path.join(self.cache_dir, f"simple_crawled_{timestamp}.json")
        
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "total_foreign": len(items["foreign"]),
            "total_chinese": len(items["chinese"]),
            "items": items
        }
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
        print(f"缓存已保存: {cache_file}")
        
        # 清理旧缓存
        self.clean_old_cache(days=3)
    
    def clean_old_cache(self, days: int = 3):
        """清理旧缓存"""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        for filename in os.listdir(self.cache_dir):
            if filename.startswith("simple_crawled_") and filename.endswith(".json"):
                filepath = os.path.join(self.cache_dir, filename)
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                if file_time < cutoff_time:
                    os.remove(filepath)
                    print(f"清理旧缓存: {filename}")
    
    def load_from_cache(self, hours: int = 72) -> Optional[Dict]:
        """从缓存加载"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        latest_cache = None
        latest_time = None
        
        for filename in os.listdir(self.cache_dir):
            if filename.startswith("simple_crawled_") and filename.endswith(".json"):
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
                print(f"从缓存加载: {os.path.basename(latest_cache)}")
                return data
            except Exception as e:
                print(f"加载缓存失败: {e}")
        
        return None
    
    def get_content_for_recommendation(self, use_cached: bool = True) -> List[Dict]:
        """获取用于推荐的内容"""
        data = None
        
        if use_cached:
            data = self.load_from_cache(hours=72)
        
        # 如果没有缓存或强制重新爬取
        if not data:
            print("无有效缓存，开始实时爬取...")
            crawled_data = self.crawl_all_sources(use_mock_if_failed=True)
            data = {
                "timestamp": datetime.now().isoformat(),
                "items": crawled_data
            }
        
        # 混合内容：70%外文，30%中文
        foreign_items = data["items"]["foreign"]
        chinese_items = data["items"]["chinese"]
        
        # 计算目标数量
        total_needed = min(20, len(foreign_items) + len(chinese_items))
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

# 测试
if __name__ == "__main__":
    crawler = SimpleWebCrawler()
    
    print("测试简化爬虫...")
    items = crawler.get_content_for_recommendation(use_cached=False)
    
    print(f"\n获取到 {len(items)} 条内容:")
    for i, item in enumerate(items[:5]):
        lang = "外文" if item.get('needs_translation') else "中文"
        print(f"{i+1}. [{lang}][{item['source']}] {item['title'][:50]}...")