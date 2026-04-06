# ------------------------------------------------------------
# vcpkg 工具链（建议放最前面）
# ------------------------------------------------------------
set(CMAKE_TOOLCHAIN_FILE "E:/software/vcpkg/vcpkg/scripts/buildsystems/vcpkg.cmake")

cmake_minimum_required(VERSION 3.10.0)

project(protocol_test VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(MSVC)
    add_compile_options(/utf-8)
endif()

include(CTest)
enable_testing()

# ------------------------------------------------------------
# 查找依赖
# ------------------------------------------------------------
find_package(protobuf CONFIG REQUIRED)
find_package(gRPC CONFIG REQUIRED)
find_package(OpenCV REQUIRED)
find_package(CURL REQUIRED)

# ------------------------------------------------------------
# 路径配置
# ------------------------------------------------------------
get_filename_component(PROJECT_ROOT "${CMAKE_CURRENT_SOURCE_DIR}" DIRECTORY)

set(PROTO_GEN_DIR "${PROJECT_ROOT}/proto/generated")
set(PROTO_GEN_CPP_DIR "${PROTO_GEN_DIR}/cpp")
set(DATA_DIR "${PROJECT_ROOT}/data")

set(PROTO_FILE "${PROJECT_ROOT}/proto/message.proto")
set(PROTO_INCLUDE_DIR "${PROJECT_ROOT}/proto")

# 确保生成目录存在
file(MAKE_DIRECTORY "${PROTO_GEN_CPP_DIR}")

# ------------------------------------------------------------
# 1. 生成 protobuf 代码（修复点在这里）
# ------------------------------------------------------------
protobuf_generate(
    LANGUAGE cpp
    OUT_VAR PROTO_SRCS
    PROTOS ${PROTO_FILE}
    IMPORT_DIRS "${PROTO_INCLUDE_DIR}"   
    PROTOC_OUT_DIR "${PROTO_GEN_CPP_DIR}"
)

# ------------------------------------------------------------
# 2. 获取 grpc 插件（更稳写法）
# ------------------------------------------------------------
set(GRPC_CPP_PLUGIN $<TARGET_FILE:gRPC::grpc_cpp_plugin>)

# ------------------------------------------------------------
# 3. 生成 gRPC 代码（手动方式）
# ------------------------------------------------------------
set(GRPC_SRCS
    "${PROTO_GEN_CPP_DIR}/message.grpc.pb.cc"
)

set(GRPC_HDRS
    "${PROTO_GEN_CPP_DIR}/message.grpc.pb.h"
)

add_custom_command(
    OUTPUT ${GRPC_SRCS} ${GRPC_HDRS}

    COMMAND protobuf::protoc
    ARGS
        --grpc_out "${PROTO_GEN_CPP_DIR}"
        --cpp_out "${PROTO_GEN_CPP_DIR}"
        -I "${PROTO_INCLUDE_DIR}"
        --plugin=protoc-gen-grpc="${GRPC_CPP_PLUGIN}"
        "${PROTO_FILE}"

    DEPENDS "${PROTO_FILE}"
    COMMENT "Generating gRPC sources"
)

# ------------------------------------------------------------
# 可执行文件
# ------------------------------------------------------------
add_executable(protocol_test 
    send.cpp
    ${PROTO_SRCS}
    ${GRPC_SRCS}
)

# ------------------------------------------------------------
# 头文件目录
# ------------------------------------------------------------
target_include_directories(protocol_test PRIVATE
    "${PROTO_GEN_CPP_DIR}"
    "${CMAKE_CURRENT_SOURCE_DIR}"
    "${PROJECT_ROOT}"
)

# ------------------------------------------------------------
# 链接库
# ------------------------------------------------------------
target_link_libraries(protocol_test PRIVATE
    ${OpenCV_LIBS}
    CURL::libcurl
    protobuf::libprotobuf
    gRPC::grpc++
    gRPC::grpc++_reflection
)

# ------------------------------------------------------------
# 宏定义
# ------------------------------------------------------------
target_compile_definitions(protocol_test PRIVATE
    DATA_DIR="${DATA_DIR}"
)