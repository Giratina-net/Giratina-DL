import os
import time
import modules.env as env
from sqlalchemy import create_engine


postgres = {
    'user': env.POSTGRES_USERNAME,
    'password': env.POSTGRES_PASSWORD,
    'host': env.POSTGRES_HOST,
    'port': env.POSTGRES_PORT,
    'database': env.POSTGRES_DATABASE
}

engine = create_engine( f'postgresql://{postgres["user"]}:{postgres["password"]}@{postgres["host"]}:{postgres["port"]}/{postgres["database"]}')
cnt = 0

def check_database():
    # 接続を試行
    try:
        session = engine.connect()
        print("PostgreSQLデータベースに接続できました。")
        session.close()
        return True
    except Exception as e:
        print(f"\n\nPostgreSQLデータベースへの接続に失敗しました: {e}")
        return False

while not check_database():
    cnt += 1
    time.sleep(10)
    if cnt == 10:
        raise Exception("データベースに接続できませんでした。")


os.makedirs("download", exist_ok=True)
