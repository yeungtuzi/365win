"""
一年365赢 - 爱国键盘侠个性化信息茧房系统

一个为爱国键盘侠量身定制的个性化信息推送系统，
每日提供符合用户偏好的精选内容。
"""

__version__ = "1.0.0"
__author__ = "大河马"
__description__ = "爱国键盘侠个性化信息茧房系统"

from .gnews_integrated_crawler import GNewsIntegratedCrawler
from .deepseek_client import DeepSeekClient
from .content_processor import ContentProcessor
from .recommendation_engine import RecommendationEngine
from .feedback_system import FeedbackSystem

__all__ = [
    "GNewsIntegratedCrawler",
    "DeepSeekClient", 
    "ContentProcessor",
    "RecommendationEngine",
    "FeedbackSystem",
]