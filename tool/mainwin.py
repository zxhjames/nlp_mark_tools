# -*- coding: utf-8 -*-
# @Time :   19-5-2 下午5:06 
# @Author :     HaiYang Gao
# @OS：  ubuntu 16.04
# @File :   mainwin.py 

from basewin import MyFrame1

import os
import codecs
import platform
import json
import sys
import collections
import wx
"""
==============================step1：参数自定义=======================================
自定义标注参数，自行调整;
通常修改record_path，id_str，content_str就可以了
"""
Numbers = 99999  # 待标注的数据条数
MaxLengthOfKeyWord = 15  # 中心词最大长度
Tag_flag = 0  # value = 0 or -1; 如果Tag_flag=-1，则可以不选tag，也可以进行下一条内容的标注
data_path = '../data/example.json'  # 待标注文件的路径
record_path = '../data/records/record_01.txt'  # 标注文件的位置
# id_str改为自己json文件对应的键值,content_str改为想显示的内容
# 中文键要在字符串前加上u，比如id_str = u'序号'
id_str = 'id'  # 主键，唯一
content_str = 'content'  # 文本内容
"""===============================step1调整结束，step2在basewin.py中====================="""
sys.setrecursionlimit(Numbers + 100)


class MainWindows(MyFrame1):
    record_file = record_path
    data_file = data_path

    def __init__(self, title):
        MyFrame1.__init__(self, None)
        self.cur_progress = 0  # 记录当前标注的条数
        self.which_words_items = -1  # 记录哪种类型的关键词
        self.textboxfont = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.content.SetFont(self.textboxfont)
        self.read_data() # 读取源数据
        self.load_record() 
        self.reinit_record()
        self.print_content()

        # 原因中的核心名词
        self.keyword_radio.item_name = 'keyword'
        self.key_words.item_name = 'keyword'

        # 原因中的核心名词的谓语状态
        self.name_radio.item_name = 'name'
        self.name_words.item_name = 'name'

        # 中心词
        self.address_radio.item_name = 'address'
        self.add_words.item_name = 'address'


        # todo add 结果集中的核心名词
        self.result_words.item_name = "result"
        self.result_radio.item_name = "result"

        # todo add 结果中的核心名词的谓语状态
        self.result_status_words.item_name = "result_status"
        self.result_status_radio.item_name = "result_status"


        

    # 初始化
    def reinit_record(self):
        # 在这里删除tags的影响
        # self.tags = []
        # # todo *****在这里重新定义结构体****
        # self.document = {} # document(包含block_id,text)
        # self.key = "" #key
        # self.qas = [] #qas
        # self.answers = {
        #     'start':0,
        #     'start_block':0,
        #     'end':0,
        #     'end_block':0,
        #     'text':''
        # }


        self.address = [] # 中心词
        self.person = [] # 人员
        self.keyword = [] # 原因中的核心名词
        # self.name = [] # 原因中核心名词的状态
        self.result = [] # 结果集合
        self.result_status = [] # 结果集中的谓语状态
        self.which_words_items = -1
        self.print_keywords()

        #for i in range(1, 21):
        #   self.__getattribute__('m_toggleBtn' + str(i)).SetValue(False)

        self.keyword_radio.SetValue(False)
        self.name_radio.SetValue(False)
        self.address_radio.SetValue(False)
        # todo add
        self.result_radio.SetValue(False)
        self.result_status_radio.SetValue(False)
        
        # todo 纪录标注内容的索引
        self.reason_arr = []
        self.reason_status_arr = []
        self.key_arr = []
        self.result_arr = []
        self.result_status_arr = []


    def read_data(self):
        with codecs.open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f, object_pairs_hook=collections.OrderedDict)
            self.data = []
            for _, v in data['data'].items():
                self.data.append(v)
            self.data_size = len(self.data)

    def print_content(self):
        cur_doc = self.data[self.cur_progress]
        if cur_doc[id_str] in self.ids:
            self.cur_progress += 1
            return self.print_content()
        # 标注界面显示的标题
        title = u'当前文本id:[' + str(cur_doc[id_str]) + '],当前是第' + str(self.cur_progress) + '条,还剩' + str((self.data_size - self.cur_progress))+ '条'
        content = cur_doc[content_str]
        self.title.SetLabel(title)
        self.redefine_Textctrl_write(self.content, content)

    # 定义按钮事件
    # def toggle_label(self, event):
    #     eo = event.GetEventObject()
    #     if eo.GetValue():
    #         self.tags.append(eo.GetLabel())
    #     else:
    #         idx = self.tags.index(eo.GetLabel())
    #         del (self.tags[idx])

    # 加载标注记录, 获得续标断点
    def load_record(self):
        self.ids = []
        if os.path.exists(self.record_file):
            with codecs.open(self.record_file, 'r', encoding='utf-8') as f:
                records = [d for d in f.read().split('\n') if len(d)]
            for rd in records:
                self.ids.append(json.loads(rd)[id_str])

    # 显示选择的数据
    def print_keywords(self):
        if len(self.address):
            self.redefine_Textctrl_write(self.add_words, '(' + '),('.join(self.address) + ')')
        else:
            self.redefine_Textctrl_write(self.add_words, '')
        if len(self.person):
            self.redefine_Textctrl_write(self.name_words, '(' + '),('.join(self.person) + ')')
        else:
            self.redefine_Textctrl_write(self.name_words, '')
        if len(self.keyword):
            self.redefine_Textctrl_write(self.key_words, '(' + '),('.join(self.keyword) + ')')
        else:
            self.redefine_Textctrl_write(self.key_words, '')
        if len(self.result):
            self.redefine_Textctrl_write(self.result_words,'(' + '),('.join(self.result) + ')')
        else:
            self.redefine_Textctrl_write(self.result_words,'')
        if len(self.result_status):
            self.redefine_Textctrl_write(self.result_status_words,'(' + '),('.join(self.result_status) + ')')
        else:
            self.redefine_Textctrl_write(self.result_status_words,'')



    """
    =============================step3:选择写入文件的内容=============================
    """

    # 写入记录
    def write_a_record(self):
        save_record = collections.OrderedDict()

        # save_record[id_str] = self.data[self.cur_progress][id_str]
        # save_record[content_str] = self.data[self.cur_progress][content_str]
        
        # todo: write to file from here
        # 文档结构体
        save_record[u'document'] = [{
            'block_id' : self.cur_progress, # 文本索引
            'text' : self.data[self.cur_progress][content_str] # 文本内容
        }]

        # 文本id
        save_record[u'key'] = self.data[self.cur_progress][id_str]

        # 文本的问题(question)，答案(answer)
        write_arr = []

        answers_obj1 = {
            'answers':[{
                'end' : self.reason_arr[1],
                'end_block':"0",
                'start':self.reason_arr[0],
                'start_block':"0",
                'text':self.address[0] if len(self.address) > 0 else ""
            }],
            'question':'原因中的核心名词'
        }
        answers_obj2 = {
            'answers':[{
                'end' : self.reason_status_arr[1],
                'end_block':"0",
                'start':self.reason_status_arr[0],
                'start_block':"0",
                'text':self.person[0] if len(self.person) > 0 else ""
            }],
            'question':'原因中的谓语或状态'
        } 
        answers_obj3 = {
             'answers':[{
                'end' : self.key_arr[1],
                'end_block':"0",
                'start':self.key_arr[0],
                'start_block':"0",
                'text':self.keyword[0] if len(self.keyword) > 0 else ""
            }],
            'question':'中心词'
        } 
        answers_obj4 = {
             'answers':[{
                'end' : self.result_arr[1],
                'end_block':"0",
                'start':self.result_arr[0],
                'start_block':"0",
                'text':self.result[0] if len(self.result) > 0 else ""
            }],
            'question':'结果中的核心名词'
        } 
        answers_obj5 = {
            'answers':[{
                'end' : self.result_status_arr[1],
                'end_block':"0",
                'start':self.result_status_arr[0],
                'start_block':"0",
                'text':self.result_status[0] if len(self.result_status) > 0 else ""
            }],
            'question': '结果中的谓语或状态'
        } 
        write_arr.append(answers_obj1)
        write_arr.append(answers_obj2)
        write_arr.append(answers_obj3)
        write_arr.append(answers_obj4)
        write_arr.append(answers_obj5)
        save_record[u'qas'] = [write_arr]

        # 文本的status
        save_record[u'status'] = '1'





        # save_record[u'reason'] = self.keyword
        # # save_record[u'reason_status'] = self.name
        # save_record[u'reason_status'] = self.person

        # save_record[u'key'] = self.address

        # #todo add
        # save_record[u'result'] = self.result
        # save_record[u'result_status'] = self.result_status
        # save_record['tags'] = self.tags

        """
        例子：添加一个写入。
        save_record[u'作者'] = self.data[self.cur_progress]['author']  
        save_record['time'] = self.data[self.cur_progress]['time']
        # 这里的'author'必须是json文件中的键，中文前要加'u'

        不写入：
        不想写入，就注释或删掉某一句，如 # line126，则不会写入地名信息
        """
        save_text = json.dumps(save_record, ensure_ascii=False)
        with codecs.open(self.record_file, 'a', encoding='utf-8') as f:
            f.write(save_text + '\n')

    """
    ========step3调整结束，可运行"mainwin.py"，开始标注================================
    """

    def next_doc(self, event):
        #if len(self.tags) == Tag_flag:
        #    wx.MessageBox(u'您没有选择任何标签', u'警告', wx.OK | wx.ICON_EXCLAMATION)
        #else:
        self.write_a_record()
        self.cur_progress += 1
        if self.cur_progress == self.data_size:
            self.exit(0)
        self.reinit_record()
        self.print_content()
        self.print_keywords()

    def get_sellect_words(self, event):
        # 选择的数据和索引
        words = self.content.GetStringSelection()
        edge = self.content.GetSelection()
        print(words,edge[0],edge[1])
        if self.which_words_items == -1 and len(words) > 0:
            wx.MessageBox(u'请选择一种要标注的关键字类型', u'警告', wx.OK | wx.ICON_EXCLAMATION)
            return False
        elif len(words) > MaxLengthOfKeyWord:
            a = wx.MessageBox(words + u' \n\n是否选为关键词?', u'关键词过长验证', wx.YES_NO | wx.ICON_EXCLAMATION)
            if not a == wx.YES:
                return False
        elif len(words) < 2:
            return False

        if self.which_words_items == 1:
            self.address.append(words)
            self.reason_arr = edge
        elif self.which_words_items == 2:
            self.person.append(words)
            self.reason_status_arr = edge
        elif self.which_words_items == 3:
            self.keyword.append(words)
            self.key_arr = edge
        elif self.which_words_items == 4:
            self.result.append(words)
            self.result_arr = edge
        elif self.which_words_items == 5:
            self.result_status.append(words)
            self.result_status_arr = edge
        self.print_keywords()

    def select_address(self, event):
        self.which_words_items = 1

    def select_name(self, event):
        self.which_words_items = 2

    def select_keyword(self, event):
        self.which_words_items = 3

    def select_result(self,event):
        # todo 结果名词
        self.which_words_items = 4

    def select_result_status(self,event):
        # todo 结果名词中的谓语状态
        self.which_words_items = 5

    def del_words(self, event):
        print(dir(event))

    def exit(self, flag):
        if flag == 0:
            wx.MessageBox(u'标注已经完成, 感谢您的参与,么么哒!', u'警告', wx.OK | wx.ICON_EXCLAMATION)

    # 根据不同平台使用不同的Textctrl方法
    def redefine_Textctrl_write(self, object, string):
        if 'windows' in platform.system().lower():
            object.SetLabel(string)
        else:
            object.SetValue(string)


if __name__ == '__main__':
    app = wx.App()
    main_win = MainWindows(title='mark tool')
    main_win.Show()
    app.MainLoop()
