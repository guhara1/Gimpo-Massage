# 전체 페이지 목록 집계
from . import main, areas, stations, livingzones, themes, info, magazine, about

PAGES = (
    [main.PAGE]
    + areas.PAGES
    + stations.PAGES
    + livingzones.PAGES
    + themes.PAGES
    + info.PAGES
    + magazine.PAGES
    + [about.PAGE]
)
