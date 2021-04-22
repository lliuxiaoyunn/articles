# mysql中重要的配置参数

## 查看配置

### 方法一：

在mysql的命令行窗口或客户端查询窗口中执行 ` show variables;` 执行完后，可以看到大概有500+个参数

### 方法二：

查看mysql的配置文件

```
/etc/my.cnf
/etc/mysql/my.cnf
/usr/etc/my.cnf
~/.my.cnf
```



## 修改参数

### 方法一：

设置全局参数值 `set global 参数名=参数值;`

### 方法二：

在配置文件中，设置参数和值



## 快速查找过滤参数

| 预期                       | 关键词      | 命令                               |
| -------------------------- | ----------- | ---------------------------------- |
| **innodb存储引擎**相关参数 | innodb      | `show variables like 'innodb_%';`  |
| **缓冲区**相关             | buffer_size | `show variables like '%buffer_%';` |
| **缓存**相关               | cacahe_     | `show variables like '%cache_%';`  |
| **最大**配置相关           | max_        | `show variables like 'max_%';`     |
| **限制**相关               | limit       | `show variables like '%limit';`    |
| **超时**相关               | timeout     | `show variables like '%timeout';`  |



## 参数讲解

| 参数                                          | 可能值                               | 用法                                                         |
| --------------------------------------------- | ------------------------------------ | ------------------------------------------------------------ |
| <font color="blue">max_connections</font>     | 151                                  | MySQL的最大连接数，如果服务器的并发连接请求量比较大，建议调高此值，以增加并行连接数量，当然这建立在机器能支撑的情况下，因为如果连接数越多，介于MySQL会为每个连接提供连接缓冲区，就会开销越多的内存，所以要适当调整该值，不能盲目提高设值。可以过'conn%'通配符查看当前状态的连接数量，以定夺该值的大小。 |
| max_connect_errors                            | 100                                  | 对于同一主机，如果有超出该参数值个数的中断错误连接，则该主机将被禁止连接。如需对该主机进行解禁，执行：FLUSH HOST。 |
| open_files_limit                              | 1048576                              | MySQL打开的文件描述符限制，默认最小1024;当open_files_limit没有被配置的时候，比较max_connections\*5和ulimit -n的值，哪个大用哪个;当open_file_limit被配置的时候，比较open_files_limit和max_connections\*5的值，哪个大用哪个 |
| table_open_cache                              | 2000                                 | MySQL每打开一个表，都会读入一些数据到table_open_cache缓存中，当MySQL在这个缓存中找不到相应信息时，才会去磁盘上读取。默认值64;假定系统有200个并发连接，则需将此参数设置为200*N(N为每个连接所需的文件描述符数目)；当把table_open_cache设置为很大时，如果系统处理不了那么多文件描述符，那么就会出现客户端失效，连接不上 |
| max_allowed_packet                            | 4M                                   | 接受的数据包大小；增加该变量的值十分安全，这是因为仅当需要时才会分配额外内存。例如，仅当你发出长查询或MySQLd必须返回大的结果行时MySQLd才会分配更多内存;该变量之所以取较小默认值是一种预防措施，以捕获客户端和服务器之间的错误信息包，并确保不会因偶然使用大的信息包而导致内存溢出。 |
| binlog_cache_size                             | 18446744073709500000                 | 一个事务，在没有提交的时候，产生的日志，记录到Cache中；等到事务提交需要提交的时候，则把日志持久化到磁盘。默认binlog_cache_size大小32K |
| <font color="blue">max_heap_table_size</font> | 16777216                             | 定义了用户可以创建的内存表(memory table)的大小。这个值用来计算内存表的最大行数值。这个变量支持动态改变 |
| <font color="blue">tmp_table_size</font>      | 16777216                             | 临时表大小                                                   |
| <font color="blue">read_buffer_size</font>    | 131072                               | 读入缓冲区大小。对表进行顺序扫描的请求将分配一个读入缓冲区，MySQL会为它分配一段内存缓冲区。read_buffer_size变量控制这一缓冲区的大小；如果对表的顺序扫描请求非常频繁，并且你认为频繁扫描进行得太慢，可以通过增加该变量值以及内存缓冲区大小提高其性能。 |
| read_rnd_buffer_size                          | 262144                               | 随机读缓冲区大小。当按任意顺序读取行时(例如，按照排序顺序)，将分配一个随机读缓存区。进行排序查询时，MySQL会首先扫描一遍该缓冲，以避免磁盘搜索，提高查询速度，如果需要排序大量数据，可适当调高该值。但MySQL会为每个客户连接发放该缓冲空间，所以应尽量适当设置该值，以避免内存开销过大 |
| <font color="blue">sort_buffer_size</font>    | 262144                               | 排序使用的缓冲大小。如果想要增加ORDER BY的速度，首先看是否可以让MySQL使用索引而不是额外的排序阶段；如果不能，可以尝试增加sort_buffer_size变量的大小 |
| <font color="blue">join_buffer_size</font>    | 262144                               | 联合查询操作所能使用的缓冲区大小，和sort_buffer_size一样，该参数对应的分配内存也是每连接独享 |
| thread_cache_size                             | 9                                    | 可以重新利用保存在缓存中线程的数量，当断开连接时如果缓存中还有空间，那么客户端的线程将被放到缓存中，如果线程重新被请求，那么请求将从缓存中读取,如果缓存中是空的或者是新的请求，那么这个线程将被重新创建,如果有很多新的线程，增加这个值可以改善系统性能 |
| query_cache_size                              | 1048576                              | 查询缓冲大小                                                 |
| query_cache_limit                             | 1048576                              | 单个查询能够使用的缓冲区大小                                 |
| key_buffer_size                               | 8388608                              | 用于索引的缓冲区大小，增加它可得到更好处理的索引(对所有读和多重写)，到你能负担得起那样多。如果你使它太大，系统将开始换页并且真的变慢了。对于内存在4GB左右的服务器该参数可设置为384M或512M。通过检查状态值Key_read_requests和Key_reads，可以知道key_buffer_size设置是否合理。 |
| ft_min_word_len                               |                                      | 分词词汇最小长度                                             |
| transaction_isolation                         | REPEATABLE-READ                      | 事物隔离级别                                                 |
| <font color="blue">slow_query_log</font>      | OFF                                  | 是否开启慢查询日志                                           |
| <font color="blue">long_query_time</font>     | 10                                   | 慢查询阀值时间                                               |
| slow_query_log_file                           | /var/lib/mysql/ebceb8215a85-slow.log | 慢查询日志文件路径                                           |
| lower_case_table_name                         | 0                                    | 表名不区分大小写                                             |
| default_storage_engine                        | innodb                               | 默认存储引擎                                                 |
| innodb_file_per_table                         |                                      | innodb表为独立空间                                           |
| <font color="blue">innodb_open_files</font>   | 2000                                 | 限制innodb能打开的表数据                                     |
| innodb_buffer_pool_size                       |                                      | 使用一个缓冲池来保存索引和原始数据的大小，设置越大,你在存取表里面数据时所需要的磁盘I/O越少 |
| innodb_write_io_threads                       | 4                                    |                                                              |
| innodb_read_io_threads                        | 4                                    | 线程处理数据页上的读写 I/O(输入输出)请求,根据你的 CPU 核数来更改 |
| innodb_thread_concurrency                     | 0                                    | 不限制并发数                                                 |
| innodb_purge_threads                          | 4                                    | 清除操作是否使用单独线程，默认0不使用，1使用                 |
| innodb_log_buffer_size                        |                                      | 日志文件所用的内存大小                                       |
| innodb_log_file_size                          |                                      | 数据日志文件的大小，更大的设置可以提高性能，但也会增加恢复故障数据库所需的时间 |
| innodb_log_files_in_group                     |                                      | 循环方式将日志文件写到多个文件                               |
| innodb_max_dirty_pages_pct                    |                                      | 主线程刷新缓存池中的数据，使脏数据比例小于多少               |
| innodb_lock_wait_timeout                      |                                      | 事务在被回滚之前可以等待一个锁定的超时秒数                   |
| interactive_timeout                           | 28800                                | 服务器关闭交互式连接前等待活动的秒数                         |
| <font color="blue">wait_timeout</font>        | 31536000                             | 服务器关闭非交互连接之前等待活动的秒数。在线程启动时，根据全局wait_timeout值或全局interactive_timeout值初始化会话wait_timeout值，取决于客户端类型(由mysql_real_connect()的连接选项CLIENT_INTERACTIVE定义)。参数默认值：28800秒（8小时） |

