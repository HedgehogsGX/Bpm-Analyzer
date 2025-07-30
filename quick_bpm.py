#!/usr/bin/env python3
"""
快速BPM分析工具
简化版本，用于快速分析音频文件的BPM
"""

import librosa
import numpy as np
import sys
import os


def format_time(seconds):
    """格式化时间为 X分XX秒"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}分{secs:02d}秒"


def analyze_bpm(file_path, segment_duration=15):
    """分析音频文件的BPM"""
    if not os.path.exists(file_path):
        return f"错误: 文件 '{file_path}' 不存在"
    
    try:
        print(f"正在分析: {file_path}")
        
        # 加载音频
        y, sr = librosa.load(file_path, sr=22050)
        total_duration = len(y) / sr
        
        print(f"音频时长: {format_time(total_duration)}")
        print("正在检测BPM...")
        
        # 分段分析
        segments = []
        samples_per_segment = segment_duration * sr
        
        for start_time in np.arange(0, total_duration, segment_duration):
            end_time = min(start_time + segment_duration, total_duration)
            start_sample = int(start_time * sr)
            end_sample = int(end_time * sr)
            segment_audio = y[start_sample:end_sample]
            
            if len(segment_audio) < sr:
                continue
            
            try:
                tempo, _ = librosa.beat.beat_track(y=segment_audio, sr=sr)
                bpm = float(tempo.item() if hasattr(tempo, 'item') else tempo)
            except:
                bpm = 0.0
            
            segments.append((start_time, end_time, bpm))
        
        # 合并相似段落
        if not segments:
            return "无法检测到BPM"
        
        merged = []
        current_start, current_end, current_bpm = segments[0]
        
        for start, end, bpm in segments[1:]:
            if abs(bpm - current_bpm) <= 8:  # 容差8 BPM
                current_end = end
            else:
                merged.append((current_start, current_end, current_bpm))
                current_start, current_end, current_bpm = start, end, bpm
        
        merged.append((current_start, current_end, current_bpm))
        
        # 格式化输出
        if len(merged) == 1 or all(abs(seg[2] - merged[0][2]) <= 8 for seg in merged):
            avg_bpm = np.mean([seg[2] for seg in merged])
            return f"{format_time(0)} - {format_time(total_duration)} Bpm{int(round(avg_bpm))}"
        else:
            result = []
            for start, end, bpm in merged:
                start_str = format_time(start)
                end_str = format_time(end)
                result.append(f"{start_str}到{end_str} Bpm{int(round(bpm))}")
            return "\n".join(result)
    
    except Exception as e:
        return f"分析失败: {e}"


def main():
    if len(sys.argv) < 2:
        print("用法: python quick_bpm.py <音频文件>")
        print("示例: python quick_bpm.py 100bpm.mp3")
        return
    
    file_path = sys.argv[1]
    result = analyze_bpm(file_path)
    
    print("\n=== BPM分析结果 ===")
    print(result)


if __name__ == "__main__":
    main()
