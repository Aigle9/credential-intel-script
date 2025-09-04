
#!/usr/bin/env python3
"""
Info Breach Notifier

- Notifies teams when data breach indicators are detected or published.
- Produces a notification payload and optional channel hooks (prepared for webhooks).

Usage:
  python script_info_breach_notifier.py --breaches breaches.json --watchlist watch.json --output payload.json
"""

import argparse
import json
import logging
from datetime import datetime
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main(args: argparse.Namespace) -> None:
    breaches = load_json(args.breaches)  # list of breach indicators
    watch = load_json(args.watchlist) if args.watchlist else []

    # Simple payload: alert for each breach item with status if requested
    payloads = []
    now = datetime.utcnow().isoformat() + "Z"
    for b in breaches if isinstance(breaches, list) else []:
        indicator = b.get("indicator") if isinstance(b, dict) else None
        payload = {
            "generated_at": now,
            "type": "breach_alert",
            "indicator": indicator,
            "details": b,
            "watchlist_matches": []  # placeholder for future enrichment
        }
        payloads.append(payload)

    # Include watchlist hit signals if provided
    for w in watch:
        # optional enrichment; here we simply append as a separate payload if relevant
        payloads.append({
            "generated_at": now,
            "type": "watchlist_hit",
            "watch_item": w
        })

    out = {"notifications": payloads}

    out_path = args.output or "breach_notifications.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    logging.info("Breach notifier payload written to %s", out_path)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--breaches", required=True, help="Path to breaches JSON (array)")
    p.add_argument("--watchlist", help="Path to watchlist JSON (optional)")
    p.add_argument("--output", help="Output path for notification payload JSON")
    main(p.parse_args())