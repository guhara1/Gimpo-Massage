#!/usr/bin/env python3
"""
RSS/Atom 피드 생성 (블로그/매거진용)

사이트의 매거진/뉴스 페이지를 RSS로 변환합니다.
"""
import os
import sys
from datetime import datetime
from xml.etree import ElementTree as ET
from xml.dom import minidom

# 설정
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT, "content")

# content 패키지로 import (builtin `site` 모듈과의 충돌 방지)
sys.path.insert(0, ROOT)
try:
    from content.site import BASE_URL, BRAND, PHONE_DISPLAY, SITE_DESC
except ImportError:
    BASE_URL = "https://gimpo-massage.pages.dev"
    BRAND = "바로 GO"
    SITE_DESC = "김포시 출장마사지·홈타이"


def pretty_print_xml(elem):
    """XML을 읽기 좋게 포매팅"""
    rough_string = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def generate_magazine_rss():
    """매거진 RSS 피드 생성"""
    # 매거진 페이지 목록 (content/magazine.py에서)
    magazines = [
        {
            "title": "마사지 비교 가이드",
            "path": "magazine/swedish-vs-thai/",
            "desc": "스웨디시와 타이마사지의 효과 차이 이해하기",
            "date": "2024-06-20",
        },
        {
            "title": "처음 이용 가이드",
            "path": "magazine/first-time-guide/",
            "desc": "출장마사지 처음 예약하는 분들을 위한 가이드",
            "date": "2024-06-19",
        },
        {
            "title": "수면과 마사지",
            "path": "magazine/sleep-and-massage/",
            "desc": "마사지가 수면의 질을 개선하는 방법",
            "date": "2024-06-18",
        },
        {
            "title": "운동 후 회복",
            "path": "magazine/post-workout-timing/",
            "desc": "운동 후 마사지의 최적 타이밍",
            "date": "2024-06-17",
        },
        {
            "title": "어깨·목 결림 관리",
            "path": "magazine/neck-shoulder-care/",
            "desc": "오래 앉아서 일하는 분들을 위한 경락 관리",
            "date": "2024-06-16",
        },
        {
            "title": "부모님 선물 가이드",
            "path": "magazine/parents-gift/",
            "desc": "효도 선물로 받는 마사지 처음 경험하기",
            "date": "2024-06-15",
        },
    ]

    # RSS 2.0 생성
    rss = ET.Element("rss", version="2.0")
    rss.set("xmlns:content", "http://purl.org/rss/1.0/modules/content/")
    rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")

    channel = ET.SubElement(rss, "channel")

    # Channel 정보
    title_elem = ET.SubElement(channel, "title")
    title_elem.text = f"{BRAND} 매거진"

    link_elem = ET.SubElement(channel, "link")
    link_elem.text = BASE_URL.rstrip("/") + "/magazine/"

    desc_elem = ET.SubElement(channel, "description")
    desc_elem.text = SITE_DESC

    language = ET.SubElement(channel, "language")
    language.text = "ko"

    lastbuild = ET.SubElement(channel, "lastBuildDate")
    lastbuild.text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

    # Items
    for mag in magazines:
        item = ET.SubElement(channel, "item")

        title = ET.SubElement(item, "title")
        title.text = mag["title"]

        link = ET.SubElement(item, "link")
        link.text = BASE_URL.rstrip("/") + "/" + mag["path"]

        description = ET.SubElement(item, "description")
        description.text = mag["desc"]

        pubdate = ET.SubElement(item, "pubDate")
        pubdate.text = datetime.fromisoformat(mag["date"]).strftime("%a, %d %b %Y 00:00:00 +0000")

        guid = ET.SubElement(item, "guid", isPermaLink="true")
        guid.text = BASE_URL.rstrip("/") + "/" + mag["path"]

    # 파일 저장
    output_file = os.path.join(ROOT, "magazine", "feed.xml")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 포매팅된 XML 작성
    xml_str = pretty_print_xml(rss)
    # <?xml 선언 제거 후 다시 추가 (포매팅 시 2개가 생김)
    xml_lines = xml_str.split('\n')[1:]  # 첫 번째 라인 제거
    with open(output_file, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('\n'.join(xml_lines))

    print(f"✓ RSS 피드 생성: {output_file}")
    print(f"  URL: {BASE_URL.rstrip('/')}/magazine/feed.xml")


def generate_sitemap_rss():
    """Sitemap RSS 피드 (선택) - 모든 페이지 변경 추적"""
    sitemap_file = os.path.join(ROOT, "sitemap.xml")

    if not os.path.exists(sitemap_file):
        print("⚠ Sitemap not found")
        return

    # Sitemap 파싱
    try:
        tree = ET.parse(sitemap_file)
        root = tree.getroot()

        rss = ET.Element("rss", version="2.0")
        rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")

        channel = ET.SubElement(rss, "channel")

        title = ET.SubElement(channel, "title")
        title.text = f"{BRAND} - 전체 페이지"

        link = ET.SubElement(channel, "link")
        link.text = BASE_URL

        desc = ET.SubElement(channel, "description")
        desc.text = f"{BRAND} 전체 페이지 업데이트"

        language = ET.SubElement(channel, "language")
        language.text = "ko"

        lastbuild = ET.SubElement(channel, "lastBuildDate")
        lastbuild.text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

        # Sitemap의 URL을 item으로 변환
        count = 0
        for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            loc = url_elem.text
            if loc and count < 100:  # 최근 100개만
                item = ET.SubElement(channel, "item")

                slug = "home" if loc.rstrip("/") == BASE_URL.rstrip("/") else loc.rstrip("/").split("/")[-1]
                title_item = ET.SubElement(item, "title")
                title_item.text = f"{BRAND} - {slug}"

                link_item = ET.SubElement(item, "link")
                link_item.text = loc

                desc_item = ET.SubElement(item, "description")
                desc_item.text = f"{BRAND} {slug} 페이지"

                pubdate = ET.SubElement(item, "pubDate")
                pubdate.text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

                guid = ET.SubElement(item, "guid", isPermaLink="true")
                guid.text = loc

                count += 1

        output_file = os.path.join(ROOT, "feed.xml")

        # 포매팅된 XML 작성
        xml_str = pretty_print_xml(rss)
        xml_lines = xml_str.split('\n')[1:]
        with open(output_file, "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('\n'.join(xml_lines))

        print(f"✓ Sitemap RSS 생성: {output_file}")

    except Exception as e:
        print(f"⚠ Failed to generate sitemap RSS: {e}")


if __name__ == "__main__":
    print("📡 RSS 피드 생성")
    print()

    generate_magazine_rss()
    generate_sitemap_rss()

    print()
    print("✅ RSS 피드 생성 완료")
    print()
    print("📌 RSS 리더에 등록:")
    print(f"   • 매거진: {BASE_URL.rstrip('/')}/magazine/feed.xml")
    print(f"   • 전체: {BASE_URL.rstrip('/')}/feed.xml")

