from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ConnectionError
from fastapi import Depends, HTTPException
from fastapi import File, UploadFile
from fastapi import Request
from sqlalchemy.orm import Session
from db.core import Files

from config.db import get_db
from config.fastapi import app_settings
from utils.s3 import get_s3_client


async def upload_file(request: Request, file: UploadFile = File(...)):
    # TODO: Add files mapping to files table
    # TODO: Add API to bulk upload files
    # TODO: Check: File size / type etc
    username = request.state.username
    try:
        s3_client = get_s3_client()
        s3_client.upload_fileobj(file.file, app_settings.S3_BUCKET_NAME, file.filename)
        file_url = f"https://{app_settings.S3_BUCKET_NAME}.s3.{app_settings.S3_AWS_REGION}.amazonaws.com/{file.filename}"
        return {"message": "File uploaded successfully", "url": file_url}
    except ConnectionError:
        raise HTTPException(status_code=500, detail="Unable to connect to AWS S3")
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not found")
    except PartialCredentialsError:
        raise HTTPException(status_code=500, detail="Incomplete AWS credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_files_list(db: Session = Depends(get_db)):
    # Returns list of all files associated with user
    payload = [{"id": 1, "name": "sample.pdf", "type": "pdf", "status": "processing"}]
    # db.query(Files).all()
    return payload

# def download_file(filename: str):
#     # try:
#     #     file_url = f"https://{app_settings.S3_BUCKET_NAME}.s3.{app_settings.S3_AWS_REGION}.amazonaws.com/{filename}"
#     #     return {"message": "File retrieved successfully", "url": file_url}
#     # except Exception as e:
#     #     raise HTTPException(status_code=500, detail=str(e))
#     try:
#         s3_client = get_s3_client()
#         pre_signed_url = s3_client.generate_presigned_url(
#             "get_object",
#             Params={"Bucket": app_settings.S3_BUCKET_NAME, "Key": filename},
#             ExpiresIn=3600,  # URL expires in 1 hour
#         )
#         return {"message": "File retrieved successfully", "url": pre_signed_url}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
