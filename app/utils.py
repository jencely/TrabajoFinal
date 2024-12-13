import boto3
import requests
import uuid
import os
from config import Config

def upload_to_s3(file, filename):
    """
    Sube un archivo a S3 y retorna la URL
    """
    s3 = boto3.client(
        's3',
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        region_name=Config.AWS_REGION
    )
    
    try:
        s3.upload_fileobj(file, Config.S3_BUCKET, filename)
        return f"https://{Config.S3_BUCKET}.s3.amazonaws.com/{filename}"
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None

def get_imagga_tags(image_url):
    """
    Obtiene tags de una imagen usando la API de Imagga
    """
    response = requests.get(
        f'https://api.imagga.com/v2/tags?image_url={image_url}',
        auth=(Config.IMAGGA_API_KEY, Config.IMAGGA_API_SECRET)
    )
    
    if response.status_code == 200:
        tags = response.json()['result']['tags']
        return [(tag['tag']['en'], tag['confidence']) for tag in tags]
    return []

def generate_filename(original_filename):
    """
    Genera un nombre único para el archivo
    """
    ext = os.path.splitext(original_filename)[1]
    return f"{str(uuid.uuid4())}{ext}"