# grafana+prometheus对tomcat监控

tomcat作为java项目首选的部署容器，还是非常受大家欢迎的。但是，当你在做测试，或者是在运维管理生产服务器的时候，想要监控tomcat的实时运行情况，却不是那么容易的。

今天，就给大家讲一种，非常容易上手，搭建出来的监控平台，又非常高大上的解决方案。

## 获取jvm_exporter

浏览器访问：https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/

![tomcat_2020-11-19_16-40-33](image\tomcat_2020-11-19_16-40-33.png)

页面中显示了多个版本，可以根据自己需要选择版本，找到你需要的jar包下载地址：https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.14.0/jmx_prometheus_javaagent-0.14.0.jar

进入tomcat服务器，执行下面命令，下载jvm_exporter

```
wget https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.14.0/jmx_prometheus_javaagent-0.14.0.jar
```

拷贝下载的jar包，到tomcat的bin文件夹中

## 配置tomcat.yaml文件

在tomcat的bin文件夹下，新建tomcat.yaml文件，黏贴

```yaml
---   
lowercaseOutputLabelNames: true
lowercaseOutputName: true
rules:
- pattern: 'Catalina<type=GlobalRequestProcessor, name=\"(\w+-\w+)-(\d+)\"><>(\w+):'
  name: tomcat_$3_total
  labels:
    port: "$2"
    protocol: "$1"
  help: Tomcat global $3
  type: COUNTER
- pattern: 'Catalina<j2eeType=Servlet, WebModule=//([-a-zA-Z0-9+&@#/%?=~_|!:.,;]*[-a-zA-Z0-9+&@#/%=~_|]), name=([-a-zA-Z0-9+/$%~_-|!.]*), J2EEApplication=none, J2EEServer=none><>(requestCount|maxTime|processingTime|errorCount):'
  name: tomcat_servlet_$3_total
  labels:
    module: "$1"
    servlet: "$2"
  help: Tomcat servlet $3 total
  type: COUNTER
- pattern: 'Catalina<type=ThreadPool, name="(\w+-\w+)-(\d+)"><>(currentThreadCount|currentThreadsBusy|keepAliveCount|pollerThreadCount|connectionCount):'
  name: tomcat_threadpool_$3
  labels:
    port: "$2"
    protocol: "$1"
  help: Tomcat threadpool $3
  type: GAUGE
- pattern: 'Catalina<type=Manager, host=([-a-zA-Z0-9+&@#/%?=~_|!:.,;]*[-a-zA-Z0-9+&@#/%=~_|]), context=([-a-zA-Z0-9+/$%~_-|!.]*)><>(processingTime|sessionCounter|rejectedSessions|expiredSessions):'
  name: tomcat_session_$3_total
  labels:
    context: "$2"
    host: "$1"
  help: Tomcat session $3 total
  type: COUNTER
- pattern: ".*"
```

## 修改catalina.sh文件

进入tomcat的bin文件夹，编辑catalina.sh文件，增加如下：

```
JAVA_OPTS="-javaagent:./jmx_prometheus_javaagent-0.14.0.jar=3088:./tomcat.yaml"

# jmx_prometheus_javaagent-0.14.0.jar 这个根据你自己下载的jvm_export修改
# 30188 监控的端口，自行设置
```

## 验证tomcat监控

执行 `./startup.sh`  看能否正常启动， 如果没有报错，可以执行

```sh
curl -s http://localhost:3088
```

能正常返回信息，就说明监控正常

## 安装grafana

浏览器访问：https://grafana.com/grafana/download

根据页面中的教程，在对应的操作系统上安装grafana， 如用于安装监控平台的机器(监控机)为centos系统

```
wget https://dl.grafana.com/oss/release/grafana-7.3.3-1.x86_64.rpm
sudo yum install grafana-7.3.3-1.x86_64.rpm
```

## 下载prometheus

浏览器访问：https://prometheus.io/download/  在页面第1个表格中，找到你要下载的对应版本，在监控机上执行

```
# 下载
wget https://github.com/prometheus/prometheus/releases/download/v2.22.2/prometheus-2.22.2.linux-amd64.tar.gz

# 解压
tar -xzvf prometheus-2.22.2.linux-amd64.tar.gz
```

## 修改prometheus.yml文件

在prometheus解压后的文件夹中，找到prometheus.yml文件，编辑，在最后面添加

```
vim prometheus.yml

- job_name: 'tomcat_export'
  static_configs:
  - targets: ['被监控机器ip:3088']
  
  
# 30188是前面在tomcat中配置的监控端口
```

![tomcat_2020-11-19_17-36-16](image\tomcat_2020-11-19_17-36-16.png)

> 注意：如果被监控的服务器和 安装了prometheus的机器不是同一台，还需要保证机器间网络和防火墙通畅

## 启动prometheus

在prometheus解压的文件夹中，执行：`./prometheus`

## 验证prometheus

在浏览器中访问： http://prometheus机器ip:9090

![tomcat_2020-11-19_17-47-12](image\tomcat_2020-11-19_17-47-12.png)

> 注意：prometheus机器的防火墙要开放9090端口，浏览器才能正常访问

想查看prometheus监控jvm信息，可以在界面中执行，jvm_info

![tomcat_2020-11-19_17-49-35](image\tomcat_2020-11-19_17-49-35.png)

## 启动grafana

在安装了grafana的机器上，执行： `systemctl restart grafana-server`

## 配置grafana+prometheus

浏览器访问 http://grafana机器ip:3000， 用admin\admin登录

添加datasource，选择prometheus，配置信息，保存

![tomcat_2020-11-19_17-58-33](image\tomcat_2020-11-19_17-58-33.png)

引入模板

![tomcat_2020-11-19_18-00-58](image\tomcat_2020-11-19_18-00-58.png)

可以输入：<font color='blue'>**8563**</font>

![tomcat_8563-1](image\tomcat_8563-1.png)![tomcat_2020-11-20_14-27-54](image\tomcat_2020-11-20_14-27-54.png)

或者可以用：<font color='blue'>**3457**</font>

![tomcat_3457-1](image\tomcat_3457-1.png)![tomcat_3457-2](image\tomcat_3457-2.png)



至此，用prometheus监控tomcat的监控平台已经搭建完成。