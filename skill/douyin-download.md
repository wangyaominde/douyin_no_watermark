---
name: douyin-download
description: 下载抖音无水印视频。当用户提供抖音分享链接或文本时，自动解析并下载无水印高清视频。
user_invocable: true
---

# 抖音无水印视频下载

当用户提供抖音分享链接或包含抖音链接的文本时，使用此技能下载无水印视频。

## 使用流程

1. **获取链接**：从用户输入中提取抖音分享链接（格式如 `https://v.douyin.com/xxxxx/`）
2. **检查环境**：确认 Python 和 requests 库已安装
3. **执行下载**：运行项目中的 `douyin_downloader.py` 脚本
4. **返回结果**：告知用户视频保存位置

## 执行步骤

### Step 1: 确认链接

从用户消息中识别抖音分享链接。链接通常包含在分享文本中，格式为：
- `https://v.douyin.com/xxxxxxxx/`

如果用户没有提供链接，请向用户询问抖音分享链接或分享文本。

### Step 2: 检查依赖

运行以下命令检查 requests 是否已安装：

```bash
python3 -c "import requests" 2>&1 || pip install requests
```

### Step 3: 下载视频

使用 Bash 工具在项目目录下执行下载脚本。注意：
- 脚本路径为项目根目录下的 `douyin_downloader.py`
- 将用户提供的完整分享文本作为参数传入（用双引号包裹）
- 视频会保存到 `output/` 目录

```bash
cd {{PROJECT_ROOT}} && python3 douyin_downloader.py "{{用户提供的分享文本或链接}}"
```

其中 `{{PROJECT_ROOT}}` 是 `douyin_downloader.py` 所在的目录。使用 Glob 工具搜索 `**/douyin_downloader.py` 来定位脚本位置。

### Step 4: 报告结果

- 如果下载成功，告知用户视频文件的保存路径
- 如果失败，分析错误原因并提供解决建议：
  - 链接失效：建议用户重新获取分享链接
  - 网络问题：建议检查网络连接
  - 依赖缺失：帮助安装 requests 库

## 注意事项

- 仅支持抖音（douyin.com）的分享链接
- 下载的视频为无水印 1080p 高清版本
- 视频保存在脚本所在目录的 `output/` 文件夹中
- 文件名格式为 `douyin_{video_id}.mp4`
