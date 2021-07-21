import os.path
import sys
import logging
import signal#python中处理信号量
from concurrent import futures

import grpc
from loguru import logger
import argparse
import socket

# sys.path.insert(0,'/home/acat/PycharmProjects/mxshop_srvs')
# 一般在项目中不使用绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0,BASE_DIR)
print(BASE_DIR)
from user_srv.proto import user_pb2_grpc
from user_srv.handler.user import UserServicer
from common.grpc_health.v1 import health_pb2,health_pb2_grpc,health
from common.grpc_health.v1.health import *
from common.register import consul
from user_srv.settings import settings
import uuid
from functools import partial

def on_exit(signo,frame,service_id):
    logger.info("进程中断")
    register = consul.ConsulRegister(settings.CONSUL_HOST,settings.CONSUL_PORT)# localhost:8500
    register.deregister(service_id)
    sys.exit(0)

'''
windows下支持的信号是有限的：SIGINT  ctrl+C中断
SIGTERM kill 发出软件终止 
'''
def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip',nargs='?',type=str,default=settings.CONSUL_HOST,help='binding ip')
    parser.add_argument('--port',nargs='?',type=int,default=0,help='the listening port')
    args = parser.parse_args()
    if args.port == 0:
        port = get_free_tcp_port()
    else:
        port = args.port


    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))# 启动grpc服务
    # 注册用户服务
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(),server)# 把用户服务添加到server
    # 注册健康检查服务
    health_pb2_grpc.add_HealthServicer_to_server(HealthServicer(),server)# 把健康检查服务添加到grpc server
    # 为grpc服务器配置ip和端口
    server.add_insecure_port(f'{args.ip}:{port}')# 为server设置套接字?

    uid = str(uuid.uuid1())
    signal.signal(signal.SIGINT,partial(on_exit,uid))
    signal.signal(signal.SIGTERM,partial(on_exit,uid))
    logger.info(f"启动服务：{args.ip}:{port}")
    #print(f"启动服务：127.0.0.1:50051")
    server.start()


    logger.info(f"服务注册开始")
    register = consul.ConsulRegister(settings.CONSUL_HOST,settings.CONSUL_PORT)# localhost:8500
    if not register.register(name=settings.SERVICE_NAME,id=uid,address=args.ip,port=port,tags=settings.SERVICE_TAGS,check=None):
        logger.info(f"服务注册失败")
        sys.exit(0)
    logger.info(f"服务注册成功")

    server.wait_for_termination()


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp.bind(("",0))
    _,port =  tcp.getsockname() # 自动获取端口号
    tcp.close()
    return port


if __name__ == '__main__':
    logging.basicConfig()
    serve()