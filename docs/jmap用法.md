# Jmap用法

官方参考：https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/tooldescr014.html#BABGAFEG

## 安装

linux下安装java8： `yum install java-1.8.0-openjdk-devel.x86_64 -y `

**注意**：在安装jdk8时，一定要安装全，如果没有安装全，系统将不能使用jvm自带的一些命令

## 简介

jdk8引入了任务控制，运行记录和用于诊断JVM和java应用程序问题的工具-jmap

该命令打印指定进程、核心文件或远程调试服务器的共享对象内存映射或堆内存详细信息

jmap常用的参数有： -heap、 -histo、 permstat

jmap使用监控命令： jmap -F -dump:format=b, file=filename.bin  进程pid

```shell
[root@vircent7 apache-tomcat-8.5.59]# jmap --help
Usage:
    jmap [option] <pid>
        (to connect to running process)
    jmap [option] <executable <core>
        (to connect to a core file)
    jmap [option] [server_id@]<remote server IP or hostname>
        (to connect to remote debug server)

where <option> is one of:
    <none>               to print same info as Solaris pmap
    -heap                to print java heap summary
    -histo[:live]        to print histogram of java object heap; if the "live"
                         suboption is specified, only count live objects
    -clstats             to print class loader statistics
    -finalizerinfo       to print information on objects awaiting finalization
    -dump:<dump-options> to dump java heap in hprof binary format
                         dump-options:
                           live         dump only live objects; if not specified,
                                        all objects in the heap are dumped.
                           format=b     binary format
                           file=<file>  dump heap to <file>
                         Example: jmap -dump:live,format=b,file=heap.bin <pid>
    -F                   force. Use with -dump:<dump-options> <pid> or -histo
                         to force a heap dump or histogram when <pid> does not
                         respond. The "live" suboption is not supported
                         in this mode.
    -h | -help           to print this help message
    -J<flag>             to pass <flag> directly to the runtime system

```

+ 选项
  + 无选项 将打印共享对象映射。对于目标 JVM 中加载的每个共享对象，将打印开始地址、映射大小和共享对象文件的完整路径
  + -dump:[live,] format=b, file=filename  默认生成hprof的二进制格式堆信息，可以使用jhat读取文件
  + -finalizerinfo  打印有关等待最终完成的对象的信息
  + -heap  打印使用的垃圾回收、头配置和按生成方式使用堆的堆摘要
  + -histo[:live]  打印堆的直方图。对于每个 Java 类，将打印对象数、内存大小（以字节为单位）和完全限定的类名
  + -clstats  打印类加载器对 Java 堆的明智统计信息。将打印每个类加载程序的名称、活动状态、地址、父类加载程序以及已加载的类的数量和大小
  + -F  当 pid 不响应时 可以和 -dump 或 -histro 一起使用

### jconsole

启动图形控制台，用于监视和管理java应用程序

### jps

列出所有的java进程

-q： 指定jps只输出进程ID

-M: 输出传递给JAVA进程的参数

-l： 输出主函数的完整路径

-v： 显示传递给java虚拟机的参数

### jstat

用于观察java堆信息的详细情况，

jstat -<option> [-t] [-h<lines>] <vmid> [<interval>] [<count>]

-class： 监视类装载、卸载数量、总空间以及类装载所耗费的时间

-gc： 监视java堆状况，包括eden区、survivor区、老年代、元空间的容量、已用空间、GC时间合计等信息

-gccapacity：监视的内容与-gc基本相同，但输出主要关注Java堆各个区域使用到的最大、最小空间

-gcutil：监视内容与-gc基本相同，但输出主要关注已使用空间占总空间的百分比

-gccause：与-gcutil功能一样，但是会额外输出导致上一次GC产生的原因

-gcnew：监视新生代GC状况

-gcnewcapacity： 监视内容与-gcnew基本相同，输出主要关注使用到的最大、最小空间

-gcold：监视老年代GC状况

-gcoldcapacity：监视内容与-gcold基本相同，输出主要关注使用到的最大、最小空间

-gcpermcapacity：输出永久代使用到的最大、最小空间

-compiler：输出JIT编译器编译过的方法、耗时信息

-printcompliation：输出已经被JIT编译的方法

-t 参数表示输出时间戳、-h 参数表示在多少行后输出一个表头、vmid 则是虚拟机的进程ID、interval 和 count 表示输出间隔以及输出次数











