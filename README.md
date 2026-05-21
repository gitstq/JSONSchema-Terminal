# 🎯 SchemaPilot

**Lightweight JSON Schema Terminal Visualizer & Validator**

**轻量级JSON Schema终端可视化与验证工具**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-0-orange)](setup.py)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-black)](https://github.com/psf/black)

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

---

## English

### 🎉 Introduction

SchemaPilot is a **zero-dependency** CLI tool that brings JSON Schema visualization and validation directly to your terminal. No more switching between browser tabs or dealing with heavy GUI applications—understand, validate, and compare your JSON Schemas with beautiful terminal output.

**Why SchemaPilot?**
- 🚀 **Zero Dependencies**: Uses only Python standard library
- 🎨 **Beautiful Terminal UI**: Color-coded tree visualization with type icons
- ✅ **Full Draft 7 Support**: Comprehensive JSON Schema validation
- 🔍 **Schema Comparison**: Diff two schemas and see changes instantly
- 📊 **Statistics**: Get insights into schema complexity
- ⚡ **Lightning Fast**: No bloat, instant results

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📊 **Visualize** | Display schema structure as a colorful tree with type icons |
| ✅ **Validate** | Validate JSON data against schemas with detailed error reports |
| 🔍 **Compare** | Diff two schemas and see added/removed/modified fields |
| 📈 **Statistics** | Get property counts, type distribution, and complexity metrics |
| 🎨 **Colorful Output** | Syntax highlighting with customizable color schemes |
| 🚫 **Zero Dependencies** | Pure Python, no external packages required |

### 🚀 Quick Start

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/JSONSchema-Terminal.git
cd JSONSchema-Terminal

# Make executable
chmod +x schemapilot.py

# Optional: Install globally
pip install -e .
```

#### Usage

```bash
# Visualize a schema
python schemapilot.py visualize schema.json

# Validate JSON data
python schemapilot.py validate schema.json data.json

# Compare two schemas
python schemapilot.py compare schema-v1.json schema-v2.json

# Get schema statistics
python schemapilot.py stats schema.json
```

### 📖 Detailed Usage Guide

#### Visualize Command

Display your JSON Schema as a beautiful tree structure:

```bash
$ python schemapilot.py visualize examples/user-schema.json

============================================================
  📋 user-schema
============================================================

📊 Schema Information:
  • ID: https://example.com/user-schema.json
  • Title: User
  • Description: A user profile in the system
  • Version: http://json-schema.org/draft-07/schema#

🌳 Structure Tree:

⧉ root: object
  │ 💡 A user profile in the system
  │ ⚙️  no extra props
  ├── # id: integer *
  │   💡 Unique identifier for the user
  │   ⚙️  ≥1
  ├── "" username: string *
  │   💡 User's login name
  │   ⚙️  min:3, max:50, pattern
  └── ...

📈 Statistics:
  • Total Properties: 14
  • Required Fields: 3
  • Nested Objects: 3
  • Arrays: 1
```

#### Validate Command

Validate JSON data with detailed error reporting:

```bash
$ python schemapilot.py validate schema.json data.json

✓ Validation passed!
  Data conforms to schema: schema.json
```

Or see detailed errors when validation fails:

```bash
✗ Validation failed!
  Found 3 error(s):

  1. Path: email
     Message: Value does not match format "email"
     Value: invalid-email

  2. Path: age
     Message: Value 200 exceeds maximum 150
     Value: 200
```

#### Compare Command

Compare two schemas to see differences:

```bash
$ python schemapilot.py compare schema-v1.json schema-v2.json

Comparing schemas:
  Left:  schema-v1.json
  Right: schema-v2.json

✚ Added (2):
  + properties.email
  + required[2]

✗ Removed (1):
  - properties.username.pattern

✎ Modified (1):
  ~ properties.age.maximum
    Old: 100
    New: 150
```

### 💡 Design Philosophy

SchemaPilot was designed with these principles:

1. **Simplicity**: Do one thing and do it well
2. **Zero Dependencies**: No pip install hell
3. **Developer Experience**: Beautiful, readable output
4. **Performance**: Fast enough for CI/CD pipelines
5. **Standards Compliant**: Full JSON Schema Draft 7 support

### 📦 Packaging & Distribution

#### Build from Source

```bash
# Build wheel
python -m build

# Install locally
pip install dist/schemapilot-1.0.0-py3-none-any.whl
```

#### Run Tests

```bash
python -m pytest tests/ -v
```

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 简体中文

### 🎉 项目介绍

SchemaPilot 是一个**零依赖**的 CLI 工具，将 JSON Schema 可视化和验证功能直接带到您的终端。无需在浏览器标签之间切换，也无需处理笨重的 GUI 应用程序——通过美观的终端输出，理解、验证和比较您的 JSON Schema。

**为什么选择 SchemaPilot？**
- 🚀 **零依赖**：仅使用 Python 标准库
- 🎨 **美观的终端界面**：带有类型图标的彩色树形可视化
- ✅ **完整 Draft 7 支持**：全面的 JSON Schema 验证
- 🔍 **Schema 比较**：对比两个 Schema 并即时查看变更
- 📊 **统计分析**：获取 Schema 复杂度洞察
- ⚡ **极速运行**：无冗余，即时结果

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📊 **可视化** | 以彩色树形结构显示 Schema，带类型图标 |
| ✅ **验证** | 验证 JSON 数据，提供详细的错误报告 |
| 🔍 **比较** | 对比两个 Schema，查看新增/删除/修改的字段 |
| 📈 **统计** | 获取属性数量、类型分布和复杂度指标 |
| 🎨 **彩色输出** | 语法高亮，支持自定义配色方案 |
| 🚫 **零依赖** | 纯 Python，无需外部包 |

### 🚀 快速开始

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/JSONSchema-Terminal.git
cd JSONSchema-Terminal

# 添加执行权限
chmod +x schemapilot.py

# 可选：全局安装
pip install -e .
```

#### 使用

```bash
# 可视化 Schema
python schemapilot.py visualize schema.json

# 验证 JSON 数据
python schemapilot.py validate schema.json data.json

# 比较两个 Schema
python schemapilot.py compare schema-v1.json schema-v2.json

# 获取 Schema 统计信息
python schemapilot.py stats schema.json
```

### 📖 详细使用指南

#### 可视化命令

将您的 JSON Schema 显示为美观的树形结构：

```bash
$ python schemapilot.py visualize examples/user-schema.json

============================================================
  📋 user-schema
============================================================

📊 Schema 信息：
  • ID: https://example.com/user-schema.json
  • 标题: User
  • 描述: A user profile in the system
  • 版本: http://json-schema.org/draft-07/schema#

🌳 结构树：

⧉ root: object
  │ 💡 A user profile in the system
  │ ⚙️  no extra props
  ├── # id: integer *
  │   💡 用户的唯一标识符
  │   ⚙️  ≥1
  ├── "" username: string *
  │   💡 用户登录名
  │   ⚙️  min:3, max:50, pattern
  └── ...

📈 统计信息：
  • 总属性数: 14
  • 必填字段: 3
  • 嵌套对象: 3
  • 数组: 1
```

#### 验证命令

验证 JSON 数据并获取详细的错误报告：

```bash
$ python schemapilot.py validate schema.json data.json

✓ 验证通过！
  数据符合 Schema: schema.json
```

验证失败时查看详细错误：

```bash
✗ 验证失败！
  发现 3 个错误：

  1. 路径: email
     消息: 值不匹配 "email" 格式
     值: invalid-email

  2. 路径: age
     消息: 值 200 超过最大值 150
     值: 200
```

#### 比较命令

比较两个 Schema 查看差异：

```bash
$ python schemapilot.py compare schema-v1.json schema-v2.json

正在比较 Schema：
  左侧:  schema-v1.json
  右侧: schema-v2.json

✚ 新增 (2)：
  + properties.email
  + required[2]

✗ 删除 (1)：
  - properties.username.pattern

✎ 修改 (1)：
  ~ properties.age.maximum
    旧值: 100
    新值: 150
```

### 💡 设计理念

SchemaPilot 遵循以下设计原则：

1. **简洁性**：专注做好一件事
2. **零依赖**：避免 pip 安装地狱
3. **开发者体验**：美观、可读的输出
4. **性能**：快到可以在 CI/CD 流水线中使用
5. **标准兼容**：完整支持 JSON Schema Draft 7

### 📦 打包与分发

#### 从源码构建

```bash
# 构建 wheel
python -m build

# 本地安装
pip install dist/schemapilot-1.0.0-py3-none-any.whl
```

#### 运行测试

```bash
python -m pytest tests/ -v
```

### 🤝 贡献指南

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 📄 开源协议

基于 MIT 协议分发。详见 `LICENSE` 文件。

---

## 繁體中文

### 🎉 專案介紹

SchemaPilot 是一個**零依賴**的 CLI 工具，將 JSON Schema 視覺化和驗證功能直接帶到您的終端機。無需在瀏覽器分頁之間切換，也無需處理笨重的 GUI 應用程式——透過美觀的終端機輸出，理解、驗證和比較您的 JSON Schema。

**為什麼選擇 SchemaPilot？**
- 🚀 **零依賴**：僅使用 Python 標準庫
- 🎨 **美觀的終端機介面**：帶有類型圖示的彩色樹形視覺化
- ✅ **完整 Draft 7 支援**：全面的 JSON Schema 驗證
- 🔍 **Schema 比較**：對比兩個 Schema 並即時查看變更
- 📊 **統計分析**：取得 Schema 複雜度洞察
- ⚡ **極速執行**：無冗餘，即時結果

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📊 **視覺化** | 以彩色樹形結構顯示 Schema，帶類型圖示 |
| ✅ **驗證** | 驗證 JSON 資料，提供詳細的錯誤報告 |
| 🔍 **比較** | 對比兩個 Schema，查看新增/刪除/修改的欄位 |
| 📈 **統計** | 取得屬性數量、類型分布和複雜度指標 |
| 🎨 **彩色輸出** | 語法高亮，支援自訂配色方案 |
| 🚫 **零依賴** | 純 Python，無需外部套件 |

### 🚀 快速開始

#### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/JSONSchema-Terminal.git
cd JSONSchema-Terminal

# 添加執行權限
chmod +x schemapilot.py

# 可選：全域安裝
pip install -e .
```

#### 使用

```bash
# 視覺化 Schema
python schemapilot.py visualize schema.json

# 驗證 JSON 資料
python schemapilot.py validate schema.json data.json

# 比較兩個 Schema
python schemapilot.py compare schema-v1.json schema-v2.json

# 取得 Schema 統計資訊
python schemapilot.py stats schema.json
```

### 📖 詳細使用指南

#### 視覺化命令

將您的 JSON Schema 顯示為美觀的樹形結構：

```bash
$ python schemapilot.py visualize examples/user-schema.json

============================================================
  📋 user-schema
============================================================

📊 Schema 資訊：
  • ID: https://example.com/user-schema.json
  • 標題: User
  • 描述: A user profile in the system
  • 版本: http://json-schema.org/draft-07/schema#

🌳 結構樹：

⧉ root: object
  │ 💡 A user profile in the system
  │ ⚙️  no extra props
  ├── # id: integer *
  │   💡 使用者的唯一識別碼
  │   ⚙️  ≥1
  ├── "" username: string *
  │   💡 使用者登入名稱
  │   ⚙️  min:3, max:50, pattern
  └── ...

📈 統計資訊：
  • 總屬性數: 14
  • 必填欄位: 3
  • 嵌套物件: 3
  • 陣列: 1
```

#### 驗證命令

驗證 JSON 資料並取得詳細的錯誤報告：

```bash
$ python schemapilot.py validate schema.json data.json

✓ 驗證通過！
  資料符合 Schema: schema.json
```

驗證失敗時查看詳細錯誤：

```bash
✗ 驗證失敗！
  發現 3 個錯誤：

  1. 路徑: email
     訊息: 值不符合 "email" 格式
     值: invalid-email

  2. 路徑: age
     訊息: 值 200 超過最大值 150
     值: 200
```

#### 比較命令

比較兩個 Schema 查看差異：

```bash
$ python schemapilot.py compare schema-v1.json schema-v2.json

正在比較 Schema：
  左側:  schema-v1.json
  右側: schema-v2.json

✚ 新增 (2)：
  + properties.email
  + required[2]

✗ 刪除 (1)：
  - properties.username.pattern

✎ 修改 (1)：
  ~ properties.age.maximum
    舊值: 100
    新值: 150
```

### 💡 設計理念

SchemaPilot 遵循以下設計原則：

1. **簡潔性**：專注做好一件事
2. **零依賴**：避免 pip 安裝地獄
3. **開發者體驗**：美觀、可讀的輸出
4. **效能**：快到可以在 CI/CD 流水線中使用
5. **標準相容**：完整支援 JSON Schema Draft 7

### 📦 打包與分發

#### 從原始碼建置

```bash
# 建置 wheel
python -m build

# 本地安裝
pip install dist/schemapilot-1.0.0-py3-none-any.whl
```

#### 執行測試

```bash
python -m pytest tests/ -v
```

### 🤝 貢獻指南

歡迎貢獻！請隨時提交 Pull Request。

1. Fork 本倉庫
2. 建立您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 📄 開源授權

基於 MIT 授權分發。詳見 `LICENSE` 檔案。

---

## 🔗 Links

- **Repository**: https://github.com/gitstq/JSONSchema-Terminal
- **Issues**: https://github.com/gitstq/JSONSchema-Terminal/issues
- **License**: [MIT](LICENSE)

---

<p align="center">Made with ❤️ by the SchemaPilot Team</p>
