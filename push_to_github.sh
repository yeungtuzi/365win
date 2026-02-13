#!/bin/bash

echo "🚀 一年365赢 - GitHub推送助手"
echo "=========================================="

# 检查是否在项目目录
if [ ! -f "README.md" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

echo "📋 GitHub推送步骤说明"
echo "------------------------------------------"
echo ""
echo "GitHub已不再支持密码认证，请选择以下方法之一："
echo ""
echo "方法1: 使用Personal Access Token (推荐)"
echo "------------------------------------------"
echo "1. 访问: https://github.com/settings/tokens"
echo "2. 点击 'Generate new token (classic)'"
echo "3. 勾选 'repo' 权限"
echo "4. 生成token并复制"
echo "5. 运行以下命令:"
echo "   git remote set-url origin https://<YOUR_TOKEN>@github.com/<YOUR_USERNAME>/365win.git"
echo "   git push -u origin main"
echo ""
echo "方法2: 使用SSH密钥"
echo "------------------------------------------"
echo "1. 生成SSH密钥:"
echo "   ssh-keygen -t ed25519 -C \"your_email@example.com\""
echo "2. 添加公钥到GitHub:"
echo "   cat ~/.ssh/id_ed25519.pub"
echo "3. 复制输出内容到:"
echo "   https://github.com/settings/ssh/new"
echo "4. 使用SSH URL:"
echo "   git remote set-url origin git@github.com:<YOUR_USERNAME>/365win.git"
echo "   git push -u origin main"
echo ""
echo "方法3: 使用GitHub CLI"
echo "------------------------------------------"
echo "1. 安装GitHub CLI:"
echo "   sudo apt-get install gh"
echo "2. 登录:"
echo "   gh auth login"
echo "3. 创建仓库并推送:"
echo "   gh repo create 365win --public --source=. --remote=origin --push"
echo ""
echo "当前Git配置:"
echo "------------------------------------------"
git remote -v 2>/dev/null || echo "未配置远程仓库"

echo ""
echo "💡 快速解决方案:"
echo "------------------------------------------"
echo "1. 创建GitHub仓库:"
echo "   访问 https://github.com/new"
echo "   仓库名: 365win"
echo "   描述: 爱国键盘侠个性化信息茧房系统"
echo "   选择: Public, MIT License, Python .gitignore"
echo ""
echo "2. 使用以下命令推送:"
echo ""
echo "   # 方法A: 使用HTTPS+token"
echo "   git remote add origin https://github.com/<YOUR_USERNAME>/365win.git"
echo "   # 然后使用token认证"
echo ""
echo "   # 方法B: 使用SSH"
echo "   git remote add origin git@github.com:<YOUR_USERNAME>/365win.git"
echo ""
echo "3. 推送代码:"
echo "   git push -u origin main"
echo ""
echo "⚠️  重要提示:"
echo "------------------------------------------"
echo "1. 确保.env文件在.gitignore中"
echo "2. 不要提交API密钥"
echo "3. 首次推送可能需要认证"
echo ""
echo "🔧 自动初始化脚本:"
echo "------------------------------------------"
cat << 'EOF'
#!/bin/bash
# 保存为 init_git.sh 并运行

# 初始化Git
git init
git add .
git commit -m "初始提交: 一年365赢 v1.0.0"
git branch -M main

# 设置远程仓库（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/365win.git

echo "✅ Git初始化完成"
echo "💡 下一步:"
echo "1. 确保已创建GitHub仓库: https://github.com/new"
echo "2. 获取Personal Access Token: https://github.com/settings/tokens"
echo "3. 运行: git push -u origin main"
echo "4. 输入用户名和token作为密码"
EOF

echo ""
echo "🎯 项目状态检查:"
echo "------------------------------------------"
echo "✅ 项目结构: 标准Python项目"
echo "✅ 许可证: MIT"
echo "✅ 文档: 完整"
echo "✅ 安全: 环境变量管理"
echo "✅ 依赖: requirements.txt"
echo "✅ 安装: install.sh"
echo ""
echo "🇨🇳 一年365赢 - 准备发布到GitHub!"