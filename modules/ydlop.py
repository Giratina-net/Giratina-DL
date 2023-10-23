def get_ydlop(request_type, working_directory):
    ydlop = dict()
    if request_type == "mp4":
        ydlop["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    elif request_type in ["mp3", "mp3_album"]:
        ydlop["format"] = "bestaudio/best"
        ydlop["postprocessors"] = [
            {'key': 'FFmpegExtractAudio', 'preferredquality': '192', 'preferredcodec': 'mp3'},
            {'key': 'FFmpegMetadata', 'add_metadata': True},
            {'key': 'EmbedThumbnail', 'already_have_thumbnail': False},
        ]
        ydlop["prefer_ffmpeg"] = True
        ydlop["writethumbnail"] = True
        ydlop["merge_output_format"] = "mp3"
    if request_type in ["mp4", "mp3"]:
        ydlop["outtmpl"] = working_directory + "/%(title)s.%(ext)s"
    elif request_type == "mp3_album":
        ydlop["outtmpl"] = working_directory + "/%(album)s/%(title)s.%(ext)s"
    ydlop["external_downloader"] = "aria2c"
    ydlop["external_downloader_args"] = ["-x 16", "-k 1M", "-c", "-n"]
    return ydlop