#!/usr/bin/env python3
# 每日爬取调度器

import os
import sys
import json
from datetime import datetime, timedelta
import schedule
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.full_content_crawler import FullContentCrawler

class DailyCrawlScheduler:
    """每日爬取调度器"""
    
    def __init__(self):
        self.crawler = FullContentCrawler()
        self.log_file = "logs/crawl_scheduler.log"
        
        # 创建日志目录
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        print(log_message)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + "\n")
    
    def run_daily_crawl(self):
        """运行每日爬取任务"""
        self.log("开始每日爬取任务")
        
        try:
            # 运行爬取
            result = self.crawler.daily_crawl()
            
            # 记录结果
            stats = {
                "date": datetime.now().isoformat(),
                "foreign_articles": len(result["foreign"]),
                "chinese_articles": len(result["chinese"]),
                "total_articles": len(result["foreign"]) + len(result["chinese"]),
                "status": "success"
            }
            
            self.log(f"爬取完成: {stats['foreign_articles']}外文 + {stats['chinese_articles']}中文 = {stats['total_articles']}篇")
            
            # 保存统计
            stats_dir = "data/crawl_stats"
            os.makedirs(stats_dir, exist_ok=True)
            stats_file = f"{stats_dir}/stats_{datetime.now().strftime('%Y%m%d')}.json"
            
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            
            self.log(f"统计已保存: {stats_file}")
            
        except Exception as e:
            error_msg = f"爬取任务失败: {type(e).__name__}: {e}"
            self.log(error_msg)
            
            # 保存错误信息
            error_stats = {
                "date": datetime.now().isoformat(),
                "error": str(e),
                "error_type": type(e).__name__,
                "status": "failed"
            }
            
            error_dir = "data/crawl_errors"
            os.makedirs(error_dir, exist_ok=True)
            error_file = f"{error_dir}/error_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            
            with open(error_file, 'w', encoding='utf-8') as f:
                json.dump(error_stats, f, ensure_ascii=False, indent=2)
    
    def check_buffer_status(self):
        """检查缓冲状态"""
        try:
            articles = self.crawler.load_recent_data(days=3)
            
            status = {
                "check_time": datetime.now().isoformat(),
                "total_articles": len(articles),
                "foreign_articles": len([a for a in articles if a["language"] == "en"]),
                "chinese_articles": len([a for a in articles if a["language"] == "zh"]),
                "oldest_article": min([a.get("crawl_date", "") for a in articles], default="无数据"),
                "newest_article": max([a.get("crawl_date", "") for a in articles], default="无数据")
            }
            
            self.log(f"缓冲状态: {status['total_articles']}篇文章 ({status['foreign_articles']}外文, {status['chinese_articles']}中文)")
            
            # 保存状态报告
            status_dir = "data/buffer_status"
            os.makedirs(status_dir, exist_ok=True)
            status_file = f"{status_dir}/status_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            
            with open(status_file, 'w', encoding='utf-8') as f:
                json.dump(status, f, ensure_ascii=False, indent=2)
            
            return status
            
        except Exception as e:
            self.log(f"检查缓冲状态失败: {e}")
            return None
    
    def setup_schedule(self):
        """设置定时任务"""
        # 每日凌晨2点运行爬取（服务器负载较低时）
        schedule.every().day.at("02:00").do(self.run_daily_crawl)
        
        # 每小时检查一次缓冲状态
        schedule.every().hour.do(self.check_buffer_status)
        
        self.log("定时任务已设置:")
        self.log("  - 每日 02:00: 运行爬取任务")
        self.log("  - 每小时: 检查缓冲状态")
    
    def run_scheduler(self):
        """运行调度器"""
        self.log("启动每日爬取调度器")
        self.log(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 设置定时任务
        self.setup_schedule()
        
        # 立即运行一次缓冲检查
        self.check_buffer_status()
        
        # 如果当前时间接近2点，立即运行一次爬取
        current_hour = datetime.now().hour
        if current_hour == 1 or current_hour == 2:  # 1-2点之间
            self.log("当前时间接近爬取时间，立即运行爬取任务")
            self.run_daily_crawl()
        
        self.log("调度器运行中，按Ctrl+C退出")
        
        try:
            # 主循环
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
                
        except KeyboardInterrupt:
            self.log("调度器已停止")
        except Exception as e:
            self.log(f"调度器异常退出: {e}")

def manual_crawl():
    """手动运行爬取"""
    print("手动运行每日爬取...")
    
    scheduler = DailyCrawlScheduler()
    scheduler.run_daily_crawl()
    
    # 检查缓冲状态
    status = scheduler.check_buffer_status()
    
    if status:
        print(f"\n缓冲状态:")
        print(f"  总文章数: {status['total_articles']}")
        print(f"  外文文章: {status['foreign_articles']}")
        print(f"  中文文章: {status['chinese_articles']}")
        print(f"  最早文章: {status['oldest_article'][:19] if status['oldest_article'] != '无数据' else '无数据'}")
        print(f"  最新文章: {status['newest_article'][:19] if status['newest_article'] != '无数据' else '无数据'}")

def check_status():
    """检查状态"""
    print("检查系统状态...")
    
    scheduler = DailyCrawlScheduler()
    status = scheduler.check_buffer_status()
    
    if status:
        print(f"\n📊 缓冲状态报告:")
        print(f"  总文章数: {status['total_articles']}篇")
        print(f"  外文文章: {status['foreign_articles']}篇 ({(status['foreign_articles']/max(status['total_articles'],1))*100:.1f}%)")
        print(f"  中文文章: {status['chinese_articles']}篇 ({(status['chinese_articles']/max(status['total_articles'],1))*100:.1f}%)")
        
        if status['total_articles'] > 0:
            print(f"\n📅 数据时间范围:")
            print(f"  最早: {status['oldest_article'][:19]}")
            print(f"  最新: {status['newest_article'][:19]}")
            
            # 计算数据新鲜度
            newest_date = datetime.fromisoformat(status['newest_article'].replace('Z', '+00:00'))
            hours_old = (datetime.now() - newest_date).total_seconds() / 3600
            
            if hours_old < 24:
                print(f"  数据新鲜度: ✅ {hours_old:.1f}小时前")
            elif hours_old < 72:
                print(f"  数据新鲜度: ⚠️ {hours_old/24:.1f}天前")
            else:
                print(f"  数据新鲜度: ❌ {hours_old/24:.1f}天前（建议运行爬取）")
        else:
            print("\n❌ 缓冲中没有数据，请运行爬取任务")
    else:
        print("❌ 无法获取状态信息")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="每日爬取调度器")
    parser.add_argument("--crawl", action="store_true", help="手动运行爬取")
    parser.add_argument("--status", action="store_true", help="检查状态")
    parser.add_argument("--start", action="store_true", help="启动调度器")
    
    args = parser.parse_args()
    
    if args.crawl:
        manual_crawl()
    elif args.status:
        check_status()
    elif args.start:
        scheduler = DailyCrawlScheduler()
        scheduler.run_scheduler()
    else:
        print("请指定操作:")
        print("  --crawl   手动运行爬取")
        print("  --status  检查状态")
        print("  --start   启动调度器")