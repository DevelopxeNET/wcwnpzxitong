<div align="center">

# 🚚 物流凭证查询系统

**Logistics Voucher Query System**

*一个优雅、高效的物流签收凭证管理与查询平台*

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask Version](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [API文档](#-api-文档) • [部署指南](#-部署指南)

</div>

---

## 📋 项目简介

物流凭证查询系统是一个专为物流行业打造的签收凭证管理平台，提供Web界面和RESTful API双重访问方式，支持订单号、物流单号快速查询，实时展示物流状态和签收凭证。

### ✨ 核心优势

- 🎯 **精准查询** - 支持订单号和物流单号模糊搜索，毫秒级响应
- 🖼️ **凭证管理** - 弹窗预览签收凭证，一键下载保存
- 🌐 **RESTful API** - 标准化接口，轻松集成第三方系统
- 📱 **响应式设计** - 完美适配PC、平板、手机多端访问
- 🔄 **智能转换** - 自动统一签收状态显示，确保数据一致性
- 🚀 **生产就绪** - 支持Waitress/Gunicorn，高并发稳定运行

---

## 🎨 功能特性

### 🔍 Web查询界面

<div align="center">

| 功能 | 描述 |
|:---:|:---|
| 🔎 **智能搜索** | 支持订单号、物流单号精确/模糊查询 |
| 📊 **数据统计** | 实时展示总订单数、已签收、运输中等统计信息 |
| 🎭 **状态标签** | 不同物流状态用不同颜色标识，一目了然 |
| 📅 **时间格式** | 统一的日期显示格式(YYYY-MM-DD) |
| 🖼️ **图片弹窗** | 点击查看大图，支持多种关闭方式 |
| 💾 **一键下载** | 直接下载签收凭证，自动命名 |

</div>

### 🌐 RESTful API

```http
GET /api/tracking/{tracking_no}
```

**响应示例:**
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "order_no": "ORDER123456",
    "logistics_channel": "顺丰速运",
    "tracking_no": "SF1234567890",
    "logistics_status": "已签收",
    "signed_time": "2025-12-30",
    "image_url": "https://example.com/voucher.jpg"
  }
}
```

### 📚 在线API文档

访问 `/api-docs` 查看交互式API文档，支持在线测试和代码示例。

---

## 🛠️ 技术栈

<div align="center">

| 层级 | 技术 |
|:---:|:---|
| **后端** | Python 3.8+ • Flask 3.0 • PyMySQL |
| **前端** | HTML5 • CSS3 • JavaScript |
| **数据库** | MySQL 5.7+ |
| **服务器** | Waitress (Windows) • Gunicorn (Linux) |
| **部署** | 宝塔面板 • Docker (可选) |

</div>

---

## 🚀 快速开始

### 前置要求

- Python 3.8 或更高版本
- MySQL 5.7 或更高版本
- pip 包管理器

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/DevelopxeNET/wcwnpzxitong.git
cd wcwnpzxitong

# 2. 创建虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库连接信息

# 5. 初始化数据库
python create_logistics_table.py

# 6. 启动服务
python app.py
```

访问 http://localhost:5000 即可使用！

---

## 📖 API 文档

### 查询物流单号

**请求:**
```bash
curl -X GET http://localhost:5000/api/tracking/SF1234567890
```

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "order_no": "ORDER123456",
    "logistics_channel": "顺丰速运",
    "tracking_no": "SF1234567890",
    "query_time": "2025-12-30 10:30:00",
    "logistics_status": "已签收",
    "signed_time": "2025-12-30",
    "image_url": "https://example.com/voucher.jpg"
  }
}
```

**失败响应 (404):**
```json
{
  "code": 404,
  "message": "未找到该物流单号的信息",
  "data": null
}
```

更多API详情请访问: http://localhost:5000/api-docs

---

## 🎯 部署指南

### 方式一: 宝塔面板部署 (推荐)

1. 上传项目到 `/www/wwwroot/` 目录
2. 在宝塔【Python项目管理器】中添加项目
3. 配置环境变量和数据库
4. 设置Nginx反向代理
5. 启动项目

详细步骤请查看: [宝塔部署说明.txt](宝塔部署说明.txt)

### 方式二: 命令行部署

```bash
# Linux/Mac
./start.sh

# Windows
start.bat
```

### 方式三: 使用Waitress (Windows)

```bash
waitress-serve --host=0.0.0.0 --port=5000 wsgi:app
```

### 方式四: 使用Gunicorn (Linux)

```bash
gunicorn -c gunicorn_config.py wsgi:app
```

---

## 📁 项目结构

```
wcwnpzxitong/
├── 📄 app.py                      # Flask主应用
├── 📄 config.py                   # 配置管理
├── 📄 wsgi.py                     # WSGI入口
├── 📄 requirements.txt            # 项目依赖
├── 📄 .env.example               # 环境变量模板
├── 📁 templates/                 # HTML模板
│   ├── 📄 index.html             # 查询系统主页
│   └── 📄 api_docs.html          # API文档页面
├── 📄 create_logistics_table.py  # 数据库建表脚本
├── 📄 fix_all_status.py          # 状态统一脚本
├── 📄 waitress_config.py         # Waitress配置
├── 📄 gunicorn_config.py         # Gunicorn配置
├── 📄 start.sh                   # Linux启动脚本
└── 📄 start.bat                  # Windows启动脚本
```

---

## ⚙️ 配置说明

### 环境变量 (.env)

```bash
# Flask环境
FLASK_ENV=production

# 安全密钥
SECRET_KEY=your-secret-key-here

# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=logistics_db
```

### 数据库表结构

```sql
CREATE TABLE logistics_voucher (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_no VARCHAR(100) NOT NULL,
    logistics_channel VARCHAR(100),
    tracking_no VARCHAR(100),
    query_time DATETIME,
    logistics_status VARCHAR(50),
    signed_time DATE,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

## 🔒 安全建议

- ✅ 修改默认 `SECRET_KEY`
- ✅ 使用强密码保护数据库
- ✅ 启用HTTPS加密传输
- ✅ 限制数据库访问IP
- ✅ 定期备份数据库
- ✅ 更新依赖包到最新版本

---

## 🐛 故障排查

### 问题1: 无法连接数据库

**解决方案:**
- 检查 `.env` 配置是否正确
- 确认数据库服务正在运行
- 验证防火墙设置

### 问题2: Windows环境无法启动

**解决方案:**
- 使用 `python app.py` 而不是 gunicorn
- 或安装 waitress: `pip install waitress`

### 问题3: 签收状态显示不一致

**解决方案:**
- 运行状态统一脚本: `python fix_all_status.py`
- 系统会自动将"成功签收"转为"已签收"

---

## 📊 性能优化

- 🔹 启用数据库连接池
- 🔹 配置适当的worker进程数
- 🔹 使用Redis缓存查询结果
- 🔹 开启Nginx gzip压缩
- 🔹 图片资源使用CDN

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

---

## 📄 开源协议

本项目采用 [MIT](LICENSE) 协议开源。

---

## 📞 联系方式

- 项目地址: https://github.com/DevelopxeNET/wcwnpzxitong
- 问题反馈: [Issues](https://github.com/DevelopxeNET/wcwnpzxitong/issues)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个Star支持！⭐**

Made with ❤️ by DevelopxeNET

</div>
