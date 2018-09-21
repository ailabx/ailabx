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



json_str = json.dumps(params[0], sort_keys=True,ensure_ascii=False, indent=4, separators=(',', ':'))
print('json_str:=========',json_str)


str2 = '''
{
    "job_id":"AAAAA-ZZZZZ",
    "name":"人生何其短",
    "rules":[
        "rule1",
        "rule2"
    ]
}
'''
ret = json.loads(str2)
print(type(ret),ret)

with open('strategies.json', 'w') as f:
    '''写入json文件'''
    json.dump(params, f)


with open('strategies.json') as f:
    '''读取json文件'''
    datas = json.load(f)  # 返回列表数据，也支持字典
    print("读取json文件：", type(datas),datas)

