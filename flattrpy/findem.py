

from pip.util import get_installed_distributions

for d in get_installed_distributions():
    for ln in d._get_metadata("PKG-INFO"):
        if ln.startswith("Home-page: "):
            home_page_url = ln.split(" ",1)[1].strip()
            if home_page_url == "UNKNOWN":
                home_page_url = None
            if home_page_url is not None:
                print home_page_url


