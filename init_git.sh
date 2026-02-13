#!/bin/bash

echo "🚀 一年365赢 - Git初始化脚本"
echo "=========================================="

# 检查是否在项目目录
if [ ! -f "README.md" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

echo "🔍 检查当前状态..."
if [ -d ".git" ]; then
    echo "✅ Git仓库已存在"
    git status --short
else
    echo "📁 初始化Git仓库..."
    git init
fi

echo ""
echo "📦 添加文件到Git..."
git add .

echo ""
echo "💾 提交更改..."
git commit -m "初始提交: 一年365赢 v1.0.0

- 爱国键盘侠个性化信息茧房系统
- 支持一日三推：晨间、午间、晚间简报
- 集成gnews.io和DeepSeek API
- 完整的安全配置和环境变量管理
- MIT开源许可证"

echo ""
echo "🌿 设置主分支..."
git branch -M main

echo ""
echo "🌐 远程仓库配置..."
echo "------------------------------------------"
echo "请选择远程仓库配置方式:"
echo ""
echo "1. HTTPS (需要Personal Access Token)"
echo "2. SSH (需要配置SSH密钥)"
echo "3. 手动配置"
echo ""
read -p "请选择 (1/2/3): " choice

case $choice in
    1)
        read -p "请输入GitHub用户名: " username
        git remote add origin "https://github.com/$username/365win.git"
        echo "✅ 已配置HTTPS远程仓库"
        echo "💡 推送时需要使用Personal Access Token作为密码"
        ;;
    2)
        read -p "请输入GitHub用户名: " username
        git remote add origin "git@github.com:$username/365win.git"
        echo "✅ 已配置SSH远程仓库"
        echo "💡 确保已配置SSH密钥到GitHub"
        ;;
    3)
        echo "📝 手动配置远程仓库:"
        read -p "请输入远程仓库URL: " remote_url
        git remote add origin "$remote_url"
        echo "✅ 已配置远程仓库: $remote_url"
        ;;
    *)
        echo "⚠️  未选择，跳过远程仓库配置"
        ;;
esac

echo ""
echo "📊 Git配置状态:"
echo "------------------------------------------"
git remote -v 2>/dev/null || echo "未配置远程仓库"

echo ""
echo "📋 推送说明:"
echo "=========================================="
echo ""
echo "如果使用HTTPS，推送命令:"
echo "  git push -u origin main"
echo ""
echo "如果遇到认证问题，请使用以下方法:"
echo ""
echo "方法A: 使用Personal Access Token"
echo "------------------------------------------"
echo "1. 访问: https://github.com/settings/tokens"
echo "2. 生成token (勾选repo权限)"
echo "3. 推送时:"
echo "   用户名: 你的GitHub用户名"
echo "   密码: 生成的token"
echo ""
echo "方法B: 配置SSH密钥"
echo "------------------------------------------"
echo "1. 生成SSH密钥:"
echo "   ssh-keygen -t ed25519 -C \"your_email@example.com\""
echo "2. 添加公钥到GitHub:"
echo "   cat ~/.ssh/id_ed25519.pub"
echo "3. 复制到: https://github.com/settings/ssh/new"
echo "4. 使用SSH URL:"
echo "   git remote set-url origin git@github.com:<用户名>/365win.git"
echo ""
echo "方法C: 使用GitHub CLI"
echo "------------------------------------------"
echo "1. 安装: sudo apt-get install gh"
echo "2. 登录: gh auth login"
echo "3. 创建仓库: gh repo create 365win --public --source=. --remote=origin --push"
echo ""
echo "🔧 验证配置:"
echo "------------------------------------------"
echo "运行以下命令验证:"
echo "  git config --list | grep -E \"user\.(name|email)\""
echo ""
echo "如果需要设置用户信息:"
echo "  git config user.name \"Your Name\""
echo "  git config user.email \"your.email@example.com\""
echo ""
echo "🎉 Git初始化完成!"
echo "=========================================="
echo ""
echo "💡 下一步:"
echo "1. 确保GitHub仓库已创建: https://github.com/new"
echo "2. 配置认证方式 (token或SSH)"
echo "3. 运行推送命令"
echo "4. 检查GitHub仓库"
echo ""
echo "🇨🇳 一年365赢 - 代码已准备就绪!"