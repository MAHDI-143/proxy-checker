import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

TEST_URL = "http://httpbin.org/ip"
TIMEOUT  = 3
WORKERS  = 100
OUTPUT   = "proxies.txt"

SCHEME = {
    "http":   "http",
    "socks4": "socks4",
    "socks5": "socks5",
}


def _test(proxy: str, protocol: str) -> tuple[str, bool]:
    scheme = SCHEME.get(protocol, "http")
    proxy_url = f"{scheme}://{proxy}"
    try:
        response = requests.get(
            TEST_URL,
            proxies={"http": proxy_url, "https": proxy_url},
            timeout=TIMEOUT,
        )
        return proxy, response.status_code == 200
    except Exception:
        return proxy, False


def validate(proxies_by_protocol: dict[str, list[str]]) -> list[str]:
    alive = []
    for protocol, proxies in proxies_by_protocol.items():
        if not proxies:
            continue
        total = len(proxies)
        proto_alive = []
        print(f"\n[validator] Testing {total} {protocol.upper()} proxies...")
        with ThreadPoolExecutor(max_workers=WORKERS) as executor:
            futures = {executor.submit(_test, p, protocol): p for p in proxies}
            done = 0
            for future in as_completed(futures):
                proxy, is_alive = future.result()
                done += 1
                if is_alive:
                    proto_alive.append(proxy)
                    print(f"[{done}/{total}] OK {protocol} {proxy}")
        print(f"[validator] {protocol.upper()} alive: {len(proto_alive)} / {total}")
        alive.extend(proto_alive)
    alive = sorted(set(alive))
    print(f"\n[validator] Total alive (all protocols): {len(alive)}")
    return alive


def save(proxies: list[str], path: str = OUTPUT) -> None:
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    with open(path, "w") as f:
        f.write(f"# Proxy List — {now}\n")
        f.write(f"# Total   : {len(proxies)}\n")
        f.write("# " + "=" * 48 + "\n")
        for proxy in proxies:
            f.write(proxy + "\n")
    print(f"[validator] Saved {len(proxies)} live proxies -> {path}")
