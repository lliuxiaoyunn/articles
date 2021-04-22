# redis 基础知识

## 入门介绍

RemoteDictionaryServer(Redis)是一个开源的使用c语言编写的，遵守BSD协议，支持网络、可基于内存持久化的日志型、key-value数据库。

它的值(value)可以是字符串、哈希、列表、集合、有序集合等类型。

## Redis特点与优势

**特点**：

+ 支持数据的持久化，可以将内存中的数据，保存到磁盘中，重启时，再次加载使用。
+ 不仅提供key-value类型数据，还提供list、hash、set、zset等数据结构。
+ 支持数据备份，可以用master-slave分布式方式实现数据的备份。

**优势**：

+ 高性能， 读速度可达110000次/s， 写速度可达 81000 次/s
+ 丰富的数据类型
+ 原子性， 所有操作都是原子性的，要么成功执行，要么失败完成不执行。
+ 丰富的特性

##  基本知识

redis的默认服务端口：6379

redis的默认配置文件： redis.conf (redis.windows.conf)

redis 默认的最大连接数为： 10000

### 安装

**用docker安装redis**：

```sh
# 获取最行redis镜像
docker pull redis:latest

# 成功下载后，运行容器
docker run --itd --name you_redis_name -p 6379:639 redis
# -p 6379:6379 映射容器6379端口到宿主机的6379端口

# 选择执行
# 进入redis容器
docker exec --it you_redis_name /bin/bash
# 测试连接
redis-cli
set test 1
```

### 查看配置

```sh
# 进入redis容器
docker exec --it you_redis_name /bin/bash
# 客户端连接
redis-cli

# 查看所有配置信息 
127.0.0.1:6379> config get *
# 支持 * 号模糊匹配

# 查看所有配置信息
127.0.0.1:6379> info

# 查看最大连接数
127.0.0.1:6379> config get maxclients
```

**修改配置**：

```sh
# 语法 config set 配置项目名 值
# 例如：
127.0.0.1:6379> config set loglevel "notice"

# 修改最大连接数
127.0.0.1:6379> config set maxclients 100000

```

**配置项说明：**

| 配置项                      | 默认值                  | 说明                                                         |
| --------------------------- | ----------------------- | ------------------------------------------------------------ |
| daemonize                   | no                      | redis默认不是守护进程方式运行，可以通过修改值为yes，启用守护进程 |
| pidfile                     |                         | 以守护进程方式运行，默认会把pid写到/var/run/redis.pid文件，可以通过pidfile指定 |
| port                        | 6379                    | 默认端口                                                     |
| bind                        | 127.0.0.1               | 绑定的主机地址                                               |
| timeout                     | 0                       | 客户端闲置多少秒后关闭连接。0 表示关闭该功能                 |
| loglevel                    | notice                  | 日志级别，四级：debug\verbose\notice\warning                 |
| logfile                     |                         | 标准输出日志文件地址                                         |
| database                    | 16                      | 设置数据库的数量，可以用select 指定数据库id                  |
| <span id='save'>save</span> | 3600 1 300 100 60 10000 | 指定多少秒时间内，有多少次更新操作，就将数据同步到数据文件，可以多个条件配合 |
| rdbcompression              | yes                     | 存储到本地的数据时是否压缩数据                               |
| dbfilename                  | dump.rdb                | 数据库文件名                                                 |
| dir                         | /data                   | 数据库存放目录                                               |
| masteruser                  |                         | master-slave时的主控用户                                     |
| masterauth                  |                         | master-slave时的主控密码                                     |
| slaveof                     | <masterip> <masterport> | 当为slave时， 连接的主控机器ip 和 端口                       |
| requirepass                 |                         | 连接redis的密码，默认关闭                                    |
| **appendonly**              | no                      | 每次更新操作后，是否进行日志记录。默认情况下，redis是异步存储数据，按照“[save](#save)” 配置的时间保存。所以，可能在突然断电时，丢失少量数据。默认no，不写日志 |
| **appendfilename**          | appendonly.aof          | 更新日志的文件名称，默认 appendonly.aof                      |
| **appendfsync**             | everysec                | 更新日志条件：<br />  no 表示等操作系统进行数据换同步到磁盘(快)<br />always 表示每次更新操作后手动调用fsync()将数据写到磁盘(慢，安全)<br />everysec 表示每秒同步一次 (折中，默认值) |
|                             |                         |                                                              |
|                             |                         |                                                              |

### 数据类型

string **字符串**： 最基本的类型，可以包含任何数据，最大能存储512MB数据

```shell
# 案例
# 向redis中，写入一个key-value对， 存储一个value字符串，key为 title
# 汉字会编码
127.0.0.1:6379> SET title "redis基础知识"

# 获取redis中某个key的值
127.0.0.1:6379> GET title

# 删除redis中某个key
127.0.0.1:6379> DEL title
```

hash **哈希**： 也是key-value对，但是value是一个 field和value的映射表，适合存储对象

```shell
# 案例
# 向redis中，写入一个key-value对， 存储一个hash值, key为 desc
127.0.0.1:6379> HMSET desc field1 "这篇文章的描述" filed2 "作者是 Allen"

# 获取某个hash值
127.0.0.1:6379> HGET desc fild1
```

list **列表**： 按照插入顺序排序

```sh
# 案例
# 向redis中，写入一个列表，key为course， 值有多个
127.0.0.1:6379> lpush course redis
127.0.0.1:6379> lpush course mongodb
127.0.0.1:6379> lpush course rabitmq

# 获取列表 第0-10个值
127.0.0.1:6379> lrange course 0 10

```

set **集合：** 集合是无序的， 集合天生去重，重复值，自动去掉

```sh
# 案例
# 向redis中，写入一个集合，key为course， 值有多个
127.0.0.1:6379> sadd crse redis
127.0.0.1:6379> sadd crse mongodb
127.0.0.1:6379> sadd crse rabitmq

# 获取集合
127.0.0.1:6379> smembers crse
```

zset **有序集合：**zset 和 set 一样也是string类型元素的集合,且不允许重复的成员。不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。

```sh
# 案例
# 向redis中，写入一个集合，key为cou， 值有多个
127.0.0.1:6379> zadd cou redis
127.0.0.1:6379> zadd cou mongodb
127.0.0.1:6379> zadd cou rabitmq

# 获取有序集合
127.0.0.1:6379> zrangebyscore cou 0 100
```

## redis 性能测试

在redis目录执行命令： `redis-benchmark [option] [option value]`

```sh
root@2757f85ade62:/data# redis-benchmark -n 10000 -q
PING_INLINE: 119047.62 requests per second
PING_BULK: 129870.13 requests per second
SET: 117647.05 requests per second
GET: 133333.33 requests per second
INCR: 133333.33 requests per second
LPUSH: 135135.14 requests per second
RPUSH: 117647.05 requests per second
LPOP: 131578.95 requests per second
RPOP: 136986.30 requests per second
SADD: 138888.89 requests per second
HSET: 140845.06 requests per second
SPOP: 135135.14 requests per second
LPUSH (needed to benchmark LRANGE): 126582.27 requests per second
LRANGE_100 (first 100 elements): 65789.48 requests per second
LRANGE_300 (first 300 elements): 25974.03 requests per second
LRANGE_500 (first 450 elements): 19417.48 requests per second
LRANGE_600 (first 600 elements): 15748.03 requests per second
MSET (10 keys): 144927.55 requests per second

root@2757f85ade62:/data#

```

```shell
root@2757f85ade62:/data# redis-benchmark --help
Usage: redis-benchmark [-h <host>] [-p <port>] [-c <clients>] [-n <requests>] [-k <boolean>]

 -h <hostname>      Server hostname (default 127.0.0.1)
 -p <port>          Server port (default 6379)
 -s <socket>        Server socket (overrides host and port)
 -a <password>      Password for Redis Auth
 --user <username>  Used to send ACL style 'AUTH username pass'. 
 					Needs -	a.
 -c <clients>       Number of parallel connections (default 50)
 -n <requests>      Total number of requests (default 100000)
 -d <size>          Data size of SET/GET value in bytes (default 3)
 --dbnum <db>       SELECT the specified db number (default 0)
 --threads <num>    Enable multi-thread mode.
 --cluster          Enable cluster mode.
 --enable-tracking  Send CLIENT TRACKING on before starting benchmark.
 -k <boolean>       1=keep alive 0=reconnect (default 1)
 -r <keyspacelen>   Use random keys for SET/GET/INCR, random values for SADD
  Using this option the benchmark will expand the string __rand_int__
  inside an argument with a 12 digits number in the specified range
  from 0 to keyspacelen-1. The substitution changes every time a command
  is executed. Default tests use this to hit random keys in the
  specified range.
 -P <numreq>        Pipeline <numreq> requests. Default 1 (no pipeline).
 -e                 If server replies with errors, show them on stdout.
                    (no more than 1 error per second is displayed)
 -q                 Quiet. Just show query/sec values
 --precision        Number of decimal places to display in latency output (defa                                                                          ult 0)
 --csv              Output in CSV format
 -l                 Loop. Run the tests forever
 -t <tests>         Only run the comma separated list of tests. The test
                    names are the same as the ones produced as output.
 -I                 Idle mode. Just open N idle connections and wait.

Examples:

 Run the benchmark with the default configuration against 127.0.0.1:6379:
   $ redis-benchmark

 Use 20 parallel clients, for a total of 100k requests, against 192.168.1.1:
   $ redis-benchmark -h 192.168.1.1 -p 6379 -n 100000 -c 20

 Fill 127.0.0.1:6379 with about 1 million keys only using the SET test:
   $ redis-benchmark -t set -n 1000000 -r 100000000

 Benchmark 127.0.0.1:6379 for a few commands producing CSV output:
   $ redis-benchmark -t ping,set,get -n 100000 --csv

 Benchmark a specific command line:
   $ redis-benchmark -r 10000 -n 10000 eval 'return redis.call("ping")' 0

 Fill a list with 10000 random elements:
   $ redis-benchmark -r 10000 -n 10000 lpush mylist __rand_int__

 On user specified command lines __rand_int__ is replaced with a random integer
 with a range of values selected by the -r option.
root@2757f85ade62:/data#

```

| 参数             | 默认值    | 用户描述                                |
| ---------------- | --------- | --------------------------------------- |
| -h <hostname>    | 127.0.0.1 | 服务器ip                                |
| -p <port>        | 6379      | 服务器端口                              |
| -s <socket>      |           | 指定服务器ip和端口                      |
| -c <clients>     | 50        | 并发连接数                              |
| -n <requests>    | 10000     | 总请求数                                |
| -d <size>        | 3         | 指定set\get的值大小                     |
| -k <boolean>     | 1         | 1保存连接 0 重连                        |
| -r <keyspacelen> |           | SET\GET\INCR随机key，SADD集合添加随机值 |
| -P <numreq>      | 1         | 通过管道传输请求                        |
| -q               |           | 强制退出redis                           |
| --csv            |           | 输出格式为csv                           |
| -l               |           | 永远循环执行                            |
| -t <tests>       |           | 仅允许以逗号分隔的测试命令列表          |
| -I               |           | Idle模式，仅打开N个idle连接并等待       |

