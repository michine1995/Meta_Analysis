import os
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# アップロード先のGoogle DriveフォルダID（GitHub Actions側で設定）
FOLDER_ID = os.environ.get("AD_INSIGHT_FOLDER_ID")
CSV_FILENAME = "ad_insight.csv"

# 📊 ダミーデータ作成（本来はここを Meta Ad Library API のレスポンスに置き換える）
def fetch_ads():
    with open(CSV_FILENAME, "w") as f:
        f.write("campaign_name,ad_text\n")
        f.write("Sample Campaign,This is a sample ad.\n")

# ☁️ Google Drive にアップロード
def upload_to_drive():
    creds = service_account.Credentials.from_service_account_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    service = build("drive", "v3", credentials=creds)

    media = MediaFileUpload(CSV_FILENAME, mimetype="text/csv")
    file_metadata = {
        "name": CSV_FILENAME,
        "parents": [FOLDER_ID]
    }

    service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()
    print("✅ アップロード完了：", CSV_FILENAME)

# 🚀 メイン処理
if __name__ == "__main__":
    fetch_ads()
    upload_to_drive()
