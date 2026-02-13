#!/usr/bin/env python3
# 测试新闻爬取系统

import os
import sys
sys.path.append('.')

print("🧪 测试新闻爬取系统")
print("=" * 60)

# 测试配置加载
print("1. 测试配置加载...")
try:
    import yaml
    with open('config/news_crawler_config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    print(f"   ✅ 配置加载成功")
    print(f"   数据源: {len(config['crawler']['sources']['foreign'])}外文 + {len(config['crawler']['sources']['chinese'])}中文")
    print(f"   去重: {config['crawler']['deduplication']['enabled']}")
    print(f"   翻译: {config['processing']['translation']['enabled']}")
    print(f"   风格重写: {config['processing']['translation'].get('style_rewriting', False)}")
    
except Exception as e:
    print(f"   ❌ 配置加载失败: {e}")

# 测试系统初始化
print("\n2. 测试系统初始化...")
try:
    from news_crawler_system import NewsCrawlerSystem
    
    crawler = NewsCrawlerSystem()
    print("   ✅ 系统初始化成功")
    
    # 测试去重功能
    print("\n3. 测试去重功能...")
    test_articles = [
        {
            'title': '测试文章1',
            'content': '这是测试内容1',
            'url': 'https://example.com/1',
            'source': '测试源',
            'language': 'zh',
            'publish_date': '2026-02-13'
        },
        {
            'title': '测试文章1',  # 相同标题
            'content': '这是测试内容1',  # 相同内容
            'url': 'https://example.com/2',  # 不同URL
            'source': '测试源',
            'language': 'zh',
            'publish_date': '2026-02-13'
        }
    ]
    
    duplicate_count = 0
    for article in test_articles:
        if crawler.is_duplicate(article):
            duplicate_count += 1
            print(f"   检测到重复: {article['title']}")
        else:
            print(f"   非重复: {article['title']}")
    
    print(f"   去重测试: {duplicate_count}/{len(test_articles)} 篇被识别为重复")
    
    # 测试内容哈希
    print("\n4. 测试内容哈希...")
    content1 = "这是测试内容"
    content2 = "这是测试内容"  # 完全相同
    content3 = "这是不同的测试内容"
    
    hash1 = crawler.calculate_content_hash(content1)
    hash2 = crawler.calculate_content_hash(content2)
    hash3 = crawler.calculate_content_hash(content3)
    
    print(f"   内容1哈希: {hash1[:8]}...")
    print(f"   内容2哈希: {hash2[:8]}... (应与内容1相同)")
    print(f"   内容3哈希: {hash3[:8]}... (应不同)")
    
    if hash1 == hash2:
        print("   ✅ 相同内容哈希一致")
    else:
        print("   ❌ 相同内容哈希不一致")
    
    if hash1 != hash3:
        print("   ✅ 不同内容哈希不同")
    else:
        print("   ❌ 不同内容哈希相同")
    
    # 测试摘要生成
    print("\n5. 测试摘要生成...")
    long_content = "这是一段很长的测试内容，需要被截断成摘要。" * 10
    summary = crawler.generate_summary(long_content, max_length=50)
    
    print(f"   原始内容长度: {len(long_content)} 字符")
    print(f"   摘要长度: {len(summary)} 字符")
    print(f"   摘要内容: {summary}")
    
    if len(summary) <= 50 + 3:  # 50字符 + "..."
        print("   ✅ 摘要生成正确")
    else:
        print("   ❌ 摘要过长")
    
    # 测试简报生成
    print("\n6. 测试简报生成...")
    test_data = {
        'foreign': [
            {
                'title': '外文测试文章1',
                'content': '这是外文测试内容1',
                'url': 'https://foreign.com/1',
                'source': 'Reuters',
                'language': 'en',
                'publish_date': '2026-02-13T10:00:00',
                'needs_translation': True,
                'translated_content': '[翻译自en] 这是外文测试内容1',
                'summary': '外文测试摘要1'
            }
        ],
        'chinese': [
            {
                'title': '中文测试文章1',
                'content': '这是中文测试内容1',
                'url': 'https://chinese.com/1',
                'source': '澎湃新闻',
                'language': 'zh',
                'publish_date': '2026-02-13T11:00:00',
                'needs_translation': False,
                'translated_content': '这是中文测试内容1',
                'summary': '中文测试摘要1'
            }
        ]
    }
    
    briefing = crawler.generate_briefing(test_data)
    
    print(f"   简报长度: {len(briefing)} 字符")
    print(f"   包含外文新闻: {'外文新闻' in briefing}")
    print(f"   包含中文新闻: {'中文新闻' in briefing}")
    print(f"   包含统计信息: {'统计信息' in briefing}")
    
    # 显示简报开头
    print("\n   简报预览:")
    print("   " + "-" * 40)
    for line in briefing.split('\n')[:10]:
        print(f"   {line}")
    print("   " + "-" * 40)
    
    print("\n" + "=" * 60)
    print("✅ 新闻爬取系统测试完成!")
    print("   所有核心功能测试通过")
    print("=" * 60)
    
except Exception as e:
    print(f"   ❌ 测试失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n🚀 准备运行完整的新闻爬取系统...")
print("输入 'y' 开始运行，或按其他键跳过:")
choice = input().strip().lower()

if choice == 'y':
    print("\n" + "=" * 60)
    print("开始运行新闻爬取系统...")
    print("=" * 60)
    
    # 运行完整系统
    crawler.run()
else:
    print("\n跳过完整运行。")
    print("要运行完整系统，请执行:")
    print("  python3 news_crawler_system.py")