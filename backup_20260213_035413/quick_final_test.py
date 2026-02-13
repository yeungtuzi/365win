#!/usr/bin/env python3
# 快速最终测试

import os
import sys
import json
from datetime import datetime

print("🚀 一年365赢 - 快速最终测试")
print("=" * 50)

# 设置环境变量
# 从环境变量获取API密钥
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

test_results = []

def test_component(name, func):
    """测试组件"""
    print(f"\n🧪 测试: {name}")
    try:
        result = func()
        print(f"✅ {name}: 通过")
        test_results.append({"component": name, "status": "PASS", "details": result})
        return True
    except Exception as e:
        print(f"❌ {name}: 失败 - {e}")
        test_results.append({"component": name, "status": "FAIL", "error": str(e)})
        return False

try:
    # 1. 测试混合爬虫
    def test_hybrid_crawler():
        from scripts.hybrid_crawler import HybridCrawler
        crawler = HybridCrawler()
        info = crawler.get_data_source_info()
        articles = crawler.get_content_for_processing(use_cached=True)
        return {
            "real_crawler_available": info["real_crawler_available"],
            "using_mock_data": info["using_mock_data"],
            "articles_count": len(articles),
            "mock_data_quality": info["mock_data_quality"]
        }
    
    test_component("混合爬虫", test_hybrid_crawler)
    
    # 2. 测试主工作流
    def test_main_workflow():
        from scripts.main_workflow import Year365WinWorkflow
        workflow = Year365WinWorkflow()
        
        # 测试数据采集
        raw_data = workflow.collect_sample_data("morning", use_cached=True)
        
        # 测试简报生成
        briefing = workflow.run_daily_workflow("morning", use_cached=True)
        
        return {
            "raw_data_count": len(raw_data),
            "briefing_generated": briefing is not None,
            "briefing_length": len(briefing) if briefing else 0,
            "test_mode": workflow.test_mode
        }
    
    test_component("主工作流", test_main_workflow)
    
    # 3. 测试定时任务调度器
    def test_scheduler():
        from scripts.scheduler import DailyScheduler
        scheduler = DailyScheduler()
        
        # 检查状态文件
        status_exists = os.path.exists(scheduler.status_file)
        
        return {
            "scheduler_initialized": True,
            "status_file_exists": status_exists,
            "test_mode": scheduler.test_mode
        }
    
    test_component("定时任务调度器", test_scheduler)
    
    # 4. 测试文件系统
    def test_filesystem():
        required_files = [
            "scripts/main_workflow.py",
            "scripts/hybrid_crawler.py", 
            "scripts/scheduler.py",
            "config/system_config.yaml",
            "config/user_profile.json"
        ]
        
        existing_files = []
        missing_files = []
        
        for file in required_files:
            if os.path.exists(file):
                existing_files.append(file)
            else:
                missing_files.append(file)
        
        return {
            "total_required": len(required_files),
            "existing_files": len(existing_files),
            "missing_files": len(missing_files),
            "all_files_exist": len(missing_files) == 0
        }
    
    test_component("文件系统", test_filesystem)
    
    # 5. 测试DeepSeek API
    def test_deepseek_api():
        from scripts.deepseek_client import DeepSeekClient
        client = DeepSeekClient(os.environ["DEEPSEEK_API_KEY"])
        
        # 测试简单翻译
        test_text = "Hello, this is a test of the DeepSeek API."
        translated = client.translate_content(test_text, "en", "zh")
        
        return {
            "api_connected": True,
            "translation_test": translated is not None,
            "translation_length": len(translated) if translated else 0
        }
    
    test_component("DeepSeek API", test_deepseek_api)
    
    # 生成测试报告
    print("\n" + "=" * 50)
    print("📊 测试报告")
    print("=" * 50)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for r in test_results if r["status"] == "PASS")
    failed_tests = total_tests - passed_tests
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"总测试数: {total_tests}")
    print(f"通过测试: {passed_tests}")
    print(f"失败测试: {failed_tests}")
    print(f"通过率: {pass_rate:.1f}%")
    
    print("\n详细结果:")
    for result in test_results:
        status_icon = "✅" if result["status"] == "PASS" else "❌"
        print(f"  {status_icon} {result['component']}")
        if result["status"] == "PASS" and "details" in result:
            for key, value in result["details"].items():
                print(f"      {key}: {value}")
        elif result["status"] == "FAIL":
            print(f"      错误: {result.get('error', '未知错误')}")
    
    # 保存测试结果
    test_dir = "data/final_test_results"
    os.makedirs(test_dir, exist_ok=True)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "pass_rate": pass_rate,
        "system_ready": failed_tests == 0,
        "test_results": test_results,
        "recommendation": "系统已就绪，可以部署" if failed_tests == 0 else "需要修复失败测试"
    }
    
    result_file = f"{test_dir}/quick_final_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 测试结果已保存到: {result_file}")
    
    print("\n" + "=" * 50)
    if failed_tests == 0:
        print("🎉 🎉 🎉 所有测试通过！")
        print("✅ 一年365赢系统已完全就绪")
        print("🚀 可以开始部署到OpenClaw")
    else:
        print(f"⚠️  有 {failed_tests} 个测试失败")
        print("🔧 需要修复失败测试后再部署")
    
    print("=" * 50)
    
except Exception as e:
    print(f"\n❌ 测试框架错误: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()