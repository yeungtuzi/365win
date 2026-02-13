#!/usr/bin/env python3
"""
一年365赢 - 基本使用示例
"""

import os
import sys

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def example_gnews_crawler():
    """示例: 使用gnews.io集成爬虫"""
    print("示例1: 使用gnews.io集成爬虫")
    print("=" * 60)
    
    try:
        from src.gnews_integrated_crawler import GNewsIntegratedCrawler
        
        # 初始化爬虫
        crawler = GNewsIntegratedCrawler()
        print("✅ 爬虫初始化成功")
        
        # 检查API密钥
        if not crawler.deepseek_api_key:
            print("⚠️  DeepSeek API密钥未设置，部分功能受限")
        
        if not crawler.gnews_api_key:
            print("⚠️  gnews.io API密钥未设置，使用模拟数据")
        
        # 获取新闻文章
        print("\n📡 获取新闻文章...")
        articles = crawler.fetch_news_articles(max_articles=5)
        
        print(f"✅ 获取到 {len(articles)} 篇文章")
        
        for i, article in enumerate(articles[:3], 1):
            print(f"\n{i}. {article.get('title', '无标题')[:60]}...")
            print(f"   来源: {article.get('source', {}).get('name', '未知')}")
            print(f"   语言: {article.get('language', '未知')}")
        
        # 生成简报
        print("\n📝 生成简报...")
        briefing = crawler.generate_briefing("示例")
        
        if briefing:
            print(f"✅ 简报生成成功 ({len(briefing)} 字符)")
            print("\n简报预览:")
            for line in briefing.split('\n')[:5]:
                if line.strip():
                    print(f"  {line[:80]}...")
        else:
            print("❌ 简报生成失败")
        
    except Exception as e:
        print(f"❌ 示例执行失败: {type(e).__name__}: {e}")

def example_cli_usage():
    """示例: 使用命令行接口"""
    print("\n\n示例2: 使用命令行接口")
    print("=" * 60)
    
    print("可以通过命令行直接使用系统:")
    print()
    print("  生成晨间简报:")
    print("    python -m src.cli morning")
    print()
    print("  生成午间简报:")
    print("    python -m src.cli noon")
    print()
    print("  生成晚间简报:")
    print("    python -m src.cli evening")
    print()
    print("  执行数据爬取:")
    print("    python -m src.cli crawl")
    print()
    print("  测试系统功能:")
    print("    python -m src.cli test")
    print()
    print("  查看版本信息:")
    print("    python -m src.cli version")

def example_environment_setup():
    """示例: 环境设置"""
    print("\n\n示例3: 环境设置")
    print("=" * 60)
    
    print("1. 复制环境变量模板:")
    print("   cp .env.example .env")
    print()
    print("2. 编辑.env文件，填入API密钥:")
    print("   DEEPSEEK_API_KEY=your_deepseek_api_key_here")
    print("   GNEWS_API_KEY=your_gnews_api_key_here")
    print()
    print("3. 或者直接设置环境变量:")
    print("   export DEEPSEEK_API_KEY=your_key")
    print("   export GNEWS_API_KEY=your_key")
    print()
    print("4. 运行设置脚本:")
    print("   ./setup.sh")

def example_openclaw_integration():
    """示例: OpenClaw集成"""
    print("\n\n示例4: OpenClaw集成")
    print("=" * 60)
    
    print("设置OpenClaw定时任务:")
    print()
    print("  每日晨间简报 (08:00 UTC):")
    print("    openclaw cron add --name \"365win_morning\" \\")
    print("      --schedule \"0 8 * * *\" \\")
    print("      --command \"cd /path/to/365win && python -m src.cli morning\"")
    print()
    print("  每日午间简报 (12:00 UTC):")
    print("    openclaw cron add --name \"365win_noon\" \\")
    print("      --schedule \"0 12 * * *\" \\")
    print("      --command \"cd /path/to/365win && python -m src.cli noon\"")
    print()
    print("  每日晚间简报 (20:00 UTC):")
    print("    openclaw cron add --name \"365win_evening\" \\")
    print("      --schedule \"0 20 * * *\" \\")
    print("      --command \"cd /path/to/365win && python -m src.cli evening\"")

def main():
    """主函数"""
    print("一年365赢 - 使用示例")
    print("=" * 60)
    
    examples = [
        example_gnews_crawler,
        example_cli_usage,
        example_environment_setup,
        example_openclaw_integration,
    ]
    
    for example in examples:
        try:
            example()
            print()
        except Exception as e:
            print(f"❌ 示例执行失败: {type(e).__name__}: {e}")
            print()
    
    print("=" * 60)
    print("🎉 示例演示完成!")
    print()
    print("💡 下一步:")
    print("  1. 设置环境变量")
    print("  2. 运行测试: python tests/test_basic.py")
    print("  3. 尝试生成简报: python -m src.cli morning")
    print("  4. 部署到OpenClaw")

if __name__ == "__main__":
    main()