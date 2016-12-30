# Medium 博客分类器

### 功能简介

从[medium.com](https://medium.com)上抓取文章，存储在本地然后分类，显示分类标签。

### 运行方法
**注意**: 本程序使用python3.5    
GNU/Linux 或 macOS 命令行：    
进入项目目录，运行
```
$ pip install -r requirements.txt
$ python main.py
```
Windows 类似

### 原理简述：

##### 1. 爬取文章：    
  - 接受的输入为medium用户名，爬取该用户的最近十篇文章。使用requests和BeautifulSoup    
  - **注意**：medium.com不允许爬取数据(scraping)    

##### 2. 文本特征向量生成：    
  - 输入HTML文件路径
  - 去除HTML标签
  - tokenization:转换成小写，去除标点，换行和制表符替换为空格。使用空格分词    
    例：`"I'm a sutdent."->"im a student"`
  - 统计词条(token)出现的次数，存储在字典中    
    字典形如:`{...,"the":1332,...}`
  - 根据生成的词条频数字典生成词条频率字典，从中取出除常用词汇外('the','a'等)频数最高的30个词条，存储在高频词条字典中，这个字典形如:`{...,"data":0.05,...}`    

##### 3. 文本分类：    
  - 原理：朴素贝叶斯分类器(Naive Bayes Classifier)
  - 训练数据来源：[BlogCorpus](http://u.cs.biu.ac.il/~koppel/BlogCorpus.htm)
    - 19320个文件，xml格式，标签：年龄，职业，星座
    - 8240 "10s" blogs (ages 13-17)
    - 8086 "20s" blogs(ages 23-27)
    - 2994 "30s" blogs (ages 33-47)
    - 每个年龄段男女人数相等
  - 训练：
    1. 对13-17岁的男性：扫描所有文档，取出频率最高的50个词条和它们出现的频率
    2. 对13-17岁的女性重复1.
    3. 对其他年龄段，重复1,2    
    形成6个字典，形如`{...,"word":0.03,...}`
  - 分类：
    1. 待分类文本的特征向量 V,
    2. 使用
    P(tag|V)=P(tag)\*P(V_1_|tag)\*P(V_2_|tag)\*...\*P(V_n_|tag)/P(V)分别计算V在各类别中出现的概率，其中P(V)在V给定的情况下为一常数，可以忽略，
    3. 比较各个标签计算出的P(tag|V),取最大的作为该文本的类别。

### 项目结构
~~~~
$ tree .
.    
├── main.py    
├── prepare.py    
├── README.md    
├── requirements.txt     
└── scraper.py
~~~~
