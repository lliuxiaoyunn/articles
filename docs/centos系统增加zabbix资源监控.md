# linux系统增加zabbix资源监控(四)

zabbix可以对服务器进行资源监控，如果你已经拥有zabbix-server，可以在浏览器中正常访问zabbix服务，你想再增加对其他服务器的资源监控，你只需要在被监控的机器上安装zabbix-agent，然后再在zabbix前端页面中添加主机即可。

下面，我们就来操作一下吧！

首先，准备好一台被监控的linux主机。如：centos8、ip：192.168.1.49

然后，在linux机器上安装zabbix-agent

```sh
# 更新数据源
rpm -Uvh https://repo.zabbix.com/zabbix/5.0/rhel/7/x86_64/zabbix-release-5.0-1.el7.noarch.rpm
yum clean all

# 安装zabbix-agent
dnf install -y zabbix-agent

# centos7
yum install -y zabbix-agent

```

然后，修改zabbix-agent的配置

```sh
vim /etc/zabbix/zabbix_agent.conf

Server=zabbix-server的机器ip
ListenIP=zabbix-agent的机器ip
ServerActive=zabbix-agent的机器ip:10051
Hostname=当前机器的名称
# 注意，这个当前机器名称，不建议为localhost，如果你的电脑为这个名称，建议修改，因为后面在zabbix上配置主机时要用这个名称，如果有n多个监控主机都用这个名称，自己也就比较难区分了

```

然后，启动zabbix-agent

```sh
# centos8
systemctl restart zabbix-agent.service

# 停止防火墙，或在防火墙上开放10050、 10051端口
systemctl stop firewalld

```

然后，浏览器访问你已经拥有的zabbix监控平台，登录后，进入 **Configuration > Hosts** 点击页面右上角的 **Create host** 按钮

![zabbix-11](image/zabbix-11.png)

页面中的‘Hostname’为你的被监控机器的hostname，也是你在zabbix-agent中填的，然后选择‘Groups’，填写好Agent的ip地址，确认最下面的‘Enabled’复选框勾选中，点击‘update’按钮。

再在主机列表中，找到自己添加的这个主机，进入‘templates’，选择一个‘Link new templates’，点击update，这样一个最基本的服务器资源监控就已经好了。

> 如果想要停止对某个机器的监控，可以点击Hosts列表的‘Status’状态，当为‘Disable’时，为禁用该服务主机

最后，查看新添加的服务器实时监控情况。

进入 **Monitoring > Hosts**  在列表中，即可看到新增加的监控主机，点击‘Graphs’列的链接，即可打开当前服务器资源监控情况

![zabbix-12](image/zabbix-12.png)



至此，我们的一个新服务监控已经弄好了。