#!/usr/bin/env python3
# 混合爬虫 - 真实爬取 + 高质量模拟数据

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib

class HybridCrawler:
    """混合爬虫：真实爬取失败时使用高质量模拟数据"""
    
    def __init__(self, storage_dir: str = "data/hybrid_content"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
        # 尝试导入可靠爬虫
        self.real_crawler = None
        try:
            from scripts.reliable_crawler import ReliableCrawler
            self.real_crawler = ReliableCrawler(storage_dir)
            print("✅ 可靠爬虫可用（Hacker News + RSS + 公开API）")
        except ImportError as e:
            print(f"⚠️ 无法导入可靠爬虫: {e}")
            print("将使用模拟数据")
        
        # 高质量模拟数据
        self.high_quality_mock_data = self.create_high_quality_mock_data()
        
        # 状态跟踪
        self.use_mock_data = False
        self.last_crawl_time = None
    
    def create_high_quality_mock_data(self) -> Dict[str, List[Dict]]:
        """创建高质量模拟数据"""
        current_time = datetime.now().isoformat()
        
        return {
            "foreign": [
                {
                    "url": "https://example.com/ai-breakthrough",
                    "title": "Major AI Breakthrough: New Model Achieves Human-Level Scientific Reasoning",
                    "content": """Researchers at leading international institutions have announced a significant breakthrough in artificial intelligence. The new model, named 'Cognitron-X', demonstrates human-level reasoning capabilities in complex scientific problems across multiple disciplines including medicine, materials science, and climate research.

The system was tested on 150 challenging scientific problems that typically require PhD-level expertise. Cognitron-X achieved 94% accuracy, matching or exceeding human expert performance in 85% of cases. This represents a major milestone in AI's ability to engage in genuine scientific discovery rather than just pattern recognition.

Key achievements include:
1. Predicting new pharmaceutical compounds with 30% higher efficacy than existing drugs
2. Discovering novel materials for energy storage with 50% improved capacity
3. Developing more accurate climate models that reduce prediction uncertainty by 40%

The research team emphasizes that this technology will accelerate scientific discovery across all fields, potentially reducing the time from hypothesis to breakthrough by years or even decades.""",
                    "source": "International Science Journal",
                    "language": "en",
                    "category": "tech",
                    "crawl_time": current_time,
                    "content_hash": hashlib.md5(b"ai-breakthrough").hexdigest()[:16]
                },
                {
                    "url": "https://example.com/space-exploration",
                    "title": "International Space Agencies Unveil Ambitious Mars Exploration Roadmap",
                    "content": """NASA, ESA, and international partners have announced a comprehensive roadmap for Mars exploration over the next decade. The plan includes multiple robotic missions, technology demonstrations, and preparations for eventual human exploration.

Key missions in the roadmap:
1. Mars Sample Return (2028): First-ever return of Martian soil and rock samples to Earth
2. Ice Mapper Orbiter (2029): Global mapping of subsurface water ice for future human missions
3. Mars Ascent Vehicle Test (2030): Demonstration of rocket launch from Martian surface
4. Human Landing Site Reconnaissance (2031): Detailed survey of potential human landing sites

The agencies emphasized that international cooperation is essential for these ambitious goals. "Mars represents the next great frontier for humanity," said the mission director. "The scientific knowledge gained will not only help us understand our planetary neighbor but also provide insights into Earth's past and future."

The roadmap also includes significant technology development in areas such as in-situ resource utilization, radiation protection, and closed-loop life support systems essential for sustained human presence.""",
                    "source": "Space Exploration Quarterly",
                    "language": "en",
                    "category": "tech",
                    "crawl_time": current_time,
                    "content_hash": hashlib.md5(b"mars-exploration").hexdigest()[:16]
                }
            ],
            "chinese": [
                {
                    "url": "https://example.com/china-tech-advance",
                    "title": "中国科技创新实现系列重大突破，人工智能量子计算等领域引领全球发展",
                    "content": """我国科研人员在人工智能、量子计算、生物技术等领域取得一系列重要进展，多项核心技术实现自主可控。最新发布的科技统计数据显示，中国在全球创新指数排名持续上升，科技创新对经济增长贡献率超过60%。

在人工智能领域，我国自主研发的"悟道3.0"大模型在多项国际基准测试中取得领先成绩。该模型在自然语言理解、代码生成、科学推理等方面表现优异，部分能力已达到或超过国际先进水平。

量子计算方面，我国科研团队成功研制出"九章三号"量子计算原型机，在处理特定复杂问题时，其运算速度比当前全球最快的超级计算机快亿亿倍。这一突破标志着我国在量子科技领域实现从"并跑"到"领跑"的历史性跨越。

生物技术领域同样成果丰硕。我国科学家在基因编辑、合成生物学、脑科学等方面取得重要进展，多项研究成果发表于国际顶级学术期刊。特别是在疫苗研发和重大疾病治疗方面，中国方案为全球公共卫生事业作出重要贡献。

专家表示，这些成就的取得得益于我国持续加大研发投入、完善创新体系、培养高水平人才队伍。未来，中国将继续深化科技体制改革，加强基础研究和原始创新，为世界科技发展贡献更多中国智慧和中国方案。""",
                    "source": "科技日报",
                    "language": "zh",
                    "category": "tech",
                    "crawl_time": current_time,
                    "content_hash": hashlib.md5(b"china-tech").hexdigest()[:16]
                },
                {
                    "url": "https://example.com/china-economy-growth",
                    "title": "中国经济展现强大韧性，高质量发展取得新成效市场信心持续增强",
                    "content": """国家统计局最新数据显示，我国经济在复杂国际环境下保持稳定增长，消费、投资、出口三大需求协同发力。上半年GDP同比增长6.3%，高技术制造业投资增长15.2%，经济结构持续优化，高质量发展根基更加稳固。

具体来看，我国经济发展呈现以下亮点：
1. 产业结构持续优化：高技术制造业增加值同比增长9.6%，快于全部规模以上工业3.8个百分点
2. 消费市场稳步恢复：社会消费品零售总额同比增长7.2%，服务消费快速增长
3. 外贸结构不断改善：机电产品出口增长8.6%，占出口总额比重提升至58.8%
4. 创新动能持续增强：研发经费投入强度达到2.64%，接近发达国家水平

专家分析指出，中国经济能够保持稳定增长，主要得益于以下几个因素：
- 完整的产业体系和完善的基础设施
- 超大规模的市场优势和内需潜力
- 持续优化的营商环境和改革开放
- 有效的宏观政策调控和风险防控

展望未来，我国将继续坚持稳中求进工作总基调，完整、准确、全面贯彻新发展理念，加快构建新发展格局，着力推动高质量发展。通过深化改革开放、优化经济结构、增强创新动力，中国经济将继续为世界经济复苏和增长作出重要贡献。""",
                    "source": "人民日报",
                    "language": "zh",
                    "category": "economy",
                    "crawl_time": current_time,
                    "content_hash": hashlib.md5(b"china-economy").hexdigest()[:16]
                }
            ]
        }
    
    def try_real_crawl(self) -> Optional[Dict[str, List[Dict]]]:
        """尝试真实爬取"""
        if not self.real_crawler:
            return None
        
        try:
            print("尝试真实爬取...")
            result = self.real_crawler.daily_crawl()
            
            # 检查爬取结果是否有效
            total_articles = len(result["foreign"]) + len(result["chinese"])
            
            if total_articles > 0:
                self.use_mock_data = False
                self.last_crawl_time = datetime.now()
                print(f"✅ 真实爬取成功: {len(result['foreign'])}外文 + {len(result['chinese'])}中文")
                return result
            else:
                print("⚠️ 真实爬取返回0篇文章，使用模拟数据")
                self.use_mock_data = True
                return None
            
        except Exception as e:
            print(f"⚠️ 真实爬取失败: {e}")
            print("将使用高质量模拟数据")
            self.use_mock_data = True
            return None
    
    def load_or_crawl(self, use_cached: bool = True) -> Dict[str, List[Dict]]:
        """加载或爬取数据"""
        
        # 如果要求使用缓存且真实爬虫可用
        if use_cached and self.real_crawler:
            try:
                articles = self.real_crawler.load_recent_data(days=3)
                if articles:
                    # 转换为标准格式
                    result = {"foreign": [], "chinese": []}
                    for article in articles:
                        if article["language"] == "en":
                            result["foreign"].append(article)
                        else:
                            result["chinese"].append(article)
                    
                    if result["foreign"] or result["chinese"]:
                        print(f"✅ 从缓存加载: {len(result['foreign'])}外文 + {len(result['chinese'])}中文")
                        self.use_mock_data = False
                        return result
            except Exception as e:
                print(f"⚠️ 加载缓存失败: {e}")
        
        # 如果没有缓存数据，尝试真实爬取
        real_result = self.try_real_crawl()
        if real_result:
            return real_result
        
        # 如果真实爬取失败，使用模拟数据
        print("使用高质量模拟数据")
        self.use_mock_data = True
        return self.high_quality_mock_data
    
    def get_content_for_processing(self, use_cached: bool = True) -> List[Dict]:
        """获取用于处理的内容"""
        # 加载数据
        data = self.load_or_crawl(use_cached)
        
        # 标记需要翻译的文章
        all_articles = []
        for article in data["foreign"]:
            article["needs_translation"] = True
            article["original_language"] = "en"
            all_articles.append(article)
        
        for article in data["chinese"]:
            article["needs_translation"] = False
            article["original_language"] = "zh"
            all_articles.append(article)
        
        # 混合比例：70%外文，30%中文
        foreign_articles = [a for a in all_articles if a["needs_translation"]]
        chinese_articles = [a for a in all_articles if not a["needs_translation"]]
        
        total_needed = min(10, len(all_articles))
        foreign_target = int(total_needed * 0.7)
        chinese_target = total_needed - foreign_target
        
        selected_foreign = foreign_articles[:min(foreign_target, len(foreign_articles))]
        selected_chinese = chinese_articles[:min(chinese_target, len(chinese_articles))]
        
        result = selected_foreign + selected_chinese
        
        data_source = "模拟数据" if self.use_mock_data else "真实爬取"
        print(f"准备处理 ({data_source}): {len(selected_foreign)}外文 + {len(selected_chinese)}中文 = {len(result)}篇")
        
        return result
    
    def get_data_source_info(self) -> Dict:
        """获取数据源信息"""
        return {
            "using_mock_data": self.use_mock_data,
            "real_crawler_available": self.real_crawler is not None,
            "last_crawl_time": self.last_crawl_time.isoformat() if self.last_crawl_time else None,
            "mock_data_quality": "high",
            "total_mock_articles": len(self.high_quality_mock_data["foreign"]) + len(self.high_quality_mock_data["chinese"])
        }

# 测试函数
if __name__ == "__main__":
    print("测试混合爬虫...")
    crawler = HybridCrawler()
    
    # 获取处理内容
    articles = crawler.get_content_for_processing(use_cached=True)
    
    print(f"\n获取到 {len(articles)} 篇文章:")
    for i, article in enumerate(articles):
        lang = "外文" if article["needs_translation"] else "中文"
        data_source = "模拟" if crawler.use_mock_data else "真实"
        print(f"{i+1}. [{data_source}][{lang}][{article['source']}] {article['title'][:50]}...")
        print(f"   内容长度: {len(article['content'])} 字符")
        print(f"   摘要: {article['content'][:100]}...")
        print()