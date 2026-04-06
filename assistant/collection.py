import os
import sys
from pathlib import Path
from datetime import datetime


def read_directory_tree(directory, indent_level=0, max_depth=3):
    """
    递归读取目录树中的所有文件（不限制后缀）

    Args:
        directory: 要扫描的目录路径
        indent_level: 缩进级别
        max_depth: 最大递归深度

    Returns:
        dict: 文件路径和内容的字典
    """
    file_contents = {}

    if not directory.exists() or indent_level > max_depth:
        return file_contents

    # 读取当前目录下的所有文件
    for item in sorted(directory.iterdir()):
        if item.is_file():
            try:
                with open(item, 'r', encoding='utf-8') as f:
                    content = f.read()
                    file_contents[str(item)] = content
            except UnicodeDecodeError:
                # 二进制文件无法以文本方式读取，记录错误信息
                file_contents[str(item)] = f"[二进制文件，无法显示文本内容]"
            except Exception as e:
                file_contents[str(item)] = f"[读取失败: {e}]"
        elif item.is_dir() and indent_level < max_depth:
            # 递归读取子目录
            sub_contents = read_directory_tree(item, indent_level + 1, max_depth)
            file_contents.update(sub_contents)

    return file_contents


def main():
    """主函数 - 读取cpp、data、proto、python四个文件夹以及.vscode文件夹"""
    print("正在导出项目文件内容...")

    # 获取当前脚本所在的目录
    current_dir = Path(__file__).parent

    # 获取上一级目录
    parent_dir = current_dir.parent

    all_contents = {}

    # 定义要扫描的文件夹（包括.vscode）
    target_folders = ['cpp', 'data', 'proto', 'python', '.vscode']
    
    for folder_name in target_folders:
        folder_path = parent_dir / folder_name
        
        if folder_path.exists():
            print(f"扫描 {folder_name}/ 文件夹...")
            folder_contents = read_directory_tree(folder_path, indent_level=0, max_depth=3)
            all_contents.update(folder_contents)
        else:
            print(f"警告: {folder_name}/ 文件夹不存在: {folder_path}")

    print(f"扫描完成！共找到 {len(all_contents)} 个文件")

    # 直接保存到文件，不询问用户
    output_file = current_dir / "project_files_content.txt"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("项目文件内容导出\n")
            f.write(f"生成时间: {datetime.now()}\n")
            f.write(f"项目根目录: {parent_dir}\n")
            f.write("=" * 60 + "\n\n")
            
            for file_path, content in all_contents.items():
                f.write(f"\n{'=' * 60}\n")
                f.write(f"文件: {file_path}\n")
                f.write(f"{'=' * 60}\n")
                f.write(content)
                f.write(f"\n\n{'-' * 60}\n")

        print(f"内容已保存到: {output_file}")
        print(f"文件大小: {output_file.stat().st_size / 1024:.2f} KB")
    except Exception as e:
        print(f"保存失败: {e}")


if __name__ == "__main__":
    main()