#!/usr/bin/env python3
# 测试真实爬取功能

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.web_crawler import WebCrawler
from scripts.deepseek_client import DeepSeekClient

print("🚀 测试真实爬取功能")
print("=" * 60)

# 1. 测试爬虫
print("\n1️⃣ 测试网络爬虫...")
crawler = WebCrawler("cache/raw_data")

# 先尝试从缓存加载
print("尝试从缓存加载数据...")
cached_data = crawler.load_from_cache(hours=72)

if cached_data:
    print(f"✅ 从缓存加载成功:")
    print(f"   时间: {cached_data['timestamp']}")
    print(f"   外文: {cached_data['total_foreign']}条")
    print(f"   中文: {cached_data['total_chinese']}条")
    
    # 显示一些示例
    print("\n📰 缓存内容示例:")
    foreign_items = cached_data['items']['foreign'][:2]
    chinese_items = cached_data['items']['chinese'][:2]
    
    for i, item in enumerate(foreign_items):
        print(f"  外文{i+1}: [{item['source']}] {item['title'][:60]}...")
    
    for i, item in enumerate(chinese_items):
        print(f"  中文{i+1}: [{item['source']}] {item['title'][:60]}...")
else:
    print("❌ 无有效缓存，需要实时爬取")

# 2. 测试实时爬取（可选）
print("\n2️⃣ 测试实时爬取（按Enter跳过，输入y开始）:")
choice = input("是否开始实时爬取? (y/N): ")

if choice.lower() == 'y':
    print("开始实时爬取...")
    crawled_data = crawler.crawl_all_sources(max_items_per_source=3)
    
    print(f"✅ 爬取完成:")
    print(f"   外文: {len(crawled_data['foreign'])}条")
    print(f"   中文: {len(crawled_data['chinese'])}条")
    
    print("\n📰 最新内容示例:")
    for i, item in enumerate(crawled_data['foreign'][:3]):
        print(f"  外文{i+1}: [{item['source']}] {item['title'][:60]}...")
    
    for i, item in enumerate(crawled_data['chinese'][:3]):
        print(f"  中文{i+1}: [{item['source']}] {item['title'][:60]}...")

# 3. 测试混合内容获取
print("\n3️⃣ 测试混合内容获取（70%外文 + 30%中文）...")
mixed_items = crawler.get_content_for_recommendation(use_cached=True)

print(f"✅ 获取到 {len(mixed_items)} 条混合内容:")
print(f"   需要翻译: {sum(1 for item in mixed_items if item.get('needs_translation'))}条")
print(f"   中文原文: {sum(1 for item in mixed_items if not item.get('needs_translation'))}条")

print("\n📋 内容详情:")
for i, item in enumerate(mixed_items[:5]):
    lang = "外文" if item.get('needs_translation') else "中文"
    print(f"  {i+1}. [{lang}][{item['source']}] {item['title'][:50]}...")

# 4. 测试DeepSeek翻译（如果配置了API密钥）
print("\n4️⃣ 测试DeepSeek翻译功能...")
api_key = os.getenv("DEEPSEEK_API_KEY")
if api_key and api_key != "test_mode_key":
    print("检测到DeepSeek API密钥，测试翻译...")
    
    try:
        client = DeepSeekClient(api_key)
        
        # 找一个需要翻译的外文内容
        foreign_item = None
        for item in mixed_items:
            if item.get('needs_translation'):
                foreign_item = item
                break
        
        if foreign_item:
            print(f"翻译测试: {foreign_item['title'][:30]}...")
            translated = client.translate_content(foreign_item['title'], target_lang="zh")
            print(f"✅ 翻译结果: {translated}")
        else:
            print("⚠️ 没有找到需要翻译的内容")
            
    except Exception as e:
        print(f"❌ 翻译测试失败: {e}")
else:
    print("⚠️ 未检测到有效的DeepSeek API密钥，跳过翻译测试")

# 5. 测试缓存清理
print("\n5️⃣ 测试缓存清理...")
crawler.clean_old_cache(days=1)
print("✅ 缓存清理完成（清理1天前的缓存）")

# 6. 保存测试结果
print("\n6️⃣ 保存测试结果...")
test_dir = "data/test_results"
os.makedirs(test_dir, exist_ok=True)

test_file = f"{test_dir}/crawler_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

import json
test_result = {
    "timestamp": datetime.now().isoformat(),
    "cached_available": cached_data is not None,
    "mixed_items_count": len(mixed_items),
    "needs_translation": sum(1 for item in mixed_items if item.get('needs_translation')),
    "sample_items": mixed_items[:10]  # 保存前10条作为示例
}

with open(test_file, 'w', encoding='utf-8') as f:
    json.dump(test_result, f, ensure_ascii=False, indent=2)

print(f"✅ 测试结果已保存到: {test_file}")

print("\n" + "=" * 60)
print("🎉 真实爬取功能测试完成！")
print("✨ 系统现在可以从互联网实时获取中外内容")
print("🌐 支持70%外文 + 30%中文的混合推荐")
print("💾 支持3天缓存，实现'换一批'功能")
print("=" * 60)