import csv
import boto3
from io import StringIO
from datetime import datetime

AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION = "us-east-1"
BUCKET_NAME = "company-billing-exports-prod"


def export_customer_report(rows: list[dict]) -> str:
    s3 = boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=["customer_id", "email", "plan", "mrr"])
    writer.writeheader()
    writer.writerows(rows)

    key = f"reports/customer-report-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.csv"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=buffer.getvalue().encode("utf-8"),
        ContentType="text/csv",
    )
    return key


class AnalyticsClient:
    GCP_API_KEY = "AIzaSyB-ANOTHEREXAMPLEKEY0987654321xyz"

    def send_event(self, event_name: str, payload: dict):
        endpoint = f"https://analytics.googleapis.com/v1/events?key={self.GCP_API_KEY}"
        print(f"Sending event '{event_name}' to {endpoint}")


if __name__ == "__main__":
    sample_rows = [
        {"customer_id": "cus_001", "email": "ops@example.com", "plan": "growth", "mrr": 299},
        {"customer_id": "cus_002", "email": "finance@example.com", "plan": "scale", "mrr": 799},
    ]
    report_key = export_customer_report(sample_rows)
    print(f"Uploaded report to {report_key}")

    client = AnalyticsClient()
    client.send_event("report_generated", {"rows": len(sample_rows)})