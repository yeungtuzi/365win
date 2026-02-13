#!/bin/bash

echo "🚀 一年365赢 - 最终端到端测试"
echo "=========================================="
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
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
mkdir -p data/final_test_results
TEST_DIR="data/final_test_results"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

echo "📁 测试目录: $TEST_DIR"
echo ""

# 函数：记录测试结果
log_test_result() {
    local test_name="$1"
    local status="$2"
    local message="$3"
    
    echo "[$(date '+%H:%M:%S')] $test_name: $status - $message"
    
    # 保存到日志文件
    echo "$(date '+%Y-%m-%d %H:%M:%S'),$test_name,$status,$message" >> "$TEST_DIR/test_results_$TIMESTAMP.csv"
}

# 函数：运行Python测试
run_python_test() {
    local test_file="$1"
    local test_name="$2"
    
    echo ""
    echo "🧪 运行测试: $test_name"
    echo "------------------------------------------"
    
    if timeout 30 python3 "$test_file" 2>&1; then
        log_test_result "$test_name" "PASS" "测试成功完成"
        return 0
    else
        log_test_result "$test_name" "FAIL" "测试失败或超时"
        return 1
    fi
}

# 开始测试
echo "🔧 测试准备..."
echo "1. 检查Python环境..."
python3 --version
pip3 list | grep -E "(requests|schedule|PyYAML)"

echo ""
echo "2. 检查项目结构..."
ls -la scripts/

echo ""
echo "=========================================="
echo "🧪 开始功能测试"
echo "=========================================="

# 测试1: 混合爬虫
run_python_test "test_crawl_only.py" "混合爬虫测试"

# 测试2: 主工作流
echo ""
echo "🧪 运行测试: 主工作流测试"
echo "------------------------------------------"
if timeout 45 python3 -c "
import sys
sys.path.append('.')
from scripts.main_workflow import Year365WinWorkflow

workflow = Year365WinWorkflow()
print('✅ 主工作流初始化成功')

# 测试数据采集
raw_data = workflow.collect_sample_data('morning', use_cached=True)
print(f'✅ 采集到 {len(raw_data)} 条数据')

# 测试简报生成
briefing = workflow.run_daily_workflow('morning', use_cached=True)
if briefing:
    print(f'✅ 简报生成成功，长度: {len(briefing)} 字符')
    print('简报预览:')
    for line in briefing.split('\\n')[:5]:
        if line.strip():
            print(f'  {line[:80]}...')
else:
    print('❌ 简报生成失败')
" 2>&1; then
    log_test_result "主工作流测试" "PASS" "工作流测试成功"
else
    log_test_result "主工作流测试" "FAIL" "工作流测试失败"
fi

# 测试3: 定时任务调度器
echo ""
echo "🧪 运行测试: 定时任务调度器测试"
echo "------------------------------------------"
if timeout 30 python3 -c "
import sys
sys.path.append('.')
from scripts.scheduler import DailyScheduler

scheduler = DailyScheduler()
print('✅ 定时任务调度器初始化成功')

# 测试立即运行任务
print('测试立即运行爬取任务...')
scheduler.run_once('crawl')

# 检查状态文件
import os
if os.path.exists(scheduler.status_file):
    print('✅ 状态文件存在')
    import json
    with open(scheduler.status_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f'状态记录: {len(data.get(\"tasks\", {}))} 个任务')
else:
    print('⚠️ 状态文件不存在')
" 2>&1; then
    log_test_result "定时任务测试" "PASS" "调度器测试成功"
else
    log_test_result "定时任务测试" "FAIL" "调度器测试失败"
fi

# 测试4: 完整系统测试
echo ""
echo "🧪 运行测试: 完整系统测试"
echo "------------------------------------------"
if timeout 60 python3 "final_integration_test.py" 2>&1; then
    log_test_result "完整系统测试" "PASS" "系统集成测试成功"
else
    log_test_result "完整系统测试" "FAIL" "系统集成测试失败"
fi

# 测试5: 文件系统检查
echo ""
echo "📁 运行测试: 文件系统检查"
echo "------------------------------------------"
echo "检查数据目录:"
ls -la data/

echo ""
echo "检查缓存目录:"
ls -la cache/ 2>/dev/null || echo "缓存目录不存在"

echo ""
echo "检查日志目录:"
ls -la logs/ 2>/dev/null || echo "日志目录不存在"

# 检查关键文件
KEY_FILES=(
    "scripts/main_workflow.py"
    "scripts/hybrid_crawler.py"
    "scripts/scheduler.py"
    "config/system_config.yaml"
    "config/user_profile.json"
)

all_files_exist=true
for file in "${KEY_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 不存在"
        all_files_exist=false
    fi
done

if $all_files_exist; then
    log_test_result "文件系统检查" "PASS" "所有关键文件存在"
else
    log_test_result "文件系统检查" "FAIL" "部分关键文件缺失"
fi

# 生成测试报告
echo ""
echo "=========================================="
echo "📊 测试报告"
echo "=========================================="
echo "测试时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "测试目录: $TEST_DIR"
echo ""

# 统计测试结果
if [ -f "$TEST_DIR/test_results_$TIMESTAMP.csv" ]; then
    total_tests=$(wc -l < "$TEST_DIR/test_results_$TIMESTAMP.csv")
    passed_tests=$(grep -c ",PASS," "$TEST_DIR/test_results_$TIMESTAMP.csv" || echo "0")
    failed_tests=$(grep -c ",FAIL," "$TEST_DIR/test_results_$TIMESTAMP.csv" || echo "0")
    
    echo "测试统计:"
    echo "  总测试数: $total_tests"
    echo "  通过测试: $passed_tests"
    echo "  失败测试: $failed_tests"
    
    # 计算通过率
    if [ $total_tests -gt 0 ]; then
        pass_rate=$((passed_tests * 100 / total_tests))
        echo "  通过率: $pass_rate%"
    fi
    
    echo ""
    echo "详细结果:"
    cat "$TEST_DIR/test_results_$TIMESTAMP.csv"
    
    # 生成JSON格式报告
    cat > "$TEST_DIR/test_summary_$TIMESTAMP.json" << EOF
{
  "timestamp": "$(date '+%Y-%m-%d %H:%M:%S')",
  "test_run": "$TIMESTAMP",
  "total_tests": $total_tests,
  "passed_tests": $passed_tests,
  "failed_tests": $failed_tests,
  "pass_rate": $pass_rate,
  "system_ready": $([ $failed_tests -eq 0 ] && echo "true" || echo "false"),
  "recommendation": "$([ $failed_tests -eq 0 ] && echo "系统已就绪，可以部署" || echo "需要修复失败测试")"
}
EOF
    
    echo ""
    echo "📋 测试总结已保存到: $TEST_DIR/test_summary_$TIMESTAMP.json"
    
    if [ $failed_tests -eq 0 ]; then
        echo ""
        echo "🎉 🎉 🎉 所有测试通过！"
        echo "✅ 一年365赢系统已完全就绪"
        echo "🚀 可以开始部署到OpenClaw"
    else
        echo ""
        echo "⚠️  ⚠️  ⚠️ 有 $failed_tests 个测试失败"
        echo "🔧 需要修复失败测试后再部署"
    fi
else
    echo "❌ 测试结果文件未生成"
fi

echo ""
echo "=========================================="
echo "🏁 测试完成时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="