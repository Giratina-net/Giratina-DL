#!/usr/bin/env python3
import os
import json
import random, string
import boto3
import discord
from os import getenv
from yt_dlp import YoutubeDL
from discord.ext import commands
from boto3.session import Session
from botocore.config import Config

AWS_SECRET_ACCESS=getenv("AWS_SECRET_ACCESS")
AWS_ACCESS_KEY_ID=getenv("AWS_ACCESS_KEY_ID")
DISCORD_BOT_TOKEN = getenv("DISCORD_BOT_TOKEN")
AWS_DEFAULT_REGION="us-east-1"
AWS_S3_ENDPOINT_URL="https://s3.giratina.net"
bucketname="download"

def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def ydl(ctx, *arg):
    if arg:
        ytlink = arg[0]

        with YoutubeDL() as ydl: 
            info_dict = ydl.extract_info(ytlink, download=False)
            title = info_dict.get('title', None)
            name=randomname(10)
            filename=name+"."+"mp4"

        ydlop = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl':f"{name}.%(ext)s"}

        await ctx.channel.send(title+"をダウンロードしています")

        with YoutubeDL(ydlop) as ydl:
            ydl.download(ytlink)

        await ctx.channel.send(title+"をアップロードしています")

        s3 = boto3.client("sts", 
                        region_name=AWS_DEFAULT_REGION,
                        endpoint_url=AWS_S3_ENDPOINT_URL,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS)

        s3up = boto3.client("s3", 
                        region_name=AWS_DEFAULT_REGION,
                        endpoint_url=AWS_S3_ENDPOINT_URL,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS)
        
        s3up.upload_file("./"+filename, bucketname,filename)

        policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Effect": "Allow",
            "Resource": [
                f"arn:aws:s3:::{bucketname}/*"
            ],
            "Sid": "Stmt1"
            }
        ]
        }

        response = s3.assume_role(
            RoleArn='arn:xxx:xxx:xxx:xxxx',
            RoleSessionName='anything',
            Policy=json.dumps(policy, separators=(',',':')),
            DurationSeconds=1800
        )

        sts = {
            'aws_access_key_id': response['Credentials']['AccessKeyId'],
            'aws_secret_access_key': response['Credentials']['SecretAccessKey'],
            'aws_session_token': response['Credentials']['SessionToken']   
        }

        session = Session(**sts)

        s3 = session.client('s3', config=Config(signature_version='s3v4'), endpoint_url=AWS_S3_ENDPOINT_URL)

        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucketname, 'Key': filename},
            ExpiresIn=1800,
            HttpMethod='GET')

        await ctx.channel.send(url)
        os.remove(filename)
 
    if not arg:
        await ctx.channel.send("urlを入力してください")

@bot.command()
async def ydl3(ctx, *arg):
    if arg:
        ytlink = arg[0]

        with YoutubeDL() as ydl: 
            info_dict = ydl.extract_info(ytlink, download=False)
            title = info_dict.get('title', None)
            name=randomname(10)
            filename=name+"."+"mp3"

        ydlop = {'format': 'bestaudio/best',
                'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredquality': '192',
                'preferredcodec': 'mp3'}],
                'prefer_ffmpeg': True,
                'outtmpl':f"{name}.%(ext)s"
        }

        await ctx.channel.send(title+"をダウンロードしています")

        with YoutubeDL(ydlop) as ydl:
            ydl.download(ytlink)

        await ctx.channel.send(title+"をアップロードしています")

        s3 = boto3.client("sts", 
                        region_name=AWS_DEFAULT_REGION,
                        endpoint_url=AWS_S3_ENDPOINT_URL,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS)

        s3up = boto3.client("s3", 
                        region_name=AWS_DEFAULT_REGION,
                        endpoint_url=AWS_S3_ENDPOINT_URL,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS)
        
        s3up.upload_file("./"+filename, bucketname,filename)

        policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Effect": "Allow",
            "Resource": [
                f"arn:aws:s3:::{bucketname}/*"
            ],
            "Sid": "Stmt1"
            }
        ]
        }

        response = s3.assume_role(
            RoleArn='arn:xxx:xxx:xxx:xxxx',
            RoleSessionName='anything',
            Policy=json.dumps(policy, separators=(',',':')),
            DurationSeconds=1800
        )

        sts = {
            'aws_access_key_id': response['Credentials']['AccessKeyId'],
            'aws_secret_access_key': response['Credentials']['SecretAccessKey'],
            'aws_session_token': response['Credentials']['SessionToken']   
        }

        session = Session(**sts)

        s3 = session.client('s3', config=Config(signature_version='s3v4'), endpoint_url=AWS_S3_ENDPOINT_URL)

        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucketname, 'Key': filename},
            ExpiresIn=1800,
            HttpMethod='GET')

        await ctx.channel.send(url)
        os.remove(filename)
 
    if not arg:
        await ctx.channel.send("urlを入力してください")

@bot.command()
async def ydlw(ctx, *arg):
    if arg:
        ytlink = arg[0]

        with YoutubeDL() as ydl: 
            info_dict = ydl.extract_info(ytlink, download=False)
            title = info_dict.get('title', None)
            name=randomname(10)
            filename=name+"."+"wav"
        ydlop = {'format': 'bestaudio/best',
                'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav'}],
                'prefer_ffmpeg': True,
                'outtmpl':f"{name}.%(ext)s"
        }

        await ctx.channel.send(title+"をダウンロードしています")

        with YoutubeDL(ydlop) as ydl:
            ydl.download(ytlink)

        await ctx.channel.send(title+"をアップロードしています")

        s3 = boto3.client("sts", 
                        region_name=AWS_DEFAULT_REGION,
                        endpoint_url=AWS_S3_ENDPOINT_URL,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS)

        s3up = boto3.client("s3", 
                        region_name=AWS_DEFAULT_REGION,
                        endpoint_url=AWS_S3_ENDPOINT_URL,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS)
        
        s3up.upload_file("./"+filename, bucketname,filename)

        policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Effect": "Allow",
            "Resource": [
                f"arn:aws:s3:::{bucketname}/*"
            ],
            "Sid": "Stmt1"
            }
        ]
        }

        response = s3.assume_role(
            RoleArn='arn:xxx:xxx:xxx:xxxx',
            RoleSessionName='anything',
            Policy=json.dumps(policy, separators=(',',':')),
            DurationSeconds=1800
        )

        sts = {
            'aws_access_key_id': response['Credentials']['AccessKeyId'],
            'aws_secret_access_key': response['Credentials']['SecretAccessKey'],
            'aws_session_token': response['Credentials']['SessionToken']   
        }

        session = Session(**sts)

        s3 = session.client('s3', config=Config(signature_version='s3v4'), endpoint_url=AWS_S3_ENDPOINT_URL)

        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucketname, 'Key': filename},
            ExpiresIn=1800,
            HttpMethod='GET')

        await ctx.channel.send(url)
        os.remove(filename)
 
    if not arg:
        await ctx.channel.send("urlを入力してください")
        
bot.run(DISCORD_BOT_TOKEN)