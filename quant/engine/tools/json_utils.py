import json
import yaml

params = [
    {'job_id':'AAAAA-ZZZZZ',
     'name':'策略1',
     'rules':['rule1','rule2']
     },
    {'job_id':'AAAAA-CCCCC',
     'name':'策略2',
     'rules':['rule1','rule2']
     }
]

with open('strategies.json', 'w') as f:
    '''写入json文件'''
    json.dump(params, f)

    print("写入json文件：", params)

with open('yaml.config','w') as f:
    yaml.dump(params,f)

with open('strategies.json') as f:
    '''读取json文件'''
    numbers = json.load(f)  # 返回列表数据，也支持字典
    print("读取json文件：", numbers)

with open('yaml.config') as f:
    params = yaml.load(f)
    print(params)