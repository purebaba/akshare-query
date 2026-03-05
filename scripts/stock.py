#!/usr/bin/env python3
"""A股数据查询工具 - 实时行情、历史K线、个股信息"""

from lib.formatter import to_markdown
import akshare as ak
import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def quotes(args):
    df = ak.stock_zh_a_spot_em()
    if args.symbol:
        df = df[df["代码"] == args.symbol]
        if df.empty:
            print(f"未找到股票代码: {args.symbol}", file=sys.stderr)
            sys.exit(1)
    print(to_markdown(df, limit=args.limit))


def hist(args):
    if not args.symbol:
        print("错误: hist 命令需要 --symbol 参数", file=sys.stderr)
        sys.exit(1)
    df = ak.stock_zh_a_hist(
        symbol=args.symbol,
        period=args.period,
        start_date=args.start,
        end_date=args.end,
        adjust=args.adjust,
    )
    print(to_markdown(df, limit=args.limit))


def info(args):
    if not args.symbol:
        print("错误: info 命令需要 --symbol 参数", file=sys.stderr)
        sys.exit(1)
    df = ak.stock_individual_info_em(symbol=args.symbol)
    print(to_markdown(df, limit=None))


def main():
    parser = argparse.ArgumentParser(description="A股数据查询")
    subparsers = parser.add_subparsers(dest="command")

    p_quotes = subparsers.add_parser("quotes", help="实时行情")
    p_quotes.add_argument("--symbol", help="股票代码，如 000001")
    p_quotes.add_argument("--limit", type=int, default=50, help="返回行数限制")

    p_hist = subparsers.add_parser("hist", help="历史K线")
    p_hist.add_argument("--symbol", required=True, help="股票代码")
    p_hist.add_argument("--period", default="daily",
                        choices=["daily", "weekly", "monthly"], help="K线周期")
    p_hist.add_argument("--start", default="20240101", help="开始日期 YYYYMMDD")
    p_hist.add_argument("--end", default="20991231", help="结束日期 YYYYMMDD")
    p_hist.add_argument("--adjust", default="qfq",
                        choices=["qfq", "hfq", ""], help="复权方式")
    p_hist.add_argument("--limit", type=int, default=50, help="返回行数限制")

    p_info = subparsers.add_parser("info", help="个股基本信息")
    p_info.add_argument("--symbol", required=True, help="股票代码")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        {"quotes": quotes, "hist": hist, "info": info}[args.command](args)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
