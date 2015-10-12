# -*- coding:utf-8 -*-
import requests		#网页处理模块
import re 			#正则表达式模块
import code			#解决编码错误
page=[]			#建立目标网页的列表
for i in range(0,101,50):			#手动获取每一页的编页信息
	html='http://tieba.baidu.com/f?kw=%E6%9E%97%E6%88%90%E5%88%9A&ie=utf-8&pn='+str(i)				#获取网页地址
	page.append(html)			#逐个添加至目标网页列表当中
	#print html.text.encode('utf-8')			#输出网页源代码，已强制转化为uft-8形式
for url in page:			#对每一个目标网页进行处理
	html=requests.get(url)			#获取网页源代码
	titles=re.findall('<a href="/p/(.*?)" title="(.*?)" target="_blank" class="j_th_tit ">',html.text)		#用正则表达式匹配标题，生成列表
	#两处(.*?)则生成二维列表
