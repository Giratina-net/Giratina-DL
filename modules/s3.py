import boto3
import modules.env as env

s3 = boto3.client(
    service_name ="s3",
    endpoint_url=env.S3_ENDPOINT_URL,
    aws_access_key_id=env.S3_ACCESS_KEY_ID,
    aws_secret_access_key=env.S3_SECRET_ACCESS_KEY,
    region_name=env.S3_REGION
)

# S3にアップロード
def upload_file(filename):
    try:
        s3.upload_file(filename, env.S3_BUDGET_NAME, filename)
    except Exception as e:
        print("S3へのアップロードに失敗しました。")
        return False
    return True
# S3からURLを取得

def get_presigned_url(filename, expiration=86400):
    try:
        r = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": env.S3_BUDGET_NAME,
                "Key": filename
            },
            ExpiresIn=expiration
        )
        r = r.replace(env.S3_ENDPOINT_URL, env.S3_DOMAIN)
    except Exception as e:
        print("S3からのURL取得に失敗しました。")
        return False
    return r


