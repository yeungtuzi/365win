#!/usr/bin/env python3
# 修复内容过滤器

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.content_processor import ContentProcessor
from scripts.deepseek_client import DeepSeekClient

print("🔧 修复内容过滤器")
print("=" * 50)

# 创建模拟客户端
class TestClient:
    def analyze_content(self, text):
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
        return f"重写后的内容: {text}"
    
    def translate_content(self, text, target_lang):
        return f"翻译后的内容: {text}"

# 测试不同的内容长度
test_cases = [
    {
        "title": "简短标题",
        "content": "这是一个简短的内容",
        "expected": "应该被过滤（太短）"
    },
    {
        "title": "正常标题",
        "content": "这是一段正常长度的内容，包含足够的信息来进行分析和处理。这段文字大约有50个字符左右，应该能通过过滤。",
        "expected": "应该通过"
    },
    {
        "title": "AI Breakthrough News",
        "content": "New AI model achieves breakthrough in natural language understanding. Researchers say this could revolutionize how computers interact with humans.",
        "expected": "应该通过（外文内容）"
    }
]

print("\n测试内容过滤器...")
processor = ContentProcessor(TestClient(), {"min_content_length": 20})  # 降低最小长度要求

for i, test in enumerate(test_cases):
    print(f"\n测试 {i+1}: {test['title']}")
    print(f"内容长度: {len(test['content'])} 字符")
    print(f"预期: {test['expected']}")
    
    result = processor.process_content_item({
        "id": f"test_{i}",
        "title": test["title"],
        "content": test["content"],
        "source": "测试源",
        "type": "test"
    })
    
    if result:
        print(f"✅ 结果: 通过处理")
        print(f"   处理后的标题: {result.get('processed_title', 'N/A')[:30]}...")
    else:
        print(f"❌ 结果: 被过滤")

print("\n" + "=" * 50)
print("修复建议:")
print("1. 降低最小内容长度要求（当前: 20字符）")
print("2. 对于外文内容，即使较短也先保留进行翻译")
print("3. 改进爬虫，获取更完整的内容摘要")
print("=" * 50)