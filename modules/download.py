import os
import shutil
import datetime
from zoneinfo import ZoneInfo
from yt_dlp import YoutubeDL
from modules.database import DB
from modules.kutt import kutt
from modules.ydlop import get_ydlop
from modules.s3 import upload_file, get_presigned_url
from modules.edit_mp3 import edit_song_metadata, edit_album_metadata

def get_metadata(task_id, url, request_type, metadata_only=False):
    # メタデータ取得
    try:
        metadata = YoutubeDL({"playlistend": 1}).extract_info(url, download=False)
        sanitized_title = metadata["title"].replace('Album - ', '').replace('/', '／')
        #taskの更新
        task_data = DB.get_task(task_id=task_id)
        task_data["media"] = {
            "title": sanitized_title,
            "request_type": request_type,
            "url": url,
            "metadata": metadata
        }
        if metadata_only  == True:
            task_data["status"] = "success"
            task_data["complated_time"] = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).isoformat()
        DB.update_task(task_id=task_id, data=task_data)
    except Exception as e:
        print("メタデータの取得に失敗しました。")
        return {"status": "error", "message": "Metadata cannot be obtained"}

def download_media(task_id, url, request_type):
    
    # 作業ディレクトリの作成
    working_directory = "download/" + task_id
    os.makedirs(working_directory)
    
    try:
        # ダウンロード
        YoutubeDL( get_ydlop(request_type=request_type, working_directory=working_directory) ).download([url])
        
        # メディアファイルの取得
        task_data = DB.get_task(task_id=task_id)
        media_title = task_data["media"]["title"]
        global filename
        filename = working_directory + "/" + media_title + "." + request_type
        if request_type == "mp3":
            edit_song_metadata(filename)
        elif request_type == "mp3_album":
            filename = working_directory + "/" + media_title + ".zip"
            media_dir = os.path.join(working_directory, media_title)
            edit_album_metadata(media_dir)
            shutil.make_archive(os.path.join(working_directory, media_title), 'zip', media_dir)
            shutil.rmtree(media_dir)
        
        # S3にアップロード
        is_uploaded = upload_file(filename)
        download_url_raw = get_presigned_url(filename)
        
        if not is_uploaded or not download_url_raw:
            return {"status": "error", "message": "S3 upload error"}
        
        # Kuttで短縮URLを取得
        download_url_short = kutt(download_url_raw)
        
        if not download_url_short:
            return {"status": "error", "message": "Kutt error"}
        
        complated_time = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).isoformat()
        # レスポンスの作成
        return {"status": "success", "complated_time": complated_time, "download_url": {"short": download_url_short, "raw": download_url_raw}}
    except Exception as e:
        print(f"不明なエラー: {str(e)}")
        return {"status": "error", "message": "Unknown error"}
    finally:
        shutil.rmtree(working_directory)

def download_task(task_id, url, request_type):
    # ダウンロード
    download_result = download_media(task_id=task_id, url=url, request_type=request_type)
    # taskの更新
    task_data = DB.get_task(task_id=task_id)
    task_data.update(download_result)
    DB.update_task(task_id=task_id, data=task_data)
