#!/usr/bin/env python3
# 推荐引擎

import os
import json
import math
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class RecommendationEngine:
    """智能推荐引擎"""
    
    def __init__(self, user_profile_path: str, deepseek_client):
        self.user_profile = self.load_user_profile(user_profile_path)
        self.deepseek = deepseek_client
        self.recommendation_history = []
        
    def load_user_profile(self, profile_path: str) -> Dict:
        """加载用户配置文件"""
        with open(profile_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def recommend_content(self, 
                         content_items: List[Dict], 
                         count: int = 3,
                         time_of_day: str = "morning") -> List[Dict]:
        """推荐内容"""
        
        if not content_items:
            return []
        
        # 为每个内容项评分
        scored_items = []
        for item in content_items:
            score = self.score_content(item, time_of_day)
            if score > 0:  # 只考虑正分内容
                item["recommendation_score"] = score
                scored_items.append(item)
        
        # 按分数排序
        scored_items.sort(key=lambda x: x["recommendation_score"], reverse=True)
        
        # 选择top N，考虑多样性
        selected = self.select_with_diversity(scored_items, count)
        
        # 记录推荐历史
        self.record_recommendation(selected, time_of_day)
        
        return selected
    
    def score_content(self, item: Dict, time_of_day: str) -> float:
        """计算内容推荐分数"""
        
        scores = {
            "topic_score": self.calculate_topic_score(item),
            "style_score": self.calculate_style_score(item),
            "source_score": self.calculate_source_score(item),
            "time_score": self.calculate_time_score(item, time_of_day),
            "freshness_score": self.calculate_freshness_score(item),
            "quality_score": item.get("quality_score", 0.5),
            "blacklist_penalty": self.calculate_blacklist_penalty(item)
        }
        
        # 权重配置
        weights = {
            "topic_score": 0.35,
            "style_score": 0.20,
            "source_score": 0.15,
            "time_score": 0.10,
            "freshness_score": 0.05,
            "quality_score": 0.15,
            "blacklist_penalty": -0.1  # 惩罚项
        }
        
        # 计算加权总分
        total_score = 0
        for key in scores:
            total_score += scores[key] * weights[key]
        
        # 使用DeepSeek进行最终调整
        final_score = self.deepseek_adjustment(item, total_score)
        
        return max(0, min(1, final_score))  # 限制在0-1之间
    
    def calculate_topic_score(self, item: Dict) -> float:
        """计算话题匹配度"""
        
        item_topics = item.get("tags", [])
        if not item_topics:
            return 0.5  # 默认值
        
        user_topic_weights = self.user_profile["preferences"]["topic_weights"]
        
        # 计算最高的话题权重
        max_score = 0
        for topic in item_topics:
            score = user_topic_weights.get(topic, 0.5)
            max_score = max(max_score, score)
        
        return max_score
    
    def calculate_style_score(self, item: Dict) -> float:
        """计算风格匹配度"""
        
        # 从内容分析中获取风格特征
        style_features = item.get("original_style", {})
        if not style_features:
            return 0.5
        
        user_style_prefs = self.user_profile["preferences"]["style_preferences"]
        
        # 计算关键风格特征的匹配度
        style_scores = []
        
        # 爱国程度匹配
        patriotic_level = style_features.get("patriotic_level", 0.5)
        patriotic_pref = user_style_prefs.get("patriotic_tone", 0.8)
        patriotic_score = 1 - abs(patriotic_level - patriotic_pref)
        style_scores.append(patriotic_score * 0.4)
        
        # 正式程度匹配
        formality = style_features.get("formality", 0.5)
        formality_pref = user_style_prefs.get("formality", 0.8)
        formality_score = 1 - abs(formality - formality_pref)
        style_scores.append(formality_score * 0.3)
        
        # 情感程度匹配
        emotional = style_features.get("sentiment_score", 0)
        emotional_pref = user_style_prefs.get("emotional_level", 0.7)
        # 用户喜欢正面情感
        if emotional >= 0:
            emotional_score = 1 - abs(emotional - emotional_pref)
        else:
            emotional_score = 0.2  # 负面情感低分
        style_scores.append(emotional_score * 0.3)
        
        return sum(style_scores)
    
    def calculate_source_score(self, item: Dict) -> float:
        """计算来源可信度"""
        
        source = item.get("source", "")
        if not source:
            return 0.5
        
        source_weights = self.user_profile["preferences"]["source_weights"]
        
        # 尝试匹配来源类型
        source_type = self.classify_source(source)
        return source_weights.get(source_type, 0.5)
    
    def classify_source(self, source: str) -> str:
        """分类来源类型"""
        
        source_lower = source.lower()
        
        # 官方媒体
        official_keywords = ["人民", "新华", "央视", "求是", "学习强国"]
        for keyword in official_keywords:
            if keyword in source_lower:
                return "official_media"
        
        # 科技媒体
        tech_keywords = ["科技", "创新", "数码", "it", "人工智能"]
        for keyword in tech_keywords:
            if keyword in source_lower:
                return "tech_media"
        
        # 学术来源
        academic_keywords = ["大学", "学院", "研究", "科学", "学术"]
        for keyword in academic_keywords:
            if keyword in source_lower:
                return "academic"
        
        # 默认
        return "mainstream_media"
    
    def calculate_time_score(self, item: Dict, time_of_day: str) -> float:
        """计算时间匹配度"""
        
        time_prefs = self.user_profile["schedule_preferences"]
        preferred_types = time_prefs.get(time_of_day, [])
        
        # 简单实现：检查内容类型是否匹配时间偏好
        item_type = item.get("type", "general")
        if item_type in preferred_types:
            return 0.9
        else:
            return 0.5
    
    def calculate_freshness_score(self, item: Dict) -> float:
        """计算新鲜度"""
        
        publish_time = item.get("publish_time")
        if not publish_time:
            return 0.5
        
        try:
            # 解析发布时间
            if isinstance(publish_time, str):
                # 尝试解析ISO格式
                from datetime import datetime
                publish_dt = datetime.fromisoformat(publish_time.replace('Z', '+00:00'))
            else:
                # 假设是timestamp
                publish_dt = datetime.fromtimestamp(publish_time)
            
            # 计算时间差（小时）
            now = datetime.now()
            hours_diff = (now - publish_dt).total_seconds() / 3600
            
            # 新鲜度衰减：24小时内新鲜，之后衰减
            if hours_diff <= 24:
                return 1.0
            elif hours_diff <= 168:  # 一周内
                return 0.7
            else:
                return 0.3
                
        except:
            return 0.5
    
    def calculate_blacklist_penalty(self, item: Dict) -> float:
        """计算黑名单惩罚"""
        
        blacklists = self.user_profile["preferences"]["blacklists"]
        
        penalty = 0
        
        # 检查作者黑名单
        author = item.get("author", "")
        if author in blacklists["authors"]:
            penalty += 0.5
        
        # 检查媒体黑名单
        source = item.get("source", "")
        if source in blacklists["media"]:
            penalty += 0.3
        
        # 检查关键词黑名单
        content_text = f"{item.get('title', '')} {item.get('content', '')}"
        for keyword in blacklists["keywords"]:
            if keyword in content_text:
                penalty += 0.2
                break
        
        return penalty
    
    def deepseek_adjustment(self, item: Dict, base_score: float) -> float:
        """使用DeepSeek进行最终评分调整"""
        
        # 构建提示词
        user_prefs_summary = self.summarize_user_preferences()
        
        prompt = f"""基于用户历史偏好，评估以下内容是否适合推荐：

用户偏好摘要：
{user_prefs_summary}

内容信息：
标题：{item.get('title', '无标题')}
话题：{', '.join(item.get('tags', ['未分类']))}
质量分数：{item.get('quality_score', 0.5):.2%}
基础推荐分：{base_score:.2%}

请给出最终推荐分数（0-1），并简要说明理由："""

        response = self.deepseek.call_api(
            prompt, 
            system_prompt="你是一个推荐系统专家，擅长评估内容与用户偏好的匹配度。",
            temperature=0.2,
            max_tokens=500
        )
        
        if not response:
            return base_score
        
        # 尝试从响应中提取分数
        try:
            import re
            # 查找0-1之间的分数
            score_match = re.search(r'(\d+\.?\d*)\s*(分|/|score)', response, re.IGNORECASE)
            if score_match:
                score_str = score_match.group(1)
                score = float(score_str)
                
                # 归一化到0-1
                if score > 1:
                    score = score / 10 if score <= 10 else score / 100
                
                # 与基础分数加权平均
                final_score = base_score * 0.7 + score * 0.3
                return final_score
        except:
            pass
        
        return base_score
    
    def summarize_user_preferences(self) -> str:
        """总结用户偏好"""
        
        prefs = self.user_profile["preferences"]
        
        summary = f"""用户画像：爱国键盘侠
最喜欢的话题：{', '.join([k for k, v in prefs['topic_weights'].items() if v > 0.8])}
最讨厌的话题：{', '.join([k for k, v in prefs['topic_weights'].items() if v < 0.2])}
风格偏好：理性冷静、爱国情怀强、喜欢宏大叙事
情感倾向：积极正面，厌恶负面情绪
近期满意度：{self.user_profile['feedback_stats']['satisfaction_rate']:.1%}"""
        
        return summary
    
    def select_with_diversity(self, scored_items: List[Dict], count: int) -> List[Dict]:
        """考虑多样性的选择"""
        
        if len(scored_items) <= count:
            return scored_items
        
        selected = []
        selected_topics = set()
        
        for item in scored_items:
            if len(selected) >= count:
                break
            
            item_topics = set(item.get("tags", []))
            
            # 检查话题多样性
            if not selected_topics.intersection(item_topics):
                # 新话题，优先选择
                selected.append(item)
                selected_topics.update(item_topics)
            elif len(selected) < count * 0.7:
                # 允许部分重复话题
                selected.append(item)
            # 否则跳过，避免同质化
        
        # 如果选择不足，补充高分内容
        if len(selected) < count:
            for item in scored_items:
                if item not in selected:
                    selected.append(item)
                if len(selected) >= count:
                    break
        
        return selected[:count]
    
    def record_recommendation(self, items: List[Dict], time_of_day: str):
        """记录推荐历史"""
        
        recommendation = {
            "timestamp": datetime.now().isoformat(),
            "time_of_day": time_of_day,
            "items": [
                {
                    "id": item.get("id", "unknown"),
                    "title": item.get("title", ""),
                    "score": item.get("recommendation_score", 0),
                    "topics": item.get("tags", [])
                }
                for item in items
            ]
        }
        
        self.recommendation_history.append(recommendation)
        
        # 保持历史记录大小
        if len(self.recommendation_history) > 100:
            self.recommendation_history = self.recommendation_history[-100:]
    
    def update_from_feedback(self, feedback_data: Dict):
        """根据反馈更新推荐策略"""
        
        # 这里可以添加根据反馈调整权重的逻辑
        # 例如：如果用户频繁点赞某类内容，提高该类权重
        
        print(f"收到反馈：{feedback_data}")
        # 实际实现需要更复杂的逻辑


if __name__ == "__main__":
    # 测试代码
    from deepseek_client import DeepSeekClient
    
    # 需要先设置DEEPSEEK_API_KEY环境变量
    client = DeepSeekClient()
    engine = RecommendationEngine("../config/user_profile.json", client)
    
    test_items = [
        {
            "id": "1",
            "title": "中国人工智能技术取得突破",
            "content": "我国在AI领域实现重大进展...",
            "source": "科技日报",
            "tags": ["科技", "爱国"],
            "quality_score": 0.85,
            "type": "tech"
        },
        {
            "id": "2",
            "title": "一带一路建设成果显著",
            "content": "一带一路倡议取得丰硕成果...",
            "source": "人民日报",
            "tags": ["爱国", "经济"],
            "quality_score": 0.90,
            "type": "general"
        }
    ]
    
    recommendations = engine.recommend_content(test_items, count=2, time_of_day="morning")
    
    print("推荐结果：")
    for i, item in enumerate(recommendations, 1):
        print(f"{i}. {item['title']} (分数：{item.get('recommendation_score', 0):.2%})")