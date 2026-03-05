import argparse

from poly_market_maker.strategy import Strategy


def get_args(args) -> dict:
    parser = argparse.ArgumentParser(prog="poly-market-maker")

    parser.add_argument("--private-key", type=str, required=True, help="Private key")

    parser.add_argument("--rpc-url", type=str, required=True, help="RPC URL")

    parser.add_argument("--clob-api-url", type=str, required=True, help="CLOB API url")

    parser.add_argument(
        "--sync-interval",
        type=int,
        required=False,
        default=30,
        help="The number of seconds in between synchronizations",
    )

    parser.add_argument(
        "--min-size",
        type=float,
        required=False,
        default=15,
        help="The minimum size of a newly placed order",
    )

    parser.add_argument(
        "--min-tick",
        type=float,
        required=False,
        default=0.01,
        help="The distance between two successive prices",
    )

    parser.add_argument(
        "--refresh-frequency",
        type=int,
        default=5,
        help="Order book refresh frequency (in seconds, default: 5)",
    )

    parser.add_argument(
        "--gas-strategy",
        type=str,
        default="web3",
        help="Gas strategy to be used['fixed', 'station', 'web3']",
    )

    parser.add_argument("--gas-station-url", type=str, help="Gas station url")

    parser.add_argument(
        "--fixed-gas-price",
        type=int,
        help="Fixed gas price(gwei) to be used",
    )

    parser.add_argument(
        "--metrics-server-port",
        type=int,
        default=9008,
        help="The port where the process must start the metrics server",
    )

    parser.add_argument(
        "--condition-id",
        type=str,
        required=True,
        help="The condition id of the market being made",
    )

    parser.add_argument(
        "--strategy",
        type=Strategy,
        required=True,
        help="Market making strategy",
    )

    parser.add_argument(
        "--strategy-config",
        type=str,
        required=True,
        help="Strategy configuration file path",
    )

    return parser.parse_args(args)
