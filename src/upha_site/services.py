import os


async def upload_image(file, folder, generated_filename):
    allowed_image_types = ["image/png", "image/jpeg", "image/jpg", "image/svg"]
    if file.content_type in allowed_image_types:
        with open(str(f"static/{folder}/{generated_filename}"), "wb") as image:
            image.write(file.file.read())
            return {"message": "File uploaded successfully."}
    else:
        return {"error": "File must be an image instance."}


async def delete_image(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"The file {file_path} does not exist.")


async def is_empty(**kwargs):
    for value in kwargs.values():
        if str(value).strip() == "":
            return {"error": "Values can not be empty."}

    return {"message": "status 200"}

