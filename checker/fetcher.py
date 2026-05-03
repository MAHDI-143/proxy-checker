import requests

# ── Proxy Sources ─────────────────────────────────────────────────────────────
SOURCES = {
    "http": [
        "https://raw.githubusercontent.com/MAHDI-143/proxies/main/proxies.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
        "https://proxy-list.download/api/v1/get?type=http",
        "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/http/data.txt",
    ],
    "socks4": [
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
        "https://proxy-list.download/api/v1/get?type=socks4",
        "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt",
    ],
    "socks5": [
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",
        "https://proxy-list.download/api/v1/get?type=socks5",
        "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks5/data.txt",
    ],
}


def _parse(text: str) -> list[str]:
    result = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "://" in line:
            line = line.split("://", 1)[1]
        parts = line.split(":")
        if len(parts) == 2 and parts[1].isdigit():
            result.append(line)
    return result


def _fetch_url(url: str, protocol: str) -> list[str]:
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        proxies = _parse(r.text)
        print(f"[fetcher] {protocol:6s} | {len(proxies):>5} proxies <- {url}")
        return proxies
    except requests.RequestException as e:
        print(f"[fetcher] {protocol:6s} | FAILED <- {url} ({e})")
        return []


def get_all_proxies() -> dict[str, list[str]]:
    result = {}
    total = 0
    for protocol, urls in SOURCES.items():
        collected = []
        for url in urls:
            collected.extend(_fetch_url(url, protocol))
        unique = sorted(set(collected))
        result[protocol] = unique
        total += len(unique)
        print(f"[fetcher] {protocol:6s} | {len(unique)} unique proxies collected\n")
    print(f"[fetcher] Grand total: {total} unique proxies across all protocols")
    return result
