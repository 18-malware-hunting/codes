from flask import Flask, render_template, request

import json
import os
with open(os.path.join(os.path.join(os.path.expanduser("~"), "%s" % "anadata".lower()),"data.json"),'r') as load_f:
    data_dict = json.load(load_f)
app = Flask(__name__)

@app.route('/')
def index():
    my_dict = data_dict

    # render_template方法:渲染模板
    # 参数1: 模板名称  参数n: 传到模板里的数据
    return render_template('hello.html',
                           my_dict=my_dict)

@app.route('/result',methods = ['POST', 'GET'])
def result():

   if request.method == 'POST':
      result = request.form
      r="ok"
      return render_template("result.html",result = result,r=r)



if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=False)
