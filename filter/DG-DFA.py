# -*- coding: utf-8 -*-
# @Author: liuying
# @Date:   2019/7/22
# @Last Modified by:   liuying
# @Last Modified time: 2020/9/27
# @ ---------- GD-DFA过滤算 法----------
import time

time1 = time.time()


class node(object):  # 存放敏感词节点值
    def __init__(self):
        self.isStart = 0  # 是否 结束节点  0--中间节点 ， 1--开始节点
        self.isEnd = 0  # 是否 结束节点  0--中间节点 ， 1--结束节点
        self.next = {}  # 存下一个敏感词键，值为node对象,node对象的next（）为字典
        self.starts = {}  # 存放该节点的开始节点


class DFAFilter(object):
    """DFA过滤算法"""

    def __init__(self):
        super(DFAFilter, self).__init__()
        self.keyword_chains = {}  # 入口表、树
        # 叶节点结束符--先留着

    # 读取解析敏感词
    def parseSensitiveWords(self, path):
        ropen = open(path, 'r')
        text = ropen.read()
        keyWordList = text.split(',')
        for keyword in keyWordList:
            self.addSensitiveWords(str(keyword).strip())
        # 输出敏感词树
        print("敏感词树：")
        print(str(self.keyword_chains))
        # print("敏感词：")
        # print( text)

    # 生成敏感词树
    def addSensitiveWords(self, keyword):  # keyword=傻逼
        # 数据预处理
        keyword = keyword.lower()  # lower() 方法转换字符串中所有大写字符为小写。
        chars = keyword.strip()  # chars=傻逼  #strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
        if not chars:  # 敏感词不为空？
            return

        entrance = self.keyword_chains  # 入口表

        # 构造敏感词表、树        先建立连接关系，再设置起点、末点标志   将起点 添加到该末节点

        for i in range(len(chars)):

            if chars[i] not in entrance:  # 是否在 入口表
                entrance[chars[i]] = node()  # 不在--新建节点
            if i > 0:
                entrance[last_char].next[chars[i]] = entrance[chars[i]]  # 将该节点加到上一个节点的next
            last_char, last_node = chars[i], entrance[chars[i]]  # 将当前节点保存，以便 链接下一节点

        # 设置起点、末点

        entrance[chars[0]].isStart = 1
        entrance[chars[len(chars) - 1]].isEnd = 1
        start_key, start_node = chars[0], entrance[chars[0]]  # 起点
        entrance[chars[len(chars) - 1]].starts[start_key] = start_node  # 将起点 添加到该末节点

    # 过滤敏感词   起字 在入口表里查询  有：进入next匹配   无：查询下一个字
    def filterSensitiveWords(self, message, repl="*"):  # repl="*"    默认参数------->可做笔记
        message = message.lower()
        ret = []  # 存储过滤后得字符串
        start_index = 0
        end_index = 0

        # 文本为空，直接返回空字符串
        if len(message) <= 0:
            return ""
        count = 0  # 替换敏感词的数量
        # 文本不为空
        entrance = self.keyword_chains
        level = entrance
        i = 0
        while i < len(message):  # 循环
            if message[i] in entrance and entrance[message[i]].isStart == 1:  # 是否为 入口表 起点
                start_index = i
                level = entrance[message[i]].next

                for j in range(i + 1, len(message)):
                    if message[j] in level:  # 判断 匹不匹配下一节点
                        # 此处需要添加 是否为 末节点的判断代码
                        if message[i] in level[message[j]].starts:  # 判断当前节点是不是 当前起点的末点
                            end_index = j  # 是-敏感词末端位置
                            ret.append(repl * ((end_index - start_index) + 1))  # 替换敏感词
                            count = count + 1
                            i = j  # 查找起点时，跳过已被检测出来的敏感词
                            break
                        else:  # 为此次的中间节点
                            level = entrance[message[j]].next

                    else:  # 不匹配-此次匹配均无效，从起点的下一位开始搜搜索
                        ret.append(message[i])
                        break
            else:  # 该字不是入口，退出本次循环
                ret.append(message[i])

            i = i + 1  # while 的自增
        print(count)
        return ''.join(ret)


# 主函数执行
if __name__ == "__main__":
    gfw = DFAFilter()
    gfw.parseSensitiveWords('sensitive_words.txt')

    # text = "你真是个傻逼，大傻子，傻逼蛋，大坏蛋，坏人。SB！"

    file = open("in.txt", "r")  # 从文件中读入数据
    text = file.read()

    print()
    print("过滤前文本：")
    print(text)
    result = gfw.filterSensitiveWords(text)

    file = open("out.txt", "w")  # 把过滤后的内容写到txt中
    file.write(result)
    file.close()

    print()
    print("过滤后文本：")
    print(result)
    time2 = time.time()
    print('总共耗时:' + str(time2 - time1) + 's')
