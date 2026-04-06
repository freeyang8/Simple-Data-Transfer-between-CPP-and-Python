import grpc
from concurrent import futures
import sys
import os

# 使用 path_config 动态添加路径（proto生成的python文件）
from path_config import PROTO_GEN_PY_DIR
sys.path.insert(0, PROTO_GEN_PY_DIR)
import message_pb2
import message_pb2_grpc

#继承基类，然后重写方法
class SearchServiceServicer(message_pb2_grpc.SearchServiceServicer):
    #self是实例对象自身
    def Search(self, request, context):
        print(f"收到请求: query={request.query}, page={request.page_number}, success={request.success}")
        # 模拟处理
        result = f"你搜索了 '{request.query}'，这是第 {request.page_number} 页，成功标志={request.success}"
        return message_pb2.SearchResponse(result=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_SearchServiceServicer_to_server(SearchServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("服务器启动，监听 50051 端口")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()