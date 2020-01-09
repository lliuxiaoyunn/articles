# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://mkdocs.org).

【柠檬班】不写代码搞定jmeter录制和响应结果中文乱码牛皮癣[原创]

如果你已经开始使用jmeter工具，进行接口测试了，也许你曾经或者正在被一个问题困扰，哪就是你录制脚本或接口请求返回中包含中文时，一不小心就中文乱码了。

中文乱码，不是我们想要的，但是却经常性的困扰着大家。那么如何解决这个牛皮癣呢？

也许，在你没有看到这篇文章之前，你已经百度了很多，尝试了很多很多方法，但是，你可能都已经沮丧了，因为你百度的结果都是告诉你如何设置‘UTF-8’，你按照他们说的做了，甚至还写了一大堆你不知所云的代码，但是很可惜，可能你的付出与你的回报不一致，问题依旧，是不是？

那我今天，我就给大家讲一个万能的方法，不用写代码，而且非常非常简单，是不是很想马上尝试一下呢？

> 想了解更多的jmeter使用技巧，想获得一些百度很多次，却依然无法解决你问题的办法，欢迎关注**柠檬班**微信公众号，里面有非常多最新最全的测试技巧哦

**注意**：我讲的windows系统，linux、mac请同理设置，但不能照搬

哈哈，来吧，开干......
大家应该用的比较多的都是windows电脑吧，那你知道你的windows电脑字符集编码吗？不知道，那就快来看看吧

打开dos窗口，输入 chcp 回车

此时，你看到了什么？
## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs help` - Print this help message.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
