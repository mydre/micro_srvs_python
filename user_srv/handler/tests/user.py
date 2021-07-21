import grpc
from user_srv.proto import user_pb2_grpc,user_pb2
from google.protobuf import empty_pb2

class UserTest:
    def __init__(self):
        # 连接grpc服务器
        channel = grpc.insecure_channel("127.0.0.1:50051")
        self.stub = user_pb2_grpc.UserStub(channel)
    def user_list(self):
        rsp : user_pb2.UserListResponse = self.stub.GetUserList(user_pb2.PageInfo(pn=2,pSize=2))
        print(rsp.total)
        for user in rsp.data:
            print(user.mobile,user.birthDay)
    def get_user_by_id(self,id):
        rsp:user_pb2.UserInfoResponse = self.stub.GetUserById(user_pb2.IdRequest(id=id))
        print(rsp.mobile)
    def create_user(self,nick_name,mobile,password):
        rsp:user_pb2.UserInfoResponse = self.stub.CreateUser(user_pb2.CreateUserInfo(
            nickName=nick_name,
            passWord=password,
            mobile=mobile
        ))
        print(rsp.id)
    def update_user(self,id,nickname,gender,birthday):
        rsp :empty_pb2.Empty = self.stub.UpdateUser(user_pb2.UpdateUserInfo(
            id=id,
            nickName=nickname,
            gender=gender,
            birthDay=birthday
        ))
        print('更新完成')


if __name__ == "__main__":
    user = UserTest()
    #user.user_list()
    #user.get_user_by_id(100)
    #user.create_user("bobby","13232323232","123456")
    user.update_user(2,"dahai",'男',132338822)