import nacos
import json
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin
from loguru import logger
# mysql gone away
class ReconnectMysqlDatabase(ReconnectMixin,PooledMySQLDatabase):
    pass

NACOS = {
    "Host":"10.114.21.16",
    "Port": 8848,
    "NameSpace":"496fd773-32af-42a1-841c-cc675e58f417",
    "User":"nacos",
    "Password":"nacos",
    "DataId":"user-srv.json",
    "Group":"dev"
}
client = nacos.NacosClient(f'{NACOS["Host"]}:{NACOS["Port"]}',namespace=NACOS["NameSpace"],username=NACOS["User"],password=NACOS["Password"])
# get config
data = client.get_config(NACOS["DataId"],NACOS["Group"])
data = json.loads(data)
logger.info(data)

def update_cfg(args):
    print('配置发生变化')
    print(args)

client.add_config_watcher(NACOS["DataId"],NACOS["Group"],update_cfg)

# # consul的配置
CONSUL_PORT = data['consul']['port']
CONSUL_HOST = data['consul']['host']

# #服务相关的配置
SERVICE_NAME = data['name']
SERVICE_TAGS = data['tags']
DB = ReconnectMysqlDatabase(data['mysql']['db'],host=data['mysql']['host'],port=data['mysql']['port'],user=data['mysql']['user'],password=data['mysql']['password'])
