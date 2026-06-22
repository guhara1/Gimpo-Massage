#!/usr/bin/env python3
"""
Google Indexing API 를 통한 즉시 URL 색인 통보

구글은 IndexNow를 미참여하기 때문에 이 스크립트가 필요합니다.
Sitemap ping과 달리 개별 URL을 즉시 색인하도록 요청할 수 있습니다.

📋 사전 설정:
  1. Google Cloud Project 생성
     https://console.cloud.google.com/
  2. Indexing API 활성화
  3. Service Account 생성 (JSON 키 다운로드)
  4. Search Console에서 Service Account 인증

📁 키 파일 위치: tools/google-service-account.json

사용법:
  python3 tools/google_indexing_api.py              # 모든 URL 요청
  python3 tools/google_indexing_api.py gurae-dong/  # 특정 경로만
"""
import os
import sys
import json
import argparse
from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Optional

# 구글 API 라이브러리 (선택 설치)
try:
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
    import requests

    HAS_GOOGLE_API = True
except ImportError:
    HAS_GOOGLE_API = False
    print(
        "📌 Google API 라이브러리 필요:",
        "pip install google-auth google-auth-httplib2 google-auth-oauthlib requests",
    )

# 설정
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")
SITEMAP_FILE = os.path.join(ROOT, "sitemap.xml")
SERVICE_ACCOUNT_FILE = os.path.join(TOOLS_DIR, "google-service-account.json")

GOOGLE_INDEXING_API = "https://indexing.googleapis.com/batch"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def parse_sitemap(sitemap_path: str) -> list:
    """Sitemap.xml에서 모든 URL 추출"""
    if not os.path.exists(sitemap_path):
        print(f"❌ Sitemap not found: {sitemap_path}")
        return []

    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()

        urls = []
        for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            loc = url_elem.text
            if loc:
                urls.append(loc)

        return urls
    except Exception as e:
        print(f"❌ Failed to parse sitemap: {e}")
        return []


def get_service_account_credentials():
    """Service Account 인증"""
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Service account file not found: {SERVICE_ACCOUNT_FILE}")
        print()
        print("📋 설정 방법:")
        print("  1. Google Cloud Console에서 Service Account 생성")
        print("  2. JSON 키 다운로드")
        print(f"  3. 다음 위치에 저장: {SERVICE_ACCOUNT_FILE}")
        print()
        return None

    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        return credentials
    except Exception as e:
        print(f"❌ Failed to load credentials: {e}")
        return None


def send_indexing_request(url: str, credentials) -> bool:
    """Google Indexing API에 개별 URL 전송"""
    request_body = {
        "url": url,
        "type": "URL_UPDATED",
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {credentials.token}",
    }

    try:
        # 토큰 갱신
        credentials.refresh(Request())
        headers["Authorization"] = f"Bearer {credentials.token}"

        response = requests.post(GOOGLE_INDEXING_API, json=request_body, headers=headers)

        if response.status_code == 200:
            return True
        else:
            print(f"  ⚠ {url}: {response.status_code} {response.text}")
            return False

    except Exception as e:
        print(f"  ⚠ {url}: {e}")
        return False


def batch_send_indexing(urls: list, credentials) -> dict:
    """배치 처리로 URL 전송 (1초 간격)"""
    import time

    results = {"success": 0, "failed": 0}

    for i, url in enumerate(urls):
        if send_indexing_request(url, credentials):
            results["success"] += 1
            print(f"  ✓ [{i+1}/{len(urls)}] {url}")
        else:
            results["failed"] += 1

        # API 속도 제한 회피
        if i < len(urls) - 1:
            time.sleep(1)

    return results


def filter_urls_by_pattern(urls: list, pattern: str) -> list:
    """경로 패턴으로 URL 필터링"""
    return [url for url in urls if pattern in url]


def main():
    if not HAS_GOOGLE_API:
        print(
            "❌ Google API 라이브러리가 필요합니다:",
            "pip install google-auth requests",
        )
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Google Indexing API로 URL 즉시 색인 요청",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python3 tools/google_indexing_api.py                # 모든 URL 요청
  python3 tools/google_indexing_api.py gurae-dong/    # 특정 경로만
        """,
    )
    parser.add_argument(
        "pattern", nargs="?", default="", help="URL 패턴 필터 (예: 'gurae-dong/')"
    )
    parser.add_argument("--dry-run", action="store_true", help="실제 요청하지 않고 URL만 표시")

    args = parser.parse_args()

    print("\n🔍 Google Indexing API 색인 요청")
    print()

    # Sitemap 파싱
    urls = parse_sitemap(SITEMAP_FILE)
    if not urls:
        print("❌ No URLs found in sitemap")
        sys.exit(1)

    print(f"✓ Sitemap loaded: {len(urls)} URLs")

    # 패턴 필터링
    if args.pattern:
        filtered_urls = filter_urls_by_pattern(urls, args.pattern)
        print(f"  Filtered by '{args.pattern}': {len(filtered_urls)} URLs")
        urls = filtered_urls

    print()

    if args.dry_run:
        print("🔸 DRY-RUN MODE: URLs to be indexed:")
        for url in urls[:10]:
            print(f"   {url}")
        if len(urls) > 10:
            print(f"   ... and {len(urls) - 10} more")
        return

    # 자격증명 로드
    credentials = get_service_account_credentials()
    if not credentials:
        sys.exit(1)

    print(f"📤 Google Indexing API로 {len(urls)}개 URL 전송...")
    print()

    results = batch_send_indexing(urls, credentials)

    print()
    print(f"✅ 완료!")
    print(f"   성공: {results['success']}")
    print(f"   실패: {results['failed']}")
    print()


if __name__ == "__main__":
    main()
