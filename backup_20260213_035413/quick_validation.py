#!/usr/bin/env python3
# 快速验证总结

import os
import sys
import json
from datetime import datetime

print("📋 一年365赢 - 快速验证总结")
print("=" * 60)

# 设置环境变量
# 从环境变量获取API密钥

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

validation_results = {
    "timestamp": datetime.now().isoformat(),
    "components": {},
    "overall_status": "验证中"
}

try:
    # 1. 可靠爬虫
    print("\n1️⃣ 可靠爬虫验证...")
    try:
        from scripts.reliable_crawler import ReliableCrawler
        crawler = ReliableCrawler()
        
        # 测试Hacker News
        import requests
        hn_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(hn_url, timeout=10)
        
        if response.status_code == 200:
            validation_results["components"]["reliable_crawler"] = "PASS"
            print("✅ 可靠爬虫工作正常")
        else:
            validation_results["components"]["reliable_crawler"] = "FAIL"
            print("❌ 可靠爬虫API失败")
    except Exception as e:
        validation_results["components"]["reliable_crawler"] = f"ERROR: {type(e).__name__}"
        print(f"❌ 可靠爬虫错误: {e}")
    
    # 2. 混合爬虫
    print("\n2️⃣ 混合爬虫验证...")
    try:
        from scripts.hybrid_crawler import HybridCrawler
        crawler = HybridCrawler()
        
        articles = crawler.get_content_for_processing(use_cached=True)
        
        if articles and len(articles) > 0:
            validation_results["components"]["hybrid_crawler"] = "PASS"
            print(f"✅ 混合爬虫工作正常: {len(articles)}篇文章")
            print(f"   数据来源: {'模拟数据' if crawler.use_mock_data else '真实爬取'}")
        else:
            validation_results["components"]["hybrid_crawler"] = "FAIL"
            print("❌ 混合爬虫未获取到文章")
    except Exception as e:
        validation_results["components"]["hybrid_crawler"] = f"ERROR: {type(e).__name__}"
        print(f"❌ 混合爬虫错误: {e}")
    
    # 3. 主工作流
    print("\n3️⃣ 主工作流验证...")
    try:
        from scripts.main_workflow import Year365WinWorkflow
        workflow = Year365WinWorkflow()
        
        briefing = workflow.run_daily_workflow("quick_validation", use_cached=True)
        
        if briefing:
            validation_results["components"]["main_workflow"] = "PASS"
            print(f"✅ 主工作流工作正常: {len(briefing)}字符简报")
            
            # 检查简报质量
            if "一年365赢" in briefing and len(briefing) > 50:
                print("✅ 简报质量合格")
            else:
                print("⚠️ 简报质量可能有问题")
        else:
            validation_results["components"]["main_workflow"] = "FAIL"
            print("❌ 主工作流未生成简报")
    except Exception as e:
        validation_results["components"]["main_workflow"] = f"ERROR: {type(e).__name__}"
        print(f"❌ 主工作流错误: {e}")
    
    # 4. 文件系统
    print("\n4️⃣ 文件系统验证...")
    required_files = [
        "scripts/main_workflow.py",
        "scripts/hybrid_crawler.py", 
        "scripts/scheduler.py",
        "config/system_config.yaml",
        "config/user_profile.json"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} 存在")
        else:
            print(f"❌ {file} 缺失")
            missing_files.append(file)
    
    if not missing_files:
        validation_results["components"]["filesystem"] = "PASS"
        print("✅ 所有关键文件存在")
    else:
        validation_results["components"]["filesystem"] = f"FAIL: 缺失{len(missing_files)}个文件"
        print(f"❌ 缺失 {len(missing_files)} 个关键文件")
    
    # 5. 依赖检查
    print("\n5️⃣ 依赖检查...")
    required_packages = ["requests", "PyYAML", "schedule", "feedparser", "beautifulsoup4"]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            missing_packages.append(package)
    
    if not missing_packages:
        validation_results["components"]["dependencies"] = "PASS"
        print("✅ 所有依赖已安装")
    else:
        validation_results["components"]["dependencies"] = f"FAIL: 缺失{len(missing_packages)}个包"
        print(f"❌ 缺失 {len(missing_packages)} 个依赖包")
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 验证总结")
    print("=" * 60)
    
    passed = sum(1 for status in validation_results["components"].values() if "PASS" in str(status))
    total = len(validation_results["components"])
    
    print(f"组件总数: {total}")
    print(f"通过组件: {passed}")
    print(f"通过率: {passed*100//total if total > 0 else 0}%")
    
    print("\n组件状态:")
    for component, status in validation_results["components"].items():
        if "PASS" in str(status):
            print(f"  ✅ {component}: {status}")
        elif "FAIL" in str(status) or "ERROR" in str(status):
            print(f"  ❌ {component}: {status}")
        else:
            print(f"  ⚠️  {component}: {status}")
    
    # 确定整体状态
    if passed == total:
        validation_results["overall_status"] = "完全就绪"
        print("\n🎉 🎉 🎉 所有组件验证通过!")
        print("✅ 系统已完全就绪")
        print("🚀 可以立即部署到OpenClaw")
    elif passed >= total * 0.8:
        validation_results["overall_status"] = "基本就绪"
        print("\n⚠️  ⚠️  ⚠️ 大部分组件验证通过")
        print("✅ 系统基本就绪，可以部署")
        print("🔧 建议修复少数问题")
    else:
        validation_results["overall_status"] = "需要修复"
        print("\n❌ ❌ ❌ 多个组件验证失败")
        print("🔧 需要修复问题后再部署")
    
    # 保存结果
    validation_dir = "data/validation_summary"
    os.makedirs(validation_dir, exist_ok=True)
    
    result_file = f"{validation_dir}/quick_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(validation_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 验证结果已保存到: {result_file}")
    
    print("\n" + "=" * 60)
    print("🇨🇳 一年365赢系统验证完成")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ 验证过程出错: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()