from os import getenv

from dotenv import load_dotenv
from fastapi import UploadFile
from supabase import Client, create_client

load_dotenv()

__SUPABASE_URL = getenv("SUPABASE_URL")
__SUPABASE_API_TOKEN = getenv("SUPABASE_API_TOKEN")
__storage_name: str = "file_storage"
supabase_client: Client = create_client(supabase_url=__SUPABASE_URL,
                                        supabase_key=__SUPABASE_API_TOKEN)

__DEFAULT_URL: str = "https://dzmpeskjgukecrebnptg.supabase.co/storage/v1/object/public/file_storage/default_images/new-product-presentation.png"


def get_all_buckets():
    res = supabase_client.storage.list_buckets()
    return res


def get_all_files(bucket: str):
    res = supabase_client.storage.from_(bucket).list()
    return res


async def upload_file(file: UploadFile) -> str:
    try:
        file_content = await file.read()
        bucket_in_path = f"products/resources/{file.filename}"
        # Open the file and upload it to supabase storage

        supabase_client.storage.from_(__storage_name).upload(file=file_content,
                                                             path=bucket_in_path,
                                                             file_options={"content-type": "image/*"})
        # Get the public URL after uploading
        public_url: str = supabase_client.storage.from_(__storage_name).get_public_url(bucket_in_path)
        return public_url.replace("?", "")
    except Exception:
        return __DEFAULT_URL


async def update_file(new_file: UploadFile, old_file_name: str) -> str:
    """
    :param new_file: The new file to upload
    :param old_file_name: The old file name inside the bucket
    :return:
    """

    try:
        file_content = await new_file.read()
        bucket_in_path = f"products/resources/{old_file_name}"
        supabase_client.storage.from_(__storage_name).update(file=file_content, path=bucket_in_path,
                                                             file_options={"content-type": "image/*"})
        public_url: str = supabase_client.storage.from_(__storage_name).get_public_url(bucket_in_path)
        return public_url.replace("?", "")
    except Exception:
        return __DEFAULT_URL


def delete_file(file_name: str):
    try:
        bucket_in_path = f"products/resources/{file_name}"
        supabase_client.storage.from_(__storage_name).remove(bucket_in_path)
    except Exception:
        print("Exception")
