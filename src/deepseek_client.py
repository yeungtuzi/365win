#!/usr/bin/env python3
# DeepSeek API客户端

import os
import json
import time
import hashlib
from typing import Dict, List, Optional, Any
import requests
from datetime import datetime

class DeepSeekClient:
    """DeepSeek API客户端"""
    
    def __init__(self, api_key: str = None, base_url: str = "https://api.deepseek.com"):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DeepSeek API密钥未设置")
            
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json; charset=utf-8"
        }
        self.request_count = 0
        self.total_tokens = 0
        
    def call_api(self, 
                 prompt: str, 
                 system_prompt: str = None,
                 temperature: float = 0.3,
                 max_tokens: int = 2000,
                 retry_count: int = 3) -> Optional[str]:
        """调用DeepSeek API"""
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        for attempt in range(retry_count):
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                response.raise_for_status()
                
                result = response.json()
                self.request_count += 1
                
                # 记录token使用量
                if "usage" in result:
                    self.total_tokens += result["usage"]["total_tokens"]
                
                return result["choices"][0]["message"]["content"]
                
            except requests.exceptions.RequestException as e:
                if attempt == retry_count - 1:
                    print(f"DeepSeek API调用失败（尝试{retry_count}次）: {e}")
                    return None
                time.sleep(2 ** attempt)  # 指数退避
        
        return None
    
    def translate_content(self, text: str, target_lang: str = "zh") -> str:
        """翻译内容"""
        system_prompt = "你是一个专业的翻译助手，擅长将各种语言的内容准确翻译成中文。"
        prompt = f"请将以下内容翻译成{target_lang}，保持专业、准确的风格：\n\n{text}"
        return self.call_api(prompt, system_prompt, temperature=0.1)
    
    def rewrite_content(self, text: str, style_requirements: Dict) -> str:
        """重写内容为爱国键盘侠风格"""
        system_prompt = """你是一个专业的内容编辑，擅长将各种风格的内容重写为符合爱国键盘侠偏好的风格。
        
        重写要求：
        1. 语言风格：理性冷静、用词精准、逻辑清晰
        2. 情感处理：增强爱国情怀，转为积极正面表达
        3. 结构优化：确保段落分明，重点突出
        4. 语气调整：避免轻佻、夸张、网络流行语
        5. 信息保留：保留所有核心事实和信息点
        6. 爱国增强：适当添加爱国情感和民族自豪感"""
        
        requirements = self._format_style_requirements(style_requirements)
        prompt = f"""{requirements}

请重写以下内容：
{text}

重写后的内容："""
        
        return self.call_api(prompt, system_prompt, temperature=0.4)
    
    def analyze_content(self, text: str) -> Dict:
        """分析内容情感和风格"""
        system_prompt = """你是一个内容分析专家，擅长分析文本的情感倾向、风格特征和主题内容。
        请以JSON格式返回分析结果。"""
        
        prompt = f"""分析以下内容：

{text}

请以JSON格式返回分析结果，包含以下字段：
- sentiment_score: 情感分数（-1到1，负数为负面）
- patriotic_level: 爱国程度（0-1）
- tech_relevance: 科技相关性（0-1）
- formality: 正式程度（0-1）
- sensationalism: 煽情程度（0-1）
- clickbait_score: 标题党程度（0-1）
- main_topics: 主要话题列表
- recommended_action: 建议处理方式（keep/rewrite/filter）"""
        
        result = self.call_api(prompt, system_prompt, temperature=0.1)
        try:
            return json.loads(result)
        except:
            return {"error": "解析失败", "recommended_action": "keep"}
    
    def generate_briefing(self, content_items: List[Dict], briefing_type: str) -> str:
        """生成简报"""
        system_prompt = """你是一个专业的简报编辑，擅长将多个内容项组织成结构清晰、阅读流畅的简报。
        简报风格：积极正面、信息丰富、鼓舞人心。"""
        
        items_text = ""
        for i, item in enumerate(content_items, 1):
            items_text += f"{i}. {item.get('title', '无标题')}\n"
            items_text += f"   摘要：{item.get('summary', '无摘要')}\n"
            if item.get('url'):
                items_text += f"   链接：{item['url']}\n"
            items_text += "\n"
        
        prompt = f"""请根据以下内容项生成{briefing_type}简报：

{items_text}

简报要求：
1. 开头：吸引人的标题和简短引言
2. 主体：清晰列出每个内容项，突出亮点
3. 结尾：总结和积极展望
4. 风格：符合爱国键盘侠偏好，积极正面
5. 格式：使用适当的emoji和分段

请输出完整的简报内容："""
        
        return self.call_api(prompt, system_prompt, temperature=0.3)
    
    def _format_style_requirements(self, requirements: Dict) -> str:
        """格式化风格要求"""
        req_text = "风格要求：\n"
        for key, value in requirements.items():
            req_text += f"- {key}: {value}\n"
        return req_text
    
    def get_usage_stats(self) -> Dict:
        """获取使用统计"""
        return {
            "request_count": self.request_count,
            "total_tokens": self.total_tokens,
            "estimated_cost": self.total_tokens * 0.000002  # 估算成本
        }


if __name__ == "__main__":
    # 测试代码
    client = DeepSeekClient()
    
    # 测试翻译
    test_text = "China has made significant progress in technology development."
    translated = client.translate_content(test_text)
    print("翻译测试:", translated)
    
    # 测试分析
    analysis = client.analyze_content(translated)
    print("分析结果:", json.dumps(analysis, ensure_ascii=False, indent=2))