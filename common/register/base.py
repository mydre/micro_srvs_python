import abc

# 定义抽象基类
class Register(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def register(self,name,id,address,port):
        pass

    @abc.abstractmethod
    def deregister(self,service_id):
        pass

    @abc.abstractmethod
    def get_all_service(self):
        pass

    @abc.abstractmethod
    def filter_service(self,filter):
        pass