#!/bin/bash

echo "🚀 一年365赢 - 安装脚本"
echo "=========================================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: Python3未安装"
    echo "   请安装Python3.9或更高版本"
    exit 1
fi

echo "✅ Python版本: $(python3 --version)"

# 安装依赖
echo ""
echo "📦 安装依赖..."
pip3 install -r requirements.txt

# 创建目录结构
echo ""
echo "📁 创建目录结构..."
mkdir -p data logs

# 设置环境变量
echo ""
echo "⚙️  环境变量设置..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ 已创建 .env 文件"
        echo ""
        echo "⚠️  重要: 请编辑 .env 文件，填入你的API密钥:"
        echo "   DEEPSEEK_API_KEY=your_deepseek_api_key_here"
        echo "   GNEWS_API_KEY=your_gnews_api_key_here"
    else
        echo "❌ 错误: .env.example 文件不存在"
        exit 1
    fi
else
    echo "✅ .env 文件已存在"
fi

# 运行测试
echo ""
echo "🧪 运行基本测试..."
python3 tests/test_basic.py

echo ""
echo "=========================================="
echo "🎉 安装完成！"
echo "=========================================="
echo ""
echo "💡 下一步:"
echo "1. 编辑 .env 文件，填入API密钥"
echo "2. 测试系统: python -m src.cli test"
echo "3. 生成简报: python -m src.cli morning"
echo "4. 查看示例: python examples/basic_usage.py"
echo ""
echo "🇨🇳 一年365赢，准备开始赢！"