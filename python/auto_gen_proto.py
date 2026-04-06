#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_gen_proto.py
使用 grpc_tools.protoc 自动将 proto 文件编译为 Python gRPC 代码。
无需手动查找 grpc_python_plugin 路径。
"""

import os
import sys
from pathlib import Path

# 尝试导入 grpc_tools
try:
    from grpc_tools import protoc
except ImportError:
    print("错误: 未找到 grpc_tools，请运行: pip install grpcio-tools")
    sys.exit(1)

# ---------------------------- 配置区域 ----------------------------
# 默认 proto 文件路径（相对于脚本位置）
DEFAULT_PROTO_FILE = "../proto/message.proto"
# 默认输出目录（相对于脚本位置）
DEFAULT_OUTPUT_DIR = "../proto/generated/py"
# ----------------------------------------------------------------

def main():
    # 确定脚本所在目录
    script_dir = Path(__file__).parent.resolve()

    # 允许通过命令行参数覆盖默认值
    proto_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PROTO_FILE
    output_dir = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_DIR

    # 转换为绝对路径
    proto_abs = (script_dir / proto_file).resolve()
    output_abs = (script_dir / output_dir).resolve()

    # 检查 proto 文件是否存在
    if not proto_abs.exists():
        print(f"错误: proto 文件不存在: {proto_abs}")
        sys.exit(1)

    # 创建输出目录
    output_abs.mkdir(parents=True, exist_ok=True)

    # proto 文件所在目录（用于 --proto_path）
    proto_dir = proto_abs.parent

    # 调用 grpc_tools.protoc 生成代码
    # 参数格式与命令行 protoc 类似，但需要以列表形式传入
    protoc.main([
        'grpc_tools.protoc',
        f'--proto_path={proto_dir}',
        f'--python_out={output_abs}',
        f'--grpc_python_out={output_abs}',
        str(proto_abs)
    ])

    print(f"✅ 代码生成完成！输出目录: {output_abs}")

if __name__ == "__main__":
    main()