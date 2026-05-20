import os

import cloudinary
import cloudinary.uploader


def configure_cloudinary():
    cloudinary_url = os.getenv("CLOUDINARY_URL")
    if cloudinary_url:
        cloudinary.config(cloudinary_url=cloudinary_url, secure=True)
        return

    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True,
    )


def upload_file_to_cloudinary(file_path, folder="drivemarket"):
    configure_cloudinary()

    try:
        response = cloudinary.uploader.upload(
            file_path,
            folder=folder,
            resource_type="image",
            overwrite=False,
        )
        return response.get("secure_url")
    except Exception as exc:
        print(f"[cloudinary] Error subiendo archivo: {exc}")
        return None
