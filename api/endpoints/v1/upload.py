from fastapi import APIRouter, File, UploadFile, HTTPException
import boto3
from botocore.exceptions import NoCredentialsError
import os


router = APIRouter(
    prefix = "/v1/upload",
    tags = ["upload"],
)


s3_client = boto3.client(
    's3',
    aws_access_key_id=f"{os.getenv('AWS_ACCESS_KEY')}",
    aws_secret_access_key=f"{os.getenv('AWS_SECRET_KEY')}",
    region_name=f"{os.getenv('AWS_REGION')}"
)


@router.post("")
async def upload_file(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    try:
        s3_client.upload_fileobj(file.file, f"{os.getenv('S3_BUCKET_NAME')}", file.filename)
        
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": os.getenv('S3_BUCKET_NAME'), "Key": file.filename},
            ExpiresIn=36000
        )
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="AWS credentials not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

    return {"url": response}
