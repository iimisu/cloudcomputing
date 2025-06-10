# analyzer.py
import sys
import boto3
from botocore.exceptions import ClientError

def main():
    # 检查命令行参数是否足够
    if len(sys.argv) < 4:
        print("Usage: python analyzer.py <source_bucket> <source_key> <destination_bucket>")
        sys.exit(1)

    # 从命令行参数获取S3信息
    source_bucket = sys.argv[1]
    source_key = sys.argv[2]
    destination_bucket = sys.argv[3]
    
    # 初始化boto3 S3客户端
    s3_client = boto3.client('s3')

    print(f"Starting processing for s3://{source_bucket}/{source_key}")

    try:
        # 从源S3桶下载文件
        print("--> Downloading file...")
        response = s3_client.get_object(Bucket=source_bucket, Key=source_key)
        file_content = response['Body'].read().decode('utf-8')
        
        # 执行简单的分析：计算行数
        print("--> Analyzing file...")
        lines = file_content.splitlines()
        line_count = len(lines)
        result_content = f"The file '{source_key}' contains {line_count} lines."
        print(f"--> Analysis complete: {result_content}")

        # 准备上传结果
        destination_key = f"result-{source_key}.txt"
        print(f"--> Uploading result to s3://{destination_bucket}/{destination_key}")
        
        # 将结果上传到目标S3桶
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