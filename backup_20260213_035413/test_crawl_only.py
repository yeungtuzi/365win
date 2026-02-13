#!/usr/bin/env python3
# 只测试爬虫功能

import os
import sys
from datetime import datetime

print("🕷️ 测试完整内容爬虫功能")
print("=" * 50)

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.full_content_crawler import FullContentCrawler

try:
    # 1. 初始化爬虫
    print("1. 初始化完整内容爬虫...")
    crawler = FullContentCrawler()
    print("✅ 爬虫初始化成功")
    
    # 2. 检查现有数据
    print("\n2. 检查现有数据...")
    articles = crawler.load_recent_data(days=3)
    
    if articles:
        print(f"✅ 找到 {len(articles)} 篇现有文章")
        
        # 显示统计
        foreign = [a for a in articles if a["language"] == "en"]
        chinese = [a for a in articles if a["language"] == "zh"]
        
        print(f"   外文文章: {len(foreign)} 篇")
        print(f"   中文文章: {len(chinese)} 篇")
        
        # 显示示例
        if articles:
            print("\n   文章示例:")
            for i, article in enumerate(articles[:2]):
                lang = "外文" if article["language"] == "en" else "中文"
                print(f"   {i+1}. [{lang}][{article['source']}]")
                print(f"      标题: {article['title'][:50]}...")
                print(f"      内容长度: {len(article['content'])} 字符")
                print(f"      摘要: {article['content'][:80]}...")
    
    else:
        print("⚠️ 没有现有数据，需要执行爬取")
        
        # 3. 测试爬取（可选）
        print("\n3. 是否执行测试爬取？")
        print("   注意：这可能需要几分钟时间，并且需要网络连接")
        print("   输入 'y' 开始爬取，其他键跳过...")
        
        import select
        import sys
        
        # 非阻塞输入检查
        i, o, e = select.select([sys.stdin], [], [], 5)
        
        if i:
            choice = sys.stdin.readline().strip().lower()
        else:
            choice = 'n'
            print("   超时，跳过爬取测试")
        
        if choice == 'y':
            print("\n开始测试爬取...")
            try:
                result = crawler.daily_crawl()
                print(f"✅ 爬取完成!")
                print(f"   外文文章: {len(result['foreign'])} 篇")
                print(f"   中文文章: {len(result['chinese'])} 篇")
                
                if result['foreign']:
                    print("\n   外文文章示例:")
                    for i, article in enumerate(result['foreign'][:2]):
                        print(f"     {i+1}. {article['title'][:50]}...")
                        print(f"        内容: {article['content'][:80]}...")
                
                if result['chinese']:
                    print("\n   中文文章示例:")
                    for i, article in enumerate(result['chinese'][:2]):
                        print(f"     {i+1}. {article['title'][:50]}...")
                        print(f"        内容: {article['content'][:80]}...")
                        
            except Exception as e:
                print(f"❌ 爬取失败: {e}")
                print("建议：")
                print("  1. 检查网络连接")
                print("  2. 网站可能限制了爬取")
                print("  3. 可以稍后重试或使用模拟数据")
        else:
            print("跳过爬取测试")
    
    # 4. 测试获取处理内容
    print("\n4. 测试获取处理内容...")
    process_content = crawler.get_content_for_processing(use_cached=True)
    
    if process_content:
        print(f"✅ 获取到 {len(process_content)} 篇处理内容")
        
        foreign = [a for a in process_content if a["needs_translation"]]
        chinese = [a for a in process_content if not a["needs_translation"]]
        
        print(f"   需要翻译（外文）: {len(foreign)} 篇")
        print(f"   中文原文: {len(chinese)} 篇")
        
        print("\n   处理内容示例:")
        for i, article in enumerate(process_content[:2]):
            lang = "外文" if article["needs_translation"] else "中文"
            print(f"   {i+1}. [{lang}][{article['source']}] {article['title'][:40]}...")
            print(f"      内容长度: {len(article['content'])} 字符")
    
    else:
        print("⚠️ 没有可处理的内容")
        print("建议执行爬取任务或使用模拟数据")
    
    # 5. 保存测试结果
    print("\n5. 保存测试结果...")
    test_dir = "data/crawl_tests"
    os.makedirs(test_dir, exist_ok=True)
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "existing_articles": len(articles) if 'articles' in locals() else 0,
        "process_content": len(process_content) if 'process_content' in locals() else 0,
        "crawl_performed": 'result' in locals(),
        "system_status": "爬虫功能测试完成"
    }
    
    result_file = f"{test_dir}/crawl_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        import json
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"💾 测试结果已保存到: {result_file}")
    
    print("\n" + "=" * 50)
    print("📊 爬虫功能测试总结:")
    print("   1. ✅ 爬虫初始化成功")
    print(f"   2. 📁 现有数据: {len(articles) if 'articles' in locals() else 0} 篇")
    print(f"   3. 🔄 可处理内容: {len(process_content) if 'process_content' in locals() else 0} 篇")
    print("   4. ⚙️ 系统就绪: 需要数据才能运行完整流程")
    print("=" * 50)
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请检查文件路径和依赖")
except Exception as e:
    print(f"❌ 测试失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()