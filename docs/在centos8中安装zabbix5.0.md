# 在centos8中安装zabbix5.0(二)

## 安装与配置

1、设置yum源

```sh
rpm -Uvh https://repo.zabbix.com/zabbix/5.0/rhel/8/x86_64/zabbix-release-5.0-1.el8.noarch.rpm
dnf clean all
```

2、安装zabbix server、web前端、agent

```sh
dnf install -y zabbix-server-mysql zabbix-web-mysql zabbix-nginx-conf zabbix-agent
```

3、创建mysql数据库

centos8中，安装最新的mysql数据库

```sh
# 安装mysql8
sudo dnf install @mysql

# 启动mysql 和配置开机自启动
sudo systemctl enable --now mysqld
sudo systemctl daemon-reload
# 查看mysql服务状态
sudo systemctl status mysqld

# 添加密码及安全设置
sudo mysql_secure_installation
	# 输入： y
	# 设置密码策略等级0为低、1为中、2为强，此次输入：0
	# 输入两次密码，密码长度大于8位：zabbixmysql
	# 确认是否继续使用提供的密码，输入：y
	# 是否移除匿名登录： 输入：y
	# 不允许root远程登录？ 输入：n
	# 移除test数据库？ 输入：y
	# 重载权限表？ 输入：y
	
# 登录数据库
mysql -uroot -pzabbixmysql

# 出现 mysql> 开头，说明进入成功
```

执行

```sh
# 设置数据库字符集
mysql> create database zabbix character set utf8 collate utf8_bin;

# 创建用户
mysql> create user zabbix@localhost identified by 'zabbixmysql';

# 授权
mysql> grant all privileges on zabbix.* to zabbix@localhost;

# 刷新权限
mysql> flush privileges;

# 退出
mysql> quit;
```

4、初始化zabbix数据库

```sh
zcat /usr/share/doc/zabbix-server-mysql/create.sql.gz | mysql -uzabbix -pzabbixmysql zabbix

# 执行过程可能会有警告提示，可以忽略
# 执行时间会有点长， 切忌中断
```

> 如果上述方法无法成功，可以下载create.sql.gz文件，解压出里面sql脚本，放到Navicat中执行

5、配置zabbix-server

```sh
vim /etc/zabbix/zabbix_server.conf

# 增加如下
DBPassword=zabbixmysql

# DBPort，如果你修改了mysql的端口，则要添加该配置，没有修改，则不需要
```

> 其他配置信息，可参考文章后部分讲解

6、配置zabbix前端

```sh
vim /etc/nginx/conf.d/zabbix.conf

# 修改启用端口和域名,去掉前面的 # 号
listen	80;
server_name	192.168.1.230;

```

7、配置php服务时区

```sh
vim /etc/php-fpm.d/zabbix.conf

# 去掉前面的 ';  ',修改值为  Asia/Shanghai 
php_value[date.timezone] = Asia/Shanghai

# 可供参考时区如下：
# Asia/Shanghai – 上海
# Asia/Chongqing – 重庆
# Asia/Urumqi – 乌鲁木齐
# Asia/Hong_Kong – 香港
# Asia/Macao – 澳门
# Asia/Taipei – 台北
# Asia/Singapore – 新加坡
```

8、启动zabbix的server\agent\nginx\php-fpm

```sh
sudo systemctl restart zabbix-server zabbix-agent nginx php-fpm
sudo systemctl enable zabbix-server zabbix-agent nginx php-fpm
```

## 其他配置

```sh
# 配置系统策略
vim /etc/selinux/config
SELINUX=permissive
重启电脑

# 关闭防火墙或开通端口
systemctl stop firewalld

# 配置文件
/etc/zabbix/zabbix_server.conf
/etc/zabbix/zabbix_agentd.conf

# 日志
/var/log/zabbix/zabbix_server.log
/var/log/zabbix/zabbix_agent.log
```

**zabbix_agent配置**

```sh
# zabbix_agent.conf中配置说明

# vim /etc/zabbix/zabbix_agent.conf

############ GENERAL PARAMETERS ########通用参数#########
# PidFile	Pid文件
PidFile=/var/run/zabbix/zabbix_agentd.pid

# LogType	日志类型，system\file\console，默认file
# LogFile	日志文件
LogFile=/var/log/zabbix/zabbix_agentd.log
# LogFileSize 	日志大小，0-1024MB，0禁用自动日志轮换
LogFileSize=0
# DebugLevel	调试级别，0~5，默认为3显示waring信息

# SourceIP 源ip，默认为空，可以写机器ip地址
SourceIP=机器ip

# AllowKey	允许执行的项目键
# DenyKey

# Server	zabbix-server的ip或名称，列出主机接受传入的连接
Server=主控机器ip
# ListenPort	监听端口，默认10050
# ListenIP	监听ip，zabbix-agent的ip
ListenIP=机器ip

# StartAgents	监听的服务，zabbix-server的ip地址
ServerActive=主控机器ip:10051

# Hostname	主机名zabbix-agent的ip，在zabbix-web上添加hosts时用这个名称
Hostname=机器的名称
# HostnameItem	


############ ADVANCED PARAMETERS #################

# Include
Include=/etc/zabbix/zabbix_agentd.d/*.conf

```

**zabbix_server😊配置说明**

```sh
# zabbix_server.conf中配置说明

# vim /etc/zabbix/zabbix_server.conf

############ GENERAL PARAMETERS ########通用参数#########
# ListenPort 监听端口，默认10051

# SourceIP 源ip，默认为空，可以写机器ip地址
SourceIP=机器ip

# LogType	日志类型，system\file\console，默认file
# LogFile 	日志路径，默认/var/log/zabbix/zabbix_server.log
LogFile=/var/log/zabbix/zabbix_server.log
# LogFileSize 	日志大小，0-1024MB，0禁用自动日志轮换
LogFileSize=0
# DebugLevel	调试级别，0~5，默认为3显示waring信息

# PidFile	pid文件，默认/var/run/zabbix/zabbix_server.pid
PidFile=/var/run/zabbix/zabbix_server.pid
# SockerDir	socker文件夹，默认/var/run/zabbix
SocketDir=/var/run/zabbix

# DBHOst	数据库地址，默认127.0.0.1
# DBName	数据库名称，默认 zabbix
DBName=zabbix
# DBSchema	数据库dschema，默认 空
# DBUser	数据库用户，默认zabbix
DBUser=zabbix
# DBPassword	数据库密码
DBPassword=zabbixmysql
# DBSocket	DBScoket地址
# DBPort	数据库端口，默认为空，

# HistoryStorageURL	历史存储的HTTP地址
# HistoryStorageTypes	用逗号分隔的类型列表，uint\dbl\str\log\text
# HistoryStorageDateIndex	是否历史记录预处理 0 disable，1 enable

# ExportDir	导出路径
# ExportFileSize	导出文件大小1M~1G，默认1G

############ ADVANCED PARAMETERS ################
# StartPollers	预分叉的轮询器实例数，默认5
# StartIPMIPollers	IPMI轮询器数量
# StartPreprocessors	启动预处理器数量，默认3
# StartPollersUnreachable	无法访问是轮询次数
# StartTrappers		
# StartPingers	ICMP预习处理数
# StartDiscoverers	发现者预处理数
# StartHTTPPollers	HTTP查询器预处理数
# StartTimers	计时器数
# JavaGateway	zabbix网关ip地址或主机名，仅在启动java轮询器时需要
JavaGateway=机器当前ip

# JavaGatewayPort	zabbix网关的监听端口，默认10052
# StartJavaPollers	java轮询器预处理数
StartJavaPollers=5

# StartVMwareCollectors	虚拟收集器的数量
# SNMPTrapperFile	SNMPtrapper文件，从snmp守护进程传递到服务器的临时文件
SNMPTrapperFile=/var/log/snmptrap/snmptrap.log
# StartSNMPTrapper	为1，启动SNMPTrapper
# ListenIP	trapper监听的端口列表，用逗号分隔

# CacheSize	缓存

# Timeout	SNMP服务和外部检查超时时间
Timeout=4

# AlertScriptsPath	预警脚本位置
AlertScriptsPath=/usr/lib/zabbix/alertscripts

# ExternalScripts	外部脚本路径
ExternalScripts=/usr/lib/zabbix/externalscripts

# LogSlowQueries	定义数据库慢查询时长，单位毫秒
LogSlowQueries=3000

# StatsAllowedIP	允许访问的ip列表，用逗号分隔0.0.0.0/0代表所有ipv4地址
StatsAllowedIP=0.0.0.0/0

####### LOADABLE MODULES #######
# ...
```

## 访问zabbix

在浏览器中输入： http://机器ip/	用户\密码：Admin\zabbix

![zabbix-08](image/zabbix-08.png)

## 卸载

```sh
# 卸载 zabbix-server
yum remove zabbix-server
# 或 dnf autoremove zabbix-server

# 卸载 zabbix-agent
yum remove zabbix-agent
# 或 dnf autoremove zabbix-agent
```

