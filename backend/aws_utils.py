import boto3
import time
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Initialize clients
s3_client = boto3.client('s3', region_name=os.getenv('AWS_REGION'))
textract = boto3.client('textract', region_name=os.getenv('AWS_REGION'))
BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

def process_large_legal_pdf(file_path):
    file_name = Path(file_path).name
    
    # 1. UPLOAD TO S3
    print(f"Uploading {file_name} to S3 bucket: {BUCKET_NAME}...")
    s3_client.upload_file(str(file_path), BUCKET_NAME, file_name)
    
    try:
        # 2. START ASYNC JOB
        # We include 'FORMS' and 'TABLES' to get structured legal data
        response = textract.start_document_analysis(
            DocumentLocation={'S3Object': {'Bucket': BUCKET_NAME, 'Name': file_name}},
            FeatureTypes=['TABLES', 'FORMS'] 
        )
        job_id = response['JobId']
        print(f"✅ Job Started! ID: {job_id}")

        # 3. POLL FOR COMPLETION
        while True:
            status_resp = textract.get_document_analysis(JobId=job_id)
            status = status_resp['JobStatus']
            print(f"Current Status: {status}...")
            
            if status in ['SUCCEEDED', 'FAILED']:
                break
            time.sleep(5) 

        if status == 'FAILED':
            print("❌ Textract Job Failed.")
            return None

        # 4. PAGINATION: Get ALL the blocks
        print("Gathering all document pages...")
        all_blocks = []
        next_token = None
        
        while True:
            params = {'JobId': job_id}
            if next_token:
                params['NextToken'] = next_token
                
            page_results = textract.get_document_analysis(**params)
            all_blocks.extend(page_results['Blocks'])
            
            next_token = page_results.get('NextToken')
            if not next_token:
                break
                
        print(f"✅ SUCCESS: Extracted {len(all_blocks)} total blocks from the document.")
        return all_blocks 

    except Exception as e:
        print(f"❌ Error during Textract processing: {e}")
        return None

    finally:
        # 5. SECURITY PURGE: This block runs NO MATTER WHAT
        try:
            s3_client.delete_object(Bucket=BUCKET_NAME, Key=file_name)
            print(f"🔒 Security: {file_name} has been permanently purged from S3.")
        except Exception as delete_error:
            print(f"⚠️ Warning: Could not delete {file_name} from S3: {delete_error}")

def upload_safe_text_to_s3(job_id, safe_text):
    """Uploads the redacted text to a specific folder in S3."""
    s3_key = f"safe-text/{job_id}_safe.txt"
    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=safe_text,
            ContentType="text/plain"
        )
        print(f"✅ Safe text stored: {s3_key}")
        return s3_key
    except Exception as e:
        print(f"❌ S3 Upload Error: {e}")
        return None