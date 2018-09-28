from flask import Flask
from flask import jsonify
#解决cors
from flask_cors import *
import xmlrpc
#tornado
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask import render_template

app = Flask(__name__)
#这一句是为了jsonify显示中文
app.config['JSON_AS_ASCII'] = False
#app.config['static_url_path']=''

#解决cors问题一行代码
CORS(app, supports_credentials=True)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/echo/<message>')
def echo(message):
    proxy = xmlrpc.client.ServerProxy('http://localhost:9000')
    message = proxy.echo(message)
    data = {
        'message':message,
        'list':['你好','这是来自server的问候']
    }
    return jsonify(data)

@app.route('/start/<ids>')
def start(ids):
    proxy = xmlrpc.client.ServerProxy('http://localhost:9000')
    proxy.start_stras(ids)
    return jsonify({'msg':'done!'})


def run_flask():

    app.run()
def run_webui():
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)  # 对应flask的端口

    from tornado import autoreload
    autoreload.start()
    IOLoop.instance().current().start()

if __name__ == '__main__':

    # tornado
    run_webui()

