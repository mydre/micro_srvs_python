import nacos

server_address = "localhost:8848"
namespace = "65b3b123-1a2b-4053-8802-7665aa3356e2"

client = nacos.NacosClient(server_addresses=server_address,namespace=namespace,username="nacos",password="nacos")

# get config
data_id = "user-srv.json"
group = "dev"

import json
json_data = json.loads(client.get_config(data_id,group))
print(type(json_data))
print(json_data)

def test_cb(args):
    print("配置文件发生变化")
    print(args)

if __name__ == "__main__":
    client.add_config_watcher(data_id,group,test_cb)
    import time
    time.sleep(3000)