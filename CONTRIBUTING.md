# 贡献指南

感谢您对"一年365赢"项目的关注！我们欢迎各种形式的贡献。

## 行为准则

本项目遵循贡献者公约行为准则。参与本项目即表示您同意遵守其条款。

## 如何贡献

### 1. 报告问题
- 使用GitHub Issues报告bug或提出功能建议
- 在创建issue前，请先搜索是否已有类似问题
- 提供清晰的问题描述和复现步骤

### 2. 提交代码
1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### 3. 代码规范
- 遵循PEP 8 Python代码规范
- 添加适当的注释和文档
- 编写单元测试
- 确保代码通过所有现有测试

### 4. 文档贡献
- 修正拼写错误
- 改进文档清晰度
- 添加使用示例
- 翻译文档

## 开发环境设置

### 1. 克隆仓库
```bash
git clone https://github.com/yourusername/365win.git
cd 365win
```

### 2. 设置环境
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入API密钥
# 需要DeepSeek API和gnews.io API密钥
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 运行测试
```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_crawler.py
```

## 项目结构

```
365win/
├── config/          # 配置文件
├── src/            # 源代码
├── tests/          # 测试代码
├── docs/           # 文档
├── scripts/        # 工具脚本
└── data/           # 数据文件（不提交到Git）
```

## 提交信息规范

使用约定式提交信息格式：
- `feat:` 新功能
- `fix:` bug修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具变动

示例：
```
feat: 添加gnews.io API集成
fix: 修复内容过滤逻辑错误
docs: 更新README安装说明
```

## 安全注意事项

- 永远不要在代码中硬编码API密钥
- 使用环境变量管理敏感信息
- 运行安全扫描：`gitleaks detect --source .`
- 确保.env文件在.gitignore中

## 代码审查流程

1. 所有Pull Request都需要通过代码审查
2. 至少需要一个维护者批准
3. 必须通过所有自动化测试
4. 代码覆盖率不能降低

## 联系方式

- GitHub Issues: 功能建议和bug报告
- 项目维护者: [你的GitHub用户名]
- 电子邮件: [你的电子邮件]

## 致谢

感谢所有为项目做出贡献的人！您的每一份贡献都让项目变得更好。

---

*本指南根据项目发展会持续更新。最后更新: 2026-02-13*