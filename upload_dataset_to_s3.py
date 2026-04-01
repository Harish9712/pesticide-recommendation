"""
Upload the dataset folder to AWS S3.
Requires: pip install boto3
Uses AWS credentials from environment (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
or from ~/.aws/credentials
"""

import os
import sys
from pathlib import Path

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    print("boto3 is required. Install with: pip install boto3")
    sys.exit(1)

# Configuration
DATASET_DIR = Path(__file__).parent / "dataset"
BUCKET_ENV = "S3_BUCKET"
PREFIX_ENV = "S3_DATASET_PREFIX"


def upload_dataset_to_s3(bucket: str, prefix: str = "dataset", dataset_path: Path = None):
    """
    Upload the dataset directory to S3, preserving structure.

    Args:
        bucket: S3 bucket name
        prefix: S3 key prefix (folder path in bucket), e.g. "dataset" or "ml/datasets/crop-pest"
        dataset_path: Local path to dataset (default: project/dataset)
    """
    dataset_path = dataset_path or DATASET_DIR
    if not dataset_path.exists():
        print(f"Error: Dataset directory not found: {dataset_path}")
        sys.exit(1)

    s3 = boto3.client("s3")
    dataset_path = dataset_path.resolve()
    count = 0
    errors = []

    for root, dirs, files in os.walk(dataset_path):
        for filename in files:
            local_path = Path(root) / filename
            relative = local_path.relative_to(dataset_path)
            s3_key = f"{prefix.rstrip('/')}/{relative.as_posix()}"

            try:
                s3.upload_file(str(local_path), bucket, s3_key)
                count += 1
                if count % 100 == 0:
                    print(f"  Uploaded {count} files...")
            except ClientError as e:
                errors.append((str(local_path), str(e)))

    if errors:
        print(f"\nErrors ({len(errors)} files):")
        for path, err in errors[:10]:
            print(f"  {path}: {err}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")

    print(f"\nDone. Uploaded {count} files to s3://{bucket}/{prefix}/")


def main():
    bucket = os.environ.get(BUCKET_ENV)
    prefix = os.environ.get(PREFIX_ENV, "dataset")

    if not bucket:
        if len(sys.argv) < 2:
            print("Usage:")
            print("  python upload_dataset_to_s3.py <bucket-name> [s3-prefix]")
            print("  or set S3_BUCKET (and optional S3_DATASET_PREFIX) environment variables")
            print("\nExample:")
            print("  python upload_dataset_to_s3.py my-ml-bucket dataset")
            sys.exit(1)
        bucket = sys.argv[1]
        prefix = sys.argv[2] if len(sys.argv) > 2 else "dataset"

    print(f"Uploading {DATASET_DIR} to s3://{bucket}/{prefix}/")
    upload_dataset_to_s3(bucket, prefix)


if __name__ == "__main__":
    main()
