# 🔍 검색엔진 색인 자동화

이 도구들은 빌드 후 자동으로 검색엔진(Google, Bing, Naver)에 사이트맵과 URL을 통보합니다.

## 📋 목차

- [빠른 시작](#-빠른-시작)
- [IndexNow 설정](#-indexnow-설정)
- [Google Indexing API](#-google-indexing-api)
- [Git Hook 자동화](#-git-hook-자동화)
- [Cron 정기 실행](#-cron-정기-실행)

---

## 🚀 빠른 시작

### 1단계: 즉시 모든 URL 색인 통보

```bash
# 모든 검색엔진에 通報 (IndexNow + Sitemap Ping)
python3 tools/indexnow.py

# 특정 경로만 (예: 구래동 페이지만)
python3 tools/indexnow.py gurae-dong/

# 테스트 (실제 통보하지 않음)
python3 tools/indexnow.py --dry-run
```

**통보 내용:**
- ✅ IndexNow API: Bing, Naver (개별 URL 즉시 등록)
- ✅ Sitemap Ping: Google, Bing, Naver (전체 사이트맵)

**결과:**
```
✓ BING chunk 1: 66 URLs notified
✓ NAVER chunk 1: 66 URLs notified
✓ GOOGLE: Sitemap ping successful
✓ BING: Sitemap ping successful
✓ NAVER: Sitemap ping successful
```

---

## 🔑 IndexNow 설정

### IndexNow란?

- **Bing과 Naver가 참여**하는 개방형 표준
- **개별 URL을 즉시 색인**하도록 요청
- API 기반으로 **24시간 안에 크롤링** 가능

### 자동 생성됨 ✅

IndexNow 키는 이미 생성되어 있습니다:

```
🔑 Key ID: faa20d8a-1a2a-459a-bf1a-43c4f8a03d5f
📁 파일: faa20d8a-1a2a-459a-bf1a-43c4f8a03d5f.txt (루트에 배포)
🔐 키 저장: tools/indexnow_key.txt
```

### 검증 방법

1. **Bing Webmaster Tools**
   - https://www.bing.com/webmasters/
   - 사이트 추가
   - Sitemap 등록

2. **Naver Search Advisor**
   - https://searchadvisor.naver.com/
   - 사이트 인증
   - Sitemap 등록

---

## 🟦 Google Indexing API (선택)

Google은 IndexNow를 미참여하므로 추가 설정이 필요합니다.

### 설정 방법

#### 1단계: Google Cloud Project 생성

```bash
# Google Cloud Console 접속
https://console.cloud.google.com/

# 프로젝트 만들기
- 프로젝트 이름: Gimpo-Massage 또는 임의
- 만들기 클릭
```

#### 2단계: Indexing API 활성화

```
좌측 메뉴 > APIs 및 서비스 > 라이브러리
-> "Indexing API" 검색
-> 활성화 클릭
```

#### 3단계: Service Account 생성

```
좌측 메뉴 > 서비스 계정
-> 서비스 계정 만들기
  - 서비스 계정 이름: gimpo-indexing
  - 계속
-> 역할 할당: 기본 > 편집자 (또는 "Indexing API 관리자")
-> 계속 & 완료
```

#### 4단계: JSON 키 다운로드

```
위에서 만든 서비스 계정 클릭
-> 키 탭 > 키 추가 > 새 키 만들기
-> JSON 형식 선택
-> 만들기 (자동 다운로드)
```

#### 5단계: 파일 저장

```bash
# 다운로드한 JSON 파일을 다음 위치에 저장
tools/google-service-account.json
```

#### 6단계: Google Search Console 인증

```
Google Search Console (https://search.google.com/search-console)
-> 속성 추가 또는 기존 속성 선택
-> 설정 > 소유자
-> Service Account 이메일 추가 (google-service-account.json의 "client_email")
   권한: 소유자
```

### 사용

```bash
# 라이브러리 설치 (첫 1회만)
pip install google-auth requests

# 모든 URL 색인 요청
python3 tools/google_indexing_api.py

# 특정 경로만
python3 tools/google_indexing_api.py gurae-dong/

# 테스트
python3 tools/google_indexing_api.py --dry-run
```

---

## 🔄 Git Hook 자동화

### Post-Commit Hook 설정

빌드 후 자동으로 색인 통보:

```bash
# Hook 파일 생성
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash
# 빌드 후 IndexNow 통보 (선택)
if grep -q "^import.*build" build.py; then
    python3 tools/indexnow.py --sitemap-only 2>/dev/null || true
fi
EOF

# 실행 권한
chmod +x .git/hooks/post-commit
```

### Post-Merge Hook (Pull 후)

```bash
cat > .git/hooks/post-merge << 'EOF'
#!/bin/bash
# Pull 후 빌드 및 색인 통보
if [ -f build.py ]; then
    python3 build.py
    python3 tools/indexnow.py --sitemap-only 2>/dev/null || true
fi
EOF

chmod +x .git/hooks/post-merge
```

---

## ⏰ Cron 정기 실행

### 매일 자정에 Sitemap ping

```bash
# Crontab 편집
crontab -e

# 다음 추가 (매일 자정 00:00)
0 0 * * * cd /home/user/Gimpo-Massage && python3 tools/indexnow.py --sitemap-only >> /tmp/indexnow.log 2>&1
```

### 매주 전체 색인 통보

```bash
# 매주 월요일 02:00 전체 색인 통보
0 2 * * 1 cd /home/user/Gimpo-Massage && python3 tools/indexnow.py >> /tmp/indexnow.log 2>&1
```

### 로그 확인

```bash
tail -f /tmp/indexnow.log
```

---

## 📊 색인 통보 모니터링

### 각 검색엔진에서 확인

| 검색엔진 | URL | 확인 항목 |
|---------|-----|---------|
| **Google** | https://search.google.com/search-console | URL 검사 & 색인 상태 |
| **Bing** | https://www.bing.com/webmasters | 사이트맵 & 크롤링 통계 |
| **Naver** | https://searchadvisor.naver.com | 크롤링 통계 & 수집 상태 |

### 로그 확인

```bash
# 최근 색인 통보 로그
tail -20 /tmp/indexnow.log

# 특정 엔진만
grep "BING\|NAVER\|GOOGLE" /tmp/indexnow.log
```

---

## 🐛 문제 해결

### IndexNow 키 오류

```
❌ IndexNow key file not found
```

**해결:** 키가 자동 생성되어야 합니다. 다음을 확인하세요:

```bash
ls -la tools/indexnow_key.txt
ls -la faa20d8a-1a2a-459a-bf1a-43c4f8a03d5f.txt
```

### Google API 오류

```
❌ Google API 라이브러리가 필요합니다
```

**해결:**

```bash
pip install google-auth requests
```

### Timeout 오류

```
⚠ BING: timed out
```

**해결:** 네트워크 연결 확인 및 다시 시도:

```bash
python3 tools/indexnow.py --sitemap-only  # Sitemap ping만 재시도
```

---

## 📚 참고 자료

- **IndexNow 공식**: https://www.indexnow.org/
- **Google Indexing API**: https://developers.google.com/search/apis/indexing-api
- **robots.txt 가이드**: https://developers.google.com/search/docs/crawling-indexing/robots/intro
- **Sitemap 프로토콜**: https://www.sitemaps.org/

---

## 🎯 모범 사례

### ✅ 효과적인 색인 전략

1. **첫 배포 후**: `python3 tools/indexnow.py` (모든 URL 한 번)
2. **정기 실행**: Cron으로 매일 Sitemap ping
3. **주요 업데이트**: 새 글 작성 직후 IndexNow 수동 실행
4. **모니터링**: Search Console에서 색인 상태 확인

### ⚡ 빠른 색인 팁

- Sitemap은 `robots.txt`에 자동 포함됨
- 각 페이지에 `<lastmod>` 시간 명시 (선택)
- 내부 링크 구조 최적화 (이미 완료)
- 사이트 속도 최적화 (문제 시)

---

**마지막 업데이트:** 2024년 6월  
**IndexNow 키:** faa20d8a-1a2a-459a-bf1a-43c4f8a03d5f
