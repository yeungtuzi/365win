#!/usr/bin/env python3
# 简化的第一次赢测试

import os
import json
from datetime import datetime

# 设置环境变量
# 从环境变量获取API密钥

from scripts.deepseek_client import DeepSeekClient

print("🎯 一年365赢 - 真正的第一次赢！")
print("=" * 50)

# 初始化DeepSeek客户端
client = DeepSeekClient()
print("✅ DeepSeek API客户端初始化成功")

# 测试内容分析
test_content = "中国在人工智能领域取得重大突破，相关技术达到国际领先水平"
print(f"\n📊 分析测试内容: {test_content}")
analysis = client.analyze_content(test_content)
sentiment = analysis.get('sentiment_score')
patriotic = analysis.get('patriotic_level')
print(f"   情感分数: {sentiment:.2f if isinstance(sentiment, (int, float)) else 'N/A'}")
print(f"   爱国程度: {patriotic:.2f if isinstance(patriotic, (int, float)) else 'N/A'}")
print(f"   建议处理: {analysis.get('recommended_action', 'N/A')}")

# 测试内容重写
print("\n🔄 测试内容重写（转为爱国键盘侠风格）:")
rewritten = client.rewrite_content(test_content, {
    "目标风格": "爱国键盘侠偏好",
    "情感倾向": "积极正面，增强爱国情怀"
})
print(f"   重写结果: {rewritten[:100]}...")

# 生成简单的早安简报
print("\n📨 生成早安简报:")
sample_items = [
    {
        "title": "中国航天再创辉煌",
        "content": "我国新一代载人飞船成功完成首次飞行试验",
        "summary": "航天科技重大突破",
        "url": "https://example.com/space"
    },
    {
        "title": "人工智能助力产业升级", 
        "content": "中国AI产业规模持续扩大，在智能制造领域应用成效显著",
        "summary": "科技引领发展",
        "url": "https://example.com/ai"
    }
]

briefing = client.generate_briefing(sample_items, "早安简报")
print(f"\n{briefing}")

# 保存结果
output_dir = "data/first_win"
os.makedirs(output_dir, exist_ok=True)
output_file = f"{output_dir}/first_real_win_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"一年365赢 - 第一次真正的赢！\n")
    f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 50 + "\n\n")
    f.write(briefing)
    f.write("\n\n" + "=" * 50 + "\n")
    f.write("✅ 第一次赢完成！系统运行正常，DeepSeek API工作正常。\n")

print(f"\n💾 结果已保存到: {output_file}")

# 显示使用统计
stats = client.get_usage_stats()
print(f"\n📈 API使用统计:")
print(f"   调用次数: {stats['request_count']}")
print(f"   Token使用: {stats['total_tokens']}")
print(f"   估算成本: ${stats['estimated_cost']:.6f}")

print("\n" + "=" * 50)
print("🎉 恭喜！一年365赢系统第一次真正的运行成功！")
print("✨ 你的个性化信息茧房已经准备就绪！")
print("🇨🇳 爱国键盘侠，天天都在赢！")