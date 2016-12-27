# Medium 博客分类器

### 功能简介

从[medium.com](https://medium.com)上抓取文章，存储在本地然后分类，显示分类标签。

### 原理简述：

##### 1. 爬取文章：    
  - 接受的输入为medium用户名，爬取该用户的文章。使用requests和BeautifulSoup。    
  - **注意**：medium.com不允许爬虫，所以请勿使用本程序    

##### 2. 文本特征向量生成：    
  - 输入HTML文件路径
  - 去除HTML标签
  - tokenization:转换成小写，去除标点，换行和制表符替换为空格。使用空格分词。    
    例："I'm a sutdent."->"im a student"
  - 统计词条(token)出现的次数，存储在字典中    
    字典形如:{...,"the":1332,...}
  - 根据生成的词条频数字典生成词条频率字典，从中取出除常用词汇外('the','a'等)频数最高的30 个词条，存储在高频词条字典中，这个字典形如:{...,"data":0.05,...}    

##### 3. 文本分类：    
  - 原理：朴素贝叶斯分类器(Naive Bayes Classifier)



### 项目结构
.
├── main.py
├── prepare.py
├── README.md
├── requirements.txt
└── scraper.py
