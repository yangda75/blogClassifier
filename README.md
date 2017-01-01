<meta charset="utf-8">

# Medium 博客分类器

作者：杨达 [@bill363yang](https://github.com/bill363yang)     
邮箱：yangda@sjtu.edu.cn
     billyang363@gmail.com
### 功能简介

从[medium.com](https://medium.com)上抓取文章，存储在本地然后分类，显示分类标签。

### 使用说明
**注意**: 本程序使用python3.5    
1. GNU/Linux 或 macOS 命令行 或Windows Powershell：    
  进入项目目录，运行
  ``` bash
  $ pip install -r requirements.txt
  $ python main.py
  ```
2. 程序启动后，屏幕上会出现一个标题为"Naive bayes blog classifier"的GUI窗口。在输入框中输入一个合法的medium.com用户名（注意是个人用户），然后按下start按钮，等待大约两分钟。两分钟的运行时长是因为我在scraper.py中设置了间歇10秒爬取一篇文章，我担心如果不间断爬取数据会被medium.com拒绝。
如果输入的用户名合法，约两分钟后即可看到GUI窗口和命令行中的结果输出。

3. 示例用户名: ev, mikeAllen, fisforphantom。你可以在medium.com的页面上找到更多用户名。运行截图在picture文件夹中。

4. 结果说明：
标签（形如'teen_f'） 中，'teen'表示年龄段为13-17岁，'adult'表示23-27岁，'mature'33-47岁；'f'表示女性，'m'表示男性。

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
    P(tag|V)=P(tag)\*P(V1|tag)\*P(V2|tag)\*...\*P(Vn|tag)/P(V)分别计算V在各类别中出现的概率，其中P(V)在V给定的情况下为一常数，可以忽略，
    3. 比较各个标签计算出的P(tag|V),取最大的作为该文本的类别。


### 项目结构    

``` bash
$ tree .
.
├── adult_f.csv
├── adult_m.csv
├── main.py
├── mature_f.csv
├── mature_m.csv
├── prepare.py
├── README.html
├── README.md
├── requirements.txt
├── scraper.py
├── teen_f.csv
├── teen_m.csv
└── train.py

```

1. 六个CSV文件均为数据文件，分别存储了六个类别人群的博客中不止出现一次的词语的出现概率。每一行有一个词语，一个数字，中间用逗号隔开，数字为该词语在这种人群的所有博客中出现的次数除以该人群博客中词语总数。
2. train.py 是生成CSV文件的程序，将存储[BlogCorpus](http://u.cs.biu.ac.il/~koppel/BlogCorpus.htm)这网页中数据集的绝对路径作为train.train()函数的参数得到六个CSV文件。
3. scraper.py 是负责爬取博客的部分。起初打算使用最简单的urllib加BeautifulSoup，但是发现只有修改UA才能获取到数据。后来使用了Requests这个第三方库，解决了问题。scraper.py中只有一个函数，这个函数接受一个medium用户名，返回标题出现在https://medium.com/@userid/latest 这个页面上的文章。默认数量是10篇。获取文章之后，会把requests.get()返回值的content解释成BeautifulSoup对象。在这个返回的对象中，`<div class="layoutSingleColumn">`这类DOM元素的href参数是文章地址，在文章中，`<div class="section-inner">`这类DOM下的`<p>`子元素中存储这文章内容，使用BeautifulSoup提供的方法可以轻松的取出它，然后存储在以当前userid命名的文件夹一个txt文件中。这个txt文件的数字部分是它在网页上出现的序列号。
4. prepare.py 负责处理爬取到的文章。我在程序中添加了详细的注释。这份程序是在做这份大作业之前写的。后来我看了PEP8的文档，所以除了prepare.py之外的程序中变量名都是小写字母加下划线，只有prepare.py中使用了混合大小写。
5. main.py 是主程序，所有GUI相关元素都在这个程序里。
其中的MainWin类是主窗口。主要部件有：提示语，提示操作方法；输入框，接受输入；按钮，开始分类。
按下按钮后，输入框中若没e有内容，会显示一条错误信息，如果正确，会调用analyze函数，生成一个列表，长度为得到的用户文章数目，results[i]表示第i+1篇文章的分类结果。得到这个分类结果之后，会把它逐条显示在GUI窗口中。最后，会显示出现次数最多的分类标签作为最终猜测。
analyze函数接受一个参数userid，即想要分析的medium用户名，先调用scraper.py中的get_rec10()函数，得到最近文章，然后调用prepare.py中的prepare函数，得到每篇文章中出现次数最多的30个单词，对每一个标签，计算这30个单词在这个标签的语料中出现的频率乘积(基于朴素贝叶斯分类器的独立假设)，其中没有在CSV文件中的词语(即没有在语料中出现过一次以上的)按出现一次计算，算出一个似然率，根据上面原理部分的公式，每个似然率只有之前计算的部分不同(假设各个标签与所有词语出现的概率相同)，所以用这个连乘积来相互比较，这个联合概率最大的标签作为此次猜测的结果。存储在results列表中。
除了在GUI窗口显示外，结果也会打印在命令行中。
