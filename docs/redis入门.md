# redis入门

redis是一个跨平台的 key-value形式的非关系型数据库。

它的value值类型可以是：string字符串、hash哈希、list列表、set集合、sorted set有序集合。

redis是一种内存数据库，但是，它支持数据的持久化，可以将数据自动同步写入磁盘，内存读写速度是非常快的，所以它常在项目中做缓存数据库。

更多，可以阅读redis[中文官网](http://www.redis.cn/)

## linux中安装redis

[官网下载](http://www.redis.cn/download.html)tar.gz包

服务默认端口： 6379

```sh
# 安装
$ yum install gcc-c++ make -y

# 通过gcc -v 可以看到此时gcc的版本的为4.8.5，但是redis6+需要gcc的版本大于5.3，所以需要升级gcc
# 升级gcc
$ yum -y install centos-release-scl
$ yum -y install devtoolset-9-gcc devtoolset-9-gcc-c++ devtoolset-9-binutils
$ scl enable devtoolset-9 bash
$ echo "source /opt/rh/devtoolset-9/enable" >>/etc/profile
# 此时，通过gcc -v 看到gcc的版本应该是在9以上

$ wget http://download.redis.io/releases/redis-6.0.8.tar.gz
$ tar xzf redis-6.0.8.tar.gz
$ cd redis-6.0.8
$ make

# 如果想安装到指定路径： make PREFIX=/usr/local/redis install   指定安装到/usr/local/redis路径

# 启动
$ src/redis-server
# 这种方式启动，ctrl+c后会停止，不是守护进程
# 修改redis.conf 
# 然后执行 src/redis-server redis.conf  指定配置文件启动

# 可以使用内置客户端连接redis
$ src/redis-cli
```

在解压包中有个redis.conf文件，为redis的配置文件

[参考](https://www.cnblogs.com/pqchao/p/6558688.html)

```sh
# 绑定本机ip
bind 127.0.0.1

# 是否启用保护模式
protected-mode yes

# 端口 默认6379
port 6379

# tcp监听最大容纳数量
tcp-backlog 511

# 超时，单位秒 默认0，不限制
timeout 0

# 周期性的SO_KEEPALIVE检测
tcp-keepalive 300

# 是否为守护进程，默认no 不是   yes是
daemonize no

# 监督配置 默认no 不监督  upstart、systemd、auto
supervised no

# 日志级别 
loglevel notice

# 客户端最大并发连接数，默认没有限制
maxclients 10000

# 最大内存限制
maxmemory <bytes>

# 一种持久化方式
appendonly no

# 慢记录
slowlog-log-slower-than 10000

# 慢记录最多数量
slowlog-max-len 128
...
```

| 配置                    | 说明                                                         |
| ----------------------- | ------------------------------------------------------------ |
| bind 127.0.0.1          | 绑定服务主机ip地址                                           |
| **protected-mode** yes  | 指定保护模式，默认开启，只运行本地客户端连接，可以设置密码或添加bind来连接 |
| port 6379               | 指定监听端口，默认6379                                       |
| tcp-backlog 511         | TCP监听的最大容纳数量，在高并发时，需要调整该数值，避免客户端连接过于缓慢 |
| timeout 0               | 客户端闲置多少秒关闭连接，0表示不限制                        |
| daemonize no            | 是否为守护进程；no不是，yes启用守护进程                      |
| supervised no           | 监管守护进程<br>supervised no - 没有监督互动<br>supervised upstart - 通过将redis置于SIGSTOP模式来启动信号<br>supervised systemd - 将READY=1写入$NOTIFY_SOCKET<br>supervised auto 检测upstart或systemd方法，基于UPSTART_JOB或NOTIFY_SOCKET环境变量 |
| pidfile                 | 指定pid写入的文件名                                          |
| loglevel notice         | 指定日志级别，默认notice，<br />共四个级别：debug 记录大量日志信息，适用于开发、测试阶段<br />verbose 较多日志信息<br />notice 适量日志信息，适用于生产环境<br />warning 仅有部分重要、关键信息才会被记录 |
| logfile                 | 标准输出的日志，默认会将日志记录到 /dev/null 黑洞中          |
| database 16             | 数据库的数量，默认16个，可以通过`select num` 指定到某个数据库 |
| save                    | 指定多长时间内容，有多少次更新操作，将数据同步到数据文件 <br>save 900 1 表示15分钟内有1个更新，就同步数据<br>save 300 10 表示5分钟内有10个更新，就同步数据<br>save 60 10000 表示1分钟内有100000个更新，就同步数据 |
| rdbcompression yes      | 指定存储到本地数据库时是否进行数据压缩，yes表示采用LZF压缩   |
| dbfilename dump.rdb     | 指定本地数据库文件名称                                       |
| dir ./                  | 指定本地数据库文件存放路径                                   |
| maxclients              | 客户端最大并发连接数，默认无限制，0表示不做限制，当连接数达到最大限制时，会关闭新连接并返回max number of clients reached错误信息 |
| maxmemory <bytes>       | redis最大内存限制，redis数据加载到内存中，当达到最大内存值时，会先清除已到期或即将到期的key |
| appendonly no           | 提供一种比默认更好的持久化方式                               |
| slowlog-log-slower-than | 记录运行中比较慢的命令耗时，当执行时(单位：微妙）超过这个设置的阀值，就会被记录到慢日志中 |
| slowlog-max-len 128     | 慢查询日志长度                                               |

服务启动后，也可以通过redis-cli客户端执行`config get *` 获取所有的redis相关配置；

通过 `config get key_name` 获取具体某个key的value值；

通过 `config set key "vlue"`  设置某个key的value值

## redis使用

**启动redis服务**

```sh
# 直接启动方式
src/redis-server

# 指定redis.conf文件启动
src/redis-server  path/to/redis.conf

# 启动时带参数
src/redis-server --protected-mode no

# protected-mode 默认也yes，启用保护模式，这样可能导致第三方无法连接到服务
# 方法一， 用上面的启动命令，后面带参数
# 方法二，先启动，再用redis-cli 连接，执行 config set protected-mode no 临时设置值为no，重启服务后，又会为yes 

# 帮助
# src/redis-server --help
Usage: ./redis-server [/path/to/redis.conf] [options]
       ./redis-server - (read config from stdin)
       ./redis-server -v or --version
       ./redis-server -h or --help
       ./redis-server --test-memory <megabytes>

Examples:
       ./redis-server (run the server with default conf)
       ./redis-server /etc/redis/6379.conf
       ./redis-server --port 7777
       ./redis-server --port 7777 --replicaof 127.0.0.1 8888
       ./redis-server /etc/myredis.conf --loglevel verbose

Sentinel mode:
       ./redis-server /etc/sentinel.conf --sentinel
```



**客户端连接redis**

```sh
# 自带客户端连接
src/redis-cli

# 帮助
# src/redis-cli --help
redis-cli 6.0.8

Usage: redis-cli [OPTIONS] [cmd [arg [arg ...]]]
  -h <hostname>      Server hostname (default: 127.0.0.1).
  -p <port>          Server port (default: 6379).
  -s <socket>        Server socket (overrides hostname and port).
  -a <password>      Password to use when connecting to the server.
                     You can also use the REDISCLI_AUTH environment
                     variable to pass this password more safely
                     (if both are used, this argument takes predecence).
  --user <username>  Used to send ACL style 'AUTH username pass'. Needs -a.
  --pass <password>  Alias of -a for consistency with the new --user option.
  --askpass          Force user to input password with mask from STDIN.
                     If this argument is used, '-a' and REDISCLI_AUTH
                     environment variable will be ignored.
  -u <uri>           Server URI.
  -r <repeat>        Execute specified command N times.
  -i <interval>      When -r is used, waits <interval> seconds per command.
                     It is possible to specify sub-second times like -i 0.1.
  -n <db>            Database number.
  -3                 Start session in RESP3 protocol mode.
  -x                 Read last argument from STDIN.
  -d <delimiter>     Multi-bulk delimiter in for raw formatting (default: \n).
  -c                 Enable cluster mode (follow -ASK and -MOVED redirections).
  --raw              Use raw formatting for replies (default when STDOUT is
                     not a tty).
  --no-raw           Force formatted output even when STDOUT is not a tty.
  --csv              Output in CSV format.
  --stat             Print rolling stats about server: mem, clients, ...
  --latency          Enter a special mode continuously sampling latency.
                     If you use this mode in an interactive session it runs
                     forever displaying real-time stats. Otherwise if --raw or
                     --csv is specified, or if you redirect the output to a non
                     TTY, it samples the latency for 1 second (you can use
                     -i to change the interval), then produces a single output
                     and exits.
  --latency-history  Like --latency but tracking latency changes over time.
                     Default time interval is 15 sec. Change it using -i.
  --latency-dist     Shows latency as a spectrum, requires xterm 256 colors.
                     Default time interval is 1 sec. Change it using -i.
  --lru-test <keys>  Simulate a cache workload with an 80-20 distribution.
  --replica          Simulate a replica showing commands received from the master.
  --rdb <filename>   Transfer an RDB dump from remote server to local file.
  --pipe             Transfer raw Redis protocol from stdin to server.
  --pipe-timeout <n> In --pipe mode, abort with error if after sending all data.
                     no reply is received within <n> seconds.
                     Default timeout: 30. Use 0 to wait forever.
  --bigkeys          Sample Redis keys looking for keys with many elements (complexity).
  --memkeys          Sample Redis keys looking for keys consuming a lot of memory.
  --memkeys-samples <n> Sample Redis keys looking for keys consuming a lot of memory.
                     And define number of key elements to sample
  --hotkeys          Sample Redis keys looking for hot keys.
                     only works when maxmemory-policy is *lfu.
  --scan             List all keys using the SCAN command.
  --pattern <pat>    Keys pattern when using the --scan, --bigkeys or --hotkeys
                     options (default: *).
  --intrinsic-latency <sec> Run a test to measure intrinsic system latency.
                     The test will run for the specified amount of seconds.
  --eval <file>      Send an EVAL command using the Lua script at <file>.
  --ldb              Used with --eval enable the Redis Lua debugger.
  --ldb-sync-mode    Like --ldb but uses the synchronous Lua debugger, in
                     this mode the server is blocked and script changes are
                     not rolled back from the server memory.
  --cluster <command> [args...] [opts...]
                     Cluster Manager command and arguments (see below).
  --verbose          Verbose mode.
  --no-auth-warning  Don't show warning message when using password on command
                     line interface.
  --help             Output this help and exit.
  --version          Output version and exit.

Cluster Manager Commands:
  Use --cluster help to list all available cluster manager commands.

Examples:
  cat /etc/passwd | redis-cli -x set mypasswd
  redis-cli get mypasswd
  redis-cli -r 100 lpush mylist x
  redis-cli -r 100 -i 1 info | grep used_memory_human:
  redis-cli --eval myscript.lua key1 key2 , arg1 arg2 arg3
  redis-cli --scan --pattern '*:12345*'

  (Note: when using --eval the comma separates KEYS[] from ARGV[] items)

When no command is given, redis-cli starts in interactive mode.
Type "help" in interactive mode for information on available commands
and settings.
```

```sh
# 查看所有配置信息
127.0.0.1:6379> config get *

# 查看具体某个配置信息，例如 protected-mode
127.0.0.1:6379> config get protected-mode

# 设置某个配置信息
127.0.0.1:6379> config set protected-mode

# 向数据库中插入一条数据 值为字符串类型
127.0.0.1:6379> set key value

# 获取数据库中某个key的值
127.0.0.1:6379> get key
```

+ 插入字符串

```sh
127.0.0.1:6379> set strkey strvalue

# 获取值
127.0.0.1:6379> get strkey
```

![redis_2021-02-20_17-29-56.png](../image/redis_2021-02-20_17-29-56.png)

+ 插入hash值

```sh
127.0.0.1:6379> hmset hashkey field1 "value1" field2 "value2"

# 获取值
127.0.0.1:6379> hget hashkey filed1
```

![redis_2021-02-20_17-44-16.png](../image/redis_2021-02-20_17-44-16.png)

+ 插入list表

```sh
127.0.0.1:6379> lpush listkey value1
127.0.0.1:6379> lpush listkey value2
127.0.0.1:6379> lpush listkey value3

# 获取list0到10个值
127.0.0.1:6379> lrange listkey 0 10
```

![redis_2021-02-20_17-34-19.png](../image/redis_2021-02-20_17-34-19.png)

+ 插入set集合

```sh
127.0.0.1:6379> sadd setkey value1
127.0.0.1:6379> sadd setkey value2
127.0.0.1:6379> sadd setkey value3

# 获取集合值
127.0.0.1:6379> smembers setkey
```

![redis_2021-02-20_17-36-08.png](../image/redis_2021-02-20_17-36-08.png)

+ 插入zset有序集合

```sh
zadd zsetkey 0 value1
zadd zsetkey 1 value2
zadd zsetkey 2 value3

# 获取集合0到100的值
ZRANGEBYSCORE zsetkey 0 100
```

![redis_2021-02-20_17-51-28.png](../image/redis_2021-02-20_17-51-28.png)