#!/usr/bin/env python3
# 反馈系统

import os
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import hashlib

class FeedbackSystem:
    """用户反馈系统"""
    
    def __init__(self, user_id: str, data_dir: str = "./data"):
        self.user_id = user_id
        self.data_dir = data_dir
        self.feedback_file = f"{data_dir}/feedback.json"
        self.user_model_file = f"{data_dir}/user_model.json"
        
        # 初始化数据
        self.feedback_data = self.load_feedback_data()
        self.user_model = self.load_user_model()
        
    def load_feedback_data(self) -> Dict:
        """加载反馈数据"""
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "user_id": self.user_id,
                "feedbacks": [],
                "statistics": {
                    "total_feedbacks": 0,
                    "likes": 0,
                    "dislikes": 0,
                    "refreshes": 0,
                    "last_updated": datetime.now().isoformat()
                }
            }
    
    def load_user_model(self) -> Dict:
        """加载用户模型"""
        if os.path.exists(self.user_model_file):
            with open(self.user_model_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "user_id": self.user_id,
                "preference_weights": {},
                "behavior_patterns": {},
                "comfort_levels": {},
                "last_updated": datetime.now().isoformat()
            }
    
    def save_feedback_data(self):
        """保存反馈数据"""
        os.makedirs(os.path.dirname(self.feedback_file), exist_ok=True)
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(self.feedback_data, f, ensure_ascii=False, indent=2)
    
    def save_user_model(self):
        """保存用户模型"""
        os.makedirs(os.path.dirname(self.user_model_file), exist_ok=True)
        with open(self.user_model_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_model, f, ensure_ascii=False, indent=2)
    
    def record_feedback(self, 
                       message_id: str, 
                       content_id: str, 
                       reaction_type: str,
                       content_info: Dict = None) -> Dict:
        """记录用户反馈"""
        
        feedback_id = self.generate_feedback_id()
        
        feedback_entry = {
            "id": feedback_id,
            "message_id": message_id,
            "content_id": content_id,
            "reaction": reaction_type,  # "like", "dislike", "refresh"
            "timestamp": datetime.now().isoformat(),
            "content_info": content_info or {},
            "context": {
                "time_of_day": self.get_time_of_day(),
                "day_of_week": datetime.now().strftime("%A")
            }
        }
        
        # 添加到反馈数据
        self.feedback_data["feedbacks"].append(feedback_entry)
        
        # 更新统计
        stats = self.feedback_data["statistics"]
        stats["total_feedbacks"] += 1
        
        if reaction_type == "like":
            stats["likes"] += 1
        elif reaction_type == "dislike":
            stats["dislikes"] += 1
        elif reaction_type == "refresh":
            stats["refreshes"] += 1
        
        stats["last_updated"] = datetime.now().isoformat()
        
        # 更新用户模型
        self.update_user_model(feedback_entry)
        
        # 保存数据
        self.save_feedback_data()
        self.save_user_model()
        
        return feedback_entry
    
    def generate_feedback_id(self) -> str:
        """生成反馈ID"""
        timestamp = int(time.time() * 1000)
        random_suffix = hashlib.md5(str(timestamp).encode()).hexdigest()[:8]
        return f"fb_{timestamp}_{random_suffix}"
    
    def get_time_of_day(self) -> str:
        """获取当前时间段"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        else:
            return "night"
    
    def update_user_model(self, feedback: Dict):
        """根据反馈更新用户模型"""
        
        reaction = feedback["reaction"]
        content_info = feedback.get("content_info", {})
        
        # 更新偏好权重
        if "topics" in content_info:
            for topic in content_info["topics"]:
                self.update_topic_weight(topic, reaction)
        
        # 更新风格偏好
        if "style_features" in content_info:
            self.update_style_preferences(content_info["style_features"], reaction)
        
        # 更新来源偏好
        if "source" in content_info:
            self.update_source_weight(content_info["source"], reaction)
        
        # 更新行为模式
        self.update_behavior_patterns(feedback)
        
        # 更新舒适度
        self.update_comfort_levels(feedback)
        
        self.user_model["last_updated"] = datetime.now().isoformat()
    
    def update_topic_weight(self, topic: str, reaction: str):
        """更新话题权重"""
        
        weights = self.user_model.setdefault("preference_weights", {}).setdefault("topics", {})
        current_weight = weights.get(topic, 0.5)
        
        if reaction == "like":
            new_weight = min(1.0, current_weight + 0.1)
        elif reaction == "dislike":
            new_weight = max(0.0, current_weight - 0.15)
        elif reaction == "refresh":
            new_weight = max(0.0, current_weight - 0.05)
        else:
            new_weight = current_weight
        
        weights[topic] = new_weight
    
    def update_style_preferences(self, style_features: Dict, reaction: str):
        """更新风格偏好"""
        
        prefs = self.user_model.setdefault("preference_weights", {}).setdefault("styles", {})
        
        for feature, value in style_features.items():
            if isinstance(value, (int, float)):
                current_pref = prefs.get(feature, 0.5)
                
                if reaction == "like":
                    # 向喜欢的风格靠近
                    adjustment = (value - current_pref) * 0.1
                    new_pref = current_pref + adjustment
                elif reaction == "dislike":
                    # 远离不喜欢的风格
                    adjustment = (current_pref - value) * 0.15
                    new_pref = current_pref + adjustment
                else:
                    new_pref = current_pref
                
                prefs[feature] = max(0.0, min(1.0, new_pref))
    
    def update_source_weight(self, source: str, reaction: str):
        """更新来源权重"""
        
        weights = self.user_model.setdefault("preference_weights", {}).setdefault("sources", {})
        current_weight = weights.get(source, 0.5)
        
        if reaction == "like":
            new_weight = min(1.0, current_weight + 0.08)
        elif reaction == "dislike":
            new_weight = max(0.1, current_weight - 0.12)
        else:
            new_weight = current_weight
        
        weights[source] = new_weight
    
    def update_behavior_patterns(self, feedback: Dict):
        """更新行为模式"""
        
        patterns = self.user_model.setdefault("behavior_patterns", {})
        
        # 时间模式
        time_of_day = feedback["context"]["time_of_day"]
        day_of_week = feedback["context"]["day_of_week"]
        reaction = feedback["reaction"]
        
        time_key = f"{day_of_day}_{time_of_day}"
        if reaction == "like":
            patterns.setdefault("preferred_times", {}).setdefault(time_key, 0)
            patterns["preferred_times"][time_key] += 1
        
        # 反应模式
        patterns.setdefault("reaction_patterns", {}).setdefault(reaction, 0)
        patterns["reaction_patterns"][reaction] += 1
        
        # 连续反馈模式
        self.update_consecutive_patterns(feedback)
    
    def update_consecutive_patterns(self, feedback: Dict):
        """更新连续反馈模式"""
        
        patterns = self.user_model.setdefault("behavior_patterns", {}).setdefault("consecutive", {})
        reaction = feedback["reaction"]
        
        # 获取最近几次反馈
        recent_feedbacks = self.get_recent_feedbacks(5)
        
        if recent_feedbacks:
            last_reaction = recent_feedbacks[-1]["reaction"]
            
            # 记录反应转换
            transition_key = f"{last_reaction}_to_{reaction}"
            patterns.setdefault("transitions", {}).setdefault(transition_key, 0)
            patterns["transitions"][transition_key] += 1
            
            # 记录连续相同反应
            if reaction == last_reaction:
                patterns.setdefault("streaks", {}).setdefault(reaction, 0)
                patterns["streaks"][reaction] += 1
            else:
                patterns["streaks"][reaction] = 1
    
    def update_comfort_levels(self, feedback: Dict):
        """更新舒适度水平"""
        
        comfort = self.user_model.setdefault("comfort_levels", {})
        reaction = feedback["reaction"]
        
        # 计算近期满意度
        recent_feedbacks = self.get_recent_feedbacks(20)
        if recent_feedbacks:
            likes = sum(1 for f in recent_feedbacks if f["reaction"] == "like")
            dislikes = sum(1 for f in recent_feedbacks if f["reaction"] == "dislike")
            refreshes = sum(1 for f in recent_feedbacks if f["reaction"] == "refresh")
            
            total = likes + dislikes + refreshes
            if total > 0:
                satisfaction = (likes * 1.0 + refreshes * 0.3 - dislikes * 1.5) / total
                comfort["recent_satisfaction"] = max(0.0, min(1.0, (satisfaction + 1) / 2))
        
        # 更新总体舒适度
        if "overall_comfort" not in comfort:
            comfort["overall_comfort"] = 0.7
        
        if reaction == "like":
            comfort["overall_comfort"] = min(1.0, comfort["overall_comfort"] + 0.02)
        elif reaction == "dislike":
            comfort["overall_comfort"] = max(0.0, comfort["overall_comfort"] - 0.05)
        elif reaction == "refresh":
            comfort["overall_comfort"] = max(0.0, comfort["overall_comfort"] - 0.01)
    
    def get_recent_feedbacks(self, count: int = 10) -> List[Dict]:
        """获取最近的反馈"""
        all_feedbacks = self.feedback_data.get("feedbacks", [])
        return all_feedbacks[-count:] if all_feedbacks else []
    
    def get_feedback_statistics(self) -> Dict:
        """获取反馈统计"""
        return self.feedback_data.get("statistics", {}).copy()
    
    def get_user_model_summary(self) -> Dict:
        """获取用户模型摘要"""
        
        summary = {
            "preferences": {},
            "behavior": {},
            "comfort": self.user_model.get("comfort_levels", {}).copy()
        }
        
        # 提取主要偏好
        pref_weights = self.user_model.get("preference_weights", {})
        
        # 最喜欢的话题（权重>0.7）
        topics = pref_weights.get("topics", {})
        favorite_topics = {k: v for k, v in topics.items() if v > 0.7}
        if favorite_topics:
            summary["preferences"]["favorite_topics"] = favorite_topics
        
        # 最讨厌的话题（权重<0.3）
        disliked_topics = {k: v for k, v in topics.items() if v < 0.3}
        if disliked_topics:
            summary["preferences"]["disliked_topics"] = disliked_topics
        
        # 行为模式
        behavior = self.user_model.get("behavior_patterns", {})
        if "reaction_patterns" in behavior:
            summary["behavior"]["reaction_distribution"] = behavior["reaction_patterns"]
        
        return summary
    
    def generate_insights(self) -> Dict:
        """生成用户洞察"""
        
        insights = {
            "satisfaction_trend": self.calculate_satisfaction_trend(),
            "preference_stability": self.calculate_preference_stability(),
            "optimal_times": self.find_optimal_times(),
            "improvement_suggestions": self.generate_suggestions()
        }
        
        return insights
    
    def calculate_satisfaction_trend(self) -> str:
        """计算满意度趋势"""
        
        recent_stats = self.get_feedback_statistics()
        total = recent_stats.get("total_feedbacks", 0)
        
        if total < 10:
            return "数据不足，请继续使用"
        
        like_ratio = recent_stats.get("likes", 0) / total
        dislike_ratio = recent_stats.get("dislikes", 0) / total
        
        if like_ratio > 0.7:
            return "高度满意，系统准确匹配您的偏好"
        elif like_ratio > 0.5:
            return "基本满意，部分内容需要优化"
        else:
            return "需要调整，请多使用反馈功能帮助系统学习"
    
    def calculate_preference_stability(self) -> float:
        """计算偏好稳定性"""
        
        # 简单实现：检查最近反馈的一致性
        recent_feedbacks = self.get_recent_feedbacks(10)
        if len(recent_feedbacks) < 5:
            return 0.5
        
        # 计算相同反应的比例
        reactions = [f["reaction"] for f in recent_feedbacks]
        from collections import Counter
        most_common_count = Counter(reactions).most_common(1)[0][1]
        
        return most_common_count / len(reactions)
    
    def find_optimal_times(self) -> List[str]:
        """找到最佳推送时间"""
        
        patterns = self.user_model.get("behavior_patterns", {})
        preferred_times = patterns.get("preferred_times", {})
        
        if not preferred_times:
            return ["08:00", "12:00", "20:00"]  # 默认时间
        
        # 找到反馈最多的时段
        sorted_times = sorted(preferred_times.items(), key=lambda x: x[1], reverse=True)
        optimal_times = [time for time, count in sorted_times[:3]]
        
        return optimal_times
    
    def generate_suggestions(self) -> List[str]:
        """生成改进建议"""
        
        suggestions = []
        comfort = self.user_model.get("comfort_levels", {})
        
        overall_comfort = comfort.get("overall_comfort", 0.7)
        
        if overall_comfort < 0.6:
            suggestions.append("系统检测到舒适度较低，请多使用'喜欢'功能标记满意内容")
        
        if overall_comfort > 0.9:
            suggestions.append("舒适度过高，系统将轻微增加内容多样性以避免信息茧房过厚")
        
        stats = self.get_feedback_statistics()
        if stats.get("refreshes", 0) > stats.get("total_feedbacks", 1) * 0.3:
            suggestions.append("您频繁使用'换一批'，系统将调整内容多样性")
        
        return suggestions


if __name__ == "__main__":
    # 测试代码
    feedback_system = FeedbackSystem("test_user", "./test_data")
    
    # 记录一些测试反馈
    test_feedbacks = [
        ("msg_001", "content_001", "like", {"topics": ["科技", "爱国"], "source": "人民日报"}),
        ("msg_002", "content_002", "dislike", {"topics": ["娱乐"], "source": "八卦媒体"}),
        ("msg_003", "content_003", "refresh", {"topics": ["经济"], "source": "财经网"}),
    ]
    
    for msg_id, content_id, reaction, content_info in test_feedbacks:
        feedback = feedback_system.record_feedback(msg_id, content_id, reaction, content_info)
        print(f"记录反馈：{reaction} - {content_info.get('topics', [])}")
    
    # 查看统计
    stats = feedback_system.get_feedback_statistics()
    print("\n反馈统计：", json.dumps(stats, ensure_ascii=False, indent=2))
    
    # 查看用户模型摘要
    summary = feedback_system.get_user_model_summary()
    print("\n用户模型摘要：", json.dumps(summary, ensure_ascii=False, indent=2))
    
    # 生成洞察
    insights = feedback_system.generate_insights()
    print("\n用户洞察：", json.dumps(insights, ensure_ascii=False, indent=2))