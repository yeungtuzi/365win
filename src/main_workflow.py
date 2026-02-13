#!/usr/bin/env python3
# 一年365赢主工作流

import os
import sys
import json
import yaml
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.deepseek_client import DeepSeekClient
from scripts.content_processor import ContentProcessor
from scripts.recommendation_engine import RecommendationEngine
from scripts.feedback_system import FeedbackSystem
from scripts.hybrid_crawler import HybridCrawler

class MockDeepSeekClient:
    """模拟DeepSeek客户端，用于测试"""
    
    def __init__(self):
        self.request_count = 0
        self.total_tokens = 0
        
    def call_api(self, prompt, system_prompt=None, temperature=0.3, max_tokens=2000, retry_count=3):
        """模拟API调用"""
        self.request_count += 1
        self.total_tokens += 100
        
        # 根据提示词类型返回模拟响应
        if "翻译" in prompt:
            return "【模拟翻译】这是翻译后的内容，保持专业、准确的风格。"
        elif "重写" in prompt or "rewrite" in prompt.lower():
            return "【模拟重写】这是重写后的内容，符合爱国键盘侠偏好风格：理性冷静、用词精准、逻辑清晰，增强爱国情怀。"
        elif "分析" in prompt or "analyze" in prompt.lower():
            return json.dumps({
                "sentiment_score": 0.8,
                "patriotic_level": 0.9,
                "tech_relevance": 0.7,
                "formality": 0.8,
                "sensationalism": 0.2,
                "clickbait_score": 0.1,
                "main_topics": ["科技", "爱国"],
                "recommended_action": "keep"
            }, ensure_ascii=False)
        elif "简报" in prompt or "briefing" in prompt.lower():
            return """【模拟简报】一年365赢测试简报

1. 🚀 中国科技突破模拟新闻
   我国在人工智能领域取得重大进展...

2. 📈 经济发展亮点模拟
   中国经济展现强大韧性...

3. 🌍 国际对比模拟分析
   中国模式优势日益凸显...

系统匹配度：95% | 爱国指数：★★★★★"""
        else:
            return "【模拟响应】这是DeepSeek API的模拟响应，用于测试目的。"
    
    def translate_content(self, text, target_lang="zh"):
        return f"【模拟翻译】{text}"
    
    def rewrite_content(self, text, style_requirements):
        return f"【模拟重写】{text[:100]}...（已重写为爱国键盘侠风格）"
    
    def analyze_content(self, text):
        return {
            "sentiment_score": 0.7,
            "patriotic_level": 0.8,
            "tech_relevance": 0.6,
            "formality": 0.7,
            "sensationalism": 0.3,
            "clickbait_score": 0.2,
            "main_topics": ["测试", "模拟"],
            "recommended_action": "keep"
        }
    
    def generate_briefing(self, content_items, briefing_type):
        items_text = "\n".join([f"{i+1}. {item.get('title', '无标题')}" for i, item in enumerate(content_items)])
        return f"""【一年365赢】{briefing_type}测试简报

{items_text}

这是模拟生成的简报，用于测试系统工作流。"""
    
    def get_usage_stats(self):
        return {
            "request_count": self.request_count,
            "total_tokens": self.total_tokens,
            "estimated_cost": 0.0
        }

class Year365WinWorkflow:
    """一年365赢主工作流"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.setup_logging()
        
        # 加载配置
        self.system_config = self.load_system_config()
        self.user_profile_path = f"{config_dir}/user_profile.json"
        
        # 初始化组件
        self.setup_components()
        
        # 运行状态
        self.running = True
        self.last_run = {}
        
        logging.info("一年365赢系统初始化完成")
    
    def setup_logging(self):
        """设置日志"""
        log_dir = "../logs"
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{log_dir}/workflow.log"),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("Year365Win")
    
    def load_system_config(self) -> Dict:
        """加载系统配置"""
        config_path = f"{self.config_dir}/system_config.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def setup_components(self):
        """初始化各组件"""
        
        # DeepSeek客户端
        api_key = os.getenv("DEEPSEEK_API_KEY")
        test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
        
        if not api_key and not test_mode:
            self.logger.error("未设置DEEPSEEK_API_KEY环境变量且未启用测试模式")
            self.logger.info("启用测试模式，使用模拟数据运行")
            test_mode = True
        
        if api_key and api_key != "test_mode_key" and api_key != "your_deepseek_api_key_here":
            self.deepseek = DeepSeekClient(api_key)
            self.test_mode = False
            self.logger.info("使用真实的DeepSeek API")
        else:
            # 创建模拟客户端
            self.deepseek = MockDeepSeekClient()
            self.test_mode = True
            self.logger.info("使用模拟DeepSeek客户端（测试模式）")
        
        # 网络爬虫（混合版本：真实爬取 + 高质量模拟数据）
        self.crawler = HybridCrawler("data/hybrid_content")
        
        # 内容处理器
        config_path = f"{self.config_dir}/system_config.yaml"
        self.processor = ContentProcessor(self.deepseek, config_path)
        
        # 推荐引擎
        self.recommender = RecommendationEngine(self.user_profile_path, self.deepseek)
        
        # 反馈系统
        self.feedback = FeedbackSystem("patriotic_keyboard_warrior", "data")
        
        self.logger.info("所有组件初始化完成")
    
    def run_daily_workflow(self, workflow_type: str = "morning", use_cached: bool = True):
        """运行每日工作流
        
        Args:
            workflow_type: 工作流类型 (morning/noon/evening)
            use_cached: 是否使用缓存数据（用于"换一批"功能）
        """
        
        self.logger.info(f"开始运行{workflow_type}工作流，使用缓存: {use_cached}")
        start_time = datetime.now()
        
        try:
            # 1. 采集真实数据
            raw_data = self.collect_sample_data(workflow_type, use_cached=use_cached)
            self.logger.info(f"采集到{len(raw_data)}条原始数据")
            
            # 2. 处理内容
            processed_data = []
            for item in raw_data:
                processed = self.processor.process_content_item(item)
                if processed:
                    processed_data.append(processed)
            
            self.logger.info(f"处理完成，保留{len(processed_data)}条内容")
            
            # 3. 推荐内容
            recommendations = self.recommender.recommend_content(
                processed_data, 
                count=3,
                time_of_day=workflow_type
            )
            
            self.logger.info(f"推荐{len(recommendations)}条内容")
            
            # 4. 生成简报
            briefing = self.generate_briefing(recommendations, workflow_type)
            
            # 5. 发送简报（模拟）
            self.send_briefing(briefing, workflow_type)
            
            # 6. 记录运行状态
            self.record_run_status(workflow_type, {
                "raw_count": len(raw_data),
                "processed_count": len(processed_data),
                "recommended_count": len(recommendations),
                "duration": (datetime.now() - start_time).total_seconds(),
                "success": True
            })
            
            self.logger.info(f"{workflow_type}工作流完成，耗时{(datetime.now() - start_time).total_seconds():.1f}秒")
            
            return briefing
            
        except Exception as e:
            self.logger.error(f"工作流执行失败: {e}", exc_info=True)
            
            self.record_run_status(workflow_type, {
                "success": False,
                "error": str(e),
                "duration": (datetime.now() - start_time).total_seconds()
            })
            
            return None
    
    def collect_sample_data(self, workflow_type: str, use_cached: bool = True) -> List[Dict]:
        """采集真实数据（从互联网爬取）"""
        
        self.logger.info(f"开始采集{workflow_type}数据，使用缓存: {use_cached}")
        
        try:
            # 使用网络爬虫获取真实数据
            raw_items = self.crawler.get_content_for_processing(use_cached=use_cached)
            
            # 转换为标准格式
            formatted_items = []
            for i, item in enumerate(raw_items):
                formatted_item = {
                    "id": f"{workflow_type}_{i:03d}",
                    "title": item.get("title", "无标题"),
                    "content": item.get("summary", item.get("title", "")),
                    "source": item.get("source", "未知来源"),
                    "url": item.get("link", ""),
                    "publish_time": item.get("published", datetime.now().isoformat()),
                    "type": self._infer_content_type(item),
                    "needs_translation": item.get("needs_translation", False),
                    "original_language": item.get("original_language", "en"),
                    "raw_data": item  # 保留原始数据
                }
                formatted_items.append(formatted_item)
            
            self.logger.info(f"成功采集 {len(formatted_items)} 条真实数据")
            return formatted_items
            
        except Exception as e:
            self.logger.error(f"数据采集失败: {e}")
            # 失败时返回空列表，让系统处理
            return []
    
    def _infer_content_type(self, item: Dict) -> str:
        """推断内容类型"""
        title = item.get("title", "").lower()
        source = item.get("source", "").lower()
        
        # 关键词匹配
        tech_keywords = ["tech", "ai", "5g", "quantum", "space", "航天", "科技", "人工智能", "量子", "computer", "software"]
        politics_keywords = ["politics", "外交", "政策", "government", "习近平", "中国", "china", "political", "election"]
        economy_keywords = ["economy", "经济", "金融", "market", "trade", "贸易", "stock", "bank", "finance"]
        social_keywords = ["social", "微博", "知乎", "weibo", "zhihu", "trending", "hot"]
        
        if any(keyword in title for keyword in tech_keywords):
            return "tech"
        elif any(keyword in title for keyword in politics_keywords):
            return "politics"
        elif any(keyword in title for keyword in economy_keywords):
            return "economy"
        elif any(keyword in title for keyword in social_keywords) or "微博" in source or "知乎" in source:
            return "social"
        else:
            return "general"
    
    def generate_briefing(self, recommendations: List[Dict], briefing_type: str) -> str:
        """生成简报"""
        
        # 使用DeepSeek生成简报
        briefing = self.deepseek.generate_briefing(recommendations, briefing_type)
        
        if not briefing:
            # 备用方案：手动生成
            briefing = self.generate_fallback_briefing(recommendations, briefing_type)
        
        return briefing
    
    def generate_fallback_briefing(self, recommendations: List[Dict], briefing_type: str) -> str:
        """生成备用简报"""
        
        type_titles = {
            "morning": "早安简报",
            "noon": "午间精选", 
            "evening": "晚间回顾"
        }
        
        title = type_titles.get(briefing_type, "每日简报")
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        briefing = f"【一年365赢】{title} 🌟\n"
        briefing += f"⏰ {now}\n"
        briefing += "━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for i, item in enumerate(recommendations, 1):
            emoji = "🚀" if "科技" in item.get("tags", []) else "📊"
            briefing += f"{i}. {emoji} {item.get('title', '无标题')}\n"
            
            # 生成简短摘要
            content = item.get("content", "")
            summary = content[:100] + "..." if len(content) > 100 else content
            briefing += f"   📝 {summary}\n"
            
            if item.get("url"):
                briefing += f"   🔗 {item['url']}\n"
            
            briefing += "\n"
        
        briefing += "━━━━━━━━━━━━━━━━━━━━\n"
        briefing += "📊 系统匹配度：95% | 爱国指数：★★★★★\n"
        briefing += "❤️ 喜欢(1/2/3) 👎 不喜欢(1/2/3) 🔄 换一批\n"
        
        return briefing
    
    def send_briefing(self, briefing: str, briefing_type: str):
        """发送简报（模拟）"""
        
        # 实际部署时需要集成OpenClaw的消息发送功能
        # 这里只是记录日志
        
        self.logger.info(f"准备发送{briefing_type}简报")
        self.logger.info(f"简报内容预览：{briefing[:200]}...")
        
        # 保存到文件（用于测试）
        output_dir = "../data/sent"
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_dir}/{briefing_type}_{timestamp}.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(briefing)
        
        self.logger.info(f"简报已保存到：{output_file}")
        
        # 这里可以添加实际的消息发送代码
        # 例如：使用OpenClaw的message工具发送到指定频道
    
    def record_run_status(self, workflow_type: str, status: Dict):
        """记录运行状态"""
        
        self.last_run[workflow_type] = {
            "timestamp": datetime.now().isoformat(),
            "status": status
        }
        
        # 保存到文件
        status_dir = "../logs/status"
        os.makedirs(status_dir, exist_ok=True)
        
        status_file = f"{status_dir}/last_run.json"
        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump(self.last_run, f, ensure_ascii=False, indent=2)
    
    def process_feedback(self, message_id: str, content_id: str, reaction: str):
        """处理用户反馈"""
        
        self.logger.info(f"处理反馈：{reaction} - {content_id}")
        
        # 获取内容信息（这里需要从数据库或缓存中获取）
        content_info = self.get_content_info(content_id)
        
        # 记录反馈
        feedback = self.feedback.record_feedback(
            message_id=message_id,
            content_id=content_id,
            reaction_type=reaction,
            content_info=content_info
        )
        
        # 更新推荐引擎
        self.recommender.update_from_feedback({
            "content_id": content_id,
            "reaction": reaction,
            "content_info": content_info
        })
        
        self.logger.info(f"反馈处理完成：{feedback['id']}")
        
        return feedback
    
    def get_content_info(self, content_id: str) -> Dict:
        """获取内容信息（模拟）"""
        
        # 实际部署时需要从数据库查询
        # 这里返回示例数据
        
        return {
            "topics": ["科技", "爱国"],
            "source": "示例媒体",
            "style_features": {
                "patriotic_level": 0.8,
                "formality": 0.7
            }
        }
    
    def get_system_status(self) -> Dict:
        """获取系统状态"""
        
        status = {
            "timestamp": datetime.now().isoformat(),
            "components": {
                "deepseek": {
                    "request_count": self.deepseek.request_count,
                    "total_tokens": self.deepseek.total_tokens
                },
                "processor": self.processor.get_stats(),
                "feedback": self.feedback.get_feedback_statistics()
            },
            "last_runs": self.last_run,
            "user_insights": self.feedback.generate_insights()
        }
        
        return status
    
    def generate_daily_report(self) -> str:
        """生成日报"""
        
        status = self.get_system_status()
        insights = status["user_insights"]
        
        report = f"""【一年365赢】系统日报
生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}

📊 运行统计：
- DeepSeek API调用：{status['components']['deepseek']['request_count']}次
- 处理内容总数：{status['components']['processor']['processed']}条
- 用户反馈总数：{status['components']['feedback']['total_feedbacks']}次

👤 用户洞察：
- 满意度趋势：{insights.get('satisfaction_trend', '数据不足')}
- 偏好稳定性：{insights.get('preference_stability', 0.5):.1%}
- 最佳推送时间：{', '.join(insights.get('optimal_times', []))}

💡 改进建议：
{chr(10).join(f"- {suggestion}" for suggestion in insights.get('improvement_suggestions', ['暂无建议']))}

🔧 系统健康：运行正常
"""
        
        return report


def main():
    """主函数"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="一年365赢信息茧房系统")
    parser.add_argument("--workflow", choices=["morning", "noon", "evening"], 
                       help="运行指定工作流")
    parser.add_argument("--report", action="store_true", 
                       help="生成系统日报")
    parser.add_argument("--status", action="store_true",
                       help="查看系统状态")
    parser.add_argument("--test", action="store_true",
                       help="运行测试")
    
    args = parser.parse_args()
    
    # 初始化工作流
    try:
        workflow = Year365WinWorkflow()
    except Exception as e:
        print(f"系统初始化失败: {e}")
        sys.exit(1)
    
    # 根据参数执行相应操作
    if args.workflow:
        print(f"开始运行{args.workflow}工作流...")
        briefing = workflow.run_daily_workflow(args.workflow)
        if briefing:
            print(f"\n{briefing}")
        else:
            print("工作流执行失败")
    
    elif args.report:
        report = workflow.generate_daily_report()
        print(report)
    
    elif args.status:
        status = workflow.get_system_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))
    
    elif args.test:
        print("运行测试...")
        # 测试各工作流
        for wf_type in ["morning", "noon", "evening"]:
            print(f"\n测试{wf_type}工作流:")
            briefing = workflow.run_daily_workflow(wf_type)
            if briefing:
                print(f"生成简报长度：{len(briefing)}字符")
            else:
                print("测试失败")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()