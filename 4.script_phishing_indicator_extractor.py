
#!/usr/bin/env python3
"""
Phishing Indicator Extractor

- Extracts phishing indicators from emails, links, and payloads.
- Produces IOC lists with confidence scores.

Usage:
  python script_phishing_indicator_extractor.py --emails emails.json --output iocs.json
"""

import argparse
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
import re
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

URL_PATTERN = re.compile(r"https?://[^\s]+", re.IGNORECASE)

def extract_domains(urls: List[str]) -> List[str]:
    domains = []
    for u in urls:
        try:
            p = urlparse(u)
            if p.netloc:
                domains.append(p.netloc)
        except Exception:
            continue
    return list(dict.fromkeys(domains))

def extract_iocs_from_email(email: Dict[str, Any]) -> List[Dict[str, Any]]:
    iocs: List[Dict[str, Any]] = []
    subject = str(email.get("subject", "")).lower()
    body = str(email.get("body", "")).lower()
    text = subject + " " + body

    # Simple indicators
    if "login" in text or "verify" in text:
        iocs.append({"type": "subject_keyword", "value": "login|verify", "confidence": 0.5})

    # URLs in body
    urls = URL_PATTERN.findall(body)
    for u in urls:
        iocs.append({"type": "url", "value": u, "confidence": 0.9})

    # Domains in URLs
    domains = extract_domains(urls)
    for d in domains:
        iocs.append({"type": "domain", "value": d, "confidence": 0.8})

    return iocs

def main(args: argparse.Namespace) -> None:
    emails = []
    with open(args.emails, "r", encoding="utf-8") as f:
        emails = json.load(f)

    iocs: List[Dict[str, Any]] = []
    for em in emails:
        iocs.extend(extract_iocs_from_email(em))

    # Deduplicate by (type, value)
    seen = set()
    unique_iocs = []
    for item in iocs:
        key = (item.get("type"), item.get("value"))
        if key not in seen:
            seen.add(key)
            unique_iocs.append(item)

    report = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "iocs": unique_iocs
    }

    out_path = args.output or "phishing_iocs.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    logging.info("Phishing IOC report written to %s", out_path)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--emails", required=True, help="Path to emails JSON (array of objects)")
    p.add_argument("--output", help="Output path for IOCs JSON")
    main(p.parse_args())