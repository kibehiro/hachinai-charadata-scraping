from src.dump_json import DumpJson
from src.getpages import GetPages

ssr_url = 'https://www65.atwiki.jp/hachinai_nanj/pages/455.html'
ssr_get_pages = GetPages(ssr_url)
ssr_card = ssr_get_pages.main()
ssr_dump_json = DumpJson(ssr_card, 'SSR')
ssr_dump_json.main()

sr_url = 'https://www65.atwiki.jp/hachinai_nanj/pages/456.html'
sr_get_pages = GetPages(sr_url)
sr_card = sr_get_pages.main()
sr_dump_json = DumpJson(sr_card, 'SR')
sr_dump_json.main()


r_url = 'https://www65.atwiki.jp/hachinai_nanj/pages/457.html'
r_get_pages = GetPages(r_url)
r_card = r_get_pages.main()
r_dump_json = DumpJson(r_card, 'R')
r_dump_json.main()


n_url = 'https://www65.atwiki.jp/hachinai_nanj/pages/458.html'
n_get_pages = GetPages(n_url)
n_card = n_get_pages.main()
n_dump_json = DumpJson(n_card, 'N')
n_dump_json.main()
