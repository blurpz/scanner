#!/usr/bin/env python3

import argparse
import os
import re
import sys
import time
import json
import random
from urllib.request import Request, urlopen
from urllib.parse import urlparse

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
RETRIES = 5
TIMEOUT = 90          

PUBLIC_SUFFIXES = {
    "edu.ph", "gov.ph", "com.ph", "org.ph", "net.ph", "mil.ph",
    "co.uk", "org.uk", "ac.uk", "gov.uk", "me.uk",
    "com.au", "net.au", "org.au", "edu.au",
    "co.nz", "co.in", "co.jp", "com.br", "com.sg",
}

def http_get(url, timeout=TIMEOUT):
    req = Request(url, headers={
        "User-Agent": UA,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="ignore")

def http_get_retry(url, timeout=TIMEOUT):
    last_err = None
    for attempt in range(1, RETRIES + 1):
        try:
            return http_get(url, timeout)
        except Exception as e:
            last_err = e
       
            wait = (10 * (2 ** (attempt - 1))) * random.uniform(0.7, 1.3)
            print(f"    [!] attempt {attempt}/{RETRIES} failed: {e} - retrying in {wait:.0f}s")
            time.sleep(wait)
    print(f"    [!] giving up after {RETRIES} attempts: {last_err}")
    return None

def extract_domain(line):
   
    line = line.strip()
    if not line:
        return None
    if "://" not in line:
        line = "http://" + line
    try:
        host = urlparse(line).hostname
    except ValueError:
        return None
    if not host:
        return None
    host = host.lower().strip(".").lstrip("www.") if host.startswith("www.") else host.lower().strip(".")
    # discard IPs and anything that isn't a normal domain
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host) or ":" in host:
        return None
    parts = host.split(".")
    if len(parts) < 2:
        return None
    suffix = ".".join(parts[-2:])
    if suffix in PUBLIC_SUFFIXES:
        if len(parts) > 3:
            host = ".".join(parts[-3:])   
        elif len(parts) == 3:
            host = host                    
        else:
            return None                    
    else:
        host = ".".join(parts[-2:])       
  
    if ".".join(host.split(".")[-2:]) in PUBLIC_SUFFIXES:
        return None
    return host

def is_valid_sub(sub, domain):
    sub = sub.lower().strip(".").lstrip("*.")
    return (sub.endswith("." + domain) or sub == domain) and " " not in sub

def fetch_crtsh(domain):
    subs = set()
    body = http_get_retry(f"https://crt.sh/?q=%25.{domain}&output=json")
    if body:
        try:
            for entry in json.loads(body):
                for n in entry.get("name_value", "").split("\n"):
                    n = n.strip().lower()
                    if is_valid_sub(n, domain):
                        subs.add(n.lstrip("*."))
        except (json.JSONDecodeError, ValueError):
            print("    [!] crt.sh returned invalid JSON (often happens under load)")
    return subs

def fetch_hackertarget(domain):
    subs = set()
    body = http_get_retry(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=30)
    if body:
        low = body.strip().lower()
        if "error" in low[:60] or "limit" in low[:60]:
            print(f"    [!] hackertarget: {body.strip()[:80]}")
        else:
            for line in body.splitlines():
                host = line.split(",")[0].strip().lower()
                if is_valid_sub(host, domain):
                    subs.add(host)
    return subs

def fetch_rapiddns(domain):
    subs = set()
    body = http_get_retry(f"https://rapiddns.io/subdomain/{domain}?full=1", timeout=40)
    if body:
        found = re.findall(r">\s*([a-zA-Z0-9_.-]+\.%s)\s*<" % re.escape(domain), body)
        subs.update(f.lower().lstrip("*.") for f in found if is_valid_sub(f, domain))
    return subs

def fetch_otx(domain):

    time.sleep(10)  
    subs = set()
    body = http_get_retry(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns")
    if body:
        try:
            for e in json.loads(body).get("passive_dns", []):
                host = e.get("hostname", "").lower()
                if is_valid_sub(host, domain):
                    subs.add(host)
        except (json.JSONDecodeError, ValueError):
            pass
    return subs

def sanitize_filename(name):
    return re.sub(r"[^a-zA-Z0-9._-]", "_", name)

def gather(domain):
    print(f"[*] Scanning {domain} ...")
    all_subs = set()
    sources = [
        ("crt.sh", fetch_crtsh),
        ("rapiddns", fetch_rapiddns),
        ("hackertarget", fetch_hackertarget),
        ("otx", fetch_otx),
    ]
    for name, fn in sources:
        result = fn(domain)
        print(f"    [{name}] {len(result)} found")
        all_subs |= result
    all_subs = {s for s in all_subs if is_valid_sub(s, domain)}
    print(f"  [+] Total {len(all_subs)} subdomains for {domain}")
    return sorted(all_subs)

def main():
    ap = argparse.ArgumentParser(description="Passive subdomain enumerator")
    ap.add_argument("input", help="File containing one domain or URL per line")
    ap.add_argument("-o", "--outdir", default="results", help="Output directory")
    args = ap.parse_args()

    try:
        with open(args.input, encoding="utf-8", errors="ignore") as f:
            raw_lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    except FileNotFoundError:
        sys.exit(f"[!] Input file not found: {args.input}")

    domains, seen, skipped = [], set(), []
    for line in raw_lines:
        d = extract_domain(line)
        if d and d not in seen:
            seen.add(d)
            domains.append(d)
        elif d is None:
            skipped.append(line)
    if not domains:
        sys.exit("[!] No valid domains found in input file.")
    if skipped:
        print(f"[*] Skipping {len(skipped)} invalid/suffix-only lines (e.g. {skipped[:3]})")
    print(f"[*] {len(domains)} unique base domains to scan")

    os.makedirs(args.outdir, exist_ok=True)

    for d in domains:
        subs = gather(d)
        if subs:
            out_path = os.path.join(args.outdir, sanitize_filename(d) + ".txt")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write("\n".join(subs) + "\n")
            print(f"  [+] Saved to {out_path}")
        else:
            print(f"  [-] No subdomains found for {d}")
        time.sleep(2)

    print("[*] Done.")

if __name__ == "__main__":
    main()
