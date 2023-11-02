#データベースの確認
import time
import modules.startup
import os
import json
import secrets
from collections import OrderedDict
from flask_cors import CORS
from flask import Flask, Response, request
import modules.env as env
from multiprocessing import Process
from modules.chkurl import chkurl
from modules.download import get_metadata, download_task
from modules.database import DB

# GDL_API_KEYの生成
if env.GDL_API_KEY == None:
    GDL_API_KEY = os.environ["GDL_API_KEY"] = secrets.token_hex(16)
    print("GDL_API_KEY is not set. Please set the following environment variable.\nGDL_API_KEY = "+GDL_API_KEY)

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/')
def index():
    return Response(json.dumps({}), status=200, mimetype='application/json')

@app.route('/v1/ydl/create', methods=['GET'])
def create():
    url,request_type,metadata_only,x_api_key = request.args.get("url"),request.args.get("type"),request.args.get("metadata_only"),request.headers.get("X-API-KEY")
    # X-API-KEYが指定されていない場合
    if x_api_key != env.GDL_API_KEY:
        return Response(json.dumps({"message": "X-API-KEY is invalid"}), status=401, mimetype='application/json')
    # urlが指定されていない場合
    if not url:
        return Response(json.dumps({"message": "url is not specified"}), status=400, mimetype='application/json')
    # typeが指定されていない場合
    if not request_type:
        request_type = "mp4"
    # typeが指定されているが、mp4, mp3, mp3_album以外の場合
    if request_type not in ["mp4", "mp3", "mp3_album"]:
        return Response(json.dumps({"message": "Unsupported type"}), status=400, mimetype='application/json')
    # urlがサポートされていない場合
    if not chkurl(url):
        return Response(json.dumps({"message": "Unsupported url"}), status=400, mimetype='application/json')
    # task_idの生成
    task_id = secrets.token_hex(8)
    # taskの追加
    r = DB.add_task(task_id=task_id)
    # ダウンロード処理の開始
    if not metadata_only  in  ["true", "True", "TRUE", "1", "t", "T", "y", "Y", "yes", "Yes", "YES"]:  
        Process(target=download_task, args=(task_id, url, request_type)).start()
        metadata_only = False
    else:
        metadata_only = True
    Process(target=get_metadata, args=(task_id, url, request_type, metadata_only)).start()
    return Response(json.dumps(r), status=200, mimetype='application/json')

@app.route('/v1/ydl/status', methods=['GET'])
def status():
    task_id,x_api_key = request.args.get("task_id"),request.headers.get("X-API-KEY")
    # X-API-KEYが指定されていない場合
    if x_api_key != env.GDL_API_KEY:
        return Response(json.dumps({"message": "X-API-KEY is invalid"}), status=401, mimetype='application/json')
    # task_idが指定されていない場合
    if not task_id:
        return Response(json.dumps({"message": "task_id is not specified"}), status=400, mimetype='application/json')
    # task_idが存在しない場合
    try:
        r=DB.get_task(task_id=task_id)
    except:
        return Response(json.dumps({"message": "task_id is not found"}), status=400, mimetype='application/json')
    # mediaを後方に移動 
    if "media" in r:
        r=OrderedDict(r)
        r.move_to_end("media")
    # # statusがエラーの場合    
    if r["status"] == "error":
        return Response(json.dumps(r), status=400, mimetype='application/json')
    return Response(json.dumps(r), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
