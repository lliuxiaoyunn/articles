# @IDE: PyCharm
# @Author: Allen
# @File: conf.py
# @Time: 2020/1/9 19:00


from recommonmark.parser import CommonMarkParser


source_parsers = {
    '.md':CommonMarkParser,
}
source_suffix = ['.rst', '.md', '.markdown']

extensions = []




