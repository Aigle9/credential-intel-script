
#!/usr/bin/env python3
"""
Credential Bruteforce Detector

- Detects credential stuffing and brute-force attempts from auth logs.
- Flags potential incidents and computes rate metrics.

Usage:
  python script_credentials_bruteforce_detector.py --logs logs.json --output incidents.json --config config.json
"""

import argparse
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def windowed_counts(events: List[Dict[str, Any]], window_min: int) -> List[Dict[str, Any]]:
    # Simple per-minute aggregation
    window = {}
    for e in events:
        ts = e.get("ts")
        if ts is None:
            continue
        # assume ts is ISO 8601 string; parse if needed
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except Exception:
            continue
        minute = dt.replace(second=0, microsecond=0)
        key = minute.isoformat()
        window[key] = window.get(key, 0) + 1
    return [{"minute": k, "count": v} for k, v in sorted(window.items())]

def main(args: argparse.Namespace) -> None:
    logs = load_json(args.logs)
    # Expect logs as a list of events with fields: type, action, outcome, ip, user, ts
    if not isinstance(logs, list):
        logging.error("Logs should be a list of events.")
        return

    failed_login_events = []
    for e in logs:
        if not isinstance(e, dict):
            continue
        action = str(e.get("action", "")).lower()
        outcome = str(e.get("outcome", "")).lower()
        if "login" in action and outcome in {"fail", "failed", "denied"}:
            failed_login_events.append(e)

    # Simple threshold-based detection per source IP
    ip_counts = {}
    for e in failed_login_events:
        ip = e.get("ip")
        if ip:
            ip_counts[ip] = ip_counts.get(ip, 0) + 1

    threshold = int((args.threshold or 50))
    incidents = []
    for ip, count in ip_counts.items():
        if count >= threshold:
            incidents.append({"ip": ip, "failed_attempts": count})

    # Optional per-minute rate report
    per_min = windowed_counts(failed_login_events, window_min=1)

    report = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "threshold": threshold,
        "incidents": incidents,
        "per_minute": per_min
    }

    out_path = args.output or "credentials_bruteforce_incidents.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    logging.info("Bruteforce report written to %s", out_path)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--logs", required=True, help="Path to authentication logs (JSON)")
    p.add_argument("--output", help="Output path for incidents JSON")
    p.add_argument("--config", help="Optional config path")
    p.add_argument("--threshold", help="Threshold of failed attempts per IP to trigger an incident")
    main(p.parse_args())