---
name: douyin-download
description: 下载抖音无水印视频。当用户提供抖音分享链接或文本时，自动解析并下载无水印高清视频。无需依赖外部脚本，AI 直接使用 curl 完成全部操作。
user_invocable: true
---

# 抖音无水印视频下载

当用户提供抖音分享链接或包含抖音链接的文本时，使用此技能下载无水印视频。

**核心原理：** 抖音短链接 → 302 重定向获取长链接 → 从页面提取 video_id → 拼接无水印 API 地址 → 下载视频文件。全程只需 curl，无需 Python 或其他依赖。

## Step 1: 提取链接

从用户消息中用正则提取抖音短链接，格式为：
```
https://v.douyin.com/xxxxxxxxx/
```

如果用户没有提供链接，请询问用户提供抖音分享链接或分享文本。

## Step 2: 解析短链接获取重定向地址

使用 curl 跟踪短链接的 302 重定向，获取长链接：

```bash
curl -sS -o /dev/null -w '%{redirect_url}' -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1' -k '{{SHORT_URL}}'
```

这会输出重定向后的长链接。

## Step 3: 获取页面内容并提取 video_id

用 curl 请求长链接页面内容，从中提取 `video_id` 参数：

```bash
curl -sS -k -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1' '{{LONG_URL}}' | grep -oE 'video_id=([a-zA-Z0-9]+)' | head -1 | sed 's/video_id=//'
```

提取出的就是 `video_id`。

## Step 4: 获取无水印视频的真实下载地址

用 video_id 拼接抖音无水印 API，获取视频真实地址：

```bash
curl -sS -o /dev/null -w '%{redirect_url}' -k -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1' 'https://api.amemv.com/aweme/v1/play/?video_id={{VIDEO_ID}}&ratio=1080p&line=0'
```

这会返回视频文件的真实下载 URL。

## Step 5: 下载视频

创建输出目录并下载视频文件：

```bash
mkdir -p output && curl -sS -k -L -o "output/douyin_{{VIDEO_ID}}.mp4" '{{REAL_VIDEO_URL}}'
```

## Step 6: 报告结果

- 下载成功：告知用户视频保存路径（绝对路径）和文件大小
- 下载失败：分析原因并建议：
  - 链接失效 → 建议重新获取分享链接
  - 无法提取 video_id → 抖音页面结构可能已变更
  - 网络错误 → 建议检查网络连接

## 注意事项

- 仅支持抖音（v.douyin.com）的分享链接
- 下载的视频为无水印 1080p 高清版本
- 文件命名格式为 `douyin_{video_id}.mp4`
- 所有请求使用移动端 User-Agent 模拟手机访问
- 全部步骤依次执行，每步需要上一步的输出作为输入
