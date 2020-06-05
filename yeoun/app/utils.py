from .models import Todo, Comments
from crud.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME
import boto3
from boto3.session import Session
from datetime import datetime
from django.contrib.auth.models import User

def upload_and_save(request, file_to_upload):
    # user = Todo.objects.get(author=request.user)
    session = Session(
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
            region_name = AWS_S3_REGION_NAME
    )
    s3 = session.resource('s3')
    now = datetime.now().strftime("%Y%H%M%S")
    key = str(request.user)

    img_object = s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(
        Key =  key + '/' + now + file_to_upload.name,
        Body = file_to_upload
    )

    
    s3_url = 'https://seoyoung-django.s3.ap-northeast-2.amazonaws.com/'
    img_url = s3_url+ key + '/' + now +file_to_upload.name

    return img_url

