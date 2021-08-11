'''
author SryMkr
date: 2021.8.10
the function of this library is for downloading words' phonetics
有时候单词比较多会不下载，但是也不是找不到的原因，可能是网络问题
最好的办法就是我们已经下载好了，尽量网络的还有机器的依赖
本算法最基本的逻辑结构就是一个单词一个音标写到excel中,并且也是在xls中读取单词音标,仅限与做实验使用
'''

# import packages
import os
import requests
import re
from xlutils.copy import copy
import xlrd


# write content into excel.xls  format: list[word,phonetic]
# 最不好的地方就是得一个个打开一个个复制，时间开销太大，不过做实验是够了
def write_excel_xls_append(path, value):
    # get the len of value 只有两个所以为2
    index = len(value)
    # open a workbook，看你想往哪个文件里面写
    workbook = xlrd.open_workbook(path)
    # get all sheet names
    sheets = workbook.sheet_names()
    # get the first sheet，一般都写在第一页
    worksheet = workbook.sheet_by_name(sheets[0])
    # get the rows of sheet，看文件中已经有多少行了
    rows_old = worksheet.nrows
    # copy the workbook，需要复制一个文件来覆盖原文件
    new_workbook = copy(workbook)
    # get the first worksheet，得到需要添加的那一页
    new_worksheet = new_workbook.get_sheet(0)
    for i in range(0, index):
            # column always is 0 and 1  参数i其实就是列 第一列写单词 第二列写发音，
            new_worksheet.write(rows_old, i, value[i])
    # save file 覆盖原文件
    new_workbook.save(path)


# check whether the words in excel.xls
def read_excel_xls(path,word):
    # open workbook
    workbook = xlrd.open_workbook(path)
    # get all sheets by sheet names
    sheets = workbook.sheet_names()
    # get the first sheet
    worksheet = workbook.sheet_by_name(sheets[0])
    # get the correspond content，得到第一列的所有单词
    words = worksheet.col_values(0)
    # if word in words，查看所需要的单词在不在列表中
    if word in words:
        return True
    else:
        return False


# phonetic alphabet class
class OxfordDictionary():

    # initialize empty string
    phoneticSpelling = ""

    # create directory for phonetic format ['word','xxx.xls']
    def __init__(self, word, filename):
        # convert to lowercase word
        word = word.lower()
        # move space
        self._word = word.strip()
        # filename
        self._fileName = filename
        # get the absolute current path
        self._dirRoot = os.path.dirname(os.path.abspath(__file__))
        # concatenate the file path
        self._dirSpeech = os.path.join(self._dirRoot, 'Words_phonetic')

        # file exist?
        if not os.path.exists('Words_phonetic'):
            # create if no
            os.makedirs('Words_phonetic')

        # get the filename path,直接定位到指定的xls文件
        self._filePath = os.path.join(self._dirSpeech, self._fileName)

    # get the download url
    def _getPho(self):
        # phonetic exist?
        if read_excel_xls(self._filePath,self._word):
            # yes pass
            pass
        # no download
        else:
            list = []
            list.append(self._word)
            # get the url
            request = requests.get("https://en.oxforddictionaries.com/definition/" + self._word)
            # convert the whole content to text
            html = request.text
            # locate the target content
            regularExpression = r'<span\s+class="phoneticspelling">/([^\/]*)/</span>'
            # scan all content and return the first matched content with ignoring the l_u case letter
            matchObject = re.search(regularExpression, html, re.I)
            # if get
            if matchObject:
                # if phonetic exist
                if matchObject.group(1):
                    self.phoneticSpelling = matchObject.group(1)
                else:
                    self.phoneticSpelling = None
            # make the list format
            list.append(self.phoneticSpelling)
            # write into the excel.xls
            write_excel_xls_append(self._filePath, list)


# get the word phonetic in excel.xls   path使用绝对路径和相对路径都可以
def get_word_pho(path,word):
    # open workbook
    workbook = xlrd.open_workbook(path)
    # get all sheets by sheet names
    sheets = workbook.sheet_names()
    # get the first sheet
    worksheet = workbook.sheet_by_name(sheets[0])
    # get the correspond content
    words = worksheet.col_values(0)
    # if word in words
    if word in words:
        # return the word index
        word_index = words.index(word)
        # return the phonetic
        return worksheet.cell_value(word_index, 1)
    else:
        return None


