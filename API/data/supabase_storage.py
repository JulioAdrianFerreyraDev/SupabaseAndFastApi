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


async def upload_file(file: UploadFile, username: str) -> str:
    try:
        file_content = await file.read()
        bucket_in_path = f"{username}/products/resources/{file.filename}"
        # Open the file and upload it to supabase storage

        supabase_client.storage.from_(__storage_name).upload(file=file_content,
                                                             path=bucket_in_path,
                                                             file_options={"content-type": "image/*"})
        # Get the public URL after uploading
        public_url: str = supabase_client.storage.from_(__storage_name).get_public_url(bucket_in_path)
        return public_url.replace("?", "")
    except Exception:
        return __DEFAULT_URL


async def update_file(new_file: UploadFile, old_file_name: str, username: str) -> str:
    """
    :param new_file: The new file to upload
    :param old_file_name: The old file name inside the bucket
    :param username: Will be used to indicate the root directory inside the bucket
    :return:
    """

    try:
        file_content = await new_file.read()
        bucket_in_path = f"{username}/products/resources/{old_file_name}"
        supabase_client.storage.from_(__storage_name).update(file=file_content, path=bucket_in_path,
                                                             file_options={"content-type": "image/*"})
        public_url: str = supabase_client.storage.from_(__storage_name).get_public_url(bucket_in_path)
        return public_url.replace("?", "")
    except Exception:
        return __DEFAULT_URL


def delete_file(file_name: str, username: str):
    try:
        bucket_in_path = f"{username}/products/resources/{file_name}"
        supabase_client.storage.from_(__storage_name).remove(bucket_in_path)
    except Exception:
        print("Exception")


def __delete_old_directory(old_username: str):
    try:
        supabase_client.storage.from_(__storage_name).remove(f"{old_username}/")
    except Exception as e:
        print(e)


def move_files(old_username: str, new_username: str):
    try:
        old_path: str = f"{old_username}/products/resources"
        new_path: str = f"{new_username}/products/resources"
        res: list[dict] = supabase_client.storage.from_(__storage_name).list(old_path)
        for file_dict in res:
            file = file_dict.get("name")
            supabase_client.storage.from_(__storage_name).move(from_path=f"{old_path}/{file}",
                                                               to_path=f"{new_path}/{file}")
        __delete_old_directory(old_username)
    except Exception as e:
        print(e)
