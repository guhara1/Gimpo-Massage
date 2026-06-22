# 🚀 SEO 색인 설정 체크리스트

사이트 배포 후 검색엔진 색인을 위한 필수 설정 항목입니다.

---

## ✅ 자동 생성됨 (이미 완료)

- [x] `sitemap.xml` 생성
- [x] `robots.txt` 생성
- [x] IndexNow 키 파일 생성
  - 📁 위치: `faa20d8a-1a2a-459a-bf1a-43c4f8a03d5f.txt`
  - 🔑 키 ID: `faa20d8a-1a2a-459a-bf1a-43c4f8a03d5f`
  - 💾 백업: `tools/indexnow_key.txt`
- [x] RSS 피드 생성
  - 📰 매거진: `/magazine/feed.xml`
  - 📡 전체: `/feed.xml`

---

## 🔧 배포 전 필수 작업

### 1단계: 도메인 확정

```python
# content/site.py 에서 변경
BASE_URL = "https://www.실제도메인.com"  # ← 여기 수정
```

**저장 후 빌드:**

```bash
python3 build.py
```

### 2단계: 즉시 모든 URL 색인 통보

```bash
# 모든 검색엔진에 통보 (Bing, Naver, Google)
python3 tools/indexnow.py

# 또는 Sitemap ping만 (더 안전)
python3 tools/indexnow.py --sitemap-only
```

---

## 📋 검색엔진별 등록

### Google Search Console

```
1️⃣  https://search.google.com/search-console
2️⃣  사이트 추가/선택
3️⃣  설정 > Sitemap
4️⃣  Sitemap 제출
     https://www.실제도메인.com/sitemap.xml
5️⃣  대기 (최대 7일)
```

**확인:**
- 색인된 페이지 수
- 검색 성과
- 모바일 사용성

### Naver Search Advisor

```
1️⃣  https://searchadvisor.naver.com/
2️⃣  우측 상단 + 추가
3️⃣  사이트 URL 입력
4️⃣  소유권 확인
     - HTML 메타 태그 (권장)
     - 파일 업로드
5️⃣  완료
6️⃣  수집 요청 > Sitemap 수집
     https://www.실제도메인.com/sitemap.xml
7️⃣  대기 (보통 24시간 이내)
```

**확인:**
- 크롤링 통계
- 수집 상태
- 색인 상태

### Bing Webmaster Tools

```
1️⃣  https://www.bing.com/webmasters
2️⃣  사이트 추가
3️⃣  소유권 확인 (robots.txt 방식 권장)
4️⃣  설정 > Sitemap
5️⃣  Sitemap 제출
     https://www.실제도메인.com/sitemap.xml
6️⃣  대기 (최대 48시간)
```

**확인:**
- 인덱싱 상태
- 크롤링 오류

---

## 📊 검색엔진별 현황 모니터링

| 항목 | Google | Naver | Bing |
|------|--------|-------|------|
| **URL 검사** | ✅ | ✅ | ✅ |
| **색인 상태** | 즉시 | ~24시간 | ~48시간 |
| **색인 요청** | Indexing API | IndexNow | IndexNow |
| **모니터링** | Search Console | Search Advisor | Webmaster Tools |

---

## 🔄 자동화 설정 (선택)

### Git Hook (매 커밋 후 색인 통보)

```bash
# 설정
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash
# 빌드 후 Sitemap ping
python3 tools/indexnow.py --sitemap-only 2>/dev/null || true
EOF

chmod +x .git/hooks/post-commit
```

### Cron (정기적 색인 갱신)

```bash
# Crontab 편집
crontab -e

# 매일 자정에 Sitemap ping
0 0 * * * cd /path/to/Gimpo-Massage && python3 tools/indexnow.py --sitemap-only >> /tmp/indexnow.log 2>&1

# 매주 월요일 새벽 2시에 전체 URL 통보
0 2 * * 1 cd /path/to/Gimpo-Massage && python3 tools/indexnow.py >> /tmp/indexnow.log 2>&1
```

---

## 📱 RSS 피드 등록 (선택)

### 매거진 RSS

```
URL: https://www.실제도메인.com/magazine/feed.xml

등록처:
- Google News (news.google.com)
- Naver 블로그 (blog.naver.com)
- RSS 리더 (Feedly, Inoreader 등)
```

### 전체 페이지 RSS

```
URL: https://www.실제도메인.com/feed.xml

사용처:
- 웹사이트 구독 기능
- 소셜 미디어 자동 공유
```

---

## 🔐 IndexNow 키 관리

### 키 파일 위치

```
📁 루트: faa20d8a-1a2a-459a-bf1a-43c4f8a03d5f.txt
💾 백업: tools/indexnow_key.txt
```

### 배포 요구사항

```
✅ faa20d8a-1a2a-459a-bf1a-43c4f8a03d5f.txt 는 반드시 루트에 배포됨
✅ 누구나 접근 가능: https://www.실제도메인.com/faa20d8a-1a2a-459a-bf1a-43c4f8a03d5f.txt
✅ 내용은 키 값 자체만 포함
```

### 키 재생성 (선택)

키를 재생성해야 하는 경우:

```bash
python3 << 'EOF'
import uuid
import os

new_key = str(uuid.uuid4())
root = "/path/to/Gimpo-Massage"

# 구 키 백업
os.rename(os.path.join(root, "tools/indexnow_key.txt"), 
          os.path.join(root, "tools/indexnow_key.txt.bak"))

# 신 키 저장
with open(os.path.join(root, "tools/indexnow_key.txt"), "w") as f:
    f.write(new_key)

# 루트에도 생성
with open(os.path.join(root, f"{new_key}.txt"), "w") as f:
    f.write(new_key)

print(f"New IndexNow Key: {new_key}")
EOF
```

---

## 🟦 Google Indexing API 연동 (고급)

구글은 IndexNow 미참여이므로, 더 빠른 색인이 필요하면 API 연동:

```bash
# 1. Google Cloud 설정 (tools/README.md 참고)
# 2. Service Account JSON 키 저장
#    tools/google-service-account.json
# 3. 라이브러리 설치
pip install google-auth requests
# 4. 색인 요청
python3 tools/google_indexing_api.py
```

---

## 📈 효과 측정

### 1주일 후 확인

- [ ] Google Search Console에서 URL 검사
- [ ] Naver Search Advisor에서 크롤링 상태 확인
- [ ] Bing Webmaster에서 인덱싱 상태 확인

### 2주일 후 확인

- [ ] Google에서 "site:실제도메인.com" 검색 결과
- [ ] Naver에서 "site:실제도메인.com" 검색 결과
- [ ] 각 검색엔진의 색인 페이지 수 증가

### 1개월 후 확인

- [ ] 주요 키워드로 검색 순위 확인
- [ ] Search Console에서 검색 성과 분석
- [ ] 자연 검색 트래픽 증가 추적

---

## 💡 최적화 팁

### ✅ 현재 사이트의 강점

1. **잘 구조화된 Sitemap**
   - 66개 페이지 모두 포함
   - 정확한 URL 경로
   
2. **Clean URL 구조**
   - 루트(/)에서 직접 서빙
   - 의미있는 경로명 (gurae-dong/, station/ 등)
   
3. **Schema.org JSON-LD**
   - Organization, WebPage, BreadcrumbList
   - FAQ 스키마 (메인 페이지)
   
4. **상세한 본문 콘텐츠**
   - 모든 페이지 2,000자 이상
   - 자연스러운 키워드 배치

### ⚡ 추가 개선 (선택)

1. **내부 링크 앵커 텍스트 최적화**
   - 현재: 지역명만 사용 ✅
   - 향후: 서술적 앵커 추가 (예: "구래역 역세권 안내")

2. **og: Open Graph 태그**
   - 소셜 공유용 이미지
   - og:image는 이미 포함 ✅

3. **모바일 최적화**
   - 반응형 CSS 확인
   - 모바일 속도 테스트 (PageSpeed Insights)

4. **웹사이트 속도**
   - Lighthouse 점수 확인
   - 이미지 최적화 (필요 시)

---

## 🆘 문제 해결

### Q. 색인이 안 됨

**A.**
1. Sitemap이 robots.txt에 포함되었는지 확인
2. Search Console에서 수동으로 URL 검사
3. 도메인 메타데이터 확인 (DNS, HTTPS 등)

### Q. 색인 속도가 느림

**A.**
1. IndexNow 자동화 설정 (tools/README.md)
2. 구글 Indexing API 연동 (google_indexing_api.py)
3. 정기 cron 작업으로 주기적 갱신

### Q. 색인 후 순위가 안 올라감

**A.**
1. 키워드 경합도 분석 (Google Keyword Planner)
2. 경쟁사 콘텐츠 분석
3. 백링크 추가 (외부 언급 유도)
4. 시간 경과 대기 (보통 1-3개월)

---

## 📞 고객센터 안내

색인 관련 의문사항:

- 💬 GitHub Issues: 기술적 문제
- 📧 구글 Search Central: 색인 정책
- 🤝 Naver Search Advisor: 수집 지원
- 🔧 Bing Webmaster: 기술 지원

---

**마지막 업데이트:** 2024년 6월 22일  
**IndexNow 키:** faa20d8a-1a2a-459a-bf1a-43c4f8a03d5f  
**상태:** ✅ 배포 준비 완료
