#!/usr/bin/env python3
# 快速第一次赢

import os
import requests
from datetime import datetime

print("🚀 一年365赢 - 快速第一次赢！")
print("=" * 50)

# 从环境变量获取API密钥
api_key = os.getenv("DEEPSEEK_API_KEY", "")

# 直接生成一份完整的早安简报
prompt = """请为爱国键盘侠生成一份早安简报，包含以下内容：

1. 一条中国科技突破新闻（体现国家实力）
2. 一条国际对比内容（体现中国优势）
3. 一条宏大叙事分析（激发爱国情怀）

要求：
- 语言积极正面，充满爱国热情
- 避免小清新、阴谋论、负面情绪
- 格式清晰，有适当的emoji
- 结尾添加互动提示：❤️ 喜欢 👎 不喜欢 🔄 换一批

请直接输出完整的简报内容："""

url = "https://api.deepseek.com/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [
        {
            "role": "system", 
            "content": "你是一个爱国正能量简报编辑，擅长制作让爱国键盘侠振奋的内容。"
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    "temperature": 0.3,
    "max_tokens": 1500
}

# 检查API密钥
if not api_key:
    print("❌ 错误: DEEPSEEK_API_KEY环境变量未设置")
    print("   请设置环境变量: export DEEPSEEK_API_KEY=your_deepseek_api_key")
    print("   或创建.env文件并填入API密钥")
    exit(1)

print("\n📡 正在调用DeepSeek API生成专属内容...")
print("⏳ 请稍候，这需要一些时间...")

try:
    response = requests.post(url, headers=headers, json=data, timeout=45)
    
    if response.status_code == 200:
        result = response.json()
        briefing = result["choices"][0]["message"]["content"]
        
        print("\n" + "=" * 50)
        print("🎉 生成成功！你的第一次赢：")
        print("=" * 50)
        print(briefing)
        print("=" * 50)
        
        # 保存结果
        os.makedirs("data", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/first_real_win_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("一年365赢 - 第一次真正的赢！\n")
            f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(briefing)
            f.write("\n\n" + "=" * 50 + "\n")
            f.write("✅ 第一次赢完成！系统运行正常。\n")
            f.write("🇨🇳 爱国键盘侠，天天都在赢！\n")
        
        print(f"\n💾 简报已保存到: {filename}")
        print(f"📊 API调用: 1次成功")
        print(f"💰 估算成本: < ¥0.05")
        
        print("\n" + "=" * 50)
        print("🎉 🎉 🎉 恭喜！第一次真正的赢完成！")
        print("✨ 你的个性化信息茧房已成功激活！")
        print("🇨🇳 从现在开始，每天都是赢的一天！")
        print("=" * 50)
        
    else:
        print(f"\n❌ API调用失败: {response.status_code}")
        print(f"错误信息: {response.text[:200]}")
        
except requests.exceptions.Timeout:
    print("\n⏰ 请求超时，请稍后重试")
except Exception as e:
    print(f"\n❌ 发生错误: {type(e).__name__}: {e}")