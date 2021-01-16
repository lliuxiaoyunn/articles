# sysctl与网络相关的配置

## 简介

sysctl 用于运行时配置内核参数，这些参数位于/proc/sys目录下。期中，包含了TCP/IP堆栈和虚拟内存等高级配置项。

linux系统在启动时，systemd-sysctl会根据优先级，依次读取

 ① /etc/sysctl.d/\*.conf

 ② /run/sysctl.d/\*.conf

 ③ /usr/lib/sysctl.d/*.conf  文件读取到sysctl内核参数



### 帮助信息

```sh
[root@localhost ~]# sysctl --help

Usage:
 sysctl [options] [variable[=value] ...]

Options:
  -a, --all            display all variables
  -A                   alias of -a
  -X                   alias of -a
      --deprecated     include deprecated parameters to listing
  -b, --binary         print value without new line
  -e, --ignore         ignore unknown variables errors
  -N, --names          print variable names without values
  -n, --values         print only values of the given variable(s)
  -p, --load[=<file>]  read values from file
  -f                   alias of -p
      --system         read values from all system directories
  -r, --pattern <expression>
                       select setting that match expression
  -q, --quiet          do not echo variable set
  -w, --write          enable writing a value to variable
  -o                   does nothing
  -x                   does nothing
  -d                   alias of -h

 -h, --help     display this help and exit
 -V, --version  output version information and exit

For more details see sysctl(8).

```



### 帮助说明

```sh
名字
       sysctl - 在运行时配置内核参数
语法
       sysctl [options] [variable[=value]] [...]
       sysctl -p [file or regexp] [...]
描述
       sysctl 可以在运行时配置内核参数。所有可用参数都位于 /proc/sys/ 目录下。
参数与选项
       variable
              要读取其值的变量，比如"kernel.ostype"。[提示]"."也可以用"/"代替。
       variable=value
              要设置变量及相应的值。必须同时使用 -w 选项。
              如果值中含有特殊意义的shell字符或引号，那么你最好使用双引号进行界定。
       -n, --values
              显示变量值的同时不显示变量名
       -e, --ignore
              忽略不正确的变量名而不报错
       -N, --names
              仅显示变量名。常用于脚本中。
       -q, --quiet
              不在 stdout 上显示变量值
       -w, --write
              如果你想修改变量的值，就必须使用此选项
       -p[FILE], --load[=FILE]
              从指定文件(默认 /etc/sysctl.conf)中加载已经设置好的一系列变量值。
              如果使用 - 作为文件名，那么表示从 stdin 读取配置。
              FILE 还可以是一个正则表达式，以匹配多个文件。
       -a, --all
              显示所有当前的变量名
       --deprecated
              在 --all 的输出中包含已被反对使用的参数
       -b, --binary
              打印值时不添加换行标记
       --system
              从所有下列配置文件中加载系统设置
              /run/sysctl.d/*.conf
              /etc/sysctl.d/*.conf
              /usr/local/lib/sysctl.d/*.conf
              /usr/lib/sysctl.d/*.conf
              /lib/sysctl.d/*.conf
              /etc/sysctl.conf
       -r, --pattern pattern
              仅应用与正则表达式匹配的文件中的设置。
       -h, --help
              显示帮助信息后退出
       -V, --version
              显示版本信息后退出
```



## 使用

查看sysctl所有配置

```shell
sysctl -a
```



过滤与net相关的信息

```shell
sysctl -a |grep "net" > outfile.txt
```



## 重要配置说明

| 参数                             | 用法                                                         |
| -------------------------------- | ------------------------------------------------------------ |
| net.core.wmem_max                | 最大socket<font color="blue">写</font>buffer,可参考的优化值:873200 |
| net.core.wmem_default            |                                                              |
| net.core.rmem_max                | 最大socket<font color="blue">读</font>buffer,可参考的优化值:873200 |
| net.core.rmem_default            |                                                              |
| net.core.optmem_max              | socket buffer的最大初始化值                                  |
| net.core.netdev_max_backlog      | 进入包的<font color="blue">最大设备队列</font>.对重负载服务器而言,该值太低,可调整到1000 |
| net.core.somaxconn               | listen()的默认参数,<font color="blue">挂起请求的最大数量</font>.对繁忙的服务器,增加该值有助于网络性能.可调整到256 |
| net.ipv4.tcp_wmem                | TCP<font color="blue">写</font>buffer,可参考的优化值: 8192 436600 873200 |
| net.ipv4.tcp_rmem                | TCP<font color="blue">读</font>buffer,可参考的优化值: 32768 436600 873200 |
| net.ipv4.tcp_mem                 | 有3个值，【**<font color="blue">1</font>**低于此值,TCP没有内存压力 **<font color="blue">2</font>**在此值下,进入内存压力阶段 **<font color="blue">3</font>**高于此值,TCP拒绝分配socket】 这三个值是单位是页，参考的优化值是:786432 1048576 1572864 |
| net.ipv4.**tcp_max_syn_backlog** | 进入<font color="blue">SYN包的最大请求队列</font>.对重负载服务器,增加该值显然有好处.可调整到8192 |
| net.ipv4.tcp_retries2            | TCP失败重传次数,默认值15,意味着重传15次才彻底放弃.可减少到5,以尽早释放内核资源 |
| net.ipv4.**tcp_keepalive_time**  | 默认7200s(2小时)；参考：1800s                                |
| net.ipv4.tcp_keepalive_intvl     | 默认75； 参考：30                                            |
| net.ipv4.tcp_keepalive_probes    | 默认9  <font color="blue">意思是如果某个TCP连接在idle 2个小时后,内核才发起probe.如果probe 9次(每次75秒)不成功,内核才彻底放弃,认为该连接已失效</font>。 参考：3 |
| net.ipv4.**ip_local_port_range** | <font color="blue">指定开启的端口范围</font>                 |
| net.ipv4.tcp_syncookies          | 表示开启SYN Cookies。当出现SYN等待队列溢出时，启用cookies来处理，可防范少量SYN攻击；0，表示关闭； |
| net.ipv4.tcp_syn_retries         |                                                              |
| net.ipv4.tcp_synack_retries      |                                                              |
| net.ipv4.**tcp_tw_reuse**        | <font color="blue">表示开启重用</font>。允许将TIME-WAIT sockets重新用于新的TCP连接 |
| net.ipv4.**tcp_fin_timeout**     | 表示如果套接字由本端要求关闭，这个参数决定了它保持在FIN-WAIT-2状态的时间 |
| net.ipv4.tcp_max_tw_buckets      | 表示系统同时保持TIME_WAIT套接字的最大数量，如果超过这个数字，TIME_WAIT套接字将立刻被清除并打印警告信息。对于Apache、Nginx等服务器，前面的参数可以很好地减少TIME_WAIT套接字数量，但是对于Squid，效果却不大。此项参数可以控制TIME_WAIT套接字的最大数量，避免Squid服务器被大量的TIME_WAIT套接字拖死。 |

