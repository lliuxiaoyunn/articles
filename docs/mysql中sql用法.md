# mysql数据库中sql语句语法

## DCL(Data Control Language) 数据控制语言

### 创建用户

+ 1、使用create user 语句创建用户

```sql
create user <用户> [identified by [PASSWORD]'password'] [,用户 [identified by [PASSWORD] 'password']];
-- 用户
用户名'@'主机名

-- identified by
用于指定用户密码

-- PASSWORD 'password'
PASSWORD表示使用哈希值设置密码，如果密码为普通字符串，可以不用PASSWORD关键字
```



注意事项：

①、create user 语句可以不指定初始化密码，但，从安全角度，建议添加

②、执行create user语句用户，必须拥有mysql数据库的insert权限或全局 create user权限

③、create user语句执行成功后，mysql库的user表中会添加一条记录

④、create user语句可以一次创建多个用户，多个之间用逗号分隔



+ 2、在mysql.user表中添加用户

```sql
INSERT INTO mysql.user(Host, User,  authentication_string, ssl_cipher, x509_issuer, x509_subject) VALUES ('hostname', 'username', PASSWORD('password'), '', '', '');
-- 注意：由于mysql数据库的user表中，ssl_cipher、x509_issuer 和 x509_subject 这 3 个字段没有默认值，所以向 user 表插入新记录时，一定要设置这 3 个字段的值，否则 INSERT 语句将不能执行。

-- 使用户生效
FLUSH PRIVILEGES;
```



+ 3、使用GRAT语句创建用户

这种用法，可以方便面的给账户赋予权限

```sql
GRANT priv_type ON database.table TO user [IDENTIFIED BY [PASSWORD] 'password'];

-- priv_type 表示新用户的权限
-- database.table 表示新用户的权限范围，即，只能在指定的数据库和表上使用自己的权限
-- user 指新用户账号，由用户名和主机名构成
-- identified by  关键字用来设置密码
-- 'password' 表示新用户的密码
```



### 修改用户

```sql
raname USER <旧用户> TO <新用户>;
```

注意事项：

①、rename user 语句用于对原有的mysql用户进行重命名

②、若系统中旧账户不存在或新账户已经存在，该语句会报错

③、执行该语句，必须要有mysql数据库的update权限或全局create user权限



### 删除用户

```sql
drop USER <旧用户> TO <新用户>;
```



注意事项：

①、DROP USER 语句可用于删除一个或多个用户，并撤销其权限。

②、使用 DROP USER 语句必须拥有 mysql 数据库的 DELETE 权限或全局 CREATE USER 权限。

③、在 DROP USER 语句的使用中，若没有明确地给出账户的主机名，则该主机名默认为“%”。



### 创建数据库

```sql
CREATE TABLE [IF NOT EXISTS] <数据库名>
[[DEFAULT] CHARACTER SET <字符集名>] 
[[DEFAULT] COLLATE <校对规则名>];
```

数据库名，要求符合操作系统文件夹命名规则，另外不能以数字开头，不区分大小写，不能同名。

`[DEFAULT] CHARACTER SET <字符集名>` 指定数据库字符集

`[DEFAULT] COLLATE <校对规则名>` 指定字符集的默认校对规则

`show databases;` 查看所有数据库

### 修改数据库

```sql
ALTER DATABASE [数据库名] {
[default] character set <字符集名> | [default collate <校对规则名>]
};
```



### 删除数据库

```sql
DROP DATABASE [IF EXISTS] <数据库名>
```



<font color="red">**删除请谨慎**</font>，执行命令时，不会有二次确认。执行删除后，数据库表和数据都将被物理删除，无法恢复。



## DDL(Data Definition Language)数据定义语言

### 建表

```sql
create table <表名> (<列名1> <类型>,.....<列名n> <类型>)[表选项][分区选项];
```

`show tables;` 查看数据库中所有表

### 建视图

视图：一种基于真实表的虚拟表，数据来源是建立在真实表的数据上。

```sql
create view table_view as select ...;
```

+ 创建视图的限制：
  + 操作用户，要具有create view权限，而且还需要有操作基础表和其视图的权限
  + select 语句，不能引用系统或用户变量
  + select语句，不能包含from子句中的子查询
  + select语句，不能引用预处理语句参数
  + 创建视图时，引用的基表或视图必须存储。
  + 创建视图时，不能引用temporary临时表，也不能创建temporary临时视图

`desc table_view;` 查看视图表结构 

`show create view table_view;` 查看建立视图的规则

### 建索引

索引：是一种特殊的数据库结构，由数据表中的一类或多列组合而成，可以用来快速查询数据表中某一特定值的记录。

```sql
create {primary key | index | unique} 索引名 on table_name(列名);
primary key 主键，默认也是索引
index  单值|复合索引
unique  唯一索引
```

`show index from <表名> [from <数据库名>];` 查看索引

### 修改表

```sql
alter table <表名> [修改选项];

-- 修改选项
add column <列名> <类型>
change column <旧列名> <新列名> <新列类型>
alter column <列名> {set default <默认值> | drop default}
modify column <列名> <类型>
drop column <列名>
rename to <新表名>
character set <字符集名>
collate <校对规则名>
```



### 修改视图

```sql
alter view table_view as <select语句>;
```



### 修改索引

```sql
add index [<索引名>][索引类型](<列名>,...)
```



### 删除表

```sql
drop table [if exists] 表名1、表名2....;
```



### 删除视图

```sql
drop view table_view......;
```



### 删除索引

```sql
drop index <索引名> on <表名>;
```



## DML(Data Manipulation Language)数据操作语言

### DQL(Data Query Language)数据查询语言

#### 查询表中数据

```sql
select column from table_name;
```



#### 去重查询

distinct 对列数据去重显示

```sql
select distinct column from table_name;
```

column列，有多列时，用逗号分开。

在对一列或多列去重时，distinct必须写在所有列的前面；多列名时，对多个字段组合去重，也就是说，多列的值组合完全一样时，才会被去重。



#### 设置别名

给表或列设置别名

```sql
table_name\column [as] 别名
```



#### 限制查询条数

从查询结果中返回限制数量的数据

```sql
limit 初始位置, 记录数
```

`select column from table_name limit 3,5;`  从第4条开始，返回5条数据

```sql
limit 记录数
```

`select column from table_name limt 4;` 返回前4条数据

```sql
limit 记录数 offset 初始位置
```

"初始位置"：从哪条记录开始显示，"记录数"：表示显示的记录条数

`select column from table_name limt 5 offset 3;` 从第4条开始，返回5条数据



#### 查询结果排序

查询的结果根据字段的 升序 或 降序显示， 默认asc升序

```sql
order by column [asc|desc]
```

`select column from table_name order by order_col;` 查询结果根据 order_col 列的升序进行排序

`select column_1,column_2 from tabl_name order by column_1, column_2;` 查询结果，先根据column_1列值做升序排列，column_1有重复数据时，再按column_2列做升序排序。

**注意：**使用多个字段排序时，只有在第1个字段有相同的值时，才会使用第二个字段排序；如果第1个字段值都是唯一的，将不再对第2个字段进行排序。

`select column_1,column_2 from tabl_name order by column_1 desc, column_2 asc; `  查询结果，先根据column_1进行降序排序，column_1有重复数据时，再根据column_2进行升序排序。

**注意：**当排序字段值有空值时，将空值当做最小值对待。



#### 条件查询

```sql
where condition (=、>、<、>=、<=、!=、<>)
-- and、or、xor
-- xor:满足期中一个条件，并且不满足另外一个条件
```



#### 模糊查询

```sql
-- 不区分大小写模糊匹配
[not] like 'str'
-- str可以带有通配符： % 或 _
```

通配符‘%’： 代表任意长度的字符串，长度为0也可以，但是，**不能匹配NULL**

通配符‘_’:  代表单个字符，长度不能为0

```sql
-- 区分大小写模糊匹配
[not] LIKE BINARY 'str%'
```



#### 范围查询

```sql
[NOT] BETWEEN value_1 AND value_2 
```

值在 value_1 到 value_2 之间

`select column from table_name where date_column between '2021-01-01' and '2021-01-28';` 



#### 查询空值

```sql
IS [NOT] NULL
```

IS NULL 是整体，不能把IS换成=



#### 分组查询

```sql
group by column
```

根据字段名称分组，多个字段之间用逗号分隔。被分组后，结果只显示分组的**第1条**数据

group_concat() 函数与 group by 一起用，可以把每个分组字段值都显示出来。

`select col_1, group_concat(col_2) from table_name group by col_1;`  查询结果根据col_1分组，显示col_1的值，和col_1值相同的col_2的所有数据

group_concat()函数，也可以是其他聚合函数，如：count() sum() avg() max() min()

group by 之后加上 ’with rollup' 可以在最后一行进行数据合计。



#### 过滤分组

对分组后的数据进行过滤

```sql
having condition
```

+ where 和 having 都可以用来过滤数据，但：
  + where一般用于过滤数据行； having用于过滤分组
  + where 条件不能使用聚合函数；having查询条件可以使用聚合函数
  + where 是在数据分组前进行过滤； having是在数据分组后进行过滤
  + where 是根据数据表中字段直接过滤； having是根据已经查询出的字段进行过滤
  + where 条件中不能使用字段别名； having 条件中可以使用字段别名



#### 交叉连接 CROSS JOIN

```sql
select column from table_1 CROSS JOIN table_2 where ...;
-- 与下面相同
select column from table_1, table_2 where ...;
```

进行表数据**笛卡尔积**



#### 内连接 INNER JOIN

```sql
select column from table_1 INNER JOIN table_2 [ON ...];
```

数据量比交叉连接少



#### 外连接

左连接 LEFT OUTER JOIN  或者   LEFT  JOIN 

```sql
select column from table_1 LEFT OUTER JOIN table_2 ON ...;
```

table_1为基表，table_2为参考表；查询时，如果table_1中的数据在table_2中有匹配，就显示匹配的数据，如果没有匹配，则返回table_2的字段值为NULL



右连接 RIGHT OUTER JOIN 或者  RIGHT  JOIN 

```sql
select column from table_1 RIGHT OUTER JOIN table_2 ON ...;
```

与左连接刚好相反。table_2为基表，table_1为参考表；查询时，如果table_2中的数据在table_1中有匹配，就显示匹配的数据，如果没有匹配，则返回table_1的字段值为NULL



#### 子查询

```sql
where 表达式 操作符 (子查询)
```

操作符： IN、NOT IN、 EXISTS、 NOT EXISTS

IN、NOT IN：表达式与子查询 返回的结果集中，某个值相等，返回TRUE，否则返回FALSE；  NOT IN 刚好相反

EXISTS、 NOT EXISTS：判断子查询结果集是否为空，不为空，返回TRUE， 否则返回FALSE;  NOT EXISTS刚好相反

一般情况下，内连接和外连接脚本，都可以用子查询替换，但，反过来不一定



#### 正则查询

```sql
where column REGEXP '正则式'
```

正则式规则与 java、php语言一致



### 插入数据

```sql
INSERT INTO table (column...) VALUES(...);
INSERT INTO table SET column_1= value_1,column_2= value_2,......;
```



### 修改数据

```sql
UPDATE table SET column_1=value_1,column_2=value_2,.... [where子句] [order by 子句] [limit 子句];
```



### 删除数据

```sql
DELETE FROM tale [where子句] [order by 子句] [limit 子句];
```

