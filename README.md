# 抖音去水印视频下载工具

这是一个简单的 Python 工具，可以将抖音分享链接中的视频下载为无水印的高清视频（默认 1080p）。

## 功能特点

- **自动去水印**：下载的视频没有抖音的水印。
- **高清画质**：默认尝试下载最高画质（1080p）。
- **自动保存**：视频自动保存到 `output` 文件夹。

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

## 输出

下载成功的视频将保存在 `output` 文件夹中，文件名为 `douyin_{video_id}.mp4`。

