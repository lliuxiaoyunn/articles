# 即便你是拥有最低配置的linux，你也拥有无限巨大的财富

在我们的生活中，经常会遇到这样一种情况，为了学习某个技术，我们需要去买台配置比较高的电脑，获取从云服务器提供商哪里购买云服务器。不管你选择哪种方式，成本总是需要的。

那有没有什么办法，不花钱办事，或者少花钱，办大事呢？

今天，我就给你讲一种，可以无限放到你的效益的方法。

+ 首先，在你的电脑上安装virtualbox软件。至于你自己的电脑怎么样，无所谓。
+ 然后，下载centos7的ios文件(其他linux系统的ios文件也可以)
+ 然后，用virtualbox安装centos7系统。配置信息时，注意把磁盘配置大些，至于CPU和内存，可以根据自己电脑实际情况，自行设置大小。
+ 然后，在安装好的linux中，安装docker

```shell
# 安装
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun

or
curl -sSL https://get.daocloud.io/docker | sh

# 配置加速 ---可选
vim /etc/docker/daemon.json
{"registry-mirrors":["https://reg-mirror.qiniu.com/"]}

# 启动docker
systemctl enable docker
systemctl restart docker
```



- 然后，再在虚拟机中，下载自己想要的任何linux操作系统镜像

```shell
# 如 下载centos7镜像
docker pull daocloud.io/library/centos:7
```

> 想要下载linux的其他版本，或者其他linux，都可以在 hub.docker.com网站上下载



+ 然后，使用上一步下载的镜像，创建liunx容器

```shell
# 创建容器时开启特权模式，不然，在容器中，执行某些命令是会报 Failed to get D-Bus connection: Operation not permitted
docker run -itd --name 容器名 --privileged=true -p 宿主机端口:容器端口 daocloud.io/library/centos:7 /usr/sbin/init
```



+ 然后，进入容器中，安装自己想要的软件

```shell
# 进入容器
docker exec -it 容器名 /bin/bash

# 进入后，可以安装自己想安装的任意软件
```



至此，你已经用virtualbox工具，虚拟出了一台linux机器，并且实现了，在linux机器中，再创建你想要任意版本的linux系统容器，进入到这个容器中后，你就可以像普通linux机器一样使用了。

现在，我们在学习阶段，想要在linux机器中，练习安装什么软件，搭建环境，完全可以在这个linux容器中练习了。

**但是，这还不是最完美的**。

比如说，你现在想要在linux系统中安装某个软件，这个软件，你本地已经有安装包，你想直接使用本地包，不想再在容器中去下载；另外，当你在linux容器中，搭建了某个服务，你想通过本地浏览器访问服务，发现无法访问。这些又应该怎么做呢？

+ 首先，我们要学习一个docker新命名，拷贝cp命令，掌握了这个考本命令，再也不用害怕文件互传问题了。

```shell
# docker cp命令
# 从宿主机拷贝文件到容器中
docker cp [OPTIONS] SRC_PATH|- CONTAINER:DEST_PATH
docker cp 宿主机文件路径 容器名称:/容器中的路径

# 从容器中拷贝文件到本地当前路径
docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
docker cp 容器名称:/容器中文件路径 $PWD

```



+ 接下来，我们还需要掌握，自己制作私有镜像命令。

```shell
# 先停止容器

# 制作私有镜像
docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]

OPTIONS说明：

-a :提交的镜像作者；

-c :使用Dockerfile指令来创建镜像；

-m :提交时的说明文字；

-p :在commit时，将容器暂停。

# 实例：
docker commit -a "allen" -m "这是一个案例" 容器名称 自定义镜像名称:tag版本

# -a -m 都可以不写；
# 自定义镜像名称:tag版本  也可以只写 自定义镜像名称
```



掌握了制作私有镜像，你就可以先在容器中练习搭建自己的环境，待环境搭建好了，你已经知道需要开放哪些端口了，把端口自己记下来，然后，从容器中出来，停止容器，开始把容器制作为自己的私有镜像。待镜像制作成功后，你再用自己的私有镜像创建一个新的容器，在创建时添加-p参数来开放端口就可以了，这样，就再也不用担心端口开放的不够用了。

```shell
# 使用私有镜像创建容器
docker run -itd --name 容器名 --privileged=true -p 宿主机端口:容器端口 私有镜像名称:tag版本
```



**有了上面这些操作步骤，基本上，你可以无限去造容器去进行练习了，如果练习失败，只需要几秒钟重新创建一个linux容器，又有了一个全新的linux系统了。**

如果，你还想着把自己做好的私有镜像，保存下来，或者传递到另外电脑上，可以继续往下看。

如果这个需求，是在同一个局域网中，你可以先保存私有镜像，然后再使用ftp(scp)方式即可传递给对方；如果不是在一个局域网中，那就先保存私有镜像，下载本地，再传给对方咯。

```shell
# 保存私有镜像
docker save -o IMAGE [IMAGE...]
docker save -o 保存后的文件名.tar 镜像名称:tag版本

# 实例
docker save -o pnginx.tar cnginx:0.1

# =================================================

# 导入上一步生成的镜像文件
docker load [OPTIONS]
OPTIONS 说明：

--input , -i : 指定导入的文件，代替 STDIN。

--quiet , -q : 精简输出信息。

# 实例
docker -i pnginx.tar
```



docker save和docker export对比

```tex
docker save和docker export的区别：

docker save保存的是镜像（image），docker export保存的是容器（container）；
docker load用来载入镜像包，docker import用来载入容器包，但两者都会恢复为镜像；
docker load不能对载入的镜像重命名，而docker import可以为镜像指定新名称。
```

