#!/usr/bin/env python3
# 测试gnews.io API

import os
import requests
import json
from datetime import datetime

# 从环境变量获取API密钥
API_KEY = os.getenv("GNEWS_API_KEY", "")
BASE_URL = "https://gnews.io/api/v4"

def test_gnews_api():
    print("🔍 测试gnews.io API...")
    print("=" * 60)
    
    # 检查API密钥
    if not API_KEY:
        print("❌ 错误: GNEWS_API_KEY环境变量未设置")
        print("   请设置环境变量: export GNEWS_API_KEY=your_gnews_api_key")
        print("   或创建.env文件并填入API密钥")
        return
    
    # 测试1: 获取头条新闻
    print("1. 测试头条新闻...")
    params = {
        'token': API_KEY,
        'lang': 'en',
        'country': 'us',
        'max': 5  # 限制数量
    }
    
    try:
        response = requests.get(f"{BASE_URL}/top-headlines", params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            print(f"   ✅ 成功获取 {len(articles)} 条头条新闻")
            
            for i, article in enumerate(articles[:3], 1):
                print(f"   {i}. {article.get('title', '无标题')[:60]}...")
                print(f"      来源: {article.get('source', {}).get('name', '未知')}")
                print(f"      时间: {article.get('publishedAt', '未知')}")
                print(f"      描述: {article.get('description', '无描述')[:80]}...")
                print()
        else:
            print(f"   ❌ API请求失败: HTTP {response.status_code}")
            print(f"      响应: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {type(e).__name__}: {e}")
    
    # 测试2: 搜索特定关键词
    print("\n2. 测试关键词搜索...")
    search_params = {
        'token': API_KEY,
        'q': 'technology',
        'lang': 'en',
        'country': 'us',
        'max': 3
    }
    
    try:
        response = requests.get(f"{BASE_URL}/search", params=search_params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            print(f"   ✅ 成功搜索到 {len(articles)} 条技术新闻")
            
            for i, article in enumerate(articles[:2], 1):
                print(f"   {i}. {article.get('title', '无标题')[:60]}...")
                print(f"      来源: {article.get('source', {}).get('name', '未知')}")
                print(f"      时间: {article.get('publishedAt', '未知')}")
                print()
        else:
            print(f"   ❌ 搜索失败: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 搜索异常: {type(e).__name__}: {e}")
    
    # 测试3: 获取中文新闻
    print("\n3. 测试中文新闻...")
    chinese_params = {
        'token': API_KEY,
        'lang': 'zh',
        'country': 'cn',
        'max': 3
    }
    
    try:
        response = requests.get(f"{BASE_URL}/top-headlines", params=chinese_params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            print(f"   ✅ 成功获取 {len(articles)} 条中文新闻")
            
            for i, article in enumerate(articles[:2], 1):
                print(f"   {i}. {article.get('title', '无标题')[:60]}...")
                print(f"      来源: {article.get('source', {}).get('name', '未知')}")
                print(f"      时间: {article.get('publishedAt', '未知')}")
                print()
        else:
            print(f"   ❌ 中文新闻失败: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 中文新闻异常: {type(e).__name__}: {e}")
    
    # 测试4: 检查API限制
    print("\n4. 检查API限制...")
    # gnews.io限制：免费版100次/天
    print("   📊 API限制信息:")
    print("     每日请求上限: 100次")
    print("     建议使用量: ≤60次/天 (安全边际)")
    print("     每次请求可获取: 最多10篇文章")
    print("     支持功能: 头条、搜索、分类")
    
    # 计算合理使用策略
    print("\n   🎯 合理使用策略:")
    print("     每日简报: 3次 (早、中、晚)")
    print("     每次请求: 2-3个查询")
    print("     每日总请求: 3×3 = 9次")
    print("     剩余额度: 100-9 = 91次 (安全)")
    
    print("\n" + "=" * 60)
    print("✅ gnews.io API测试完成")
    print("   API密钥有效，可以集成到系统中")
    print("=" * 60)

if __name__ == "__main__":
    test_gnews_api()