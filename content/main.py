# 김포시 메인(허브) 페이지 — 경로 /gyeonggi/gimpo/.
# 모든 키워드를 밀어 넣지 않고 대표 지역·역세권·생활권 상세 페이지로 연결한다.
from .site import BASE_URL, BRAND, HOME, PHONE, PHONE_DISPLAY
from .pricing import PRICING

_CANON = BASE_URL.rstrip("/") + HOME

_JSONLD = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{BRAND}",
  "url": "{_CANON}",
  "telephone": "{PHONE}",
  "image": "{BASE_URL.rstrip('/')}/assets/og-image.png",
  "description": "경기도 김포시 전지역 방문 출장마사지·홈타이 예약 안내",
  "areaServed": {{
    "@type": "AdministrativeArea",
    "name": "경기도 김포시"
  }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "김포시 출장마사지 · 김포시 홈타이 지역별 예약 안내",
  "url": "{_CANON}",
  "inLanguage": "ko-KR",
  "primaryImageOfPage": {{
    "@type": "ImageObject",
    "url": "{BASE_URL.rstrip('/')}/assets/og-image.png",
    "width": 1200,
    "height": 630
  }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "홈", "item": "{BASE_URL.rstrip('/')}/"}},
    {{"@type": "ListItem", "position": 2, "name": "김포시", "item": "{_CANON}"}}
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "김포시 전지역 방문이 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "예약 시간, 정확한 위치, 배정 상황에 따라 달라집니다. 구래동, 장기동, 운양동, 풍무동, 고촌읍 등 대표 지역 안내 페이지에서 생활권별 방문 조건을 확인할 수 있습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "통진읍·대곶면·월곶면·하성면처럼 외곽 지역도 되나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "차량 이동 기준이 중요한 북부·외곽 생활권은 예약 가능 시간과 추가 이동비를 각 지역 페이지에서 안내합니다. 방문 가능 여부는 주소 기준으로 확인합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "김포공항 근처도 방문되나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "김포공항 자체는 서울 강서구 생활권이므로, 김포 사이트에서는 고촌읍·풍무동 인접 생활권 기준으로 안내합니다."
      }}
    }}
  ]
}}
</script>
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">Premium Visiting Spa · 경기도 김포시 전지역</p>
    <h1>김포시 출장마사지·홈타이<br>지역별 예약 안내</h1>
    <p class="hero-lead">샵까지 갈 필요 없이, 계신 곳에서 받는 프리미엄 방문 관리.<br>자택·오피스텔·숙소 어디든 전화 한 통이면 예약이 끝납니다.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/courses/">코스 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>14개</strong><span>대표 지역</span></li>
      <li><strong>9개</strong><span>역세권 안내</span></li>
      <li><strong>12개</strong><span>생활권 안내</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""

_BODY = f"""
<section id="intro">
<h2>김포시에서 출장마사지를 찾을 때 먼저 확인할 기준</h2>
<p>김포시 출장마사지를 찾는 분들은 보통 현재 위치에서 가까운 방문 가능 지역을 먼저 확인합니다. 김포시는 김포한강신도시, 구래·마산 생활권, 장기·운양 생활권, 풍무·고촌 생활권, 사우·김포본동 원도심, 통진·양촌·대곶 북부 생활권이 함께 있는 지역입니다. 그래서 {BRAND}는 "김포 전지역 가능"만 반복하기보다 대표 지역과 역세권, 생활권을 나누어 안내하는 구조로 만들었습니다. 더 자세한 내용은 지역별·역세권·생활권 안내 페이지에서 확인하실 수 있고, 이 페이지는 김포시 전체 구조를 설명하는 허브 역할을 합니다.</p>
</section>

<section id="zones">
<h2>구래·마산·장기·운양·풍무 생활권 차이</h2>
<p>김포시 홈타이를 안내할 때 중요한 부분은 생활권을 무리하게 쪼개지 않는 것입니다. 김포시는 동 지역과 읍·면 지역의 성격 차이가 큽니다. <a href="/gurae-dong/">구래동 출장마사지</a>, 마산동, 장기동, 운양동은 김포한강신도시 검색 의도와 연결되고, 고촌읍과 풍무동은 서울 강서·김포공항 인접 생활권과 연결됩니다. 통진읍, 양촌읍, 대곶면, 월곶면, 하성면은 차량 이동 기준이 중요한 지역입니다. 생활권별 차이가 궁금하다면 <a href="/area/hangang-newtown/">김포한강신도시 생활권 안내</a>와 <a href="/area/gurae-masan/">구래·마산 생활권 안내</a>를 함께 확인해 보세요.</p>
</section>

<section id="areas">
<h2>대표 지역별 방문 가능 지역 안내</h2>
<p>대표 지역은 김포본동, 사우동, 풍무동, 장기본동, 장기동, 운양동, 구래동, 마산동, 고촌읍, 양촌읍, 통진읍, 대곶면, 월곶면, 하성면으로 구성합니다. 구래동은 구래역과 김포한강신도시 중심상권을, 마산동은 마산역과 양촌읍 인접권을, 장기동·장기본동은 장기역과 한강신도시 생활권을, 운양동은 운양역과 한강변 주거지를 중심으로 안내합니다. 아래에서 거주하시거나 머무시는 동을 선택해 주세요.</p>
<ul class="card-grid">
<li><a href="/gimpobon-dong/">김포본동</a></li>
<li><a href="/sau-dong/">사우동</a></li>
<li><a href="/pungmu-dong/">풍무동</a></li>
<li><a href="/janggibon-dong/">장기본동</a></li>
<li><a href="/janggi-dong/">장기동</a></li>
<li><a href="/unyang-dong/">운양동</a></li>
<li><a href="/gurae-dong/">구래동</a></li>
<li><a href="/masan-dong/">마산동</a></li>
<li><a href="/gochon-eup/">고촌읍</a></li>
<li><a href="/yangchon-eup/">양촌읍</a></li>
<li><a href="/tongjin-eup/">통진읍</a></li>
<li><a href="/daegot-myeon/">대곶면</a></li>
<li><a href="/wolgot-myeon/">월곶면</a></li>
<li><a href="/haseong-myeon/">하성면</a></li>
</ul>
<p>김포시의 행정 구역 구성은 <a href="https://www.gimpo.go.kr/" target="_blank" rel="noopener nofollow">김포시청 공식 누리집</a>에서도 확인할 수 있습니다. 방문 가능 여부는 행정동 경계가 아니라 실제 주소와 예약 시간으로 판단합니다.</p>
</section>

<section id="stations">
<h2>고촌역·풍무역·사우역·구래역 역세권 안내</h2>
<p>역세권 페이지는 김포시 지역 안내에서 중요한 역할을 합니다. 김포골드라인을 따라 <a href="/station/gochon-station/">고촌역</a>, <a href="/station/pungmu-station/">풍무역</a>, <a href="/station/sau-station/">사우역</a>, <a href="/station/janggi-station/">장기역</a>, <a href="/station/unyang-station/">운양역</a>, <a href="/station/gurae-station/">구래역</a>, <a href="/station/masan-station/">마산역</a>, <a href="/station/yangchon-station/">양촌역</a>까지 실제 검색 의도와 가까운 기준으로 안내합니다. 김포공항역은 서울 강서구 성격이 강하므로 <a href="/station/gimpo-airport-nearby-area/">김포공항 인접 생활권</a>으로만 다루고, 검단역·계양역은 인천 성격이 강해 김포 핵심 역세권으로 만들지 않습니다. 김포골드라인 역은 역명 기준 1개 페이지만 운영합니다. 전체 목록은 <a href="/station/">역세권 안내</a>에서 확인하세요.</p>
</section>

<section id="check">
<h2>김포시 홈타이 예약 전 확인사항</h2>
<p>김포시 출장마사지·홈타이 예약 전에는 방문 가능 지역, 예약 가능 시간, 추가 이동비, 결제 방식, 취소 기준, 개인정보 처리 기준을 먼저 확인하시는 것이 좋습니다. 구래동·장기동처럼 접근성이 좋은 신도시 지역도 있지만, 통진읍·대곶면·월곶면·하성면 일부는 시간대에 따라 차량 이동 기준이 달라질 수 있습니다. 자세한 절차는 <a href="/reservation/">예약안내</a>에서, 방문 전 준비사항은 <a href="/guide/">이용가이드</a>에서 확인하실 수 있습니다. 김포시 홈타이는 자택·숙소·사무실 인근에서 예약 가능 여부를 확인한 뒤 이용하는 방문형 관리 서비스입니다.</p>
</section>

<section id="dedup">
<h2>김포시 페이지 중복 방지 운영 기준</h2>
<p>{BRAND}는 같은 본문에서 지역명만 바꾸는 방식을 쓰지 않습니다. 장기동과 장기본동, 구래동과 구래역, 고촌읍과 김포공항 인접 생활권, 양촌읍과 양촌역은 각각 역할을 나누어 작성합니다. 동 페이지는 상권·주거 생활권을, 역 페이지는 역세권 이동 기준과 예약 전 확인사항을 담당합니다. 생활권 페이지는 여러 지역을 함께 비교하는 보조 허브로 운영합니다. 메뉴명과 URL에는 "출장마사지"를 반복하지 않고, 키워드는 제목과 첫 문단에서만 자연스럽게 사용합니다.</p>
</section>

<section id="how">
<h2>김포시 출장마사지 사이트 이용 방법</h2>
<p>김포시 메인페이지는 김포 전체 안내를 담당하고, 대표 지역 페이지는 구래동·마산동·장기동·운양동·풍무동·고촌읍 같은 세부 검색을 담당합니다. 역세권 페이지는 고촌역·풍무역·사우역·구래역처럼 실제 검색 수요가 생기는 키워드를, 생활권 페이지는 김포한강신도시·구래·마산·장기·운양·풍무·고촌처럼 위치를 더 쉽게 찾도록 돕는 안내를 담당합니다. 원하시는 관리 유형은 <a href="/themes/">테마별 안내</a>에서 고르고, 시간 구성은 <a href="/courses/">코스안내</a>에서 확인하신 뒤 예약 시 위치를 알려주시면 됩니다.</p>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>김포시 방문 관리 예약과 상담은 전화로 가장 빠르게 진행됩니다. 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "김포시 출장마사지｜구래·장기·운양·풍무 홈타이 지역 안내",
    "desc": "김포시 출장마사지·홈타이 예약 전 구래동, 장기동, 운양동, 풍무동, 고촌읍 생활권을 확인하세요.",
    "h1": "김포시 출장마사지 · 김포시 홈타이 지역별 예약 안내",
    "body": _BODY,
    "extra_head": _JSONLD,
    "breadcrumb": [],
    "hero": _HERO,
}
