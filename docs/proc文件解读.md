# proc虚拟文件系统解读

linux系统中，proc目录中是系统运行时的虚拟文件系统路径，存储的是当前内核运行状态的一系列特殊文件，用户可以通过这个目录中的文件，查看系统硬件及当前正在运行的进程的信息，也可以修改这些信息，来改变运行状态。

可以通过设置 /etc/sysctl.conf，手工设置内核参数值；也可以通过sysctl命令来设置。

```sh
sysctl -w variable=value	# 临时改变某个参数的值

sysctl -p <filename>	# 从指定文件加载系统参数，如果不指定，默认从/etc/sysctl.conf中加载

sysctl -a	# 显示所有内核参数和值
```

> 注： 用命令设置，只是临时改变，系统重启后，失效；想要固定修改，可以写在/etc/sysctl.conf文件中

[参考1](https://www.cnblogs.com/liushui-sky/p/9354536.html)

/proc/cpuinfo: 查看cpu处理器的相关信息

/proc/memifo:  查看系统中内存的使用状态信息，常由free命令使用；可以使用文件查看命令直接读取此文件，其内容显示为两列，前者为统计属性，后者为对应的值；

/proc/interrupts: 查看系统当前中断信息列表

/proc/mdstat：保存RAID相关的多块磁盘的当前状态信息

/proc/vmstat：当前系统虚拟内存的多种统计数据，信息量可能会比较大，这因系统而有所不同，可读性较好

/proc/slabinfo：在内核中频繁使用的对象（如inode、dentry等）都有自己的cache，即slab pool，而/proc/slabinfo文件列出了这些对象相关slap的信息

/proc/stat：实时追踪自系统上次启动以来的多种统计信息

/proc/swaps：当前系统上的交换分区及其空间利用信息，如果有多个交换分区的话，则会每个交换分区的信息分别存储于/proc/swap目录中的单独文件中，而其优先级数字越低，被使用到的可能性越大

/proc/zoneinfo：内存区域（zone）的详细信息列表，信息量较大

/proc/uptime：系统上次启动以来的运行时间

/proc/version：当前系统运行的内核版本号

/proc/buddyinfo：用于诊断内存碎片问题的相关信息文件

/proc/apm：高级电源管理（APM）版本信息及电池相关状态信息，通常由apm命令使用

/proc/cmdline：在启动时传递至内核的相关参数信息，这些信息通常由lilo或grub等启动管理工具进行传递

/proc/devices：系统已经加载的所有块设备和字符设备的信息，包含主设备号和设备组（与主设备号对应的设备类型）名

/proc/diskstats：每块磁盘设备的磁盘I/O统计信息列表

/proc/execdomains：内核当前支持的执行域（每种操作系统独特“个性”）信息列表

/proc/fb：帧缓冲设备列表文件，包含帧缓冲设备的设备号和相关驱动信息

/proc/filesystems：当前被内核支持的文件系统类型列表文件，被标示为nodev的文件系统表示不需要块设备的支持；通常mount一个设备时，如果没有指定文件系统类型将通过此文件来决定其所需文件系统的类型

/proc/iomem：每个物理设备上的记忆体（RAM或者ROM）在系统内存中的映射信息

/proc/ioports：当前正在使用且已经注册过的与物理设备进行通讯的输入-输出端口范围信息列表；如下面所示，第一列表示注册的I/O端口范围，其后表示相关的设备

/proc/kallsyms：模块管理工具用来动态链接或绑定可装载模块的符号定义，由内核输出；（内核2.5.71以后的版本支持此功能）；通常这个文件中的信息量相当大；

/proc/kcore：系统使用的物理内存，以ELF核心文件（core file）格式存储，其文件大小为已使用的物理内存（RAM）加上4KB；这个文件用来检查内核数据结构的当前状态，因此，通常由GBD通常调试工具使用，但不能使用文件查看命令打开此文件；

/proc/kmsg：此文件用来保存由内核输出的信息，通常由/sbin/klogd或/bin/dmsg等程序使用，不要试图使用查看命令打开此文件

/proc/loadavg：保存关于CPU和磁盘I/O的负载平均值，其前三列分别表示每1秒钟、每5秒钟及每15秒的负载平均值，类似于uptime命令输出的相关信息；第四列是由斜线隔开的两个数值，前者表示当前正由内核调度的实体（进程和线程）的数目，后者表示系统当前存活的内核调度实体的数目；第五列表示此文件被查看前最近一个由内核创建的进程的PID

/proc/locks：保存当前由内核锁定的文件的相关信息，包含内核内部的调试数据；每个锁定占据一行，且具有一个惟一的编号；如下输出信息中每行的第二列表示当前锁定使用的锁定类别，POSIX表示目前较新类型的文件锁，由lockf系统调用产生，FLOCK是传统的UNIX文件锁，由flock系统调用产生；第三列也通常由两种类型，ADVISORY表示不允许其他用户锁定此文件，但允许读取，MANDATORY表示此文件锁定期间不允许其他用户任何形式的访问

/proc/modules：当前装入内核的所有模块名称列表，可以由lsmod命令使用，也可以直接查看；如下所示，其中第一列表示模块名，第二列表示此模块占用内存空间大小，第三列表示此模块有多少实例被装入，第四列表示此模块依赖于其它哪些模块，第五列表示此模块的装载状态（Live：已经装入；Loading：正在装入；Unloading：正在卸载），第六列表示此模块在内核内存（kernel memory）中的偏移量

/proc/partitions：块设备每个分区的主设备号（major）和次设备号（minor）等信息，同时包括每个分区所包含的块（block）数目

/proc/pci：内核初始化时发现的所有PCI设备及其配置信息列表，其配置信息多为某PCI设备相关IRQ信息，可读性不高，可以用“/sbin/lspci –vb”命令获得较易理解的相关信息

[参考2](https://blog.csdn.net/genius_lg/article/details/30488203)

/proc/sys

| 路径                                                     | 文件                                                         | 用法                                                         |
| -------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| /proc/sys/kernel                                         | /msgmax                                                      | 指定从一个进程发送到另外一个进程的消息最大长度(bytes)进程间的消息传递是在内核的内存中进行的，不会交换到磁盘上，所以如果增加该值，则将增加操作系统所使用的内存数量。默认：8192 |
|                                                          | /msgmnb                                                      | 指定一个消息队列的最大长度(bytes)。默认：16384               |
|                                                          | /msgmni                                                      | 指定消息队列标识的最大数目                                   |
|                                                          | /panic                                                       | 如果内核发生严重错误，内核在重新引导之前等待的时间(秒)。默认：0 表示发生内核严重错误时，禁止自动重新引导 |
|                                                          | /shmall                                                      | 表示在任何给定时刻，系统可以使用的共享内存的总量(bytes)。    |
|                                                          | /shmmax                                                      | 表示内核所允许的最大共享内存段的大小(bytes)。建议为物理内存的一半 |
|                                                          | /shmmni                                                      | 表示用于整个系统的共享内存段的最大数目                       |
|                                                          | /shm_next_id                                                 |                                                              |
|                                                          | /shm_rmid_forced                                             |                                                              |
|                                                          | /threads-max                                                 | 表示内核所能使用的线程的最大数目                             |
| /proc/sys/vm                                             | /block_dump                                                  | 表示是否打开Block dump模式，用于记录所有的读写及dirty block写回动作 |
|                                                          | /dirty_background_ratio                                      | 表示脏数据到达系统整体内存的百分比,触发pdflush进程把脏数据写回磁盘 |
|                                                          | /dirty_expire_centisecs                                      | 表示如果脏数据在内存中驻留时间超过该值，pdflush进程在下一次将把这些数据写回磁盘 |
|                                                          | /dirty_ratio                                                 | 表示如果进程产生的脏数据到达系统整体内存的百分比，此时进程自行把脏数据写回磁盘 |
|                                                          | /dirty_writeback_centisecs                                   | 表示pdflush进程周期性间隔多久把脏数据写回磁盘                |
|                                                          | /vfs_cache_pressure                                          | 表示内核回收用于directory和inode cache内存的倾向。缺省值100表示内核将根据pagecache和swapcache，把directory和inode cache保持在一个合理的百分比；降低该值低于100，将导致内核倾向于保留directory和inode cache；增加该值超过100，将导致内核倾向于回收directory和inode cache |
|                                                          | /min_free_kbytes                                             | 表示强制Linux VM最低保留多少空闲内存                         |
|                                                          | /nr_pdflush_threads                                          | 表示当前正在运行的pdflush进程数量，在I/O负载高的情况下，内核会自动增加更多的pdflush进程 |
| /proc/sys/fs                                             | /file-max                                                    | 可以分配的**文件句柄的最大数目**                             |
|                                                          | /file-nr                                                     | 它有三个值，已分配的文件句柄数目、已使用的文件句柄的数目、文件句柄的最大数目 |
| /proc/sys/net/core主要用来控制内核和网络层之间的交互行为 | /message_burst                                               | 写新的警告消息所需的时间（以 1/10 秒为单位）；在这个时间内系统接收到的其它警告消息会被丢弃。这用于防止某些企图用消息“淹没”系统的人所使用的拒绝服务（Denial of Service）攻击 |
|                                                          | /message_cost                                                | 表示写每个警告消息相关的成本值。该值越大，越有可能忽略警告消息 |
|                                                          | /netdev_max_backlog                                          | 表示在每个网络接口接收数据包的速率比内核处理这些包的速率快时，允许送到队列的数据包的最大数目 |
|                                                          | /optmem_max                                                  | 表示每个套接字所允许的最大缓冲区的大小                       |
|                                                          | /rmem_default                                                | 指定了接收套接字缓冲区大小的缺省值                           |
|                                                          | /rmem_max                                                    | 接收套接字缓冲区大小的最大值（以字节为单位）                 |
|                                                          | /wmem_default                                                | 发送套接字缓冲区大小的缺省值（以字节为单位）                 |
|                                                          | /wmem_max                                                    | 发送套接字缓冲区大小的最大值（以字节为单位）                 |
| /proc/sys/net/ipv4                                       | /ip_forward                                                  | 是否打开ip路由，0 禁止；1 打开                               |
|                                                          | /ip_default_ttl                                              | 表示一个数据报的生存周期（Time To Live），即最多经过多少路由器。增加该值会降低系统性能 |
|                                                          | /ip_no_pmtu_disc                                             | 在全局范围内关闭路径MTU探测功能                              |
|                                                          | /route/min_pmtu                                              | 最小路径MTU的大小                                            |
|                                                          | /route/mtu_expires                                           | PMTU信息缓存多长时间（秒）                                   |
|                                                          | /route/min_adv_mss                                           | 最小的MSS（Maximum Segment Size）大小，取决于第一跳的路由器MTU |
|                                                          | /ipfrag_low_thresh<br/>/ipfrag_high_thresh                   | 重组IP分段的内存分配最低值和最高值                           |
|                                                          | /ipfrag_time                                                 | 一个IP分段在内存中保留多少秒                                 |
|                                                          | /inet_peer_threshold                                         | INET对端存储器某个合适值，当超过该阀值条目将被丢弃。该阀值同样决定生存时间以及废物收集通过的时间间隔。条目越多，存活期越低，GC 间隔越短 |
|                                                          | /inet_peer_minttl                                            | 条目的最低存活期。在重组端必须要有足够的碎片(fragment)存活期。这个最低存活期必须保证缓冲池容积是否少于 inet_peer_threshold。该值以 jiffies为单位测量。 |
|                                                          | /inet_peer_maxttl                                            | 条目的最大存活期。在此期限到达之后，如果缓冲池没有耗尽压力的话，不使用的条目将会超时。该值以 jiffies为单位测量 |
|                                                          | /inet_peer_gc_mintime                                        | 废物收集(GC)的最短间隔。这个间隔会影响到缓冲池中内存的高压力。 该值以 jiffies为单位测量 |
|                                                          | /inet_peer_gc_maxtime                                        | 废物收集(GC)的最大间隔，这个间隔会影响到缓冲池中内存的低压力。 该值以 jiffies为单位测量 |
|                                                          | /tcp_syn_retries                                             | 本机向外发起TCP SYN连接超时重传的次数，不应该高于255；该值仅仅针对外出的连接，对于进来的连接由tcp_retries1控制 |
|                                                          | /tcp_keepalive_probes                                        | 丢弃TCP连接前，进行最大TCP保持连接侦测的次数                 |
|                                                          | /tcp_keepalive_time                                          | 从不再传送数据到向连接上发送**保持连接信号之间所需的秒数**。默认：**7200秒** |
|                                                          | /tcp_retries1                                                | 放弃回应一个TCP连接请求前进行重传的次数                      |
|                                                          | /tcp_retries2                                                | 放弃在已经建立通讯状态下的一个TCP数据包前进行重传的次数      |
|                                                          | /tcp_orphan_retries                                          | 在近端丢弃TCP连接之前，要进行多少次重试                      |
|                                                          | /tcp_fin_timeout                                             | 本端断开的socket连接，TCP保持在FIN-WAIT-2状态的时间。对方可能会断开连接或一直不结束连接或不可预料的进程死亡。默认值为 60 秒。过去在2.2版本的内核中是 180 秒。您可以设置该值，但需要注意，如果您的机器为负载很重的web服务器，您可能要冒内存被大量无效数据报填满的风险，FIN-WAIT-2 sockets 的危险性低于 FIN-WAIT-1，因为它们最多只吃 1.5K的内存，但是它们存在时间更长 |
|                                                          | /tcp_max_tw_buckets                                          | 系统在同时所处理的最大timewait sockets 数目。如果超过此数的话，time-wait socket 会被立即砍除并且显示警告信息。之所以要设定这个限制，纯粹为了抵御那些简单的 DoS 攻击，千万不要人为的降低这个限制，不过，如果网络条件需要比默认值更多，则可以提高它 |
|                                                          | /tcp_tw_recyle                                               | 打开快速 TIME-WAIT sockets 回收                              |
|                                                          | /tcp_tw_reuse                                                | 是否允许重新应用处于TIME-WAIT状态的socket用于新的TCP连接     |
|                                                          | /tcp_max_orphans                                             | 系统所能处理不属于任何进程的TCP sockets最大数量。假如超过这个数量，那么不属于任何进程的连接会被立即reset，并同时显示警告信息。之所以要设定这个限制，纯粹为了抵御那些简单的 DoS 攻击，千万不要依赖这个或是人为的降低这个限制 |
|                                                          | /tcp_abort_on_overflow                                       | 当守护进程太忙而不能接受新的连接，就向对方发送reset消息，默认值是false。这意味着当溢出的原因是因为一个偶然的猝发，那么连接将恢复状态。只有在你确信守护进程真的不能完成连接请求时才打开该选项，该选项会影响客户的使用 |
|                                                          | /tcp_syncookies                                              | 表示是否打开TCP同步标签(syncookie)，内核必须打开了 CONFIG_SYN_COOKIES项进行编译。 同步标签(syncookie)可以防止一个套接字在有过多试图连接到达时引起过载 |
|                                                          | /tcp_stdurg                                                  | 使用 TCP urg pointer 字段中的主机请求解释功能。大部份的主机都使用老旧的BSD解释，因此如果您在 Linux 打开它，或会导致不能和它们正确沟通 |
|                                                          | /tcp_max_syn_backlog                                         | 对于那些依然还未获得客户端确认的连接请求，需要保存在队列中最大数目。对于超过 128Mb 内存的系统，默认值是 1024，低于 128Mb 的则为 128。如果服务器经常出现过载，可以尝试增加这个数字 |
|                                                          | /tcp_sack                                                    | 表示是否启用有选择的应答（Selective Acknowledgment），这可以通过有选择地应答乱序接收到的报文来提高性能 |
|                                                          | /tcp_timestamps                                              | 是否启用以一种比超时重发更精确的方法来启用对 RTT 的计算      |
|                                                          | /tcp_fack                                                    | 表示是否打开FACK拥塞避免和快速重传功能                       |
|                                                          | /tcp_dsack                                                   | 表示是否允许TCP发送“两个完全相同”的SACK                      |
|                                                          | /tcp_ecn                                                     | 示是否打开TCP的直接拥塞通告功能                              |
|                                                          | /tcp_reordering                                              | 表示TCP流中重排序的数据报最大数量                            |
|                                                          | /tcp_retrans_collapse                                        | 表示对于某些有bug的打印机是否提供针对其bug的兼容性           |
|                                                          | /ip_local_port_range                                         | 表示TCP／UDP协议打开的本地端口号                             |
|                                                          | /ip_nonlocal_bind                                            | 表示是否允许进程邦定到非本地地址                             |
|                                                          | /ip_dynaddr                                                  | 用于使用拨号连接的情况，可以使系统动能够立即改变ip包的源地址为该ip地址，同时中断原有的tcp对话而用新地址重新发出一个syn请求包，开始新的tcp对话。在使用ip欺骗时，该参数可以立即改变伪装地址为新的ip地址。该文件表示是否允许动态地址，如果该值非0，表示允许；如果该值大于1，内核将通过log记录动态地址重写信息 |
|                                                          | 优化系统套接字缓冲区                                         | net.core.rmem_max=16777216<br/>net.core.wmem_max=16777216    |
|                                                          | 优化TCP接收／发送缓冲区                                      | net.ipv4.tcp_rmem=4096 87380 16777216<br/>net.ipv4.tcp_wmem=4096 65536 16777216 |
|                                                          | 优化网络设备接收队列                                         | net.core.netdev_max_backlog=3000                             |
|                                                          | 关闭路由相关功能                                             | net.ipv4.conf.lo.accept_source_route=0 <br/>net.ipv4.conf.all.accept_source_route=0 <br/>net.ipv4.conf.eth0.accept_source_route=0 <br/>net.ipv4.conf.default.accept_source_route=0 |
|                                                          | 关闭路由相关功能                                             | net.ipv4.conf.lo.accept_redirects=0 <br/>net.ipv4.conf.all.accept_redirects=0 <br/>net.ipv4.conf.eth0.accept_redirects=0 <br/>net.ipv4.conf.default.accept_redirects=0 |
|                                                          | 关闭路由相关功能                                             | net.ipv4.conf.lo.secure_redirects=0 <br/>net.ipv4.conf.all.secure_redirects=0 <br/>net.ipv4.conf.eth0.secure_redirects=0 <br/>net.ipv4.conf.default.secure_redirects=0 |
|                                                          | 关闭路由相关功能                                             | net.ipv4.conf.lo.send_redirects=0<br/>net.ipv4.conf.all.send_redirects=0<br/>net.ipv4.conf.eth0.send_redirects=0<br/>net.ipv4.conf.default.send_redirects=0 |
|                                                          | 打开TCP SYN cookie选项，有助于保护服务器免受SyncFlood攻击    | net.ipv4.tcp_syncookies=1                                    |
|                                                          | 打开TIME-WAIT套接字重用功能，对于存在大量连接的Web服务器非常有效 | net.ipv4.tcp_tw_recyle=1<br/>net.ipv4.tcp_tw_reuse=1         |
|                                                          | 减少处于FIN-WAIT-2连接状态的时间，使系统可以处理更多的连接   | net.ipv4.tcp_fin_timeout=30                                  |
|                                                          | 减少TCP KeepAlive连接侦测的时间，使系统可以处理更多的连接    | net.ipv4.tcp_keepalive_time=1800                             |
|                                                          | 增加TCP SYN队列长度，使系统可以处理更多的并发连接            | net.ipv4.tcp_max_syn_backlog=8192                            |

