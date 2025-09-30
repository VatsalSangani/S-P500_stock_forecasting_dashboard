import os
import boto3
from botocore.exceptions import ClientError

# ------------------------
# Config
# ------------------------
AWS_REGION = "eu-west-2"   # Change if bucket is in another region
BUCKET_NAME = "sp500-dashboard-data"  # 🔹 your bucket name

# Folders to upload
DATA_DIRS = {
    "processed": "data/processed",
    "forecasts": "data/forecasts",
    "fundamentals": "data/fundamentals"
}


# ------------------------
# S3 Helper Functions
# ------------------------
def clear_s3_prefix(s3_client, prefix):
    """Delete all objects in S3 under a given prefix (folder)."""
    try:
        print(f"🧹 Clearing old files from s3://{BUCKET_NAME}/{prefix}/ ...")
        paginator = s3_client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix):
            if "Contents" in page:
                for obj in page["Contents"]:
                    s3_client.delete_object(Bucket=BUCKET_NAME, Key=obj["Key"])
                    print(f"   ❌ Deleted {obj['Key']}")
    except ClientError as e:
        print(f"⚠️ Could not clear prefix {prefix}: {e}")


def upload_directory_to_s3(local_dir, s3_prefix, s3_client):
    """Upload all files from a local folder to an S3 prefix."""
    for root, _, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_dir)
            s3_path = f"{s3_prefix}/{relative_path}"

            try:
                print(f"⬆️ Uploading {local_path} → s3://{BUCKET_NAME}/{s3_path}")
                s3_client.upload_file(local_path, BUCKET_NAME, s3_path)
            except ClientError as e:
                print(f"❌ Upload failed for {local_path}: {e}")


# ------------------------
# Main
# ------------------------
if __name__ == "__main__":
    s3 = boto3.client("s3", region_name=AWS_REGION)

    for prefix, folder in DATA_DIRS.items():
        if os.path.exists(folder):
            clear_s3_prefix(s3, prefix)  # Clean old files
            upload_directory_to_s3(folder, prefix, s3)  # Upload new
        else:
            print(f"⚠️ Skipping {folder} (not found)")

    print("✅ Upload complete!")
