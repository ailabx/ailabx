import requests
class SolrMgr(object):
    def __init__(self):
        pass

    def test(self):
        data = {"add": {"doc": {"id": "100002", "title": "跟老同学聚会一样 喝嗨了一起搞笑",
                                'content':'号称“券商界奥斯卡”的新财富最佳分析师评选，今年如往年一样引得业内分析师纷纷参选。不过，今年评选刚刚开始却因“不雅分析师饭局”炸开了锅。'}}}
        params = {"boost": 1.0, "overwrite": "true", "commitWithin": 1000}
        url = 'http://127.0.0.1:8983/solr/nlpcore/update?wt=json'
        headers = {"Content-Type": "application/json"}
        r = requests.post(url, json=data, params=params, headers=headers)
        print(r.text)
if __name__ == '__main__':
    SolrMgr().test()