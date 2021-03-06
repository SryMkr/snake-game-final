'''
author SryMkr
date: 2021.11.6
the function of this library is to download words' pronunciation
本函数的作用是一个个下载发音，但是单词如果有空格会找不到发音，需要在文件里自己一个个改
本页函数在游戏中没有需要使用的地方，在毕业之前本页函数没有任何需要改的地方 在游戏函数中没有需要该的地方
'''


# import package
import os
import urllib.request


# 下载的是有道的发音
class youdao():
    # 看下载的是美音还是英音
    def __init__(self, word, type=1):
        '''
        type = 0：美音
        type = 1：英音
        '''
        word = word.lower()  # 改小写
        self._type = type  # 发音方式
        self._word = word  # 要下载的单词单词

        # get file path 下载到那个发音的文件夹
        self._dirRoot = os.path.dirname(os.path.abspath(__file__))
        if 0 == self._type:
            self._dirSpeech = os.path.join(self._dirRoot, 'Speech_US')  # 美音库
        else:
            self._dirSpeech = os.path.join(self._dirRoot, 'Speech_EN')  # 英音库
        '''
        # 判断是否存在美音库
        if not os.path.exists('Speech_US'):
            # 不存在，就创建
            os.makedirs('Speech_US')
        '''
        # 判断是否存在英音库
        if not os.path.exists('Speech_EN'):
            # 不存在，就创建
            os.makedirs('Speech_EN')

        # get the pronouciation path 得到最终要下载到的文件夹
        if 0 == self._type:
            self._dirSpeech = os.path.join(self._dirRoot, 'Speech_US')  # 美音库
        else:
            self._dirSpeech = os.path.join(self._dirRoot, 'Speech_EN')  # 英音库

    #  看单词是否已经存在
    def _getWordMp3FilePath(self, word):
        '''
        获取单词的MP3本地文件路径
        如果有MP3文件，返回路径(绝对路径)
        如果没有，返回None
        '''
        word = word.lower()  # 小写
        self._word = word
        self._fileName = self._word + '.mp3'
        self._filePath = os.path.join(self._dirSpeech, self._fileName)

        # 判断是否存在这个MP3文件
        if os.path.exists(self._filePath):
            # 存在这个mp3
            return self._filePath
        else:
            # 不存在这个MP3，返回none
            return None

    # 获得单词的url
    def _getURL(self):
        '''
        私有函数，生成发音的目标URL
        http://dict.youdao.com/dictvoice?type=0&audio=
        '''
        self._url = r'http://dict.youdao.com/dictvoice?type=' + str(
            self._type) + r'&audio=' + self._word

    def down(self):
        '''
        下载单词的MP3
        判断语音库中是否有对应的MP3
        如果没有就下载
        '''
        self.word = self._word.lower()  # 小写
        tmp = self._getWordMp3FilePath(self.word)
        if tmp is None:
            self._getURL()  # 组合URL
            # 调用下载程序，下载到目标文件夹
            # print('不存在 %s.mp3 文件\n将URL:\n' % word, self._url, '\n下载到:\n', self._filePath)
            # 下载到目标地址
            urllib.request.urlretrieve(self._url, filename=self._filePath)
            #print('%s.mp3 下载完成' % self._word)
        #else:
            #print('已经存在 %s.mp3, 不需要下载' % self._word)

        # 返回声音文件路径
        return self._filePath
