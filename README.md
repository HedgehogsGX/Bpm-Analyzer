# BPM识别程序

用Python编写的BPM分析工具，可检测音频文件中的节拍变化并以时间轴格式输出结果。

## 安装
```bash
pip install -r requirements.txt
```

## 使用
```bash
# 基本用法
python bpm_analyzer.py 音频文件.mp3

# 高级选项
python bpm_analyzer.py 音频文件.mp3 --segment 15 --tolerance 3
```

## 输出示例
```
0分00秒 - 2分15秒 Bpm120
2分15秒 - 4分30秒 Bpm140
4分30秒 - 5分30秒 Bpm120
```

## 快速分析
```bash
python quick_bpm.py 音频文件.mp3
```

支持MP3、WAV、FLAC等常见音频格式。
