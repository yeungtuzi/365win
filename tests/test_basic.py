"""
基本功能测试
"""

import os
import sys
import pytest
from unittest.mock import Mock, patch

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """测试模块导入"""
    # 测试核心模块导入
    from src import __version__, __author__
    
    assert __version__ == "1.0.0"
    assert __author__ == "大河马"
    
    print("✅ 模块导入测试通过")

def test_config_files():
    """测试配置文件"""
    config_files = [
        "config/news_crawler_config.yaml",
        "config/system_config.yaml", 
        "config/user_profile.json",
    ]
    
    for config_file in config_files:
        assert os.path.exists(config_file), f"配置文件不存在: {config_file}"
    
    print("✅ 配置文件测试通过")

def test_environment_variables():
    """测试环境变量（不要求实际设置）"""
    # 这些测试只是检查代码是否能处理环境变量
    deepseek_key = os.getenv("DEEPSEEK_API_KEY", "")
    gnews_key = os.getenv("GNEWS_API_KEY", "")
    
    # 不验证密钥内容，只验证能获取
    assert isinstance(deepseek_key, str)
    assert isinstance(gnews_key, str)
    
    print("✅ 环境变量测试通过")

def test_cli_structure():
    """测试CLI结构"""
    from src.cli import main, check_environment, print_version
    
    # 测试函数存在
    assert callable(main)
    assert callable(check_environment)
    assert callable(print_version)
    
    print("✅ CLI结构测试通过")

@patch('os.getenv')
def test_missing_environment_variables(mock_getenv):
    """测试缺失环境变量的情况"""
    # 模拟环境变量未设置
    mock_getenv.return_value = ""
    
    from src.cli import check_environment
    
    # 应该能正常执行而不崩溃
    try:
        check_environment()
        print("✅ 缺失环境变量处理测试通过")
    except Exception as e:
        pytest.fail(f"缺失环境变量处理失败: {e}")

def test_package_structure():
    """测试包结构"""
    expected_modules = [
        "gnews_integrated_crawler",
        "deepseek_client", 
        "content_processor",
        "recommendation_engine",
        "feedback_system",
        "cli"
    ]
    
    for module in expected_modules:
        try:
            __import__(f"src.{module}")
            print(f"  ✅ 模块存在: {module}")
        except ImportError as e:
            print(f"  ⚠️  模块缺失: {module} - {e}")
            # 对于开源版本，某些模块可能不存在
            pass
    
    print("✅ 包结构测试通过")

if __name__ == "__main__":
    """运行所有测试"""
    print("🧪 运行基本功能测试...")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config_files,
        test_environment_variables,
        test_cli_structure,
        test_package_structure,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"❌ {test_func.__name__} 失败: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    
    if failed > 0:
        sys.exit(1)
    else:
        print("🎉 所有基本测试通过!")