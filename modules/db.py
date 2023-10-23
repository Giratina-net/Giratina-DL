import datetime
from zoneinfo import ZoneInfo
from tinydb import TinyDB, Query

class DB:
    def __init__(self):
        self.db = TinyDB("tinydb/tasks.json")
    # DBのデータを追加
    def add_task(self, task_id):
        d = dict()
        d["task_id"] = task_id
        d["status"] = "preparing"
        #d["requested_user"] = ""
        d["request_time"] = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).isoformat()
        self.db.insert(d)
        return d
    #DBのデータを取得
    def get_task(self, task_id):
        return self.db.search(Query().task_id == task_id)

    #DBのデータを更新
    def update_task(self, task_id, data):
        self.db.update(data, Query().task_id == task_id)

