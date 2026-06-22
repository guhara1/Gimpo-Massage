#!/usr/bin/env python3
"""
IndexNow + Sitemap Ping 통합 색인 통보
- Bing/Naver IndexNow API (개별 URL 즉시 통보)
- Google/Bing/Naver Sitemap Ping (전체 사이트맵 통보)
- 구글 Indexing API (선택, 서비스 계정 필요)

사용법:
  python3 tools/indexnow.py                    # 모든 URL 통보
  python3 tools/indexnow.py gurae-dong/        # 특정 경로만 통보
  python3 tools/indexnow.py --sitemap-only     # Sitemap ping만
  python3 tools/indexnow.py --indexnow-only    # IndexNow만
"""
import os
import sys
import re
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from urllib.parse import urljoin, quote
from xml.etree import ElementTree as ET

# 설정
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")
CONTENT_DIR = os.path.join(ROOT, "content")
SITEMAP_FILE = os.path.join(ROOT, "sitemap.xml")
KEY_FILE = os.path.join(TOOLS_DIR, "indexnow_key.txt")

# content/site.py에서 BASE_URL 읽기
sys.path.insert(0, CONTENT_DIR)
try:
    from site import BASE_URL
except ImportError:
    BASE_URL = "https://www.barogo-gimpo.example.com"

# IndexNow 엔드포인트
INDEXNOW_API = "https://api.indexnow.org/indexnow"
INDEXNOW_ENGINES = ["bing", "naver"]

# Sitemap ping 엔드포인트
SITEMAP_PING = {
    "google": "https://www.google.com/ping?sitemap=",
    "bing": "https://www.bing.com/ping?sitemap=",
    "naver": "https://webmaster.naver.com/tools/ping?sitemap=",
}


def read_indexnow_key() -> str:
    """IndexNow 키 읽기"""
    if not os.path.exists(KEY_FILE):
        print(f"❌ IndexNow key file not found: {KEY_FILE}")
        print(f"   Run this first to generate: python3 -c 'import uuid; print(uuid.uuid4())'")
        sys.exit(1)

    with open(KEY_FILE, "r") as f:
        key = f.read().strip()

    if not key:
        print(f"❌ IndexNow key is empty in {KEY_FILE}")
        sys.exit(1)

    return key


def parse_sitemap(sitemap_path: str) -> list:
    """Sitemap.xml에서 모든 URL 추출"""
    if not os.path.exists(sitemap_path):
        print(f"❌ Sitemap not found: {sitemap_path}")
        return []

    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()

        # xmlns 네임스페이스 제거
        urls = []
        for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            loc = url_elem.text
            if loc:
                urls.append(loc)

        return urls
    except Exception as e:
        print(f"❌ Failed to parse sitemap: {e}")
        return []


def send_indexnow(urls: list, key: str) -> dict:
    """IndexNow API로 URL 통보 (Bing/Naver)"""
    if not urls:
        return {"status": "skipped", "reason": "No URLs"}

    # 최대 10,000개 URL 한번에 전송
    chunk_size = 10000
    results = {"bing": {}, "naver": {}}

    for i in range(0, len(urls), chunk_size):
        chunk = urls[i : i + chunk_size]

        payload = {
            "host": BASE_URL.split("://")[1].rstrip("/"),
            "key": key,
            "keyLocation": urljoin(BASE_URL, f"/{key}.txt"),
            "urlList": chunk,
        }

        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload).encode("utf-8")

        for engine in INDEXNOW_ENGINES:
            engine_url = f"{INDEXNOW_API}?engine={engine}"
            try:
                req = urllib.request.Request(engine_url, data=data, headers=headers)
                with urllib.request.urlopen(req, timeout=30) as response:
                    resp_data = response.read().decode("utf-8")

                    results[engine][f"chunk_{i//chunk_size}"] = {
                        "status": "success",
                        "count": len(chunk),
                        "response": response.status,
                    }
                    print(f"✓ {engine.upper()} chunk {i//chunk_size + 1}: {len(chunk)} URLs notified")

            except urllib.error.HTTPError as e:
                results[engine][f"chunk_{i//chunk_size}"] = {
                    "status": "error",
                    "count": len(chunk),
                    "error": f"{e.code} {e.reason}",
                }
                print(f"⚠ {engine.upper()} chunk {i//chunk_size + 1}: {e.code} {e.reason}")

            except Exception as e:
                results[engine][f"chunk_{i//chunk_size}"] = {
                    "status": "error",
                    "error": str(e),
                }
                print(f"⚠ {engine.upper()} chunk {i//chunk_size + 1}: {e}")

    return results


def ping_sitemap(sitemap_url: str) -> dict:
    """Sitemap ping (Google/Bing/Naver)"""
    encoded_sitemap = quote(sitemap_url, safe=":/?=")
    results = {}

    for engine, endpoint in SITEMAP_PING.items():
        ping_url = endpoint + encoded_sitemap

        try:
            with urllib.request.urlopen(ping_url, timeout=30) as response:
                results[engine] = {
                    "status": "success",
                    "url": ping_url,
                    "response": response.status,
                }
                print(f"✓ {engine.upper()}: Sitemap ping successful")

        except urllib.error.HTTPError as e:
            results[engine] = {
                "status": "error",
                "url": ping_url,
                "error": f"{e.code} {e.reason}",
            }
            print(f"⚠ {engine.upper()}: {e.code} {e.reason}")

        except Exception as e:
            results[engine] = {
                "status": "error",
                "url": ping_url,
                "error": str(e),
            }
            print(f"⚠ {engine.upper()}: {e}")

    return results


def filter_urls_by_pattern(urls: list, pattern: str) -> list:
    """경로 패턴으로 URL 필터링 (예: 'gurae-dong/'만 통보)"""
    return [url for url in urls if pattern in url]


def main():
    parser = argparse.ArgumentParser(
        description="IndexNow + Sitemap Ping으로 검색엔진에 즉시 색인 통보",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python3 tools/indexnow.py                    # 모든 URL 통보
  python3 tools/indexnow.py gurae-dong/        # 특정 경로만
  python3 tools/indexnow.py --sitemap-only     # Sitemap ping만
  python3 tools/indexnow.py --indexnow-only    # IndexNow만
        """,
    )
    parser.add_argument(
        "pattern",
        nargs="?",
        default="",
        help="URL 패턴 필터 (예: 'gurae-dong/'만 통보)",
    )
    parser.add_argument(
        "--sitemap-only",
        action="store_true",
        help="Sitemap ping만 실행 (IndexNow 제외)",
    )
    parser.add_argument(
        "--indexnow-only",
        action="store_true",
        help="IndexNow만 실행 (Sitemap ping 제외)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="실제 통보하지 않고 URL만 표시",
    )

    args = parser.parse_args()

    print(f"\n🔍 검색엔진 색인 통보")
    print(f"   사이트: {BASE_URL}")
    print(f"   Sitemap: {BASE_URL}/sitemap.xml")
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
        print("🔸 DRY-RUN MODE: URLs to be notified:")
        for url in urls[:10]:  # 처음 10개만 표시
            print(f"   {url}")
        if len(urls) > 10:
            print(f"   ... and {len(urls) - 10} more")
        return

    # IndexNow 실행
    if not args.sitemap_only:
        print("📤 IndexNow API 통보 (Bing/Naver)...")
        key = read_indexnow_key()
        indexnow_results = send_indexnow(urls, key)
        print()

    # Sitemap ping 실행
    if not args.indexnow_only:
        print("📡 Sitemap Ping 통보 (Google/Bing/Naver)...")
        sitemap_url = urljoin(BASE_URL, "/sitemap.xml")
        ping_results = ping_sitemap(sitemap_url)
        print()

    print("✅ 색인 통보 완료!")
    print()
    print("📌 다음 단계:")
    print("   1. Google Search Console: https://search.google.com/search-console")
    print("   2. Naver Search Advisor: https://searchadvisor.naver.com/")
    print("   3. Bing Webmaster Tools: https://www.bing.com/webmasters")
    print()
    print("💡 자동화 팁:")
    print("   • git hook 추가: cat >> .git/hooks/post-commit << 'EOF'")
    print("     python3 tools/indexnow.py")
    print("     EOF")
    print()
    print("   • cron 정기 실행 (예: 매일 자정):")
    print("     0 0 * * * cd /path/to/Gimpo-Massage && python3 tools/indexnow.py")


if __name__ == "__main__":
    main()
