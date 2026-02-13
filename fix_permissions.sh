#!/bin/bash

echo "🔧 一年365赢 - 权限修复脚本"
echo "=========================================="

# 检查当前目录
if [ ! -f "README.md" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

echo "🔍 检查当前权限..."
echo "项目目录: $(pwd)"
echo "当前用户: $(whoami)"
echo ""

# 检查.git目录
if [ -d ".git" ]; then
    echo "📁 检查.git目录权限..."
    git_owner=$(stat -c '%U:%G' .git 2>/dev/null || stat -f '%Su:%Sg' .git)
    echo "当前.git所有者: $git_owner"
    
    current_user=$(whoami)
    if [[ "$git_owner" != "$current_user:"* ]]; then
        echo "⚠️  警告: .git目录所有者不是当前用户"
        echo ""
        echo "💡 解决方案:"
        echo "1. 使用sudo修复权限:"
        echo "   sudo chown -R $(whoami):$(whoami) .git"
        echo ""
        echo "2. 或删除并重新初始化:"
        echo "   rm -rf .git"
        echo "   git init"
        echo "   git add ."
        echo "   git commit -m '初始提交'"
    else
        echo "✅ .git目录权限正常"
    fi
else
    echo "📁 没有.git目录，可以正常初始化"
fi

echo ""
echo "📋 文件权限检查..."
echo "------------------------------------------"

# 检查重要文件权限
important_files=("README.md" "LICENSE" "src/__init__.py" "config/user_profile.json")

for file in "${important_files[@]}"; do
    if [ -f "$file" ]; then
        perm=$(stat -c '%A %U:%G' "$file" 2>/dev/null || stat -f '%Sp %Su:%Sg' "$file")
        echo "  $file: $perm"
    fi
done

echo ""
echo "🔧 建议操作:"
echo "=========================================="
echo ""
echo "如果遇到权限问题，请执行以下步骤:"
echo ""
echo "步骤1: 修复.git目录权限"
echo "------------------------------------------"
echo "sudo chown -R $(whoami):$(whoami) .git"
echo ""
echo "步骤2: 修复整个项目权限"
echo "------------------------------------------"
echo "sudo chown -R $(whoami):$(whoami) ."
echo ""
echo "步骤3: 重新初始化Git（如果步骤1失败）"
echo "------------------------------------------"
echo "rm -rf .git"
echo "git init"
echo "git add ."
echo "git commit -m '初始提交: 一年365赢 v1.0.0'"
echo "git branch -M main"
echo ""
echo "步骤4: 配置远程仓库"
echo "------------------------------------------"
echo "git remote add origin https://github.com/<用户名>/365win.git"
echo "# 或使用SSH"
echo "git remote add origin git@github.com:<用户名>/365win.git"
echo ""
echo "步骤5: 推送代码"
echo "------------------------------------------"
echo "git push -u origin main"
echo "# 如果使用HTTPS，需要输入:"
echo "#   用户名: GitHub用户名"
echo "#   密码: Personal Access Token"
echo ""
echo "⚠️  重要提示:"
echo "------------------------------------------"
echo "1. 确保已创建GitHub仓库"
echo "2. 准备好Personal Access Token"
echo "3. 不要提交.env文件"
echo "4. 检查.gitignore配置"
echo ""
echo "📚 更多帮助:"
echo "------------------------------------------"
echo "查看详细指南: cat GITHUB_RELEASE_GUIDE.md | head -50"
echo "运行安装测试: ./install.sh"
echo "测试系统功能: python -m src.cli test"
echo ""
echo "🇨🇳 一年365赢 - 权限修复指南"