'''
author: SryMkr
date:2021.11.6
this function is to deal with the words
该文件要在游戏函数中使用
'''

# import packages
from xlutils.copy import copy
import xlrd, xlwt
import random


# -----------------------------------------------------------------------------------------------------------------------
# 取得本次在词库中随机选择的单词，并且要读入要训练的单词数
def read_taskwords_xls(path, train_words_number):
    words = []
    rs = []
    words_tra = []
    # open workbook
    workbook = xlrd.open_workbook(path)
    # get all sheets by sheet names
    sheets = workbook.sheet_names()
    # get the first sheet
    worksheet = workbook.sheet_by_name(sheets[0])
    # 获得单词的行数
    words_numbers = worksheet.nrows
    # 如果训练库中有足够的单词数，就加载
    if str(train_words_number) == '':
        pass
    elif int(train_words_number) < int(words_numbers):
        # 在所有的单词中选择一定的数量作为本次训练的单词数，随机选择
        rs = random.sample(range(words_numbers), int(train_words_number))
    else:
        # 如果没有足够的单词数，这加载词库中的所有单词
        rs = random.sample(range(words_numbers), words_numbers)
    # 顺序获得选中单词的英文与中文
    for word_index in rs:
        # get the correspond content
        words.append(worksheet.cell_value(word_index, 0))
        # if word in words
        words_tra.append(worksheet.cell_value(word_index, 1))
    return words, words_tra


# ----------------------------------------------------------------------------------------------------------------------
# 这个主要是在选中的单词表中，在原表中删除已经记住的单词
def delete_taskwords_xls(path, wordlist):
    i = 0
    # open workbook
    workbook = xlrd.open_workbook(path)
    # get all sheets by sheet names
    sheets = workbook.sheet_names()
    # get the first sheet
    worksheet = workbook.sheet_by_name(sheets[0])
    # 创建一个空的表格
    newworkbook = xlwt.Workbook()
    # 创建一个空的表单
    new_worksheet = newworkbook.add_sheet('sheet1')
    # 得到所有单词
    words = worksheet.col_values(0)
    # 如果已经记住的单词在原来的单词表中
    for word in words:
        if word not in wordlist:
            # 取得这个单词在原单词表中的索引
            word_index = words.index(word)
            # 根据索引得到这个值
            value = worksheet.row_values(word_index)
            # 将这个值写到表中
            new_worksheet.write(i, 0, value[0])
            new_worksheet.write(i, 1, value[1])
            i = i + 1
    # save file
    newworkbook.save(path)


# ----------------------------------------------------------------------------------------------------------------------
# 将已经记住的单词添加到已经记住表单中,将单词和翻译分开
def write_knownwords_xls(path, wordlist, wordtra_list):
    # get the len of value
    index = len(wordlist)
    # open a workbook
    workbook = xlrd.open_workbook(path)
    # get all sheet names
    sheets = workbook.sheet_names()
    # get the first sheet
    worksheet = workbook.sheet_by_name(sheets[0])
    # get the rows of sheet
    rows_old = worksheet.nrows
    # 得到第一列的值
    words = worksheet.col_values(0)
    # copy the workbook
    new_workbook = copy(workbook)
    # get the first worksheet
    new_worksheet = new_workbook.get_sheet(0)
    # if word in words
    for word in wordlist:
        if word not in words:
            for i in range(index):
                new_worksheet.write(rows_old + i, 0, wordlist[i])
                new_worksheet.write(rows_old + i, 1, wordtra_list[i])
        else:
            pass
    # save file
    new_workbook.save(path)
