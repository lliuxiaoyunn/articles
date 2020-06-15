# locust的‘1’版本时代变化

斗转星移，时间已经进入2020年，在2020年5月26日，locust也进入了 ’1‘版本时代，有用过locust的，应该都知道，以前locust的版本号都是0开头，那现在这个1.0.*版本与以前的版本有些什么区别呢？

## Ⅰ 安装变化

安装的命令已经统一为 

```powershell
pip install locust
```

如果使用 locustio，则必须指定以前0开头的版本，不然安装会报错。

## Ⅱ 参数变化

```powershell
D:\>locust --help
Usage: locust [OPTIONS] [UserClass ...]

Common options:
  -h, --help            show this help message and exit
  -f LOCUSTFILE, --locustfile LOCUSTFILE
                        Python module file to import, e.g. '../other.py'.
                        Default: locustfile
  --config CONFIG       Config file path
  -H HOST, --host HOST  Host to load test in the following format:
                        http://10.21.32.33
  -u NUM_USERS, --users NUM_USERS
                        Number of concurrent Locust users. Only used together
                        with --headless
  -r HATCH_RATE, --hatch-rate HATCH_RATE
                        The rate per second in which users are spawned. Only
                        used together with --headless
  -t RUN_TIME, --run-time RUN_TIME
                        Stop after the specified amount of time, e.g. (300s,
                        20m, 3h, 1h30m, etc.). Only used together with
                        --headless
  -l, --list            Show list of possible User classes and exit

Web UI options:
  --web-host WEB_HOST   Host to bind the web interface to. Defaults to '*'
                        (all interfaces)
  --web-port WEB_PORT, -P WEB_PORT
                        Port on which to run web host
  --headless            Disable the web interface, and instead start the load
                        test immediately. Requires -u and -t to be specified.
  --web-auth WEB_AUTH   Turn on Basic Auth for the web interface. Should be
                        supplied in the following format: username:password
  --tls-cert TLS_CERT   Optional path to TLS certificate to use to serve over
                        HTTPS
  --tls-key TLS_KEY     Optional path to TLS private key to use to serve over
                        HTTPS

Master options:
  Options for running a Locust Master node when running Locust distributed. A Master node need Worker nodes that connect to it before it can run load tests.

  --master              Set locust to run in distributed mode with this
                        process as master
  --master-bind-host MASTER_BIND_HOST
                        Interfaces (hostname, ip) that locust master should
                        bind to. Only used when running with --master.
                        Defaults to * (all available interfaces).
  --master-bind-port MASTER_BIND_PORT
                        Port that locust master should bind to. Only used when
                        running with --master. Defaults to 5557.
  --expect-workers EXPECT_WORKERS
                        How many workers master should expect to connect
                        before starting the test (only when --headless used).

Worker options:

  Options for running a Locust Worker node when running Locust distributed.
  Only the LOCUSTFILE (-f option) need to be specified when starting a Worker, since other options such as -u, -r, -t are specified on the Master node.

  --worker              Set locust to run in distributed mode with this
                        process as worker
  --master-host MASTER_HOST
                        Host or IP address of locust master for distributed
                        load testing. Only used when running with --worker.
                        Defaults to 127.0.0.1.
  --master-port MASTER_PORT
                        The port to connect to that is used by the locust
                        master for distributed load testing. Only used when
                        running with --worker. Defaults to 5557.

Tag options:
  Locust tasks can be tagged using the @tag decorator. These options let specify which tasks to include or exclude during a test.

  -T [TAG [TAG ...]], --tags [TAG [TAG ...]]
                        List of tags to include in the test, so only tasks
                        with any matching tags will be executed
  -E [TAG [TAG ...]], --exclude-tags [TAG [TAG ...]]
                        List of tags to exclude from the test, so only tasks
                        with no matching tags will be executed

Request statistics options:
  --csv CSV_PREFIX      Store current request stats to files in CSV format.
                        Setting this option will generate three files:
                        [CSV_PREFIX]_stats.csv, [CSV_PREFIX]_stats_history.csv
                        and [CSV_PREFIX]_failures.csv
  --csv-full-history    Store each stats entry in CSV format to
                        _stats_history.csv file
  --print-stats         Print stats in the console
  --only-summary        Only print the summary stats
  --reset-stats         Reset statistics once hatching has been completed.
                        Should be set on both master and workers when running
                        in distributed mode

Logging options:
  --skip-log-setup      Disable Locust''s logging setup. Instead, the
                        configuration is provided by the Locust test or Python
                        defaults.
  --loglevel LOGLEVEL, -L LOGLEVEL
                        Choose between DEBUG/INFO/WARNING/ERROR/CRITICAL.
                        Default is INFO.
  --logfile LOGFILE     Path to log file. If not set, log will go to
                        stdout/stderr

Step load options:
  --step-load           Enable Step Load mode to monitor how performance
                        metrics varies when user load increases. Requires
                        --step-users and --step-time to be specified.
  --step-users STEP_USERS
                        User count to increase by step in Step Load mode. Only
                        used together with --step-load
  --step-time STEP_TIME
                        Step duration in Step Load mode, e.g. (300s, 20m, 3h,
                        1h30m, etc.). Only used together with --step-load

Other options:
  --show-task-ratio     Print table of the User classes'' task execution ratio
  --show-task-ratio-json
                        Print json data of the User classes'' task execution
                        ratio
  --version, -V         Show program''s version number and exit
  --exit-code-on-error EXIT_CODE_ON_ERROR
                        Sets the process exit code to use when a test result
                        contain any failure or error
  -s STOP_TIMEOUT, --stop-timeout STOP_TIMEOUT
                        Number of seconds to wait for a simulated user to
                        complete any executing task before exiting. Default is
                        to terminate immediately. This parameter only needs to
                        be specified for the master process when running
                        Locust distributed.

User classes:
  UserClass             Optionally specify which User classes that should be
                        used (available User classes can be listed with -l or
                        --list)
```

### 	参数对比：

| 类型       | 0版本时，参数                                      | 1版本时，参数                                      | 用法解释                               |
| ---------- | -------------------------------------------------- | -------------------------------------------------- | -------------------------------------- |
| 常用选项   | **-c** NUM_CLIENTS, **--clients** NUM_CLIENTS      | **-u** NUM_USERS, **--users** NUM_USERS            | 设置运行用户数                         |
|            |                                                    | --config CONFIG                                    | 设置config配置文件路径                 |
|            |                                                    | -l, --list                                         | 显示运行的用户定义类名                 |
| 图形界面   | -P PORT, **--port** PORT, --web-port PORT          | --web-port WEB_PORT, -P WEB_PORT                   | 图形界面运行的端口                     |
|            |                                                    | --web-auth WEB_AUTH                                | auth认证，格式为用户名:密码            |
|            |                                                    | --tls-cert TLS_CERT                                | https接口TLS认证证书路径               |
|            |                                                    | --tls-key TLS_KEY                                  | https接口TLS认证私钥路径               |
| 无图形界面 | **--no-web**                                       | **--headless**                                     | 启动无web图形界面                      |
|            | --step-**clients** STEP_CLIENTS                    | --step-**users** STEP_USERS                        | 逐步增加的用户数                       |
| 分布式     | **--slave**                                        | **--worker**                                       | 定义为助攻进程                         |
|            | --expect-**slaves** EXPECT_SLAVES                  | --expect-**workers** EXPECT_WORK                   | 定义在连接多少个助攻进程后才才开始运行 |
| 标签       |                                                    | -T [TAG [TAG ...]], --tags [TAG [TAG ...]]         | 指定执行任务中的标签                   |
|            |                                                    | -E [TAG [TAG ...]], --exclude-tags [TAG [TAG ...]] | 排除指定标签的任务                     |
| 结果文件   | --csv CSVFILEBASE, **--csv-base-name CSVFILEBASE** | --csv CSVFILEBASE                                  | 结果写入csv文件的前缀                  |

## Ⅲ 代码类变化

1、把Locust类，重命名为User， HttpLocust类，重命名为HttpUser， TaskSet类属性locust重命名为user

2、可以在继承User类下，直接使用@task装饰器

3、以前Locust类中的task_set属性，已经被移除，现在改用User类中的tasks属性，且tasks的写法**只能是列表，或字典**

```python
from locust import TaskSet, User

class MyTaskSet(TaskSet):
    pass

class WebUser(User):
    tasks = [MyTaskSet]
```

4、增加了tag标签，在执行时，可以用 -T \\ --tags 指定标签执行、-E \\ --exclude-tags排除指定标签执行

```python
from locust import User, task, tag

class WebUser(User):
    @task
    @tag("tag1", "tag2")
    def my_task(self):
        pass
```

5、环境变量发生变化

​	LOCUST_MASTER 重命名为 LOCUST_MODE_MASTER

​	LOCUST_SLAVE 重命名为 LOCUST_MODE_WORKER

​	LOCUST_MASTER_PORT 重命名为 LOCUST_MASTER_NODE_PORT

​	LOCSUT_MASTER_HOST 重命名为 LOCUST_MASTER_NODE_HOST

​	CSVFILEBASE 重命名为 LOCUST_CSV

6、分布式中，助攻进程的参数，由 --slave \\ expect-slaves 更改为 --worker \\ --expect-workers

7、无图形模式启动参数，由 --no-web 更改为 --headless

8、移除了 Locust.setup、 Locust.teardown、 TaskSet.setup、 TaskSet.teardown，改用 on_test_start、on_test_stop

9、以前的顺利类 TaskSequence 和 顺序装饰器@seq_task 已经全包变更为 SequentialTaskSet。这个顺序类，将忽略任务的权重。任务的执行顺序，**以任务的声明顺序来执行**

```python
from locust import SequentialTaskSet, task

class MySeqTasks(SequentialTaskSet)

	@task	# 在顺序类中，@task 装饰器的权重值将被忽略
    def first_task(self):
        pass
```

10、运行数据记录，csv文件，表头发生变化，增加统计，使表头意思更清晰明了

11、结果写入csv文件的参数 **--csv-base-name**  已经被移除

12、控制台日志，不在用标准输出stdout（或标准错误输出stderr），要输出日志，可以直接用print()进行输出，也可以用logging模块，定义日志

---

## Ⅳ 脚本模板

已经知道locust1.* 版本与以前locust 0.* 版本区别了，是不是就想要一个脚本模板呢？下面就给大家一个脚本模板，供大家参考：

```python
import random
from locust import HttpUser, task, between, SequentialTaskSet, tag


# 定义一个任务类，这个类名称自己随便定义，类继承SequentialTaskSet 或 TaskSet类，所以要从locust中，引入SequentialTaskSet或TaskSet
# 当类里面的任务请求有先后顺序时，继承SequentialTaskSet类， 没有先后顺序，可以使用继承TaskSet类
class MyTaskCase(SequentialTaskSet):
    # 初始化方法，相当于 setup
    def on_start(self):
        pass

    # @task python中的装饰器，告诉下面的方法是一个任务，任务就可以是一个接口请求，
    # 这个装饰器和下面的方法被复制多次，改动一下，就能写出多个接口
    # 装饰器后面带上(数字)代表在所有任务中，执行比例
    # 要用这个装饰器，需要头部引入 从locust中，引入 task
    @task
    @tag("leave_1")
    def regist_(self):  # 一个方法， 方法名称可以自己改
        url = '/erp/regist'  # 接口请求的URL地址
        self.headers = {"Content-Type": "application/json"}  # 定义请求头为类变量，这样其他任务也可以调用该变量
        self.username = "locust_" + str(random.randint(10000, 100000))
        self.pwd = '1234567890'
        data = {"name": self.username, "pwd": self.pwd}  # post请求的 请求体
        # 使用self.client发起请求，请求的方法根据接口实际选,
        # catch_response 值为True 允许为失败 ， name 设置任务标签名称   -----可选参数
        with self.client.post(url, json=data, headers=self.headers, catch_response=True) as rsp:
            if rsp.status_code > 400:
                print(rsp.text)
                rsp.failure('regist_ 接口失败！')

    @task  # 装饰器，说明下面是一个任务
    def login_(self):
        url = '/erp/loginIn'  # 接口请求的URL地址
        data = {"name": self.username, "pwd": self.pwd}
        with self.client.post(url, json=data, headers=self.headers, catch_response=True) as rsp:
            self.token = rsp.json()['token']  # 提取响应json 中的信息，定义为 类变量
            if rsp.status_code < 400 and rsp.json()['code'] == "200":
                rsp.success()
            else:
                rsp.failure('login_ 接口失败！')

    @task  # 装饰器，说明下面是一个任务
    def getuser_(self):
        url = '/erp/user'  # 接口请求的URL地址
        headers = {"Token": self.token}  # 引用上一个任务的 类变量值   实现参数关联
        with self.client.get(url, headers=headers, catch_response=True) as rsp:  # 使用self.client发起请求，请求的方法 选择 get
            if rsp.status_code < 400:
                rsp.success()
            else:
                rsp.failure('getuser_ 接口失败！')

    # 结束方法， 相当于teardown
    def on_stop(self):
        pass


# 定义一个运行类 继承HttpUser类， 所以要从locust中引入 HttpUser类
class UserRun(HttpUser):
    tasks = [MyTaskCase]
    wait_time = between(0.1, 3)  # 设置运行过程中间隔时间 需要从locust中 引入 between


'''
运行：
    在终端中输入：locust -f 被执行的locust文件.py --host=http://被测服务器域名或ip端口地址
    也可以不指定host
命令执行成功，会提示服务端口，如：*：8089
此时，则可通过浏览器访问机器ip:8089,看到任务测试页面
'''
```
> 想了解更多有趣，有料的测试相关技能技巧，欢迎关注柠檬班微信公众号，或在腾讯课堂中搜索柠檬班机构，观看测试相关视频。
