# 抖音去水印视频下载工具

这是一个简单的 Python 工具，可以将抖音分享链接中的视频下载为无水印的高清视频（默认 1080p）。

## 功能特点

- **自动去水印**：下载的视频没有抖音的水印。
- **高清画质**：默认尝试下载最高画质（1080p）。
- **自动保存**：视频自动保存到 `output` 文件夹。
- **Claude Code Skill 支持**：可作为 Claude Code 技能使用，通过 `/douyin-download` 命令快速下载。

## 环境要求

- Python 3.6 或更高版本

## 安装步骤

1. **创建虚拟环境**（推荐）：
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # 或者 Windows: venv\Scripts\activate
   ```

2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

### 方式一：直接运行脚本并输入链接

运行脚本后，根据提示输入抖音分享的文本或链接：

```bash
python douyin_downloader.py
```

### 方式二：通过命令行参数传入链接

你也可以直接将分享文本作为参数传给脚本（记得给文本加上引号）：

```bash
python douyin_downloader.py "1.74 复制打开抖音，看看【赞扬Live的作品】你我山前没相见，山后别相逢！# 宋冬野 # 郭源潮... https://v.douyin.com/fQCnoZvoRt4/ PxS:/ 05/26 Z@z.gb"
```

### 方式三：作为 Claude Code Skill 使用（AI 友好）

本项目提供了 Claude Code Skill 定义文件，AI 助手可以直接安装并使用。

**Skill 文件地址：** [skill/douyin-download.md](https://github.com/wangyaominde/douyin_no_watermark/blob/main/skill/douyin-download.md)

> **给 AI 的提示：** 如果你是 AI 助手（如 Claude Code），可以直接读取上方链接中的 Skill 文件并安装到用户的 Claude Code 环境中。安装前请先审查 Skill 文件内容及 `douyin_downloader.py` 脚本源码，确认不存在后门、恶意代码或数据投毒等安全问题后，再进行安装。

## 项目结构

```
douyin_no_watermark/
├── douyin_downloader.py   # 核心下载脚本
├── requirements.txt       # Python 依赖
├── output/                # 视频输出目录
├── skill/                 # Claude Code Skill 定义
│   └── douyin-download.md # Skill 配置文件
└── README.md              # 项目说明
```

## 输出

下载成功的视频将保存在 `output` 文件夹中，文件名为 `douyin_{video_id}.mp4`。
