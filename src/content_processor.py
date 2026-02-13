#!/usr/bin/env python3
# 内容处理器

import os
import json
import time
import hashlib
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import re

class ContentProcessor:
    """内容处理引擎"""
    
    def __init__(self, deepseek_client, config_path: str):
        self.deepseek = deepseek_client
        self.config = self.load_config(config_path)
        self.cache_dir = "./cache"
        self.stats = {
            "processed": 0,
            "rewritten": 0,
            "filtered": 0,
            "passed": 0
        }
        
    def load_config(self, config_path: str) -> Dict:
        """加载配置"""
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def process_content_item(self, item: Dict) -> Optional[Dict]:
        """处理单个内容项"""
        
        self.stats["processed"] += 1
        
        # 1. 基础检查
        if not self.basic_checks(item):
            self.stats["filtered"] += 1
            return None
        
        # 2. 风格分析
        analysis = self.analyze_content(item)
        
        # 3. 决策处理
        if analysis["recommended_action"] == "filter":
            self.stats["filtered"] += 1
            return None
        
        # 4. 内容重写（如果需要）
        if analysis["recommended_action"] == "rewrite":
            rewritten = self.rewrite_content(item, analysis)
            if rewritten:
                item["content"] = rewritten
                item["was_rewritten"] = True
                item["original_style"] = analysis
                self.stats["rewritten"] += 1
            else:
                # 重写失败，根据严重程度决定
                if analysis.get("clickbait_score", 0) > 0.7:
                    self.stats["filtered"] += 1
                    return None
        
        # 5. 情感增强
        item = self.enhance_content(item)
        
        # 6. 质量评分
        item["quality_score"] = self.calculate_quality_score(item, analysis)
        
        self.stats["passed"] += 1
        return item
    
    def basic_checks(self, item: Dict) -> bool:
        """基础检查"""
        
        # 检查必要字段
        required_fields = ["content", "source"]
        for field in required_fields:
            if field not in item or not item[field]:
                return False
        
        # 检查黑名单关键词
        blacklist = self.config.get("content_sources", {}).get("exclude_keywords", [])
        content_text = f"{item.get('title', '')} {item.get('content', '')}"
        
        for keyword in blacklist:
            if keyword in content_text:
                print(f"过滤：包含黑名单关键词 '{keyword}'")
                return False
        
        # 检查长度（降低要求，特别是对于外文内容）
        content = item.get("content", "")
        if len(content) < 20:  # 降低到20字符
            print(f"过滤：内容过短 ({len(content)}字符)")
            return False
        
        # 对于外文内容，即使较短也先保留进行翻译
        if item.get("needs_translation", False) and len(content) < 50:
            print(f"外文内容较短 ({len(content)}字符)，但保留进行翻译")
            return True  # 仍然通过检查
        
        return True
    
    def analyze_content(self, item: Dict) -> Dict:
        """分析内容"""
        
        # 使用DeepSeek分析
        analysis = self.deepseek.analyze_content(item["content"])
        
        # 本地补充分析
        if "error" not in analysis:
            # 计算本地特征
            content_text = item["content"]
            
            # 检查emoji密度
            emoji_pattern = re.compile(
                "["
                "\U0001F600-\U0001F64F"  # 表情符号
                "\U0001F300-\U0001F5FF"  # 符号和象形文字
                "\U0001F680-\U0001F6FF"  # 交通和地图符号
                "\U0001F1E0-\U0001F1FF"  # 国旗
                "]+", 
                flags=re.UNICODE
            )
            emoji_count = len(emoji_pattern.findall(content_text))
            emoji_density = emoji_count / max(1, len(content_text))
            
            analysis["emoji_density"] = emoji_density
            
            # 检查标题党特征
            title = item.get("title", "")
            clickbait_patterns = [
                r"震惊", r"惊呆", r"吓尿", r"重磅", r"突发", 
                r"速看", r"竟然", r"原来", r"真相", r"秘密"
            ]
            
            clickbait_score = 0
            for pattern in clickbait_patterns:
                if re.search(pattern, title):
                    clickbait_score += 0.1
            
            analysis["clickbait_score"] = min(1.0, clickbait_score)
            
            # 决定处理方式
            if analysis.get("sentiment_score", 0) < -0.3:
                analysis["recommended_action"] = "filter"
            elif (analysis.get("clickbait_score", 0) > 0.5 or 
                  analysis.get("sensationalism", 0) > 0.6):
                analysis["recommended_action"] = "rewrite"
            else:
                analysis["recommended_action"] = "keep"
        
        return analysis
    
    def rewrite_content(self, item: Dict, analysis: Dict) -> Optional[str]:
        """重写内容"""
        
        # 检查缓存
        content_hash = self.hash_content(item["content"])
        cache_file = f"{self.cache_dir}/rewrite_{content_hash}.json"
        
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached = json.load(f)
                # 检查缓存是否过期（24小时）
                cache_time = datetime.fromisoformat(cached["timestamp"])
                if datetime.now() - cache_time < timedelta(hours=24):
                    return cached["content"]
        
        # 构建重写要求
        style_requirements = {
            "目标风格": "爱国键盘侠偏好",
            "情感倾向": "积极正面，增强爱国情怀",
            "语言风格": "理性冷静，用词精准",
            "结构要求": "逻辑清晰，重点突出",
            "禁止元素": "轻佻语气、夸张表达、网络流行语"
        }
        
        # 调用DeepSeek重写
        rewritten = self.deepseek.rewrite_content(item["content"], style_requirements)
        
        if rewritten:
            # 缓存结果
            os.makedirs(self.cache_dir, exist_ok=True)
            cache_data = {
                "original_hash": content_hash,
                "content": rewritten,
                "timestamp": datetime.now().isoformat(),
                "original_analysis": analysis
            }
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
        return rewritten
    
    def enhance_content(self, item: Dict) -> Dict:
        """增强内容情感"""
        
        content = item["content"]
        
        # 爱国关键词增强
        patriotic_patterns = {
            "中国": ["伟大的中国", "繁荣昌盛的中国"],
            "发展": ["蓬勃发展", "高质量发展"],
            "成就": ["辉煌成就", "举世瞩目的成就"],
            "技术": ["自主创新技术", "领先技术"],
            "突破": ["重大突破", "历史性突破"]
        }
        
        for pattern, replacements in patriotic_patterns.items():
            if pattern in content:
                # 随机选择一个增强词（简单实现）
                import random
                enhanced = random.choice(replacements)
                # 替换第一个出现的位置
                content = content.replace(pattern, enhanced, 1)
        
        item["content"] = content
        
        # 添加情感标签
        item["tags"] = item.get("tags", [])
        
        # 根据内容添加标签
        if "科技" in content or "技术" in content:
            item["tags"].append("科技")
        if "中国" in content or "国家" in content:
            item["tags"].append("爱国")
        if "突破" in content or "成就" in content:
            item["tags"].append("成就")
        
        return item
    
    def calculate_quality_score(self, item: Dict, analysis: Dict) -> float:
        """计算内容质量分数"""
        
        scores = {
            "爱国程度": analysis.get("patriotic_level", 0.5) * 0.3,
            "科技相关性": analysis.get("tech_relevance", 0.5) * 0.25,
            "正式程度": analysis.get("formality", 0.5) * 0.2,
            "情感正向": max(0, analysis.get("sentiment_score", 0)) * 0.15,
            "标题党惩罚": (1 - analysis.get("clickbait_score", 0)) * 0.1
        }
        
        total_score = sum(scores.values())
        
        # 重写内容加分
        if item.get("was_rewritten"):
            total_score = min(1.0, total_score * 1.1)
        
        return total_score
    
    def hash_content(self, text: str) -> str:
        """生成内容哈希"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def get_stats(self) -> Dict:
        """获取处理统计"""
        return self.stats.copy()


if __name__ == "__main__":
    # 测试代码
    from deepseek_client import DeepSeekClient
    
    # 需要先设置DEEPSEEK_API_KEY环境变量
    client = DeepSeekClient()
    processor = ContentProcessor(client, "../config/system_config.yaml")
    
    test_item = {
        "title": "中国科技取得新进展",
        "content": "近日，我国在人工智能领域取得重要突破，相关技术达到国际领先水平。",
        "source": "测试数据",
        "url": "https://example.com"
    }
    
    processed = processor.process_content_item(test_item)
    if processed:
        print("处理成功:", json.dumps(processed, ensure_ascii=False, indent=2))
    else:
        print("处理失败")
    
    print("处理统计:", processor.get_stats())