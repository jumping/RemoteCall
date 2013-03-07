#!/bin/env python26
import os
from flask import Flask
from flask import send_from_directory
from simpleapi import Namespace, Route

app = Flask(__name__)

class RemoteAPI(Namespace):
  #as_name = "xmlapi-as"
  def execute(self, string):
    #self.cmdline = "w"
    self.cmdline = "cd /mnt/webapps/xmlapi && /usr/local/php/bin/php script/createTokenDataFile.php && /usr/local/php/bin/php script/createTrafficsourceConfFile.php"
    import remote_execute
    output = remote_execute.execute(string, self.cmdline, app)
    if output['stderr']:
      return "failed %s" % str(output)
    return "succeeded %s" % output['stdout'][0]
  
  execute.published = True

app.route('/api/', methods=['GET'])(Route(RemoteAPI, framework='flask', debug=True))

@app.route('/')
def index():
  return 'Index Page'

@app.route('/hello')
def hello():
  return 'Hello World'

@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static'),
         'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/user/<username>')
def show_user_profile(username):
  # show the user profile for that user
  return 'User %s' % username

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=80,debug=False)
