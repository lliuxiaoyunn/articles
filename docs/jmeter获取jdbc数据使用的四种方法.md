# 史上最全的jmeter获取jdbc数据使用的四种方法

jmeter使用jdbc协议获取数据库中数据，很多人都会用，因为大家在做测试的时候，有时候需要大量的用户进行登录，获取需要数据库中真实的数据用于测试，所以常常会用jdbc来获取数据库数据。

哪从数据库获取回来的数据，一般会用什么方式来接收呢？常见的有两种：Variable names 和 Result variable name。

相信，大家肯定用的最多的就是第一种Variable names，因为这种，使用Foreach控制器使用最简单。但是，其他的你懂得如何使用吗？

哪今天，我就这这里，把Variable names 和 Result variable name 这两种接收变量，并循环使用的办法做了一个汇总，给大家讲解一下。

## 我们先看用 Variable names 接收数据库返回值的情况：

![Snipaste_20200329_232438](image/Snipaste_20200329_232438.png)

Variable names为dbmobile，来接收从数据库查询返回回来的100个用户号码，我们可以看下，从数据库中返回回来的数据，是如何被变量接收的。

![Snipaste_20200330_170554](image/Snipaste_20200330_170554.png)

**方法一：** 使用**foreach控制器**，循环的使用这100个手机号，进行登录

![Snipaste_20200329_232747](image/Snipaste_20200329_232747.png)

看到上图， 输入变量前缀，输入的是<u>Variable names的变量名称</u>；然后开始循环和介绍循环值（<u>上面图中我其实只用98个值，不是100个值</u>）；再看输入变量名称，我<u>自定义了一个变量</u>；再勾选了数字之前加下划线。

![Snipaste_20200329_232834](image/Snipaste_20200329_232834.png)

这个图，我们就看到，登录接口中，使用了上面自定义的变量名称

![Variablenames-1](image/Variablenames-1.gif)

**方法二：**使用**循环控制**

![Snipaste_20200329_232944](image/Snipaste_20200329_232944.png)

循环控制器，我们填写循环次数

![Snipaste_20200329_233102](image/Snipaste_20200329_233102.png)

接下来，我们就要添加**计数器**，计数器每次计算一次，增加1，定义一个新变量 f 来接收计数器的值。

![Snipaste_20200329_233143](image/Snipaste_20200329_233143.png)

然后，我们在登录接口中，我们使用一个 关联函数 ${\_\_V(dbmobile\_${f})}

![Variablenames-2](image/Variablenames-2.gif)

## 接下来我们再看用Result variable name 接收数据库返回值的情况：

![Snipaste_20200329_233236](image/Snipaste_20200329_233236.png)

Result variable name为dbmobo，来接收从数据库查询返回回来的100个用户号码，我们可以看下，这个时候，从数据库返回回来的数怎么接收的。

![Snipaste_20200330_170357](image/Snipaste_20200330_170357.png)

**方法三：**  使用**foreach控制器**

![Snipaste_20200329_233401](image/Snipaste_20200329_233401.png)

此时，在使用foreach控制器之前，我们先要用一个正则提取器，把我们想要得用户号码提取出来。我们也来看下，提取之后的值。

![Snipaste_20200330_170917](image/Snipaste_20200330_170917.png)

看到上图，提取之后的值，是不是似曾相识，接下来用foreach控制器，是不是就很简单了。

![Snipaste_20200329_233452](image/Snipaste_20200329_233452.png)

![Snipaste_20200329_233534](image/Snipaste_20200329_233534.png)

![ResultVariablenames-3](image/ResultVariablenames-3.gif)

**方法四：**使用**循环控制**

![Snipaste_20200329_233632](image/Snipaste_20200329_233632.png)

![Snipaste_20200329_233714](image/Snipaste_20200329_233714.png)

循环控制器的配置和计数器的配置，相信大家也都已经知道了，没有难度了。难点，就在下面。

![Snipaste_20200329_233832](image/Snipaste_20200329_233832.png)

看清楚这个用户参数的设置了吗？

`${__BeanShell(vars.getObject("dbmobo").get(${d}).get("mobile"))}`

这段能理解吗？从dbmobo这个对象中，获取第 d 个mobile的值。 d是上面的计数器输出值，每次递增1

![Snipaste_20200329_233947](image/Snipaste_20200329_233947.png)

理解了上面的用户参数的值用法，这个登录接口，就么有难度了吧。看最后运行结果，是不是也可以循环登录了呢？

![ResultVariablenames-4](image/ResultVariablenames-4.gif)

好了，这四种用法你是否都掌握了呢？相信很多同学都只会其中1到2种用法吧。之前没有用过，哪就好好动手学习起来吧！

---

> 想了解更多有趣，有料的测试相关技能技巧，欢迎关注**柠檬班**微信公众号，或在腾讯课堂中搜索柠檬班机构，观看测试相关视频。