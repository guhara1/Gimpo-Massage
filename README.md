# 바로 GO — 김포시 출장마사지·홈타이 안내 사이트

경기도 김포시 전지역 방문 관리(출장마사지·홈타이) 안내용 정적 사이트입니다.
예약전화: **0508-202-4719**

## 구조

- 정적 HTML 사이트 — 어느 호스팅(GitHub Pages, Netlify, 일반 웹서버)에서든 그대로 서빙 가능
- `build.py` + `content/` 패키지에서 페이지를 생성하는 빌드 방식
- 생성물(각 디렉터리의 `index.html`, `sitemap.xml`, `robots.txt`)도 저장소에 포함
- 메인은 `/gyeonggi/gimpo/`, 루트(`/`)는 메인으로 리다이렉트

```
build.py            # 빌드 스크립트 (레이아웃·글자수 검사·sitemap·루트 리다이렉트 생성)
content/
  site.py           # 상호(바로 GO)·전화·BASE_URL·메뉴 구조·텔레그램 문의 링크
  main.py           # 김포 메인 (Organization/WebPage/Breadcrumb/FAQ JSON-LD)
  areas.py          # 지역별: 대표 동/읍/면 14개
  stations.py       # 역세권: 허브 + 김포골드라인 역 9개
  livingzones.py    # 생활권: 허브 + 생활권 12개
  themes.py         # 테마별: 허브 + 14개 테마
  info.py           # 출장마사지 안내·코스·예약·가이드·후기·고객센터·약관
  magazine.py       # 매거진(정보형 글)
  about.py          # 운영자 소개(E-E-A-T)
assets/             # CSS(프리미엄 토큰 + 컴포넌트 오버레이), 모바일 내비 JS
```

## 빌드

```bash
python3 build.py
```

빌드 시 페이지별 본문 글자수 리포트가 출력됩니다.

## SEO 운영 원칙 (빌드에 강제됨)

- 본문 **2,000자 미만 페이지는 자동 `noindex`** 처리되고 sitemap에서 제외
- 메뉴명·URL에 "출장마사지"를 반복하지 않음 — 키워드는 Title·H1·첫 문단에서만 자연스럽게
- 대표 지역은 동/읍/면 14개, 역은 김포골드라인 역명 1개당 페이지 1개 (출구별·조합 페이지 없음)
- 김포공항역은 서울 강서구 성격이라 인접 생활권으로만, 검단·계양역은 인천 성격이라 제외
- **지역+역+테마 조합 페이지 없음** (도어웨이 방지)
- 모든 페이지 본문은 페이지별 고유 작성 (지역명만 바꾼 복붙 없음)
- 실제 오프라인 사업장 주소가 없는 방문형이라 LocalBusiness 스키마는 사용하지 않음

## 배포 전 해야 할 일

1. `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경
2. `content/site.py`의 `TELEGRAM_URL`(제작·제휴 문의)을 실제 채널로 확인/변경
3. `python3 build.py` 재실행 (canonical·sitemap·robots.txt·루트 리다이렉트에 반영됨)
4. Google Search Console에 `sitemap.xml` 제출
