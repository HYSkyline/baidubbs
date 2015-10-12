# -*- coding:utf-8 -*-
import requests         #引入requests网页处理模块
from lxml import etree          #引入etree源码处理方法
import csv          #预留文件输出模块
class item:
    def __init__(self):
        self.title=[]
        self.author=[]
        self.time=[]
        self.content=[]

    def get_pagecode(self,i):
        url='http://tieba.baidu.com/f?kw=%E6%9E%97%E6%88%90%E5%88%9A&ie=utf-8&pn='+str(i*50)           #构造每一页的网页地址
        html=requests.get(url)
        selector=etree.HTML(html.text)
        print u"已读取第"+str(i+1)+u"页源码"
        return selector
    def get_titles(self,selector):
        title=selector.xpath('//*[@id="thread_list"]/li/div/div[2]/div[1]/div[1]/a')            #以xpath方法提取每一页的帖子标题，形成每一页的title列表
        print u"已读取标题"
        return title
    def get_author(self,selector):
        author=selector.xpath('//*[@id="thread_list"]/li/div/div[2]/div[1]/div[2]/span/a')
        print u"已读取作者"
        return author
    def get_time(self,selector):
        time=selector.xpath('//*[@id="thread_list"]/li/div/div[2]/div[2]/div[2]/span[2]')
        print u"已读取发帖时间"
        return time
    def get_content(self,selector):
        content=selector.xpath('//*[@id="thread_list"]/li/div/div[2]/div[2]/div[1]/div')
        print u"已读取内容摘要"
        return content

    def write_to_item(self,title,author,time,content):
        for i in range(0,len(title)):
            self.title.append(title[i].text)
            self.author.append(author[i].text)
            self.time.append(time[i].text)
            self.content.append(content[i].text)
        print u"已写入内存"
    def write_to_file(self,fileadd,filename):
        f_name=fileadd+'\\'+filename
        f=open(f_name,'w')
        print u"已写入文件"+filename+u"，文件位于目录"+fileadd
        for i in range(0,len(self.title)):
            print u"正在写入第"+str(i+1)+u"个帖子"
            f.writelines(self.title[i].encode('gb18030'))            #当前titles内的信息均以unicode编码形式存储，使用encode方法将其转化为GB18030编码，输出才能显示为中文(decode方法将某数据转化为中间编码unicode形式)
    #因为标题中含有部分颜文字符号，因此使用GB18030编码而不是GB2312编码(仅有中文的情况下使用GB2312已经能够满足要求)
            f.write('\n')           #文件的writelines不自动换行，因此需要手动写入换行符
            f.writelines(self.author[i].encode('gb18030'))
            f.write('\n')
            f.writelines(self.time[i].strip())
            f.write('\n')
            f.writelines(self.content[i].encode('gb18030').strip())
            f.write('\n')
            f.write('\n')
        f.close()
    def start(self,i):
        print u"开始读取"
        selector=self.get_pagecode(i)
        title=self.get_titles(selector)
        author=self.get_author(selector)
        time=self.get_time(selector)
        content=self.get_content(selector)
        self.write_to_item(title,author,time,content)
        self.write_to_file(fileadd,filename)

i=0
fileadd='F:\ctemp\python'
filename='baidubbs.txt'
item=item()
item.start(i)
