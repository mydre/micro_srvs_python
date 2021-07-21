from peewee import *
from user_srv.settings import settings
# 使用peewee的连接池，使用ReconnectMinxin防止出现连接断开查询失败
class BaseModel(Model):
    class Meta:
        database = settings.DB


class User(BaseModel):
    # 用户模型
    GENDER_CHOICES = (
        ("female", "女"),
        ("male", "男")
    )
    ROLE_CHOICES = (
        (1, "普通用户"),
        (2, "管理员")
    )
    mobile = CharField(max_length=11,index=True,unique=True,verbose_name="手机号码")#加索引
    password = CharField(max_length=100,verbose_name="密码")# 1.密文 2.密文不可反解
    nick_name = CharField(max_length=20,null=True,verbose_name="昵称")
    head_url = CharField(max_length=200,null=True,verbose_name="头像")
    birthday = DateField(null=True,verbose_name="生日")
    address = CharField(max_length=200,null=True,verbose_name="地址")
    desc = TextField(null=True,verbose_name="个人简介")
    gender = CharField(max_length=6,choices=GENDER_CHOICES,null=True,verbose_name="性别")
    role = IntegerField(default=1,choices=ROLE_CHOICES,verbose_name="用户角色")


if __name__ == "__main__":
    '''
    # 生成表结构
    settings.DB.create_tables([User])
    # 1.对称加密2、非对称加密
    # md5非对称加密（信息摘要算法）
    import hashlib
    m = hashlib.md5()
    salt = "gwoow"
    password = "123456"
    m.update((salt+password).encode('utf8'))
    print(m.hexdigest()) # 这个就是生成的md5值
    # 每个用户的盐值都是不一样的，使用passlib库
    '''
    from passlib.hash import pbkdf2_sha256
    settings.DB.create_tables([User])
    # for i in range(10):
    #     user = User()
    #     user.nick_name = f"bobby{i}"
    #     user.mobile = f"1324959294{i}"
    #     user.password = pbkdf2_sha256.hash("admin123")
    #     user.save()

    # hash = pbkdf2_sha256.hash("123456")
    hash = '$pbkdf2-sha256$29000$UsrZmxMCQMgZ45yztlYqJQ$SkoWEvCeDfJNGbghFnihZ1qJVAfrPb8jQREdTkMmFY8'
    # print(hash)
    print(pbkdf2_sha256.verify("admin123",hash))
    # print(pbkdf2_sha256.verify("123436", hash))
