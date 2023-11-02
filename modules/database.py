import modules.env as env
import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQLの設定
postgres = {
    'user': env.POSTGRES_USERNAME,
    'password': env.POSTGRES_PASSWORD,
    'host': env.POSTGRES_HOST,
    'port': env.POSTGRES_PORT,
    'database': env.POSTGRES_DATABASE
}

# データベースのテーブルを定義
engine = create_engine( f'postgresql://{postgres["user"]}:{postgres["password"]}@{postgres["host"]}:{postgres["port"]}/{postgres["database"]}')

Base = declarative_base()
class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    task_id = Column(String)
    data = Column(JSON)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# データベース操作のためのDBクラスを定義
class DB:
    @classmethod
    def add_task(cls, task_id):
        db = Session()
        try:
            task_data = {
                'task_id': task_id,
                'status': "preparing",
                'request_time': datetime.datetime.now(ZoneInfo("Asia/Tokyo")).isoformat()
            }
            Task = Tasks(task_id=task_id, data=task_data)
            db.add(Task)
            db.commit()
            return task_data
        except Exception as e:
            print(f"タスクの追加エラー: {str(e)}")
        finally:
            db.close()

    @classmethod
    def get_task(cls, task_id):
        db = Session()
        try:
            task_data = db.query(Tasks).filter(Tasks.task_id == task_id).first().data
            return task_data
        except Exception as e:
            print(f"タスクの取得エラー: {str(e)}")
            return False
        finally:
            db.close()

    @classmethod
    def update_task(cls, task_id, data):
        db = Session()
        try:
            db.query(Tasks).filter(Tasks.task_id == task_id).update({Tasks.data: data})
            db.commit()
            return True
        except Exception as e:
            print(f"タスクの更新エラー: {str(e)}")
            return False
        finally:
            db.close()

