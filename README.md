# BPM识别程序

这是一个用Python编写的BPM（每分钟节拍数）识别程序，可以分析音频文件并以时间轴格式输出BPM变化。

## 功能特点

- 自动检测音频文件的BPM变化
- 以时间轴格式输出结果
- 支持多种音频格式（MP3、WAV、FLAC等）
- 智能合并相似BPM的时间段
- 清晰易读的输出格式

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
python bpm_analyzer.py <音频文件路径>
```

### 高级选项

```bash
python bpm_analyzer.py <音频文件路径> --segment 15 --tolerance 3
```

参数说明：
- `--segment` 或 `-s`: 分段时长（秒），默认10秒
- `--tolerance` 或 `-t`: BPM容差，默认5.0

## 输出格式

### 全程BPM无变化
```
0分00秒 - 5分30秒 Bpm179
```

### BPM有变化
```
0分00秒到2分15秒 Bpm120
2分15秒到4分30秒 Bpm140
4分30秒到5分30秒 Bpm120
```

## 使用示例

### 单文件分析

```bash
# 分析100bpm.mp3
python bpm_analyzer.py 100bpm.mp3

# 分析ACA.mp3，使用15秒分段
python bpm_analyzer.py ACA.mp3 --segment 15

# 分析ECP.mp3，使用3.0的BPM容差
python bpm_analyzer.py ECP.mp3 --tolerance 3.0
```

### 快速分析（推荐）

```bash
# 使用简化版本快速分析
python quick_bpm.py 100bpm.mp3
```

### 批量分析

```bash
# 分析当前目录中的所有音频文件
python batch_bpm.py
```

## 工作原理

1. **音频加载**: 使用librosa库加载音频文件
2. **分段分析**: 将音频分成指定时长的段落进行BPM检测
3. **节拍检测**: 使用librosa的beat_track函数检测每段的BPM
4. **智能合并**: 将相邻且BPM相似的段落合并
5. **格式化输出**: 按照指定格式输出时间轴和BPM信息

## 程序文件说明

- `bpm_analyzer.py`: 完整版BPM分析器，支持详细参数调整
- `quick_bpm.py`: 简化版分析器，快速分析单个文件
- `batch_bpm.py`: 批量分析器，一次处理多个音频文件
- `requirements.txt`: 依赖库列表

## 注意事项

- 程序需要安装librosa等音频处理库
- 分析精度取决于音频质量和节拍明显程度
- 对于复杂的音乐（如变拍子），可能需要调整参数
- 建议使用较短的分段时长来捕捉更细微的BPM变化
- 推荐使用`quick_bpm.py`进行日常分析，速度更快
