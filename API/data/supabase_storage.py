from os import getenv

from dotenv import load_dotenv
from fastapi import UploadFile
from supabase import Client, create_client

load_dotenv()

__SUPABASE_URL = getenv("SUPABASE_URL")
__SUPABASE_API_TOKEN = getenv("SUPABASE_API_TOKEN")

supabase_client: Client = create_client(supabase_url=__SUPABASE_URL,
                                        supabase_key=__SUPABASE_API_TOKEN)


def get_all_buckets():
    res = supabase_client.storage.list_buckets()
    return res


def get_all_files(bucket: str):
    res = supabase_client.storage.from_(bucket).list()
    return res


async def upload_file(file: UploadFile, username: str) -> str:
    try:
        file_content = await file.read()
        bucket_in_path = f"{username}/products/resources/{file.filename}"
        # Open the file and upload it to supabase storage

        supabase_client.storage.from_("file_storage").upload(file=file_content,
                                                             path=bucket_in_path,
                                                             file_options={"content-type": "image/*"})
        # Get the public URL after uploading
        public_url: str = supabase_client.storage.from_("file_storage").get_public_url(bucket_in_path)
        return public_url.replace("?", "")
    except Exception:
        return "https://uppkqkteqxmhxkbuvani.supabase.co/storage/v1/object/sign/file_storage/new-product-presentation.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJmaWxlX3N0b3JhZ2UvbmV3LXByb2R1Y3QtcHJlc2VudGF0aW9uLnBuZyIsImlhdCI6MTcyOTAxMzQ4OSwiZXhwIjoxNzYwNTQ5NDg5fQ.vu1TuZUWJgUg2MzGBwiM3bc2y2-aBmeS9y5ZkUjPH_4&t=2024-10-15T17%3A31%3A31.463Z"
