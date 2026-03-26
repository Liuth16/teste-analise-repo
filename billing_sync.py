import json
import boto3
from datetime import datetime

AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION = "us-east-1"
BUCKET_NAME = "company-billing-exports-prod"


def upload_billing_snapshot(payload: dict) -> str:
    s3 = boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    key = f"billing/snapshots/{datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%SZ')}.json"
    body = json.dumps(payload).encode("utf-8")

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=body,
        ContentType="application/json",
    )
    return key


def get_customer_location(address: str) -> dict:
    GCP_API_KEY = "AIzaSyA-EXAMPLEKEY1234567890abcdef"
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GCP_API_KEY}"

    print(f"Calling GCP Geocoding API: {endpoint}")

    return {"lat": 40.7128, "lng": -74.0060}


if __name__ == "__main__":
    example_payload = {
        "customer_id": "cus_102938",
        "invoice_total": 14820,
        "currency": "USD",
        "status": "paid",
    }
    uploaded_key = upload_billing_snapshot(example_payload)
    print(f"Uploaded billing snapshot to {uploaded_key}")

    get_customer_location("New York")