# -*- coding:utf-8 -*-
import requests		# 网页处理模块
import re 			# 正则表达式模块

# 读取目标网页url
page=[]			# 建立目标网页的列表
for i in range(0,101,50):			# 手动获取每一页的编页信息
    html='http://tieba.baidu.com/f?kw=%E6%9E%97%E6%88%90%E5%88%9A&ie=utf-8&pn='+str(i)				# 获取网页地址
    page.append(html)			# 逐个添加至目标网页列表当中
    # print html.text.encode('utf-8')			#输出网页源代码，已强制转化为uft-8形式

# 提取目标网页中的各项元素
tops=[]         # 建立各页置顶帖的列表
titles=[]           # 建立各页帖子标题的列表
contents=[]         # 建立各页帖子摘要的列表
authors=[]          # 建立各页帖子主题作者的列表
times=[]            # 建立各页帖子最后回复时间的列表(发帖时间主网页内不可见)
for url in page:			# 对每一个目标网页进行处理
    html=requests.get(url)			# 获取网页源代码
    tops.append(re.findall('<i class="icon-top.*?alt="(.*?)" title="',html.text))       # 用正则表达式匹配置顶帖，生成列表
    titles.append(re.findall('<a href="/p/.*?" title="(.*?)" target="_blank" class="j_th_tit ">.*?',html.text,re.S))		# 用正则表达式匹配标题，生成列表
    contents.append(re.findall('<div class="threadlist_abs threadlist_abs_onlyline ">(.*?)</div>',html.text,re.S))          # 用正则表达式匹配摘要，生成列表
    authors.append(re.findall('<span class="tb_icon_author ".*?title="(.*?)"',html.text,re.S))          # 用正则表达式匹配作者，生成列表
    times.append(re.findall('<span class="threadlist_reply_date pull_right j_reply_data" title=".*?">(.*?)</span>',html.text,re.S))         # 用正则表达式匹配最后回复时间，生成列表
    # 两处(.*?)则生成二维列表
    # 在<>括号内部可以用.*?不加括号来剔除动态内容，也可用其来代替换行符与空格等，实现多行源码的正则表达式匹配

# 结果IDE输出测试
# for i in range(0,len(times)):
#     top_num=len(tops)
#     print titles[i+top_num]
#     if contents[i]=="":
#         print u"(没有内容)"
#     else:
#         print contents[i].strip()
#     print authors[i+top_num].strip()
#     print times[i].strip()
#     print "---------divide---------"

# 正则表达式书写如下
# re_title='<a href="/p/.*?" title="(.*?)" target="_blank" class="j_th_tit ">.*?'
# re_content='<div class="threadlist_abs threadlist_abs_onlyline ">(.*?)</div>'
# re_author='<span class="tb_icon_author ".*?title="(.*?)"'
# re_time='<span class="threadlist_reply_date pull_right j_reply_data" title=".*?">(.*?)</span>'

# 写入文件方法如下
f=open('F:\ctemp\python\\baidubbs_re.txt','w')          # 以只写方式，打开某一目录下的txt文件，用于存储帖子信息
# w为只写，并清除文件现有信息
# a为追加，在文件现有信息后加入要写入的信息
# r为只读
for i in range(0,len(times)):           # 以上各个列表均为二维列表，第一项编码为页数
    top_num=len(tops[i])            # 确定置顶帖数目，因置顶帖没有最后回复时间与内容摘要接口，因此不予录入(或考虑单独录入)
    for j in range(0,len(times[i])):            # 在每一页中按帖子顺序进行输出
        f.writelines(titles[i][j+top_num].encode('gb18030'))            # 按GB18030编码方式输出标题(去除置顶帖的影响)
        f.writelines('\n')          # 文件操作方法中writelines无法实现自动换行，因此手动写入换行符
        if contents[i][j]==u'\n            \n        ':         # 内容摘要为空时正则表达式读取为左边的格式
            f.writelines(u"(没有内容)".encode('gb18030'))           # 以(没有内容)表示内容摘要为空
            f.writelines('\n')          # 文件操作方法中writelines无法实现自动换行，因此手动写入换行符
        else:
            f.writelines(contents[i][j].strip().encode('gb18030'))          # 如果存在内容摘要，则输出内容摘要
            f.writelines('\n')          # 文件操作方法中writelines无法实现自动换行，因此手动写入换行符
        f.writelines(authors[i][j+top_num].strip().encode('gb18030'))           # 输出主题作者
        f.writelines('\n')          # 文件操作方法中writelines无法实现自动换行，因此手动写入换行符
        f.writelines(times[i][j].strip())           # 输出最后回复时间
        f.writelines('\n')          # 文件操作方法中writelines无法实现自动换行，因此手动写入换行符
        if  i != len(times)-1 or j != len(times[i])-1:          # 最后一项后面不需要再加入分割线，因此需要判定是否是最后一项
            f.writelines('\n')          # 分割线前空出一行
            f.writelines(u"-------------------我是分割线-------------------".encode('gb18030'))
            f.writelines('\n')          # 文件操作方法中writelines无法实现自动换行，因此手动写入换行符
            f.writelines('\n')          # 分割线后空出一行
f.close()           # 写入完成，关闭文件