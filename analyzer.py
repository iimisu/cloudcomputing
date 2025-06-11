import sys
import boto3
from botocore.exceptions import ClientError

def main():
    if len(sys.argv) < 4:
        print("Usage: python analyzer.py <source_bucket> <source_key> <destination_bucket>")
        sys.exit(1)

    source_bucket = sys.argv[1]
    source_key = sys.argv[2]
    destination_bucket = sys.argv[3]

    s3_client = boto3.client('s3')
    print(f"Starting processing for s3://{source_bucket}/{source_key}")

    try:
        print("--> Downloading file...")
        response = s3_client.get_object(Bucket=source_bucket, Key=source_key)
        file_content = response['Body'].read().decode('utf-8')

        print("--> Analyzing file...")
        lines = file_content.splitlines()
        line_count = len(lines)
        result_content = f"The file '{source_key}' contains {line_count} lines."
        print(f"--> Analysis complete: {result_content}")

        destination_key = f"result-{source_key}.txt"
        print(f"--> Uploading result to s3://{destination_bucket}/{destination_key}")

        s3_client.put_object(
            Bucket=destination_bucket,
            Key=destination_key,
            Body=result_content,
            ContentType='text/plain'
        )
        print("Processing finished successfully!")

    except ClientError as e:
        print(f"An AWS error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()