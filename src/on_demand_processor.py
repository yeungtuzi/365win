#!/usr/bin/env python3
# 按需处理引擎

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Optional

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.full_content_crawler import FullContentCrawler
from scripts.deepseek_client import DeepSeekClient
from scripts.content_processor import ContentProcessor
from scripts.recommendation_engine import RecommendationEngine

class OnDemandProcessor:
    """按需处理引擎"""
    
    def __init__(self, api_key: str = None):
        # 初始化组件
        self.crawler = FullContentCrawler()
        
        # DeepSeek客户端
        if not api_key:
            api_key = os.getenv("DEEPSEEK_API_KEY")
        
        if api_key and api_key != "test_mode_key":
            self.deepseek = DeepSeekClient(api_key)
            self.test_mode = False
            print("✅ 使用真实的DeepSeek API")
        else:
            # 创建模拟客户端
            self.deepseek = self.create_mock_client()
            self.test_mode = True
            print("⚠️ 使用模拟DeepSeek客户端（测试模式）")
        
        # 内容处理器
        self.processor = ContentProcessor(self.deepseek, "config/system_config.yaml")
        
        # 推荐引擎
        self.recommender = RecommendationEngine("config/user_profile.json", self.deepseek)
        
        # 输出目录
        self.output_dir = "data/processed_output"
        os.makedirs(self.output_dir, exist_ok=True)
        
        print("✅ 按需处理引擎初始化完成")
    
    def create_mock_client(self):
        """创建模拟客户端"""
        class MockDeepSeekClient:
            def __init__(self):
                self.request_count = 0
            
            def analyze_content(self, text):
                self.request_count += 1
                return {
                    "sentiment_score": 0.7,
                    "patriotic_level": 0.6,
                    "tech_relevance": 0.5,
                    "formality": 0.6,
                    "sensationalism": 0.3,
                    "clickbait_score": 0.2,
                    "main_topics": ["测试"],
                    "recommended_action": "keep"
                }
            
            def rewrite_content(self, text, style_requirements):
                self.request_count += 1
                return f"【爱国键盘侠风格重写】{text[:200]}..."
            
            def translate_content(self, text, target_lang="zh"):
                self.request_count += 1
                return f"【翻译】{text}"
            
            def generate_briefing(self, content_items, briefing_type):
                self.request_count += 1
                return f"【{briefing_type}简报】测试简报内容"
        
        return MockDeepSeekClient()
    
    def load_content_for_processing(self, use_cached: bool = True) -> List[Dict]:
        """加载待处理的内容"""
        print(f"加载内容（使用缓存: {use_cached}）...")
        
        articles = self.crawler.get_content_for_processing(use_cached=use_cached)
        
        if not articles:
            print("⚠️ 没有找到可处理的内容")
            return []
        
        print(f"✅ 加载 {len(articles)} 篇文章")
        
        # 转换为标准格式
        formatted_items = []
        for i, article in enumerate(articles):
            formatted_item = {
                "id": f"article_{i:03d}",
                "title": article.get("title", "无标题"),
                "content": article.get("content", ""),
                "source": article.get("source", "未知来源"),
                "url": article.get("url", ""),
                "publish_time": article.get("crawl_time", datetime.now().isoformat()),
                "type": article.get("category", "general"),
                "needs_translation": article.get("needs_translation", False),
                "original_language": article.get("original_language", "en"),
                "raw_data": article
            }
            formatted_items.append(formatted_item)
        
        return formatted_items
    
    def process_content(self, items: List[Dict]) -> List[Dict]:
        """处理内容"""
        print(f"开始处理 {len(items)} 篇文章...")
        
        processed_items = []
        
        for i, item in enumerate(items):
            print(f"  处理 {i+1}/{len(items)}: {item['title'][:40]}...")
            
            # 1. 翻译（如果需要）
            if item.get("needs_translation"):
                print(f"    翻译外文内容...")
                translated = self.deepseek.translate_content(item["content"], target_lang="zh")
                item["translated_content"] = translated
                item["content"] = translated  # 使用翻译后的内容进行后续处理
            
            # 2. 内容分析
            print(f"    分析内容...")
            analysis = self.deepseek.analyze_content(item["content"])
            item["analysis"] = analysis
            
            # 3. 内容重写（转为爱国键盘侠风格）
            print(f"    重写内容...")
            style_requirements = {
                "目标风格": "爱国键盘侠偏好",
                "要求": "理性冷静、用词精准、逻辑清晰、增强爱国情怀",
                "避免": "小清新、轻佻语气、阴谋论、负面情绪"
            }
            rewritten = self.deepseek.rewrite_content(item["content"], style_requirements)
            item["rewritten_content"] = rewritten
            
            # 4. 情感增强
            if analysis.get("sentiment_score", 0) < 0.6:
                print(f"    增强情感...")
                enhancement_prompt = f"请增强以下内容的爱国情怀和正面情感:\n\n{rewritten}"
                enhanced = self.deepseek.call_api(
                    enhancement_prompt,
                    system_prompt="你是一个爱国情感增强专家",
                    temperature=0.3,
                    max_tokens=1000
                )
                item["enhanced_content"] = enhanced
            else:
                item["enhanced_content"] = rewritten
            
            processed_items.append(item)
            
            # 进度显示
            if (i + 1) % 3 == 0 or i == len(items) - 1:
                print(f"    进度: {i+1}/{len(items)} 完成")
        
        print(f"✅ 处理完成: {len(processed_items)} 篇文章")
        return processed_items
    
    def generate_recommendations(self, items: List[Dict], count: int = 3) -> List[Dict]:
        """生成推荐"""
        print(f"生成推荐（选择 {count} 篇）...")
        
        # 使用推荐引擎
        recommendations = self.recommender.recommend_content(items, count=count)
        
        print(f"✅ 推荐 {len(recommendations)} 篇文章")
        return recommendations
    
    def generate_briefing(self, recommendations: List[Dict], briefing_type: str = "daily") -> str:
        """生成简报"""
        print(f"生成{briefing_type}简报...")
        
        # 准备简报内容
        briefing_items = []
        for i, rec in enumerate(recommendations):
            content = rec.get("enhanced_content", rec.get("rewritten_content", rec.get("content", "")))
            briefing_items.append({
                "title": rec["title"],
                "content": content[:500],  # 限制长度
                "source": rec["source"],
                "score": rec.get("recommendation_score", 0.5)
            })
        
        # 生成简报
        briefing = self.deepseek.generate_briefing(briefing_items, briefing_type)
        
        if not briefing:
            # 备用方案
            briefing = self.generate_fallback_briefing(recommendations, briefing_type)
        
        print(f"✅ 简报生成完成 ({len(briefing)} 字符)")
        return briefing
    
    def generate_fallback_briefing(self, recommendations: List[Dict], briefing_type: str) -> str:
        """生成备用简报"""
        type_names = {
            "daily": "每日精选",
            "morning": "早安简报",
            "noon": "午间精选",
            "evening": "晚间回顾"
        }
        
        title = type_names.get(briefing_type, "精选简报")
        
        briefing = f"【一年365赢】{title}\n"
        briefing += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        briefing += "=" * 50 + "\n\n"
        
        for i, rec in enumerate(recommendations):
            briefing += f"{i+1}. **{rec['title']}**\n"
            briefing += f"   来源: {rec['source']}\n"
            
            content = rec.get("enhanced_content", rec.get("rewritten_content", rec.get("content", "")))
            summary = content[:200] + "..." if len(content) > 200 else content
            briefing += f"   摘要: {summary}\n\n"
        
        briefing += "=" * 50 + "\n"
        briefing += "❤️ 喜欢 | 👎 不喜欢 | 🔄 换一批\n"
        briefing += "#爱国 #正能量 #一年365赢"
        
        return briefing
    
    def save_output(self, recommendations: List[Dict], briefing: str, output_type: str = "daily"):
        """保存输出"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. 保存推荐内容
        rec_file = f"{self.output_dir}/recommendations_{timestamp}.json"
        with open(rec_file, 'w', encoding='utf-8') as f:
            json.dump(recommendations, f, ensure_ascii=False, indent=2)
        
        # 2. 保存简报
        brief_file = f"{self.output_dir}/briefing_{timestamp}.txt"
        with open(brief_file, 'w', encoding='utf-8') as f:
            f.write(briefing)
        
        # 3. 保存处理统计
        stats = {
            "timestamp": datetime.now().isoformat(),
            "output_type": output_type,
            "recommendations_count": len(recommendations),
            "briefing_length": len(briefing),
            "deepseek_requests": self.deepseek.request_count if hasattr(self.deepseek, 'request_count') else 0,
            "test_mode": self.test_mode
        }
        
        stats_file = f"{self.output_dir}/stats_{timestamp}.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print(f"💾 输出已保存:")
        print(f"   推荐内容: {rec_file}")
        print(f"   简报: {brief_file}")
        print(f"   统计: {stats_file}")
        
        return {
            "recommendations_file": rec_file,
            "briefing_file": brief_file,
            "stats_file": stats_file
        }
    
    def run_on_demand(self, output_type: str = "daily", use_cached: bool = True):
        """运行按需处理"""
        print(f"🚀 开始按需处理: {output_type}")
        print("=" * 60)
        
        start_time = datetime.now()
        
        try:
            # 1. 加载内容
            items = self.load_content_for_processing(use_cached=use_cached)
            
            if not items:
                print("❌ 没有可处理的内容，请先运行爬取任务")
                return None
            
            # 2. 处理内容
            processed_items = self.process_content(items)
            
            # 3. 生成推荐
            recommendations = self.generate_recommendations(processed_items, count=3)
            
            # 4. 生成简报
            briefing = self.generate_briefing(recommendations, output_type)
            
            # 5. 保存输出
            output_files = self.save_output(recommendations, briefing, output_type)
            
            # 6. 显示简报
            print("\n" + "=" * 60)
            print("📨 生成的简报:")
            print("=" * 60)
            print(briefing[:1000] + "..." if len(briefing) > 1000 else briefing)
            print("=" * 60)
            
            # 7. 统计信息
            duration = (datetime.now() - start_time).total_seconds()
            print(f"\n📊 处理统计:")
            print(f"   处理时间: {duration:.1f}秒")
            print(f"   处理文章: {len(processed_items)}篇")
            print(f"   推荐文章: {len(recommendations)}篇")
            print(f"   DeepSeek请求: {self.deepseek.request_count if hasattr(self.deepseek, 'request_count') else 'N/A'}次")
            print(f"   输出类型: {output_type}")
            
            return {
                "success": True,
                "briefing": briefing,
                "recommendations": recommendations,
                "output_files": output_files,
                "duration": duration,
                "processed_count": len(processed_items)
            }
            
        except Exception as e:
            print(f"❌ 处理失败: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="按需处理引擎")
    parser.add_argument("--type", choices=["daily", "morning", "noon", "evening"], 
                       default="daily", help="输出类型")
    parser.add_argument("--refresh", action="store_true", 
                       help="强制重新爬取（不使用缓存）")
    parser.add_argument("--api-key", help="DeepSeek API密钥")
    
    args = parser.parse_args()
    
    # 设置API密钥
    if args.api_key:
        os.environ["DEEPSEEK_API_KEY"] = args.api_key
    
    print("🎯 一年365赢 - 按需处理引擎")
    print("=" * 60)
    
    # 运行处理
    processor = OnDemandProcessor()
    result = processor.run_on_demand(
        output_type=args.type,
        use_cached=not args.refresh
    )
    
    if result and result.get("success"):
        print("\n" + "=" * 60)
        print("🎉 按需处理完成！")
        print(f"✨ 已生成爱国键盘侠风格的{args.type}简报")
        print("🇨🇳 一年365赢，天天都在赢！")
        print("=" * 60)
    else:
        print("\n❌ 处理失败")

if __name__ == "__main__":
    main()