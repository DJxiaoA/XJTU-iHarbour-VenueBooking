"""
Project: VenueBooking
Author: Jiahui Wang
Copyright (c) 2026 Jiahui Wang
"""

import threading

from Config import Config
from funcs import run_profile


def make_profile_list(profile_names):
    """把 profile_names 统一整理成列表。"""
    if isinstance(profile_names, str):
        return [profile_names]
    return list(profile_names)


def main(config, profile_names=None, venue_target=None):
    """运行一个或多个服务端抢场 profile。"""
    profile_list = make_profile_list(profile_names or config.profile_names)

    if len(profile_list) == 1:
        run_profile(config, profile_list[0], venue_target)
        return

    errors = []
    threads = []

    def worker(profile_name):
        try:
            run_profile(config, profile_name, venue_target)
        except Exception as exc:
            errors.append(f"{profile_name}: {exc}")

    for profile_name in profile_list:
        thread = threading.Thread(target=worker, args=(profile_name,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if errors:
        text = "，".join(errors)
        raise RuntimeError(f"服务端有 profile 运行失败：{text}")


if __name__ == "__main__":
    config = Config()
    main(
        config=config,
        profile_names=None,
        venue_target=None,
    )
