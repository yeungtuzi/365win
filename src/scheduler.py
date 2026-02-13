#!/usr/bin/env python3
# 定时任务调度器

import os
import sys
import json
import time
import schedule
from datetime import datetime, timedelta
from typing import Dict, List

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.full_content_crawler import FullContentCrawler
from scripts.deepseek_client import DeepSeekClient
from scripts.content_processor import ContentProcessor
from scripts.recommendation_engine import RecommendationEngine

class DailyScheduler:
    """每日任务调度器"""
    
    def __init__(self):
        self.crawler = FullContentCrawler()
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        
        # 初始化DeepSeek客户端（如果API密钥可用）
        if self.api_key and self.api_key != "test_mode_key":
            self.deepseek = DeepSeekClient(self.api_key)
            self.test_mode = False
        else:
            self.deepseek = None
            self.test_mode = True
        
        # 日志目录
        self.log_dir = "logs/scheduler"
        os.makedirs(self.log_dir, exist_ok=True)
        
        # 状态文件
        self.status_file = "data/scheduler_status.json"
        
        print("定时任务调度器初始化完成")
        print(f"DeepSeek API模式: {'真实API' if not self.test_mode else '测试模式'}")
    
    def log_message(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # 打印到控制台
        print(log_entry)
        
        # 保存到日志文件
        log_file = f"{self.log_dir}/scheduler_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def update_status(self, task: str, status: str, details: Dict = None):
        """更新任务状态"""
        try:
            if os.path.exists(self.status_file):
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {}
            
            if "tasks" not in data:
                data["tasks"] = {}
            
            data["tasks"][task] = {
                "last_run": datetime.now().isoformat(),
                "status": status,
                "details": details or {}
            }
            data["last_updated"] = datetime.now().isoformat()
            
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self.log_message(f"更新状态失败: {e}", "ERROR")
    
    def daily_crawl_task(self):
        """每日爬取任务"""
        self.log_message("开始执行每日爬取任务")
        
        try:
            start_time = datetime.now()
            
            # 执行爬取
            result = self.crawler.daily_crawl()
            
            # 更新状态
            duration = (datetime.now() - start_time).total_seconds()
            self.update_status("daily_crawl", "success", {
                "foreign_articles": len(result["foreign"]),
                "chinese_articles": len(result["chinese"]),
                "duration_seconds": duration,
                "timestamp": start_time.isoformat()
            })
            
            self.log_message(f"每日爬取完成: {len(result['foreign'])}外文 + {len(result['chinese'])}中文文章, 耗时{duration:.1f}秒")
            
        except Exception as e:
            self.log_message(f"每日爬取失败: {e}", "ERROR")
            self.update_status("daily_crawl", "failed", {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
    
    def content_refresh_task(self):
        """内容刷新任务（生成新简报）"""
        self.log_message("开始执行内容刷新任务")
        
        try:
            start_time = datetime.now()
            
            # 1. 加载最近数据
            articles = self.crawler.get_content_for_processing(use_cached=True)
            
            if not articles:
                self.log_message("没有可用的文章数据", "WARNING")
                return
            
            # 2. 处理内容（如果DeepSeek可用）
            if self.deepseek and not self.test_mode:
                # 初始化处理器
                processor = ContentProcessor(self.deepseek, "config/system_config.yaml")
                
                # 处理文章
                processed_articles = []
                for article in articles[:10]:  # 处理前10篇
                    processed = processor.process_content_item(article)
                    if processed:
                        processed_articles.append(processed)
                
                self.log_message(f"内容处理完成: {len(processed_articles)}/{len(articles)}篇文章通过处理")
                
                # 3. 生成简报（示例）
                if processed_articles:
                    # 这里可以调用简报生成逻辑
                    pass
            
            # 更新状态
            duration = (datetime.now() - start_time).total_seconds()
            self.update_status("content_refresh", "success", {
                "total_articles": len(articles),
                "duration_seconds": duration,
                "timestamp": start_time.isoformat()
            })
            
            self.log_message(f"内容刷新完成, 耗时{duration:.1f}秒")
            
        except Exception as e:
            self.log_message(f"内容刷新失败: {e}", "ERROR")
            self.update_status("content_refresh", "failed", {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
    
    def cleanup_task(self):
        """清理任务"""
        self.log_message("开始执行清理任务")
        
        try:
            start_time = datetime.now()
            
            # 清理旧数据
            self.crawler.clean_old_data(days=7)
            
            # 清理旧日志（保留30天）
            self.cleanup_old_logs(days=30)
            
            # 更新状态
            duration = (datetime.now() - start_time).total_seconds()
            self.update_status("cleanup", "success", {
                "duration_seconds": duration,
                "timestamp": start_time.isoformat()
            })
            
            self.log_message(f"清理任务完成, 耗时{duration:.1f}秒")
            
        except Exception as e:
            self.log_message(f"清理任务失败: {e}", "ERROR")
            self.update_status("cleanup", "failed", {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
    
    def cleanup_old_logs(self, days: int = 30):
        """清理旧日志"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for filename in os.listdir(self.log_dir):
            if filename.startswith("scheduler_") and filename.endswith(".log"):
                filepath = os.path.join(self.log_dir, filename)
                
                try:
                    # 从文件名提取日期
                    date_str = filename[10:18]  # scheduler_YYYYMMDD.log
                    file_date = datetime.strptime(date_str, "%Y%m%d")
                    
                    if file_date < cutoff_date:
                        os.remove(filepath)
                        self.log_message(f"清理旧日志: {filename}")
                except:
                    pass
    
    def setup_schedule(self):
        """设置定时任务"""
        # 每日凌晨2点执行爬取任务（服务器负载较低时）
        schedule.every().day.at("02:00").do(self.daily_crawl_task)
        
        # 每日上午8点、中午12点、晚上8点执行内容刷新
        schedule.every().day.at("08:00").do(self.content_refresh_task)
        schedule.every().day.at("12:00").do(self.content_refresh_task)
        schedule.every().day.at("20:00").do(self.content_refresh_task)
        
        # 每周日凌晨3点执行清理任务
        schedule.every().sunday.at("03:00").do(self.cleanup_task)
        
        self.log_message("定时任务设置完成")
        print("已设置的定时任务:")
        print("  - 每日 02:00: 数据爬取任务")
        print("  - 每日 08:00: 内容刷新任务")
        print("  - 每日 12:00: 内容刷新任务")
        print("  - 每日 20:00: 内容刷新任务")
        print("  - 每周日 03:00: 清理任务")
    
    def run_once(self, task_name: str = None):
        """立即运行指定任务"""
        if task_name == "crawl":
            self.daily_crawl_task()
        elif task_name == "refresh":
            self.content_refresh_task()
        elif task_name == "cleanup":
            self.cleanup_task()
        else:
            print("可用任务:")
            print("  crawl   - 执行每日爬取")
            print("  refresh - 执行内容刷新")
            print("  cleanup - 执行清理任务")
    
    def run_scheduler(self):
        """运行调度器（持续运行）"""
        self.log_message("启动定时任务调度器")
        
        # 设置定时任务
        self.setup_schedule()
        
        # 立即执行一次爬取（如果今天还没有执行）
        self.check_and_run_initial_crawl()
        
        # 主循环
        self.log_message("定时任务调度器开始运行，按Ctrl+C停止")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
                
        except KeyboardInterrupt:
            self.log_message("定时任务调度器已停止")
        except Exception as e:
            self.log_message(f"调度器运行错误: {e}", "ERROR")
    
    def check_and_run_initial_crawl(self):
        """检查并执行初始爬取"""
        try:
            if os.path.exists(self.status_file):
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 检查今天是否已经执行过爬取
                if "tasks" in data and "daily_crawl" in data["tasks"]:
                    last_run_str = data["tasks"]["daily_crawl"].get("last_run", "")
                    if last_run_str:
                        last_run = datetime.fromisoformat(last_run_str.replace('Z', '+00:00'))
                        if last_run.date() == datetime.now().date():
                            self.log_message("今日已执行过爬取任务，跳过初始爬取")
                            return
            
            # 执行初始爬取
            self.log_message("执行初始爬取任务")
            self.daily_crawl_task()
            
        except Exception as e:
            self.log_message(f"检查初始爬取失败: {e}", "ERROR")

# 命令行接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="一年365赢定时任务调度器")
    parser.add_argument("--run", choices=["crawl", "refresh", "cleanup"], 
                       help="立即运行指定任务")
    parser.add_argument("--schedule", action="store_true",
                       help="启动定时任务调度器（持续运行）")
    parser.add_argument("--status", action="store_true",
                       help="查看调度器状态")
    
    args = parser.parse_args()
    
    # 初始化调度器
    scheduler = DailyScheduler()
    
    if args.run:
        # 立即运行指定任务
        scheduler.run_once(args.run)
    
    elif args.schedule:
        # 启动定时任务调度器
        scheduler.run_scheduler()
    
    elif args.status:
        # 查看状态
        if os.path.exists(scheduler.status_file):
            with open(scheduler.status_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print("调度器状态:")
            print(f"最后更新: {data.get('last_updated', '未知')}")
            print("\n任务状态:")
            
            for task_name, task_info in data.get("tasks", {}).items():
                print(f"  {task_name}:")
                print(f"    最后运行: {task_info.get('last_run', '未知')}")
                print(f"    状态: {task_info.get('status', '未知')}")
                
                details = task_info.get("details", {})
                if details:
                    print(f"    详情: {json.dumps(details, ensure_ascii=False)}")
                print()
        else:
            print("状态文件不存在，调度器可能尚未运行")
    
    else:
        parser.print_help()
        print("\n示例:")
        print("  python scheduler.py --run crawl      # 立即执行爬取任务")
        print("  python scheduler.py --schedule       # 启动定时任务调度器")
        print("  python scheduler.py --status         # 查看调度器状态")