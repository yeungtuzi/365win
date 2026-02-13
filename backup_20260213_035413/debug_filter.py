#!/usr/bin/env python3
# 调试内容过滤器

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.simple_crawler import SimpleWebCrawler
from scripts.content_processor import ContentProcessor

print("🔍 调试内容过滤器")
print("=" * 50)

# 创建模拟客户端
class DebugClient:
    def analyze_content(self, text):
        print(f"  分析内容: {text[:50]}...")
        return {
            "sentiment_score": 0.7,
            "patriotic_level": 0.6,
            "tech_relevance": 0.5,
            "formality": 0.6,
            "sensationalism": 0.3,
            "clickbait_score": 0.2,
            "main_topics": ["test"],
            "recommended_action": "keep"
        }
    
    def rewrite_content(self, text, style):
        print(f"  重写内容: {text[:50]}...")
        return f"重写: {text}"
    
    def translate_content(self, text, target_lang):
        print(f"  翻译内容: {text[:50]}...")
        return f"翻译: {text}"

# 1. 获取一些真实数据
print("\n1. 获取爬虫数据...")
crawler = SimpleWebCrawler("cache/raw_data")
raw_items = crawler.get_content_for_recommendation(use_cached=True)

print(f"获取到 {len(raw_items)} 条数据")

# 2. 创建处理器
print("\n2. 创建内容处理器...")
processor = ContentProcessor(DebugClient(), "config/system_config.yaml")

# 3. 测试处理每条数据
print("\n3. 测试处理每条数据...")
passed_count = 0
filtered_count = 0

for i, item in enumerate(raw_items[:10]):  # 测试前10条
    print(f"\n项目 {i+1}: [{item['source']}] {item['title'][:40]}...")
    print(f"  内容: {item.get('content', '无内容')[:60]}...")
    print(f"  长度: {len(item.get('content', ''))} 字符")
    print(f"  需要翻译: {item.get('needs_translation', False)}")
    
    result = processor.process_content_item(item)
    
    if result:
        print(f"  ✅ 通过处理")
        passed_count += 1
    else:
        print(f"  ❌ 被过滤")
        filtered_count += 1

print(f"\n处理结果: 通过 {passed_count} 条, 过滤 {filtered_count} 条")

# 4. 检查配置
print("\n4. 检查配置文件...")
import yaml
with open("config/system_config.yaml", 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
    
print(f"配置加载成功")
if "content_sources" in config:
    exclude_keywords = config["content_sources"].get("exclude_keywords", [])
    print(f"黑名单关键词: {exclude_keywords}")

print("\n" + "=" * 50)
print("调试完成")
print("建议:")
print("1. 检查爬虫获取的内容是否包含黑名单关键词")
print("2. 检查内容长度是否满足要求")
print("3. 考虑进一步降低过滤要求或改进爬虫")
print("=" * 50)