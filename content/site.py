# 사이트 공통 설정
# 배포 도메인 확정 후 BASE_URL 을 실제 도메인으로 변경하세요.
BASE_URL = "https://www.barogo-gimpo.example.com"

BRAND = "바로 GO"
BRAND_MARK = "GO"
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# 김포시 메인(허브) 경로 — 루트(/)에서 바로 서빙.
HOME = "/"

# 80자 이내 사이트 디스크립션(상호·연락 포함)
SITE_DESC = "김포시 출장마사지·홈타이 방문 예약 안내. 구래·장기·운양·풍무·고촌 생활권 확인. 전화 0508-202-4719."

# 제작·제휴 문의 텔레그램 링크
TELEGRAM_URL = "https://t.me/googleseolab"

# 네이버 Search Advisor 인증 (HTML 메타 태그 방식)
NAVER_SITE_VERIFICATION = "89cdb73eae87756cee5d8b474b0d97b85f823c0a"

# 구글 Search Console 인증 (필요시)
GOOGLE_SITE_VERIFICATION = ""  # 구글에서 발급받은 코드 입력

# 상단 메뉴 — 하위 메뉴에는 "출장마사지"를 반복하지 않고 지역명·역명만 표시한다.
NAV = [
    ("김포 홈", HOME, []),
    ("지역별 안내", HOME + "#areas", [
        ("김포본동", "/gimpobon-dong/"),
        ("사우동", "/sau-dong/"),
        ("풍무동", "/pungmu-dong/"),
        ("장기본동", "/janggibon-dong/"),
        ("장기동", "/janggi-dong/"),
        ("운양동", "/unyang-dong/"),
        ("구래동", "/gurae-dong/"),
        ("마산동", "/masan-dong/"),
        ("고촌읍", "/gochon-eup/"),
        ("양촌읍", "/yangchon-eup/"),
        ("통진읍", "/tongjin-eup/"),
        ("대곶면", "/daegot-myeon/"),
        ("월곶면", "/wolgot-myeon/"),
        ("하성면", "/haseong-myeon/"),
    ]),
    ("역세권 안내", "/station/", [
        ("역 전체", "/station/"),
        ("고촌역", "/station/gochon-station/"),
        ("풍무역", "/station/pungmu-station/"),
        ("사우역", "/station/sau-station/"),
        ("장기역", "/station/janggi-station/"),
        ("운양역", "/station/unyang-station/"),
        ("구래역", "/station/gurae-station/"),
        ("마산역", "/station/masan-station/"),
        ("양촌역", "/station/yangchon-station/"),
        ("김포공항 인접", "/station/gimpo-airport-nearby-area/"),
    ]),
    ("생활권 안내", "/area/", [
        ("생활권 전체", "/area/"),
        ("김포한강신도시", "/area/hangang-newtown/"),
        ("구래·마산", "/area/gurae-masan/"),
        ("장기·운양", "/area/janggi-unyang/"),
        ("사우·김포시청", "/area/sau-cityhall/"),
        ("풍무·고촌", "/area/pungmu-gochon/"),
        ("고촌·아라뱃길", "/area/gochon-ara-waterway/"),
        ("양촌·학운산단", "/area/yangchon-hagun-industrial/"),
        ("통진·마송", "/area/tongjin-masong/"),
        ("대곶·산업단지", "/area/daegot-industrial/"),
        ("월곶·문수산", "/area/wolgot-munsusan/"),
        ("하성·북부김포", "/area/haseong-north-gimpo/"),
        ("김포공항·서울 인접", "/area/gimpo-airport-seoul-nearby/"),
    ]),
    ("테마별 안내", "/themes/", [
        ("전체 테마", "/themes/"),
        ("스웨디시", "/themes/swedish/"),
        ("로미로미", "/themes/lomilomi/"),
        ("타이마사지", "/themes/thai/"),
        ("중국마사지", "/themes/chinese/"),
        ("아로마테라피", "/themes/aroma/"),
        ("홈케어", "/themes/homecare/"),
        ("호텔식마사지", "/themes/hotel-style/"),
        ("발마사지", "/themes/foot/"),
        ("스포츠·경락", "/themes/sports/"),
        ("스킨케어", "/themes/skincare/"),
        ("왁싱", "/themes/waxing/"),
        ("커플 관리", "/themes/couple/"),
        ("24시간", "/themes/24hours/"),
        ("수면 가능", "/themes/overnight/"),
    ]),
    ("코스안내", "/courses/", [
        ("전체 코스", "/courses/"),
        ("피로 회복 관리", "/courses/#recovery"),
        ("아로마 관리", "/courses/#aroma"),
        ("스포츠 관리", "/courses/#sports"),
        ("홈타이 코스", "/courses/#hometai"),
        ("커플·가족 방문 관리", "/courses/#couple"),
        ("기업·단체 방문 관리", "/courses/#group"),
        ("가격 안내", "/courses/#price"),
        ("코스 선택 가이드", "/courses/#guide"),
    ]),
    ("예약안내", "/reservation/", [
        ("예약 방법", "/reservation/#how"),
        ("예약 가능 시간", "/reservation/#hours"),
        ("방문 가능 장소", "/reservation/#place"),
        ("결제 안내", "/reservation/#payment"),
        ("변경·취소 안내", "/reservation/#change"),
        ("예약 전 체크사항", "/reservation/#check"),
    ]),
    ("이용가이드", "/guide/", [
        ("처음 이용하시는 분", "/guide/#first"),
        ("방문 전 준비사항", "/guide/#prepare"),
        ("위생 및 안전 기준", "/guide/#hygiene"),
        ("관리 후 주의사항", "/guide/#after"),
        ("금지행위 안내", "/guide/#prohibited"),
        ("이용 FAQ", "/guide/#faq"),
    ]),
    ("매거진", "/magazine/", [
        ("전체 글", "/magazine/"),
        ("마사지 비교 가이드", "/magazine/swedish-vs-thai/"),
        ("처음 이용 가이드", "/magazine/first-time-guide/"),
        ("수면과 마사지", "/magazine/sleep-and-massage/"),
        ("운동 후 회복", "/magazine/post-workout-timing/"),
        ("어깨·목 결림 관리", "/magazine/neck-shoulder-care/"),
        ("부모님 선물 가이드", "/magazine/parents-gift/"),
    ]),
    ("후기", "/reviews/", [
        ("전체 후기", "/reviews/"),
        ("지역별 후기", "/reviews/#area"),
        ("역세권 후기", "/reviews/#station"),
        ("후기 작성 안내", "/reviews/#write"),
    ]),
    ("고객센터", "/support/", [
        ("공지사항", "/support/#notice"),
        ("자주 묻는 질문", "/support/#faq"),
        ("1:1 문의", "/support/#contact"),
        ("제휴·기업 문의", "/support/#biz"),
        ("개인정보처리방침", "/support/privacy/"),
        ("이용약관", "/support/terms/"),
    ]),
]
