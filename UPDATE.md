## 如何更新网站

### 1.更新news

如需要添加新的news，以如下方式进行：

1. 进入`content/en/post`文件夹下。

2. 在`news.md`中添加即可




### 2.更新publications

如果要更新publications，以如下的方式进行：

1. 进入`content/publications`文件夹下。

2. 确定添加文章所属的类别，这一类别决定这篇文章在主页research一栏显示在哪里。已有的类别

   | 大方向                                           | 小方向                              | 编号 |
   | ------------------------------------------------ | ----------------------------------- | ---- |
   | **Secure Networking and Systems Infrastructure** | Secure Internet Routing             | 1-1  |
   |                                                  | Encrypted Traffic Analysis          | 1-2  |
   |                                                  | DDoS Attack Prevention              | 1-3  |
   |                                                  | Systems Security                    | 1-4  |
   | **AI and Data Security**                         | Privacy-Preserving Machine Learning | 2-1  |
   |                                                  | Federated Learning                  | 2-2  |
   |                                                  | AI Security                         | 2-3  |
   | **Networking Infrastructure for AI**             | Datacenter Networking               | 3-1  |
   |                                                  | Intelligent Network Architecture    | 3-2  |
   | **Web3.0 and Blockchain**                        | Interoperability                    | 4-1  |
   |                                                  | Web3.0 Infra and Application        | 4-2  |
   |                                                  | Zero-Knowledge Proof                | 4-3  |

   确定新加文章所属的方向后，找到相应的文件夹，譬如添加“AI and Data Security”方向下关于“AI Security”的文章，则找到相应文件夹后，以`2-3-x.md`的方式创建新文件。**以递增顺序添加文件，文件名不要重复，否则可能会导致team页面显示错误**

3. 文件内部格式：

   可以参考`content\en\publications\ai_and_data_security\privacy-preserving_machinelearning\2-1-2.md`

   ```markdown
   ---
   title: "<文章名>"
   excerpt: "<会议/期刊的全名>"
   authors: "<作者列表，本组学生名用<u></u> tag包裹，刘老师的名用<strong></strong>包裹，通讯标注使用<sup>✉️</sup>>"
   pdf: <arxiv 链接>
   doi: <文章链接>
   code: <开源代码链接>
   slides: <选填>
   patent: <选填>
   seq: <显示顺序>
   award:
     - <奖项名称>
     - <奖项名称>
   conference: "<会议名称，期刊可以不填>"
   conference_url: "<会议链接，期刊可以不填>"
   abstract: "<文章摘要>"
   bib: "<文章引用bibtex>"
   tag: <本文在主页展示的简称>
   year: <本文年份>
   ---
   ```

   注意点：

   - title，excerpt，authors，seq，tag为必填项目。
   - **注意双引号导致的问题，及时添加转义字符，尤其要注意title和abstract**
   - seq为本类文章显示顺序，一般而言，命名为`x-y-z.md`的文章填`seq: z`即可。
   - 对于已经接受但尚未发布的会议文章，可以选择不加abstract键值对且填conference值，会显示为`to appear in <conference>`。

4. （可选）添加新的文章类别

   如果文章属于新的类别，可以仿照`content/en/publications`的目录组织结构进行。

   - 添加大方向，则新建`content/en/publications/<name>`，并添加`_index.md`，`_index.md`结构如下：

     ```markdown
     ---
     title: "<本方向显示的名字>"
     rank: "<用于控制显示顺序，一般这是第几个方向就填几>"
     ---
     ```

   - 添加小方向在对应的大方向文件夹下重复和上面相同的操作即可。

   - **在添加方向后，最好在本文上方的表格中添加标号，方便后续查阅。**



### 3.更新team

硕士生文件在`content/en/master_members`文件夹下，博士生文件在`content/en/phd_members`文件夹下。

1. 找到对应文件夹

2. 以人名全拼的方式添加新文件，如`zhangsan.md`，如果重复，可以在人名后面加2，3，4...

3. 文件格式：

   ```markdown
   ---
   seq: <显示顺序>
   publications: 
     - x-y-z.md
     - u-w-v.md
   infos:
     - Working on <研究方向>
     - B.E. in <专业> , <院校>
   ---
   
   ### Student Name
   <p><i>Master/Ph.D. Student</i></p>
   ```

   注意：

   - 如果没有发表，publications一栏不要填，不然介绍页会出现`publications: `这样的空行。

