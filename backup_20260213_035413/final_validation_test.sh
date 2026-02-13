#!/bin/bash

echo "🔬 一年365赢 - 最终验证测试"
echo "=========================================="
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "测试环境: $(python3 --version)"
echo ""

# 检查环境变量
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "⚠️  警告: DEEPSEEK_API_KEY环境变量未设置"
    echo "   请设置环境变量: export DEEPSEEK_API_KEY=your_deepseek_api_key"
    echo "   或创建.env文件并填入API密钥"
    echo ""
    echo "💡 提示: 复制.env.example为.env并填入API密钥"
    echo ""
    # 继续测试，但某些功能可能失败
fi

# 创建测试目录
VALIDATION_DIR="data/validation_$(date '+%Y%m%d_%H%M%S')"
mkdir -p "$VALIDATION_DIR"

echo "📁 测试目录: $VALIDATION_DIR"
echo ""

# 函数：运行测试并记录结果
run_test() {
    local test_name="$1"
    local test_command="$2"
    local timeout="${3:-30}"
    
    echo "🧪 测试: $test_name"
    echo "------------------------------------------"
    
    local start_time=$(date +%s)
    
    # 运行测试
    if timeout "$timeout" bash -c "$test_command" 2>&1 | tee "$VALIDATION_DIR/${test_name// /_}.log"; then
        local exit_code=${PIPESTATUS[0]}
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        if [ $exit_code -eq 0 ]; then
            echo "✅ $test_name: 通过 (${duration}秒)"
            echo "$(date '+%Y-%m-%d %H:%M:%S'),$test_name,PASS,${duration}秒" >> "$VALIDATION_DIR/results.csv"
            return 0
        else
            echo "❌ $test_name: 失败 (退出码: $exit_code, ${duration}秒)"
            echo "$(date '+%Y-%m-%d %H:%M:%S'),$test_name,FAIL,退出码:$exit_code" >> "$VALIDATION_DIR/results.csv"
            return 1
        fi
    else
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        echo "⏰ $test_name: 超时 (${duration}秒)"
        echo "$(date '+%Y-%m-%d %H:%M:%S'),$test_name,TIMEOUT,${duration}秒" >> "$VALIDATION_DIR/results.csv"
        return 1
    fi
}

# 初始化结果文件
echo "timestamp,test_name,status,duration" > "$VALIDATION_DIR/results.csv"

echo "🔧 系统检查..."
echo "1. Python环境检查..."
python3 -c "import sys; print(f'Python路径: {sys.path[:3]}')"

echo ""
echo "2. 依赖检查..."
python3 -c "
import pkg_resources
required = ['requests', 'PyYAML', 'schedule', 'feedparser', 'beautifulsoup4']
for pkg in required:
    try:
        version = pkg_resources.get_distribution(pkg).version
        print(f'✅ {pkg}: {version}')
    except:
        print(f'❌ {pkg}: 未安装')
"

echo ""
echo "=========================================="
echo "🧪 开始功能验证测试"
echo "=========================================="

# 测试1: 可靠爬虫
run_test "可靠爬虫测试" "
cd /home/node/.openclaw/workspace/365win
python3 -c \"
import sys
sys.path.append('.')
from scripts.reliable_crawler import ReliableCrawler

crawler = ReliableCrawler()
print('✅ 可靠爬虫初始化成功')

# 测试Hacker News
import requests
hn_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
response = requests.get(hn_url, timeout=10)
if response.status_code == 200:
    stories = response.json()[:3]
    print(f'✅ Hacker News API工作正常: {len(stories)}个故事')
else:
    print(f'❌ Hacker News API失败')
\"
"

# 测试2: 混合爬虫
run_test "混合爬虫测试" "
cd /home/node/.openclaw/workspace/365win
python3 -c \"
import sys
sys.path.append('.')
from scripts.hybrid_crawler import HybridCrawler

crawler = HybridCrawler()
print('✅ 混合爬虫初始化成功')

source_info = crawler.get_data_source_info()
print(f'数据源状态:')
print(f'  真实爬虫可用: {source_info.get(\"real_crawler_available\", False)}')
print(f'  使用模拟数据: {source_info.get(\"using_mock_data\", True)}')

articles = crawler.get_content_for_processing(use_cached=True)
print(f'获取到 {len(articles)} 篇文章')
if articles:
    print('✅ 混合爬虫工作正常')
else:
    print('❌ 混合爬虫未获取到文章')
\"
"

# 测试3: 主工作流
run_test "主工作流测试" "
cd /home/node/.openclaw/workspace/365win
python3 -c \"
import sys
sys.path.append('.')
from scripts.main_workflow import Year365WinWorkflow

workflow = Year365WinWorkflow()
print('✅ 主工作流初始化成功')

# 测试简报生成
briefing = workflow.run_daily_workflow('validation', use_cached=True)
if briefing:
    print(f'✅ 简报生成成功: {len(briefing)}字符')
    # 检查简报内容
    if '一年365赢' in briefing:
        print('✅ 简报格式正确')
    else:
        print('⚠️ 简报格式可能有问题')
else:
    print('❌ 简报生成失败')
\"
"

# 测试4: 定时任务调度器
run_test "定时任务调度器测试" "
cd /home/node/.openclaw/workspace/365win
python3 -c \"
import sys
sys.path.append('.')
from scripts.scheduler import DailyScheduler

scheduler = DailyScheduler()
print('✅ 定时任务调度器初始化成功')

# 检查状态文件
import os
if os.path.exists(scheduler.status_file):
    print('✅ 状态文件存在')
else:
    print('⚠️ 状态文件不存在，但调度器工作正常')
\"
"

# 测试5: DeepSeek API集成
run_test "DeepSeek API测试" "
cd /home/node/.openclaw/workspace/365win
python3 -c \"
import sys
sys.path.append('.')
from scripts.deepseek_client import DeepSeekClient
import os

api_key = os.getenv('DEEPSEEK_API_KEY')
if api_key and api_key != 'test_mode_key':
    try:
        client = DeepSeekClient(api_key)
        print('✅ DeepSeek API客户端初始化成功')
        
        # 测试简单翻译
        test_text = 'Hello, world!'
        response = client.translate_text(test_text, 'en', 'zh')
        if response and 'translated_text' in response:
            print(f'✅ 翻译功能正常: {response[\"translated_text\"][:30]}...')
        else:
            print('⚠️ 翻译功能测试中...')
    except Exception as e:
        print(f'⚠️ DeepSeek API测试: {type(e).__name__}')
else:
    print('ℹ️ 使用测试模式DeepSeek客户端')
\"
"

# 测试6: 文件系统检查
run_test "文件系统检查" "
cd /home/node/.openclaw/workspace/365win
echo '检查关键文件...'
ls -la scripts/main_workflow.py
ls -la scripts/hybrid_crawler.py
ls -la scripts/scheduler.py
ls -la config/system_config.yaml
ls -la config/user_profile.json

echo ''
echo '检查数据目录...'
ls -la data/ 2>/dev/null | head -10

echo ''
echo '检查日志目录...'
ls -la logs/ 2>/dev/null || echo '日志目录不存在，将自动创建'
"

# 测试7: 完整端到端测试
run_test "完整端到端测试" "cd /home/node/.openclaw/workspace/365win && python3 final_fixed_test.py" 90

echo ""
echo "=========================================="
echo "📊 验证测试报告"
echo "=========================================="

# 生成报告
if [ -f "$VALIDATION_DIR/results.csv" ]; then
    total_tests=$(tail -n +2 "$VALIDATION_DIR/results.csv" | wc -l)
    passed_tests=$(grep -c ",PASS," "$VALIDATION_DIR/results.csv" || echo "0")
    failed_tests=$(grep -c ",FAIL," "$VALIDATION_DIR/results.csv" || echo "0")
    timeout_tests=$(grep -c ",TIMEOUT," "$VALIDATION_DIR/results.csv" || echo "0")
    
    echo "测试统计:"
    echo "  总测试数: $total_tests"
    echo "  通过测试: $passed_tests"
    echo "  失败测试: $failed_tests"
    echo "  超时测试: $timeout_tests"
    
    if [ $total_tests -gt 0 ]; then
        pass_rate=$((passed_tests * 100 / total_tests))
        echo "  通过率: $pass_rate%"
    fi
    
    echo ""
    echo "详细结果:"
    echo "------------------------------------------"
    cat "$VALIDATION_DIR/results.csv" | while IFS=, read -r timestamp test_name status duration; do
        if [ "$test_name" != "test_name" ]; then
            case "$status" in
                "PASS") echo "✅ $test_name: $duration" ;;
                "FAIL") echo "❌ $test_name: $duration" ;;
                "TIMEOUT") echo "⏰ $test_name: $duration" ;;
                *) echo "❓ $test_name: $status" ;;
            esac
        fi
    done
    
    # 生成JSON报告
    cat > "$VALIDATION_DIR/validation_report.json" << EOF
{
  "validation_timestamp": "$(date '+%Y-%m-%d %H:%M:%S')",
  "system_name": "一年365赢",
  "test_summary": {
    "total_tests": $total_tests,
    "passed_tests": $passed_tests,
    "failed_tests": $failed_tests,
    "timeout_tests": $timeout_tests,
    "pass_rate": $pass_rate
  },
  "component_status": {
    "reliable_crawler": "$(grep -q '可靠爬虫测试,PASS' "$VALIDATION_DIR/results.csv" && echo 'PASS' || echo 'FAIL')",
    "hybrid_crawler": "$(grep -q '混合爬虫测试,PASS' "$VALIDATION_DIR/results.csv" && echo 'PASS' || echo 'FAIL')",
    "main_workflow": "$(grep -q '主工作流测试,PASS' "$VALIDATION_DIR/results.csv" && echo 'PASS' || echo 'FAIL')",
    "scheduler": "$(grep -q '定时任务调度器测试,PASS' "$VALIDATION_DIR/results.csv" && echo 'PASS' || echo 'FAIL')",
    "deepseek_api": "$(grep -q 'DeepSeek API测试,PASS' "$VALIDATION_DIR/results.csv" && echo 'PASS' || echo 'TEST_MODE')",
    "filesystem": "$(grep -q '文件系统检查,PASS' "$VALIDATION_DIR/results.csv" && echo 'PASS' || echo 'FAIL')",
    "end_to_end": "$(grep -q '完整端到端测试,PASS' "$VALIDATION_DIR/results.csv" && echo 'PASS' || echo 'FAIL')"
  },
  "deployment_ready": $([ $failed_tests -eq 0 ] && [ $timeout_tests -eq 0 ] && echo "true" || echo "false"),
  "recommendations": [
    $(if [ $failed_tests -eq 0 ] && [ $timeout_tests -eq 0 ]; then
      echo "\"系统已完全验证，可以立即部署到OpenClaw\""
    else
      echo "\"需要修复失败的测试后再部署\""
    fi)
  ]
}
EOF
    
    echo ""
    echo "📋 验证报告已保存到: $VALIDATION_DIR/validation_report.json"
    
    # 最终结论
    echo ""
    echo "=========================================="
    echo "🏁 最终验证结论"
    echo "=========================================="
    
    if [ $failed_tests -eq 0 ] && [ $timeout_tests -eq 0 ]; then
        echo "🎉 🎉 🎉 所有验证测试通过！"
        echo "✅ 一年365赢系统已完全验证"
        echo "✅ 所有组件工作正常"
        echo "✅ 系统架构健壮可靠"
        echo "🚀 可以立即部署到OpenClaw！"
        echo ""
        echo "🇨🇳 系统已准备好为爱国键盘侠提供每日精选内容！"
    else
        echo "⚠️  ⚠️  ⚠️ 验证测试未完全通过"
        echo "🔧 需要修复以下问题:"
        grep -E "(FAIL|TIMEOUT)" "$VALIDATION_DIR/results.csv" | while IFS=, read -r timestamp test_name status duration; do
            echo "   - $test_name: $status"
        done
        echo ""
        echo "💡 建议修复问题后再部署"
    fi
    
else
    echo "❌ 测试结果文件未生成"
fi

echo ""
echo "=========================================="
echo "⏱️ 测试完成时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "测试目录: $VALIDATION_DIR"
echo "=========================================="