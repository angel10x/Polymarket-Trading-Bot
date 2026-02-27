"""Allow running the package with python -m polymarket_copy_trader."""

import argparse
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Polymarket copy trader")
    parser.add_argument(
        "--ui",
        action="store_true",
        help="Run with dashboard UI (task lines + logs)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to config.json (default: config.json in cwd)",
    )
    args = parser.parse_args()
    if args.ui:
        from ui.copy_trader_ui import main as ui_main
        ui_main(config_path=args.config)
    else:
        from polymarket_copy_trader.runner import main
        main(config_path=args.config)
