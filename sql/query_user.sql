# 建议: 可以在数据库管理软件先输入，看看有没有用，再写到代码里
# 下面的<...>在代码里均替换为%s

# 注册公共用户，插入到User表里(公开网页上应该只支持注册公共用户)
INSERT INTO user (email, password, name, role_number) VALUES (<邮箱>, <密码>, <昵称>, 0)
INSERT INTO user (email, password, name, role_number) VALUES ("example@qq.com", "this is a pwd", "nickname", 0)

# 注册内部用户，插入到User表里(这个应该只在数据库管理软件那输入)
INSERT INTO user (email, password, name, role_number) VALUES (<邮箱>, <密码>, <昵称>, 10)
INSERT INTO user (email, password, name, role_number) VALUES ("example@qq.com", "this is a pwd", "nickname", 10)

# 注册/登录前先检查用户(邮箱)是否存在(用户输入注册的信息时务必先调用这个看看有没有被注册过)
# 用户邮箱应该是唯一的
# 如果用户存在，这个SQL应该返回用户存储在数据库里的唯一ID；否则，不返回任何ID
# 检查是否返回ID，就可以判断用户(邮箱)是否存在
SELECT user_id FROM user WHERE email = <邮箱>
SELECT user_id FROM user WHERE email = "example@qq.com"

# 查询用户的昵称，以及是否为管理员(role_number>=10 为管理员)
# 在使用这个SQL前需要检查用户(邮箱)是否存在
# 因为用户不存在和密码不对是两种情况，应该返回不同的提示
# 如果密码正确，应该返回用户的昵称，以及role_number
# 如果密码不正确，应该不返回东西
SELECT name, role_number FROM user WHERE email = <邮箱> AND password = <密码>
SELECT name, role_number FROM user WHERE email = "example@qq.com" AND password = "this is a pwd"


# 下面的功能目前应该不用实现

# 彻底删除一个公共用户账号(销号，应该只对公共用户开放)
# 彻底删除一个内部用户账号(内部用户需要单独在数据库管理软件里输入)
# 更新一个用户的密码(用于设置新密码)
# 更新一个用户的昵称
# 更新一个用户的邮箱