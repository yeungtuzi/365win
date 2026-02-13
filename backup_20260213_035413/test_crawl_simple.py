#!/usr/bin/env python3
# 简单爬取测试

import os
import sys
import json
from datetime import datetime

# 使用虚拟环境的Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔧 测试网络爬虫基本功能...")

try:
    from scripts.web_crawler import WebCrawler
    print("✅ 成功导入WebCrawler")
    
    # 初始化爬虫
    crawler = WebCrawler("cache/raw_data")
    print("✅ 爬虫初始化成功")
    
    # 测试RSS解析
    print("\n📡 测试RSS解析...")
    test_url = "http://feeds.bbci.co.uk/news/rss.xml"
    items = crawler.fetch_rss_feed(test_url, "BBC测试")
    print(f"✅ 解析到 {len(items)} 条BBC新闻")
    if items:
        print(f"   示例: {items[0]['title'][:50]}...")
    
    # 测试缓存功能
    print("\n💾 测试缓存功能...")
    cached = crawler.load_from_cache(hours=72)
    if cached:
        print(f"✅ 找到缓存数据: {cached['timestamp']}")
    else:
        print("⚠️ 无缓存数据，这是正常的首次运行")
    
    # 测试获取混合内容
    print("\n🌐 测试获取混合内容...")
    mixed = crawler.get_content_for_recommendation(use_cached=False)
    print(f"✅ 获取到 {len(mixed)} 条混合内容")
    
    if mixed:
        print("\n📋 内容示例:")
        for i, item in enumerate(mixed[:3]):
            lang = "外文" if item.get('needs_translation') else "中文"
            print(f"  {i+1}. [{lang}][{item['source']}] {item['title'][:60]}...")
    
    # 保存结果
    test_dir = "data/test_results"
    os.makedirs(test_dir, exist_ok=True)
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "total_items": len(mixed),
        "foreign_count": sum(1 for item in mixed if item.get('needs_translation')),
        "chinese_count": sum(1 for item in mixed if not item.get('needs_translation')),
        "sources": list(set(item['source'] for item in mixed[:10]))
    }
    
    with open(f"{test_dir}/crawl_test_{datetime.now().strftime('%H%M%S')}.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 测试结果已保存")
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保在虚拟环境中运行: source venv/bin/activate")
except Exception as e:
    print(f"❌ 测试失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("测试完成！")