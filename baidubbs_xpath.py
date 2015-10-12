# -*- coding:utf-8 -*-
import requests         #引入requests网页处理模块
from lxml import etree          #引入etree源码处理方法

page=[]         #初始化网页地址列表，即贴吧所有页的地址
for i in range(0,101,50):           #贴吧一共有3页，符合0，50，100的规律
    url='http://tieba.baidu.com/f?kw=%E6%9E%97%E6%88%90%E5%88%9A&ie=utf-8&pn='+str(i)           #构造每一页的网页地址
    page.append(url)            #将每一页的网页地址加入贴吧所有网页地址列表当中

titles=[]           #初始化帖子标题列表
authors=[]
times=[]
contents=[]
for each in page:           #按贴吧每一页的网页地址开始循环
    html=requests.get(each)         #获取网页源代码
    selector=etree.HTML(html.text)          #以etree方法处理网页源码

    title=selector.xpath('//*[@id="thread_list"]/li/div/div[2]/div[1]/div[1]/a')            #以xpath方法提取每一页的帖子标题，形成每一页的title列表
    author=selector.xpath('//*[@id="thread_list"]/li/div/div[2]/div[1]/div[2]/span/a')
    time=selector.xpath('//*[@id="thread_list"]/li/div/div[2]/div[2]/div[2]/span[2]')
    content=selector.xpath('//*[@id="thread_list"]/li/div/div[2]/div[2]/div[1]/div')

    for i in range(0,len(title)):          #按每一页中的帖子标题进行循环(co即为count的意思)
        titles.append(title[i].text)           #把每一页中的帖子标题加入到总的标题列表当中，形成titles的标题列表
        authors.append(author[i].text)
        times.append(time[i].text.strip())
        contents.append(content[i].text.strip())

# for i in range(0,len(titles)):          #按汇总的标题列表(titles列表)中的各项开始循环，准备数据输出
#     print titles[i]            #打印各个帖子的标题

f=open('F:\ctemp\python\\baidubbs_titles.txt','w')          #以只写方式，在文件夹内创建一个txt文件，用于存储信息
for i in range(0,len(titles)):         #按汇总的标题列表开始循环
    f.writelines(titles[i].encode('gb18030'))            #当前titles内的信息均以unicode编码形式存储，使用encode方法将其转化为GB18030编码，输出才能显示为中文(decode方法将某数据转化为中间编码unicode形式)
    #因为标题中含有部分颜文字符号，因此使用GB18030编码而不是GB2312编码(仅有中文的情况下使用GB2312已经能够满足要求)
    f.write('\n')           #文件的writelines不自动换行，因此需要手动写入换行符
    f.writelines(authors[i].encode('gb18030'))
    f.write('\n')
    f.writelines(times[i])
    f.write('\n')
    f.writelines(contents[i].encode('gb18030'))
    f.write('\n')
    f.write('\n')
f.close()           #数据输出完成后关闭文件
