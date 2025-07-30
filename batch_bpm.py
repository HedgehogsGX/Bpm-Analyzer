#!/usr/bin/env python3
"""
批量BPM分析工具
可以一次分析目录中的所有音频文件
"""

import os
import glob
from quick_bpm import analyze_bpm


def find_audio_files(directory="."):
    """查找目录中的音频文件"""
    audio_extensions = ["*.mp3", "*.wav", "*.flac", "*.m4a", "*.aac", "*.ogg"]
    audio_files = []
    
    for ext in audio_extensions:
        audio_files.extend(glob.glob(os.path.join(directory, ext)))
    
    return sorted(audio_files)


def main():
    print("=== 批量BPM分析工具 ===\n")
    
    # 查找当前目录中的音频文件
    audio_files = find_audio_files()
    
    if not audio_files:
        print("当前目录中没有找到音频文件")
        print("支持的格式: MP3, WAV, FLAC, M4A, AAC, OGG")
        return
    
    print(f"找到 {len(audio_files)} 个音频文件:")
    for i, file in enumerate(audio_files, 1):
        print(f"{i}. {os.path.basename(file)}")
    
    print("\n开始分析...\n")
    
    # 分析每个文件
    for i, file_path in enumerate(audio_files, 1):
        print(f"[{i}/{len(audio_files)}] {os.path.basename(file_path)}")
        print("-" * 50)
        
        result = analyze_bpm(file_path)
        print(result)
        print()


if __name__ == "__main__":
    main()
