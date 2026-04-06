# path_config.py
# 集中管理所有路径，修改一处即可全局生效

import os

# 获取当前文件所在目录（即 python/）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 项目根目录（protocal_test/）
ROOT_DIR = os.path.dirname(BASE_DIR)

# ---- Proto 生成代码目录（Python 版本） ----
PROTO_GEN_PY_DIR = os.path.join(ROOT_DIR, "proto", "generated", "py")

# ---- 数据文件目录 ----
DATA_DIR = os.path.join(ROOT_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "data.bin")

# ---- 其他可能用到的路径 ----
# 原始 proto 文件目录
PROTO_SRC_DIR = os.path.join(ROOT_DIR, "proto")