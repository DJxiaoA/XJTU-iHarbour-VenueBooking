"""
Project: GrabVenues
Author: Jiahui Wang
Copyright (c) 2026 Jiahui Wang
"""


class Config:
    def __init__(self):
        self.site = {
            "base_url": "http://example.com",
            "login_url": "http://example.com/login",
            "venue_url": "http://example.com/venue",
            "test_venue_url": "http://example.com/test",
            "user_agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
            ),
            "booking_open_time": {
                "hour": 8,
                "minute": 40,
                "second": 0,
                "millisecond": 200,
            },
            "headless": False,
            "run_immediately": False,
            "request_timeout_seconds": 10,
            "captcha_offset": 13,
            "notification_delay_range_seconds": [0, 180],
        }

        self.integrations = {
            "notion": {
                "token": "YOUR_NOTION_TOKEN",
                "booking_database_id": "YOUR_BOOKING_DATABASE_ID",
            }
        }

        self.profiles = {
            "main": {
                "username": "YOUR_STUDENT_ID",
                "password": "YOUR_PASSWORD",
                "record_name": "YOUR_NAME",
                "days_ahead": 2,
                "venue_target": "production",
                "priority_time_period": "19:01-20:00",
            },
        }

        self.profile_names = ["main"]

    def __getitem__(self, item):
        return getattr(self, item)

    def get(self, item, default=None):
        return getattr(self, item, default)
