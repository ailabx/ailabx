## docker下mongo部署与操作

mongo是当下很流行的No SQL数据库，由于它的schema-free，则上手容易，自动分表分库的特性，受到很多新兴应用的青睐。

对于流行的关系数据库mysql，几个缺点。mongo不支持多表查询。如果需要经常关系几个表join，那使用mongo是不合适的。

当然关系数据库的事务之类的，也是不支持的。

除了如上2点吧，如果可以接受，那使用mongo还是很令人愉悦的。

```
docker pull mongo

#--auth启用密码验证
docker run -p 27017:27017 -v /mnt/db:/data/db -d --name my_mongodb mongo --bind_ip_all --auth

#进入容器，并使用mongo client进入admin
docker exec -it mymongo mongo admin

#创建用户管理员
db.createUser({ user: 'name', pwd: 'pwd', roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] });

#退出，重新进入,使用刚才创建的用户名，密码登录
db.auth("name","pwd")

#切换表
use tablexxx

#为tablexxx创建读写权限用户write/write
db.createUser({ user: 'write', pwd: 'write', roles: [ { role: "readWrite", db: "tablexxx" } ] });

#为tablexxx创建读权限用户read/read
db.createUser({ user: 'read', pwd: 'read', roles: [ { role: "read", db: "tablexxx" } ] });

#搞定！

```
这是官方最新的mongo镜像，当然可以指定版本。

```
import pymongo

#连接mongo,默认数据库是sqlData
def get_mongodb(db='db'):
    mongo_db = pymongo.MongoClient('ip', 27017)[db]
    mongo_db.authenticate('write', 'write')
    return mongo_db

#给指定表加索引
def ensure_index(tb,col):
    db = get_mongodb()
    db[tb].ensure_index(col)

#查看索引
def show_index(tb):
    db = get_mongodb()
    print(db[tb].index_information())

#添加文档
def add_doc(tb,doc):
    db = get_mongodb()
    db[tb].insert(doc)
```
