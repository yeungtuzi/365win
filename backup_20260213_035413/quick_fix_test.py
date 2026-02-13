#!/usr/bin/env python3
# 快速修复测试

import os
import sys

print("🔧 快速修复测试")
print("=" * 50)

# 设置环境变量
# 从环境变量获取API密钥

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.simple_crawler import SimpleWebCrawler
from scripts.content_processor import ContentProcessor

# 创建模拟客户端
class TestClient:
    def analyze_content(self, text):
        return {
            "sentiment_score": 0.8,
            "patriotic_level": 0.7,
            "tech_relevance": 0.6,
            "formality": 0.7,
            "sensationalism": 0.2,
            "clickbait_score": 0.1,
            "main_topics": ["科技", "发展"],
            "recommended_action": "keep"
        }
    
    def rewrite_content(self, text, style):
        return f"【重写】{text}"
    
    def translate_content(self, text, target_lang):
        return f"【翻译】{text}"

print("\n1. 测试爬虫获取数据...")
crawler = SimpleWebCrawler("cache/raw_data")
items = crawler.get_content_for_recommendation(use_cached=False)  # 强制重新爬取

print(f"获取到 {len(items)} 条数据")

if items:
    print("\n2. 检查数据质量...")
    for i, item in enumerate(items[:3]):
        print(f"  项目 {i+1}:")
        print(f"    标题: {item['title'][:50]}...")
        print(f"    内容: {item.get('content', '无内容')[:60]}...")
        print(f"    长度: {len(item.get('content', ''))} 字符")
        print(f"    来源: {item['source']}")
        print(f"    需要翻译: {item.get('needs_translation', False)}")
    
    print("\n3. 测试内容处理...")
    processor = ContentProcessor(TestClient(), "config/system_config.yaml")
    
    passed = []
    filtered = []
    
    for item in items[:5]:
        result = processor.process_content_item(item)
        if result:
            passed.append(item)
        else:
            filtered.append(item)
    
    print(f"处理结果: 通过 {len(passed)} 条, 过滤 {len(filtered)} 条")
    
    if passed:
        print("\n✅ 成功通过处理的内容:")
        for i, item in enumerate(passed[:3]):
            print(f"  {i+1}. [{item['source']}] {item['title'][:40]}...")
    else:
        print("\n❌ 没有内容通过处理")
        if filtered:
            print("可能的原因:")
            print("  - 内容长度不足")
            print("  - 包含黑名单关键词")
            print("  - 其他过滤条件")

print("\n" + "=" * 50)
print("测试完成")
print("下一步: 运行完整系统测试")