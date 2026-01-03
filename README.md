# Spider_DouYin_Videos

[![Python Version](https://img.shields.io/badge/python-≥3.6.8-blue.svg)](https://www.python.org/)
[![Node.js Required](https://img.shields.io/badge/node-required-green.svg)](https://nodejs.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 项目简介

Spider_DouYin_Videos 是一个强大的抖音视频爬虫工具，专门用于批量下载指定抖音用户的公开视频内容。本工具采用现代化的爬虫技术，确保稳定性和高效性，遇到问题优先排查是否cookie失效
只作为研究所用，切勿用于商业行为！！
商单联系wx: ytouching

## 功能特点

- ✨ 自动获取指定用户的所有公开视频
- 🚀 支持批量下载和断点续传
- 💻 跨平台支持 (Windows/MacOS)
- 🔧 简单的配置和使用方式
- 📦 自动视频文件管理

## 环境要求

- Python >= 3.6.8
- Node.js (最新稳定版)
- npm (随Node.js一起安装)

## 快速开始

### 1. 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt
```

### 2. 配置参数

在 `config.py` 文件中配置以下参数：

- `USER_SEC_UID`: 抖音用户唯一标识符
- `SAVE_FOLDER`: 视频保存路径

### 3. 获取用户ID (USER_SEC_UID)

1. 使用Chrome浏览器访问 `https://www.douyin.com/`
2. 打开目标用户主页 (例如：`https://www.douyin.com/user/MS4wLjABAAAAxxxx`)
3. 从URL中提取用户ID (即 `MS4wLjABAAAAxxxx` 部分)

### 4. 运行程序

基础用法：
```bash
python main.py
```

命令行参数方式：
```bash
python main.py <用户ID> <保存路径>
```

示例：
```bash
python main.py MS4wLjABAAAAxxxx ./downloads
```

## 项目结构

```
Spider_DouYin_Videos/
├── main.py          # 主程序入口
├── config.py        # 配置文件
├── requirements.txt # Python依赖
└── README.md       # 项目文档
```

## 注意事项

- 请确保网络连接稳定
- 建议使用代理以避免IP限制
- 遵守抖音平台的使用条款和政策
- 仅用于学习和研究目的

## 商业支持

如需定制开发或技术支持，请通过以下方式联系：

- 微信：ytouching (备注：抖音爬虫)
- 电话：13824464121

## 部署建议

推荐使用[腾讯云服务器](https://curl.qcloud.com/tTuWmDCs)进行部署，以获得更好的性能和稳定性。

## 许可证

本项目采用 MIT 许可证，详情请参见 LICENSE 文件。

## 赞赏支持

如果本项目对您有帮助，欢迎扫码赞赏支持作者：

<img src="https://ytouch-1258011219.cos.ap-nanjing.myqcloud.com/wechat_shoukuan.jpg" width="200" />

---

**免责声明：** 本工具仅供学习和研究使用，请勿用于商业用途。使用本工具所产生的一切法律责任由使用者自行承担。
