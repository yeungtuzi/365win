#!/usr/bin/env python3
# 短链接生成器 - 使用TinyURL API

import requests
import json
import time

class ShortURLGenerator:
    """短链接生成器"""
    
    def __init__(self):
        self.tinyurl_api = "https://tinyurl.com/api-create.php"
        self.cache = {}  # 缓存已生成的短链接
        
    def generate_short_url(self, long_url: str) -> str:
        """生成短链接"""
        # 检查缓存
        if long_url in self.cache:
            return self.cache[long_url]
        
        try:
            # 使用TinyURL API生成短链接
            params = {'url': long_url}
            response = requests.get(self.tinyurl_api, params=params, timeout=10)
            
            if response.status_code == 200:
                short_url = response.text.strip()
                # 验证返回的是有效的URL
                if short_url.startswith('http'):
                    self.cache[long_url] = short_url
                    print(f"   🔗 生成短链接: {long_url[:50]}... → {short_url}")
                    return short_url
                else:
                    print(f"   ⚠️  API返回异常: {short_url}")
                    return long_url  # 返回原链接
            else:
                print(f"   ⚠️  API请求失败: HTTP {response.status_code}")
                return long_url  # 返回原链接
                
        except Exception as e:
            print(f"   ⚠️  短链接生成失败: {type(e).__name__}")
            return long_url  # 返回原链接
    
    def batch_generate(self, urls: list) -> dict:
        """批量生成短链接"""
        results = {}
        print(f"📦 批量生成 {len(urls)} 个短链接...")
        
        for i, url in enumerate(urls, 1):
            print(f"   [{i}/{len(urls)}] 处理: {url[:60]}...")
            short_url = self.generate_short_url(url)
            results[url] = short_url
            time.sleep(0.5)  # 避免请求过快
        
        print(f"✅ 完成 {len(results)} 个短链接生成")
        return results

# 测试函数
def test_short_url():
    """测试短链接生成"""
    generator = ShortURLGenerator()
    
    # 测试URL
    test_urls = [
        "https://www.freightwaves.com/news/yard-management-technology-moves-out-of-the-shadows-as-supply-chains-push-for-end-to-end-visibility",
        "https://www.timesofisrael.com/unpersuaded-by-netanyahu-trump-insists-on-going-jaw-to-jaw-with-iran-and-hamas/",
        "https://www.livemint.com/companies/why-does-google-need-to-borrow-money-for-100-years-11707780000000"
    ]
    
    print("🔗 测试短链接生成...")
    results = generator.batch_generate(test_urls)
    
    print("\n📊 测试结果:")
    for long_url, short_url in results.items():
        print(f"   {long_url[:40]}... → {short_url}")

if __name__ == "__main__":
    test_short_url()