
import urllib
import requests
import tushare as ts
import pandas as pd
import matplotlib
from urllib import request
import re
import os
#df=ts.get_hist_data('600415',start='2015-04-01',end='2015-06-18')
#ts.get_hist_data('600848')
#encoding: utf-8


class Spider(object):
    def __init__(self):
        self.url='http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml'
        self.user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'

    def get_page(self,url):

        res ='null'
        # 创建Request对象
        try:
            req = request.Request(url)
            # 传入headers
            req.add_header('User-Agent', self.user_agent)

            response = request.urlopen(req,timeout=30)
            res = response.read().decode('gb18030')
        except:
            print('time out')
        # 读取响应信息并解码
        #temp = response.read()
        return res

    def analyze(self, html):
        # regex = re.compile('<div class="content">.+</div>',re.S)
        #regex = re.compile('<td><div align="center">.+?>.+?(.+?)</a></div></td>.*?<td><div align="center">(.+?)</div></td>.*?<td><div align="center">(.+?)</div></td>.*?<td><div align="center">(.+?)</div></td>.*?<td class="tdr"><div align="center">(.+?)</div></td>.*?<td class="tdr"><div align="center">(.+?)</div></td>.*?<td class="tdr"><div align="center">(.+?)</div></td>', re.S)
        regex = re.compile( 'a target=\'_blank\'.+?\n(.+?)</a>'
                            '[\s\S]+?<td><div align="center">(.+?)</div></td>'
        '[\s\S]+?<td><div align="center">(.+?)</div></td>'
        '.[\s\S]+?<td><div align="center">(.+?)</div></td>'
        '[\s\S]+?<td class="tdr"><div align="center">(.+?)</div></td>'
        '[\s\S]+?<td class="tdr"><div align="center">(.+?)</div></td>'
        '[\s\S]+?<td class="tdr"><div align="center">(.+?)</div></td>'
                            )

        # regex = re.compile('<div class=.+</div>', re.S)
        return  (re.findall(regex, html))

    def save(self,path, items, page_index):

        if not os.path.exists(path):
            os.makedirs(path)
        file_path = path + '\\' + str(page_index) + '.txt'
        f = open(file_path, 'w', encoding='utf-8')

        for item in items:
            for j in range(0,2):
                f.write(item[j])
                f.write(', ')
            f.write('\n')
        f.close()

    def save1(self,path, items, page_index):

        if not os.path.exists(path):
            os.makedirs(path)
        file_path = path + '\\' + str(page_index) + '.txt'
        f = open(file_path, 'w', encoding='utf-8')

        j=0
        for item in items:
            for i in item:
                f.write(i)
                f.write('\n')

        f.close()
    def run(self):
        for i in range(601006,601008):
            content = self.get_page(i)
            items = self.analyze(content)
            path = 'J:\\code\\python\\1\\qiubai'
            self.save(path,items,i)

    def GetShareholderCount(self,code):
        # 获取code股票的股东数量
        url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/'+code+'.phtml'
        print(url)
        html = self.get_page(url)
        print('get url over')
        #regex = re.compile('strong([\s\S]+?)a([\s\S]+?)')
        regex = re.compile('/corp/view/vCI_HoldStockState.php.+?">(.+?)<''[\s\S]+?'
                            '/corp/view/vCI_HoldStockState.php.+?">(.+?)<''[\s\S]+?'
        '/corp/view/vCI_HoldStockState.php.+?">(.+?)<''[\s\S]+?'
        '/corp/view/vCI_HoldStockState.php.+?">(.+?)<''[\s\S]+?'
        '/corp/view/vCI_HoldStockState.php.+?">(.+?)<''[\s\S]+?'
        '/corp/view/vCI_HoldStockState.php.+?">(.+?)<''[\s\S]+?'
        '/corp/view/vCI_HoldStockState.php.+?">(.+?)<''[\s\S]+?'
        '/corp/view/vCI_HoldStockState.php.+?">(.+?)<''[\s\S]+?'
        '/corp/view/vCI_HoldStockState.php.+?">(.+?)<''[\s\S]+?'
                           '/corp/view/vCI_HoldStockState.php.+?">(.+?)<[\s\S]*'
                           )
        items=(re.findall(regex, html))
        print('re over')
        self.save1('J:\\code\\python\\1\\data_Shareholder',items, code)


import os.path

def func2(df,filename):
    try:
        # 计算是否半年内到达在两年内最低点附近10%内
        minA = 1000
        j=-1
        minIndex=0
        startData=90
        for i in df.close:
            j = j + 1
            if j<startData:
                continue
            if j> 500+startData:
                break
            if i < minA:
                minIndex=j
                minA = i
                minDate1=df.date[j]


        if minIndex < 125+startData:
            return 0

        j=-1
        flag = 0 #是否半年内到达在两年内最低点附近10%内
        for i in df.close:
            j += 1
            if j<startData:
                continue
            if j> 125+startData:
                break
            if i < minA * 1.1:
                minDate2 = df.date[j]
                flag = i

        if 0 == flag:
            return 0


        # 比半个月前股价高0.1，
        if len(df) <= 12+startData :
            return 0

        if  float(df.close[0+startData]) <= float(df.close[15+startData]) * 1.1:
            return 0
        # 获取5日线、10日线、20日线

        # 日期 ，开盘价， 最高价， 收盘价， 最低价， 成交量， 价格变动 ，涨跌幅，5日均价，10日均价，20日均价，5日均量，10日均量，20日均量，换手率

        if (float(df.ma5[0+startData]) <= float(df.ma10[0+startData])):
            return 0
        if (float(df.ma10[0+startData]) <= float(df.ma20[0+startData])):
            return 0

        print(filename)
        res = df.date[startData]
        print(res)
        #print(minDate1)
        #print(minA)
        #print(minDate2)
        #print(flag)
    except:
        pass

def func1():
    """
    到2年内的最低点位附近 半个月内股价趋势向上 5日10日20日 成多头排列 意思就是5日线最上 10日线其次 20日线最下方 这个应该是熊市的选股策略
    :return:
    """
    #遍历文件夹

    rootdir = 'J:\\code\\python\\1/data'  # 指明被遍历的文件夹

    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:  # 输出文件信息
            #print(      "the full name of the file is:" + os.path.join(parent, filename) ) # 输出文件路径信息
            df = pd.read_csv(os.path.join(parent, filename))
            func2(df,filename)

def GetData():
    stock_info = ts.get_stock_basics()
    # 获取所有股票代码
    for i in stock_info.index:
        print(i)
        try:
            df = ts.get_hist_data(code=i, start="2013-07-16")
            df.to_csv('J:\\code\\python\\1/data/'+ i +'_'+'hist_data'+'.csv',encoding="utf-8")
        except:
            pass

#获取股东数
def get_shareholders(code):
    df = pd.read_csv('J:\\code\\python\\1/data_stock_basics/stock_basics.csv')
    #res = df[df['code'].isin([codeIn]),'holders']
    index= df['code'].isin([code])
    res =  df.holders[index]
    return res

def save_shareholders():
    #获取并保存所有股东数
    spider = Spider()
    stock_info = ts.get_stock_basics()
    # 获取所有股票代码
    for i in stock_info.index:
        spider.GetShareholderCount(i)

def get_profit_add(code):
    df = pd.read_csv('J:\\code\\python\\1/data_stock_basics/report_data.csv')
    res = df.profits_yoy[df['code'].isin([code])]
    return res

def low_price(code):
    try:
        df = pd.read_csv('J:\\code\\python\\1/data/' + code + '_' + 'hist_data' + '.csv')
        min = 1000
        for i in df.index:
            if min>df.close[i]:
                min = df.close[i]
        if df.close[0]<min+2:
            return True
        else:
            return False
    except:
        return False

def trusts(code):
    return

def arange_trusts(input):
    trusts=[]
    for i in input:
        #查找i对应的信托数
        count = trusts(i)
        trusts.append(count)
    nvs = zip(trusts, input)
    nvDict = dict((trusts, input) for trusts, input in nvs)
    nvDict.sort
    return nvDict.input

def func_yao():
    stock_info = ts.get_stock_basics()
    res = []
    for i in stock_info.index:
## 2.股东户数（3万内即可）
        if get_shareholders(i) > 30000:
            continue
# 3.股东户数减少（20%以上）
        if get_shareholders_dec(i) < 20:
            continue
# 4.净利润同比增长（20%以上）
        if get_profit_add(i) < 20:
            continue
# 5.阶段跌幅大（目前价位位于近三年最低价两元以内范围）
        if False == low_price(i):
            continue
# 6.预增预盈（扭亏为盈）
        if False == return_profit(i):
            continue
# 7.财政扶持
        if False == Financial_support(i):
            continue
# 8.热门板块（锂电，高科技...）
        if False == hot_block(i):
            continue
# 9.国家扶持政策
        if False == State_support(i):
            continue
        res.append(i)

#1.信托计划（排序）
    res = arange_trusts(res)
    return res

if __name__ == '__main__':
    #GetData()

    #spider=Spider()
    #spider.run()
    #df = ts.get_industry_classified()
    #df = ts.get_hist_data(code="601006", start="2016-07-16")
    #print(df.ma5[0])
    #print(    df[['code', 'name', 'c_name']])
    #df.to_csv('J:\\code\\python\\1/1.csv')  # 选择保存

    #stock_info = ts.get_stock_basics()
    # 获取所有股票代码
    #for i in stock_info.index:
        #func1(i)

    #艇舫的策略
    #func1()

    #df = ts.get_index()
    #df = ts.get_hist_data(code='sh',start='2001-01-01')
    #df.to_csv('J:\\code\\python\\1/data_sh/hist_data.csv')
    #print(df)


    #df = ts.get_stock_basics()
    #df.to_csv('J:\\code\\python\\1/data_stock_basics/stock_basics.csv',encoding="utf-8")

    #df = ts.get_report_data(2017, 1)
    #df.to_csv('J:\\code\\python\\1/data_stock_basics/report_data.csv', encoding="utf-8")

    #res = get_shareholders('300675')
    #print(res)
    a= [9,8,7]
    b= [1,2,3]
    nvs = zip(a, b)
    nvDict = dict((a, b) for a, b in nvs)

    keys = nvDict.keys()
    keys.sort()

    print([nvDict[key] for key in keys])


