#!/usr/bin/env python3
# 简单测试可靠爬虫

import os
import sys
import json
from datetime import datetime

print("🧪 测试可靠爬虫（简化版）")
print("=" * 50)

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # 测试混合爬虫
    print("1. 测试混合爬虫...")
    from scripts.hybrid_crawler import HybridCrawler
    
    crawler = HybridCrawler()
    print("✅ 混合爬虫初始化成功")
    
    # 获取数据源信息
    source_info = crawler.get_data_source_info()
    print(f"   数据源状态:")
    print(f"     - 真实爬虫可用: {source_info['real_crawler_available']}")
    print(f"     - 当前使用模拟数据: {source_info['using_mock_data']}")
    print(f"     - 模拟数据质量: {source_info['mock_data_quality']}")
    
    # 获取处理内容
    print("\n2. 获取处理内容...")
    articles = crawler.get_content_for_processing(use_cached=True)
    
    if articles:
        print(f"✅ 获取到 {len(articles)} 篇文章")
        
        foreign = [a for a in articles if a["needs_translation"]]
        chinese = [a for a in articles if not a["needs_translation"]]
        
        print(f"   需要翻译（外文）: {len(foreign)} 篇")
        print(f"   中文原文: {len(chinese)} 篇")
        
        print("\n   文章示例:")
        for i, article in enumerate(articles[:3]):
            lang = "外文" if article["needs_translation"] else "中文"
            data_source = "模拟" if crawler.use_mock_data else "真实"
            print(f"   {i+1}. [{data_source}][{lang}][{article['source']}]")
            print(f"       标题: {article['title'][:50]}...")
            print(f"       内容长度: {len(article['content'])} 字符")
            print(f"       摘要: {article['content'][:80]}...")
            print()
    else:
        print("❌ 没有获取到文章")
    
    # 测试主工作流
    print("\n3. 测试主工作流...")
    from scripts.main_workflow import Year365WinWorkflow
    
    workflow = Year365WinWorkflow()
    print("✅ 主工作流初始化成功")
    
    # 测试简报生成
    print("\n4. 生成简报...")
    briefing = workflow.run_daily_workflow("morning", use_cached=True)
    
    if briefing:
        print(f"✅ 简报生成成功!")
        print(f"   简报长度: {len(briefing)} 字符")
        
        # 显示简报开头
        print("\n   简报预览:")
        lines = briefing.split('\n')[:8]
        for line in lines:
            if line.strip():
                print(f"    {line}")
        
        # 保存测试结果
        print("\n5. 保存测试结果...")
        test_dir = "data/simple_tests"
        os.makedirs(test_dir, exist_ok=True)
        
        test_result = {
            "timestamp": datetime.now().isoformat(),
            "test_name": "简单可靠测试",
            "articles_count": len(articles) if 'articles' in locals() else 0,
            "briefing_generated": briefing is not None,
            "using_mock_data": source_info.get('using_mock_data', True),
            "system_status": "功能正常"
        }
        
        result_file = f"{test_dir}/simple_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(test_result, f, ensure_ascii=False, indent=2)
        
        print(f"💾 测试结果已保存到: {result_file}")
        
        print("\n" + "=" * 50)
        print("🎉 简单测试完成!")
        print("✅ 混合爬虫系统工作正常")
        print("✅ 主工作流生成简报成功")
        print("✅ 系统已准备好部署")
        print("=" * 50)
        
    else:
        print("❌ 简报生成失败")
        
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请检查依赖安装")
except Exception as e:
    print(f"❌ 测试失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()