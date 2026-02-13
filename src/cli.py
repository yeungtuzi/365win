#!/usr/bin/env python3
"""
一年365赢命令行接口
"""

import os
import sys
import argparse
from datetime import datetime
from .gnews_integrated_crawler import GNewsIntegratedCrawler

def main():
    """主命令行入口"""
    parser = argparse.ArgumentParser(
        description="一年365赢 - 爱国键盘侠个性化信息茧房系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s morning      # 生成晨间简报
  %(prog)s noon         # 生成午间简报  
  %(prog)s evening      # 生成晚间简报
  %(prog)s crawl        # 执行数据爬取
  %(prog)s test         # 测试系统功能
        """
    )
    
    parser.add_argument(
        "command",
        choices=["morning", "noon", "evening", "crawl", "test", "version"],
        help="要执行的命令"
    )
    
    parser.add_argument(
        "--config",
        default="config/news_crawler_config.yaml",
        help="配置文件路径"
    )
    
    parser.add_argument(
        "--output",
        help="输出文件路径"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="详细输出模式"
    )
    
    args = parser.parse_args()
    
    # 检查环境变量
    check_environment()
    
    # 执行命令
    if args.command == "version":
        print_version()
    elif args.command == "test":
        run_tests(args.verbose)
    else:
        run_workflow(args.command, args.config, args.output, args.verbose)

def check_environment():
    """检查环境变量"""
    required_vars = ["DEEPSEEK_API_KEY", "GNEWS_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  警告: 以下环境变量未设置:")
        for var in missing_vars:
            print(f"    - {var}")
        print("\n💡 提示: 创建.env文件或设置环境变量")
        print("      参考 .env.example 文件")
        
        # 询问是否继续
        response = input("\n是否继续? (y/N): ").lower()
        if response != 'y':
            sys.exit(1)

def print_version():
    """打印版本信息"""
    from . import __version__, __author__, __description__
    
    print(f"一年365赢 v{__version__}")
    print(f"作者: {__author__}")
    print(f"描述: {__description__}")
    print(f"Python: {sys.version}")
    print(f"路径: {os.path.dirname(os.path.abspath(__file__))}")

def run_tests(verbose=False):
    """运行测试"""
    print("🧪 运行系统测试...")
    
    try:
        # 测试1: 初始化爬虫
        print("1. 测试爬虫初始化...")
        crawler = GNewsIntegratedCrawler()
        print("   ✅ 爬虫初始化成功")
        
        # 测试2: 检查API密钥
        print("2. 检查API密钥...")
        if crawler.deepseek_api_key:
            print("   ✅ DeepSeek API密钥已设置")
        else:
            print("   ⚠️  DeepSeek API密钥未设置")
            
        if crawler.gnews_api_key:
            print("   ✅ gnews.io API密钥已设置")
        else:
            print("   ⚠️  gnews.io API密钥未设置")
        
        # 测试3: 配置文件
        print("3. 检查配置文件...")
        if os.path.exists("config/news_crawler_config.yaml"):
            print("   ✅ 配置文件存在")
        else:
            print("   ❌ 配置文件不存在")
        
        print("\n✅ 基本测试完成")
        print("💡 运行完整测试请使用: pytest tests/")
        
    except Exception as e:
        print(f"❌ 测试失败: {type(e).__name__}: {e}")
        sys.exit(1)

def run_workflow(command, config_path, output_path, verbose=False):
    """运行工作流"""
    print(f"🚀 开始执行: {command} 工作流")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # 初始化爬虫
        crawler = GNewsIntegratedCrawler(config_path)
        
        if command == "crawl":
            # 执行数据爬取
            print("📡 执行数据爬取...")
            articles = crawler.fetch_news_articles()
            print(f"✅ 爬取完成: {len(articles)} 篇文章")
            
            # 保存结果
            if output_path:
                crawler.save_to_file(articles, output_path)
                print(f"💾 数据已保存到: {output_path}")
                
        else:
            # 生成简报
            print(f"📝 生成{command}简报...")
            
            # 确定简报类型
            if command == "morning":
                briefing_type = "晨间"
            elif command == "noon":
                briefing_type = "午间"
            else:  # evening
                briefing_type = "晚间"
            
            # 生成简报
            briefing = crawler.generate_briefing(briefing_type)
            
            if briefing:
                print(f"✅ 简报生成成功: {len(briefing)} 字符")
                
                # 输出简报
                print("\n" + "=" * 60)
                print(briefing)
                print("=" * 60)
                
                # 保存简报
                if output_path:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(briefing)
                    print(f"\n💾 简报已保存到: {output_path}")
                else:
                    # 自动保存
                    filename = f"data/{command}_briefing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                    os.makedirs("data", exist_ok=True)
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(briefing)
                    print(f"\n💾 简报已自动保存到: {filename}")
            else:
                print("❌ 简报生成失败")
                sys.exit(1)
        
        print("\n" + "=" * 60)
        print(f"✅ {command} 工作流执行完成!")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"\n❌ 工作流执行失败: {type(e).__name__}: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()