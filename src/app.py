from fastapi import FastAPI 
from pydantic import BaseModel 
import pandas as pd 
import boto3 
from typing import List 

app = FastAPI() 

@app.post('./{account}')
def get_aws_account():
    pass 

@app.post('./connect')
def connect_to_aws():
    pass 

@app.get('./images/{bucket}') 
def renvoie_list_images(s3: boto3.resource, bucket: str) -> List[str]:
    my_bucket = s3.Bucket(bucket)
    ids = []
    for my_bucket_object in my_bucket.objects.all():
        ids.append(my_bucket_object.key)
    
    return ids


@app.get('./images/{id}')
def renvoie_image_from_id(id: str, s3: boto3.resource, bucket: str) -> pd.DataFrame:
    obj = s3.Bucket(bucket).Object(f'{id}').get()
    img = pd.read_csv(obj['Body'], index_col=0) 
    return img


@app.delete('./images/{id}')
def delete_image_from_id(id: str, s3: boto3.resource, bucket: str) -> bool:
    s3.Object(bucket, id).delete()
    return True

@app.post('./images/{id}') 
def upload_image(id: str, s3: boto3.resource, bucket: str) -> bool:
    s3.Bucket(bucket).upload_file(Filename=id, Key=id) 
    return True 

