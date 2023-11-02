from PIL import Image
from io import BytesIO
from pathlib import Path
from mutagen.id3 import ID3, APIC, TPE2, TRCK

#正方形にクロップ
def crop_center_square(data):
    try:
        img = Image.open(BytesIO(data))
        size = img.height
        center_x = int(img.width / 2)
        center_y = int(img.height / 2)
        img_crop = img.crop((center_x - size // 2, center_y - size // 2, center_x + size // 2, center_y + size // 2))
        img_bytes = BytesIO()
        img_crop.save(img_bytes, format='PNG')
        return img_bytes.getvalue()
    except Exception as e:
        print(f"画像のクロップエラー: {str(e)}")
        return False

#メタデータの編集
def edit_song_metadata(filepath):
    try:
        music = ID3(filepath)
        music["TRCK"] = TRCK(text="")
        apic = music.getall("APIC")[0]
        if apic:
            music.add(APIC(mime="image/png", type=3, data=crop_center_square(apic.data), quality=100, optimize=True))
        music.save()
    except Exception as e:
        print(f"メタデータの編集エラー: {str(e)}")
        return False

#メタデータの編集(アルバム)
def edit_album_metadata(filepath):
    try:
        audio_files = list(Path(filepath).glob('*.mp3'))
        audio_files.sort(key=lambda x: x.stat().st_ctime)
        
        for i, file in enumerate(audio_files, start=1):
            music = ID3(file)
            apic = music.getall("APIC")[0]
            artist = str(music.get("TPE1")).split(',')[0]
            music["TRCK"] = TRCK(text=str(i))
            music["TPE2"] = TPE2(text=artist) 
            if apic:
                music.add(APIC(mime="image/png", type=3, data=crop_center_square(apic.data), quality=100, optimize=True))
            music.save()
    except Exception as e:
        print(f"メタデータの編集エラー: {str(e)}")
        return False
