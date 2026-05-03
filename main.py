from checker.fetcher import get_all_proxies
from checker.validator import validate, save


def run():
    print("=" * 52)
    print("  Proxy Checker — GitHub Actions Edition")
    print("=" * 52)

    proxies_by_protocol = get_all_proxies()

    total = sum(len(v) for v in proxies_by_protocol.values())
    if total == 0:
        print("[main] No proxies found. Exiting.")
        return

    alive = validate(proxies_by_protocol)
    save(alive)

    print("\n[main] Done.")


if __name__ == "__main__":
    run()
