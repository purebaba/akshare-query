#!/usr/bin/env python3
"""基金数据查询工具 - ETF行情、基金排名、基金净值"""

from lib.formatter import to_markdown
import akshare as ak
import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def etf(args):
    df = ak.fund_etf_spot_em()
    print(to_markdown(df, limit=args.limit))


def rank(args):
    df = ak.fund_open_fund_rank_em(symbol=args.type)
    print(to_markdown(df, limit=args.limit))


def nav(args):
    if not args.code:
        print("错误: nav 命令需要 --code 参数", file=sys.stderr)
        sys.exit(1)
    df = ak.fund_open_fund_info_em(symbol=args.code, indicator="单位净值走势")
    print(to_markdown(df, limit=args.limit))


def main():
    parser = argparse.ArgumentParser(description="基金数据查询")
    subparsers = parser.add_subparsers(dest="command")

    p_etf = subparsers.add_parser("etf", help="ETF实时行情")
    p_etf.add_argument("--limit", type=int, default=50, help="返回行数限制")

    p_rank = subparsers.add_parser("rank", help="开放式基金排名")
    p_rank.add_argument("--type", default="全部",
                        help="基金类型: 全部/股票型/混合型/债券型/指数型/QDII")
    p_rank.add_argument("--limit", type=int, default=50, help="返回行数限制")

    p_nav = subparsers.add_parser("nav", help="基金净值")
    p_nav.add_argument("--code", required=True, help="基金代码，如 110011")
    p_nav.add_argument("--limit", type=int, default=50, help="返回行数限制")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        {"etf": etf, "rank": rank, "nav": nav}[args.command](args)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
