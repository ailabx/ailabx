import re
import pandas as pd

#基础的特征支持，比如ohlc,return,volume,amount,还有各种指标
def parse_feature(feature):
    items = feature.split('_')
    if items and len(items) > 1 and re.match('[a-z]+',items[0]):
        return items[0],items[1:len(items)]
    return None,None

def parse_operator(item):
    operators = ['+', '-', '*', '/']
    # 包含+,-,*,/
    splited = None
    for ope in operators:
        if ope in item:
            splited = item.split(ope)
    return splited

 #把features集合里，所有需要提取的因子都列出来
def extra_features(items):
        features = []

        new_items = []
        for item in items:
            splited = parse_operator(item)
            if splited is None:
                new_items.append(item.strip())
            else:
                new_items.extend(splited)

        for item in new_items:
            ret =  re.search('([a-z]+_[\d+].*?$)',item)
            if ret:
               features.append(ret.group().strip())
        return list(set(features))

class FeatureCalc(object):
    def calc_feature(self,df,name,args):
        if name == 'return':
            close = df['close']
            return close / close.shift(int(args[0]) + 1) - 1
        else:
            return df[name].shift(int(args[0]))

    #features['close_5','macd_12_9_6','return_5']等基本变量
    def calc_basic_features(self,df,features):
        for feature in features:
            name,args = parse_feature(feature)
            df[feature] = self.calc_feature(df,name,args)
        return df

    def extra_basic_features(self,items):
        return extra_features(items)

    #计算加减乘除的运算
    def calc_operators(self,df,items):
        # 计算+-*/
        for feature in items:
            splited = parse_operator(feature)
            if splited:
                new_name = ''
                for item in splited:
                    new_name += item
                    new_name += '_'
                df = df.eval(new_name[:len(new_name)-1] + '=' + feature)
        return df

    def calc_func(self,df,items):

        for item in items:
            #加减乘除的不在这里算
            if parse_operator(item):
                continue
            if re.search('[a-z]+_[a-z]+_[\d+].*?$',item):
                feature_name = re.findall('[a-z]+_[\d+].*?$', item)[0]
                #print('feature：',feature_name)
                funcs = re.findall('[a-z]+',item)
                if len(funcs) > 1:
                    funcs = funcs[:len(funcs) - 1]
                    funcs.reverse()
                    df = self.do_funcs(df,funcs,item,feature_name)
        return df

    def do_funcs(self,df,funcs,item,feature):
        if type(df) is str:
            print(funcs,feature,df)
        se = df[feature]
        for func in funcs:
            if func == 'avg':
                pass
            elif func == 'rank':
                se = se.rank()

        df[item] = se
        return df

    def calc(self,df,items):
        basic_features = self.extra_basic_features(items)
        df = self.calc_basic_features(df, basic_features)
        df = self.calc_operators(df, items)
        return df


