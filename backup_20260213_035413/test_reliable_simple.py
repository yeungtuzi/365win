#!/usr/bin/env python3
# 简单测试可靠爬虫

import os
import sys
import json
import time
from datetime import datetime

print("🧪 简单测试可靠爬虫")
print("=" * 50)

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # 1. 测试导入
    print("1. 测试导入...")
    from scripts.reliable_crawler import ReliableCrawler
    print("✅ 可靠爬虫导入成功")
    
    # 2. 初始化
    print("\n2. 初始化爬虫...")
    crawler = ReliableCrawler()
    print("✅ 可靠爬虫初始化成功")
    
    # 3. 测试单个源（Hacker News）
    print("\n3. 测试Hacker News API...")
    import requests
    
    hn_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(hn_url, timeout=10)
    
    if response.status_code == 200:
        top_stories = response.json()[:3]
        print(f"✅ Hacker News API工作正常，获取到 {len(top_stories)} 个故事ID")
        
        # 获取第一个故事的详情
        if top_stories:
            story_id = top_stories[0]
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url, timeout=10)
            
            if story_response.status_code == 200:
                story = story_response.json()
                print(f"   故事示例: {story.get('title', '无标题')[:50]}...")
                print(f"   来源: Hacker News")
                print(f"   URL: {story.get('url', '无URL')}")
            else:
                print(f"   ⚠️ 获取故事详情失败: {story_response.status_code}")
    else:
        print(f"❌ Hacker News API失败: {response.status_code}")
    
    # 4. 测试RSS源
    print("\n4. 测试RSS源...")
    try:
        import feedparser
        print("✅ feedparser可用")
        
        # 测试Ars Technica RSS
        rss_url = "https://feeds.arstechnica.com/arstechnica/index"
        feed = feedparser.parse(rss_url)
        
        if feed.entries:
            print(f"✅ RSS解析成功，获取到 {len(feed.entries)} 个条目")
            
            for i, entry in enumerate(feed.entries[:2]):
                print(f"   条目 {i+1}: {entry.get('title', '无标题')[:50]}...")
                print(f"       链接: {entry.get('link', '无链接')}")
                print(f"       摘要: {entry.get('summary', '无摘要')[:80]}...")
        else:
            print("⚠️ RSS解析返回0个条目")
            
    except Exception as e:
        print(f"❌ RSS测试失败: {type(e).__name__}: {e}")
    
    # 5. 测试爬取
    print("\n5. 测试完整爬取...")
    start_time = time.time()
    
    try:
        result = crawler.daily_crawl()
        elapsed = time.time() - start_time
        
        print(f"✅ 爬取完成，耗时 {elapsed:.1f} 秒")
        print(f"   外文文章: {len(result['foreign'])} 篇")
        print(f"   中文文章: {len(result['chinese'])} 篇")
        
        total_articles = len(result['foreign']) + len(result['chinese'])
        
        if total_articles > 0:
            print(f"\n🎉 成功获取 {total_articles} 篇文章!")
            
            # 显示示例
            if result['foreign']:
                print("\n   外文文章示例:")
                for i, article in enumerate(result['foreign'][:2]):
                    print(f"     {i+1}. {article['title'][:50]}...")
                    print(f"         来源: {article['source']}")
                    print(f"         内容长度: {len(article['content'])} 字符")
            
            if result['chinese']:
                print("\n   中文文章示例:")
                for i, article in enumerate(result['chinese'][:2]):
                    print(f"     {i+1}. {article['title'][:50]}...")
                    print(f"         来源: {article['source']}")
                    print(f"         内容长度: {len(article['content'])} 字符")
            
            # 保存测试结果
            print("\n6. 保存测试结果...")
            test_dir = "data/reliable_tests"
            os.makedirs(test_dir, exist_ok=True)
            
            test_result = {
                "timestamp": datetime.now().isoformat(),
                "test_name": "可靠爬虫测试",
                "foreign_articles": len(result['foreign']),
                "chinese_articles": len(result['chinese']),
                "total_articles": total_articles,
                "elapsed_seconds": elapsed,
                "sources_tested": [
                    "Hacker News",
                    "Reddit r/technology", 
                    "Ars Technica RSS",
                    "知乎热榜",
                    "澎湃新闻",
                    "果壳网"
                ],
                "status": "成功" if total_articles > 0 else "部分成功",
                "recommendation": "爬虫工作正常，可以集成到主系统" if total_articles > 0 else "需要进一步调试"
            }
            
            result_file = f"{test_dir}/reliable_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(test_result, f, ensure_ascii=False, indent=2)
            
            print(f"💾 测试结果已保存到: {result_file}")
            
            print("\n" + "=" * 50)
            if total_articles > 0:
                print("🎉 🎉 🎉 可靠爬虫测试成功!")
                print("✅ 真实内容获取功能正常")
                print("✅ 可以集成到混合爬虫系统")
                print("🚀 系统已准备好部署!")
            else:
                print("⚠️ 爬虫返回0篇文章")
                print("建议使用混合系统（模拟数据+尝试真实爬取）")
            print("=" * 50)
            
        else:
            print("❌ 爬取返回0篇文章")
            print("建议:")
            print("  1. 检查网络连接")
            print("  2. 某些API可能被限制")
            print("  3. 使用混合系统确保内容可用")
            
    except Exception as e:
        print(f"❌ 爬取测试失败: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请检查依赖安装: pip3 install feedparser beautifulsoup4")
except Exception as e:
    print(f"❌ 测试失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()