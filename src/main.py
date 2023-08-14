from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
import pandas as pd 
import boto3 
from typing import List 
import requests 
from get_image import create_presigned_url
import os

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION")
S3_Bucket = os.environ.get("S3_Bucket")
S3_Key = os.environ.get("S3_Key")

origins = [
    "http://localhost",
    "http://localhost:3001",  # Ajoutez les origines autorisées ici
    "https://example.com"
]


app = FastAPI() 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3_client = boto3.client(service_name='s3',
                            region_name=AWS_REGION, 
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                            )


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/images/{image_id}")
def renvoie_image(image_id: str):
    
    url_signed = create_presigned_url(s3_client=s3_client,
                                      object_name=image_id)

    return {"url_signed" : url_signed}

@app.get('/images')
def renvoie_toutes_images():
    files_of_bucket = s3_client.list_objects(Bucket="projecttolondon")
    files_of_bucket = files_of_bucket["Contents"] 
    print(files_of_bucket)
    all_imgs = {}

    for i in range(len(files_of_bucket)):
        url_signed = create_presigned_url(s3_client=s3_client,
                                        object_name=files_of_bucket[i]["Key"])
        
        all_imgs[files_of_bucket[i]["Key"]] = url_signed
    

    return all_imgs

@app.delete('/images/{image_id}') 
def delete_image(image_id: str):
    s3_client.delete_object(Bucket='projecttolondon', Key=image_id)
    return {"Image":" deleted"}

@app.post('/images/')
async def upload_image(file: UploadFile=File(...)):
    file_name = file.filename
    content_file = await file.read() 
   
    with open(file_name, "wb") as image_id:
        image_id.write(content_file) 
    
    s3_client.upload_file(image_id.name, "projecttolondon", image_id.name)



    return {f"Le ficher {image_id.name} ": " a été ajouté avec succès"}
    

    
    



