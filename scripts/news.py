#!/usr/bin/env python3
"""新闻数据查询工具 - 个股新闻资讯"""

from lib.formatter import to_markdown
import akshare as ak
import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def main():
    parser = argparse.ArgumentParser(description="个股新闻查询")
    parser.add_argument("--symbol", required=True, help="股票代码，如 000001")
    parser.add_argument("--limit", type=int, default=10, help="返回条数限制")

    args = parser.parse_args()

    try:
        df = ak.stock_news_em(symbol=args.symbol)
        if "content" in df.columns:
            df = df.drop(columns=["content"])
        print(to_markdown(df, limit=args.limit))
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
