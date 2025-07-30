#!/usr/bin/env python3
"""
BPM识别程序
分析音频文件的BPM变化，并以时间轴格式输出结果
"""

import librosa
import numpy as np
import argparse
import os
from typing import List, Tuple


class BPMAnalyzer:
    def __init__(self, hop_length: int = 512, sr: int = 22050):
        """
        初始化BPM分析器
        
        Args:
            hop_length: 帧跳跃长度
            sr: 采样率
        """
        self.hop_length = hop_length
        self.sr = sr
    
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        加载音频文件
        
        Args:
            file_path: 音频文件路径
            
        Returns:
            音频数据和采样率
        """
        try:
            y, sr = librosa.load(file_path, sr=self.sr)
            return y, sr
        except Exception as e:
            raise Exception(f"无法加载音频文件 {file_path}: {e}")
    
    def analyze_bpm_segments(self, y: np.ndarray, sr: int, segment_duration: int = 10) -> List[Tuple[float, float, float]]:
        """
        分段分析BPM
        
        Args:
            y: 音频数据
            sr: 采样率
            segment_duration: 每段的持续时间（秒）
            
        Returns:
            [(开始时间, 结束时间, BPM), ...]
        """
        total_duration = len(y) / sr
        segments = []
        
        # 计算每段的样本数
        samples_per_segment = segment_duration * sr
        
        for start_time in np.arange(0, total_duration, segment_duration):
            end_time = min(start_time + segment_duration, total_duration)
            
            # 提取当前段的音频
            start_sample = int(start_time * sr)
            end_sample = int(end_time * sr)
            segment_audio = y[start_sample:end_sample]
            
            if len(segment_audio) < sr:  # 如果段太短，跳过
                continue
            
            # 分析当前段的BPM
            try:
                tempo, _ = librosa.beat.beat_track(y=segment_audio, sr=sr, hop_length=self.hop_length)
                # 确保tempo是标量值
                if hasattr(tempo, 'item'):
                    bpm = float(tempo.item())
                else:
                    bpm = float(tempo)
            except:
                bpm = 0.0  # 如果分析失败，设为0
            
            segments.append((start_time, end_time, bpm))
        
        return segments
    
    def merge_similar_segments(self, segments: List[Tuple[float, float, float]], tolerance: float = 5.0) -> List[Tuple[float, float, float]]:
        """
        合并相似BPM的相邻段
        
        Args:
            segments: BPM段列表
            tolerance: BPM容差
            
        Returns:
            合并后的段列表
        """
        if not segments:
            return []
        
        merged = []
        current_start, current_end, current_bpm = segments[0]
        
        for start, end, bpm in segments[1:]:
            # 如果BPM相似，合并段
            if abs(bpm - current_bpm) <= tolerance:
                current_end = end
            else:
                # 保存当前段，开始新段
                merged.append((current_start, current_end, current_bpm))
                current_start, current_end, current_bpm = start, end, bpm
        
        # 添加最后一段
        merged.append((current_start, current_end, current_bpm))
        
        return merged
    
    def format_time(self, seconds: float) -> str:
        """
        将秒数格式化为 "X分XX秒" 格式
        
        Args:
            seconds: 秒数
            
        Returns:
            格式化的时间字符串
        """
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}分{secs:02d}秒"
    
    def format_output(self, segments: List[Tuple[float, float, float]], total_duration: float) -> str:
        """
        格式化输出结果
        
        Args:
            segments: BPM段列表
            total_duration: 总时长
            
        Returns:
            格式化的输出字符串
        """
        if not segments:
            return "无法检测到BPM信息"
        
        # 如果只有一段或所有段的BPM都相同
        if len(segments) == 1 or all(abs(seg[2] - segments[0][2]) <= 5 for seg in segments):
            avg_bpm = np.mean([seg[2] for seg in segments])
            start_time = self.format_time(0)
            end_time = self.format_time(total_duration)
            return f"{start_time} - {end_time} Bpm{int(round(avg_bpm))}"
        
        # 多段不同BPM
        result = []
        for start, end, bpm in segments:
            start_str = self.format_time(start)
            end_str = self.format_time(end)
            result.append(f"{start_str}到{end_str} Bpm{int(round(bpm))}")
        
        return "\n".join(result)
    
    def analyze_file(self, file_path: str, segment_duration: int = 10, tolerance: float = 5.0) -> str:
        """
        分析音频文件的BPM
        
        Args:
            file_path: 音频文件路径
            segment_duration: 分段时长（秒）
            tolerance: BPM容差
            
        Returns:
            格式化的BPM分析结果
        """
        print(f"正在分析文件: {file_path}")
        
        # 加载音频
        y, sr = self.load_audio(file_path)
        total_duration = len(y) / sr
        
        print(f"音频时长: {self.format_time(total_duration)}")
        
        # 分段分析BPM
        print("正在分析BPM...")
        segments = self.analyze_bpm_segments(y, sr, segment_duration)
        
        # 合并相似段
        merged_segments = self.merge_similar_segments(segments, tolerance)
        
        # 格式化输出
        result = self.format_output(merged_segments, total_duration)
        
        return result


def main():
    parser = argparse.ArgumentParser(description="BPM识别程序")
    parser.add_argument("file_path", help="音频文件路径")
    parser.add_argument("--segment", "-s", type=int, default=10, help="分段时长（秒），默认10秒")
    parser.add_argument("--tolerance", "-t", type=float, default=5.0, help="BPM容差，默认5.0")
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.exists(args.file_path):
        print(f"错误: 文件 '{args.file_path}' 不存在")
        return
    
    try:
        # 创建分析器
        analyzer = BPMAnalyzer()
        
        # 分析文件
        result = analyzer.analyze_file(args.file_path, args.segment, args.tolerance)
        
        print("\n=== BPM分析结果 ===")
        print(result)
        
    except Exception as e:
        print(f"分析过程中出现错误: {e}")


if __name__ == "__main__":
    main()
