# 🎯 一年365赢 - 爱国键盘侠个性化信息茧房

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Issues](https://img.shields.io/github/issues/yourusername/365win)](https://github.com/yourusername/365win/issues)
[![GitHub Stars](https://img.shields.io/github/stars/yourusername/365win)](https://github.com/yourusername/365win/stargazers)

> **信息茧房不够舒适？那就自己织一个！**

一个为爱国键盘侠量身定制的个性化信息推送系统，每日提供符合用户偏好的精选内容，让你每天沉浸在正能量中。

## ✨ 特性

### 🎯 精准内容匹配
- **爱国情怀优先**: 自动筛选符合爱国价值观的内容
- **科技突破聚焦**: 重点关注中国科技成就和突破
- **宏大叙事强化**: 提供有深度的国家发展分析
- **负面内容过滤**: 自动过滤小清新、阴谋论、负面情绪内容

### 🔧 智能技术架构
- **多源数据采集**: 集成gnews.io、DeepSeek等优质数据源
- **智能内容处理**: AI驱动的翻译、摘要、风格优化
- **个性化推荐**: 基于用户反馈的动态学习系统
- **安全可靠**: 环境变量管理，无硬编码密钥

### ⏰ 便捷使用体验
- **一日三推**: 晨间、午间、晚间三次精选推送
- **多种部署**: 支持命令行、OpenClaw集成、独立运行
- **成本极低**: 月成本<20元，性价比超高
- **开源自由**: MIT许可证，可自由使用和修改

## 📦 快速开始

### 1. 安装
```bash
# 克隆项目
git clone https://github.com/yourusername/365win.git
cd 365win

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入你的API密钥
# 需要: DeepSeek API密钥和gnews.io API密钥
```

### 3. 使用
```bash
# 生成晨间简报
python -m src.cli morning

# 生成午间简报
python -m src.cli noon

# 生成晚间简报
python -m src.cli evening

# 测试系统
python -m src.cli test
```

## 🏗️ 项目结构

```
365win/
├── src/                    # 源代码
│   ├── __init__.py        # 包定义
│   ├── cli.py             # 命令行接口
│   ├── gnews_integrated_crawler.py  # 主爬虫
│   ├── deepseek_client.py           # DeepSeek客户端
│   ├── content_processor.py         # 内容处理器
│   ├── recommendation_engine.py     # 推荐引擎
│   ├── feedback_system.py           # 反馈系统
│   └── ... 其他模块
├── tests/                 # 测试代码
├── config/                # 配置文件
├── examples/              # 使用示例
├── docs/                  # 文档
├── data/                  # 数据目录（不提交）
├── logs/                  # 日志目录（不提交）
├── .github/               # GitHub配置
├── LICENSE               # MIT许可证
├── README.md             # 本文件
├── CONTRIBUTING.md       # 贡献指南
├── CODE_OF_CONDUCT.md    # 行为准则
├── setup.py              # 安装配置
├── requirements.txt      # 依赖列表
├── .env.example          # 环境变量模板
└── .gitignore           # Git忽略配置
```

## 🚀 高级功能

### OpenClaw集成
```bash
# 设置定时任务
openclaw cron add --name "365win_morning" \
  --schedule "0 8 * * *" \
  --command "cd /path/to/365win && python -m src.cli morning"
```

### 自定义配置
编辑 `config/` 目录下的配置文件：
- `news_crawler_config.yaml`: 新闻爬取配置
- `system_config.yaml`: 系统运行配置
- `user_profile.json`: 用户偏好配置

### 安全扫描
```bash
# 安装gitleaks
# 运行安全扫描
gitleaks detect --source . --no-git
```

## 🤝 贡献

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何开始。

## 📄 许可证

本项目基于 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢所有爱国键盘侠的灵感
- 感谢DeepSeek提供优秀的AI API
- 感谢gnews.io提供新闻数据
- 感谢OpenClaw提供部署平台

## 📞 支持

- 📖 查看 [文档](docs/)
- 🐛 报告 [问题](https://github.com/yourusername/365win/issues)
- 💡 提出 [功能请求](https://github.com/yourusername/365win/issues)
- ⭐ 给项目点个星！

---

**🇨🇳 一年365赢，天天都在赢！**