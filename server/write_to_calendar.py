"""
Project: GrabVenues
Author: Jiahui Wang
Copyright (c) 2026 Jiahui Wang
"""

from Config import Config
from funcs import run_calendar_sync


def main(config, days_ahead=None, archive_days_before=None):
    """执行一次服务端日历聚合。"""
    run_calendar_sync(config, days_ahead, archive_days_before)


if __name__ == "__main__":
    config = Config()
    main(config=config, days_ahead=None, archive_days_before=None)
