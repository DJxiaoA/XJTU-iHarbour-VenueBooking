# GrabVenues

西安交通大学 创新港巨构 羽毛球场地预约

## 作者

Jiahui Wang

## 说明 

本项目仅供学习与交流使用。 如需参考、修改或二次开发，请保留原作者信息。

## 项目简介

本项目包含两部分能力：

1. 登录体育场馆系统并抢场
2. 将 booking 数据库中的预约记录聚合写入 calendar 数据库

项目主入口：

- `main.py`：执行抢场流程
- `write_to_calendar.py`：执行 booking 到 calendar 的聚合流程
- `start_server.bat`：Windows 一键串联执行脚本

## 目录说明

- `Config.py`：统一配置文件
- `funcs.py`：抢场与日历聚合实现
- `main.py`：抢场入口
- `write_to_calendar.py`：日历聚合入口
- `start_server.bat`：Windows 启动脚本

## 运行前准备

1. 安装 Python，建议 3.10 或更高版本。
2. 安装 Google Chrome。
3. 安装依赖：

```bash
pip install selenium requests beautifulsoup4 lxml ddddocr pillow notion-client
```

4. 确保 Selenium 可以正常启动 Chrome。

## 如何配置登录信息

打开 `Config.py`，找到：

```python
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
```

至少需要修改以下字段：

- `username`：登录学号
- `password`：登录密码
- `record_name`：写入 booking 数据库时使用的姓名
- `priority_time_period`：目标预约时段

常用字段说明：

- `days_ahead`：预约几天后的场地
- `venue_target`：`production` 为正式场地，`test` 为测试场地

## 如何配置同时预约的账号数

抢场流程会对 `self.profile_names` 中列出的 profile 并发执行。

单账号运行保持默认即可：

```python
self.profile_names = ["main"]
```

多账号并发示例：

```python
self.profiles = {
    "main": {
        "username": "2023000001",
        "password": "PASSWORD_1",
        "record_name": "张三",
        "days_ahead": 2,
        "venue_target": "production",
        "priority_time_period": "19:01-20:00",
    },
    "main2": {
        "username": "2023000002",
        "password": "PASSWORD_2",
        "record_name": "李四",
        "days_ahead": 2,
        "venue_target": "production",
        "priority_time_period": "20:01-21:00",
    },
}

self.profile_names = ["main", "main2"]
```

并发账号数等于 `self.profile_names` 的数量。

## 预约与聚合配置

### 站点配置

`self.site` 可调整以下字段：

- `venue_url`：正式场地页面
- `test_venue_url`：测试场地页面
- `booking_open_time`：放号时间
- `headless`：是否无界面运行
- `run_immediately`：是否启动后立即执行
- `request_timeout_seconds`：HTTP 请求超时
- `captcha_offset`：滑块距离补偿值
- `notification_delay_range_seconds`：写入 booking 数据库前的随机等待时间

### Notion 配置

```python
self.integrations = {
    "notion": {
        "token": "YOUR_NOTION_TOKEN",
        "booking_database_id": "YOUR_BOOKING_DATABASE_ID",
        "calendar_database_id": "YOUR_CALENDAR_DATABASE_ID",
    },
    "pushplus": {
        "token": "YOUR_PUSHPLUS_TOKEN",
        "topic": "YOUR_PUSHPLUS_TOPIC",
    },
}
```

字段说明：

- `booking_database_id`：预约结果写入的 booking 数据库
- `calendar_database_id`：聚合后的日历数据库
- `pushplus.token`：PushPlus 推送 token，不需要推送可自行留空
- `pushplus.topic`：PushPlus 主题，可按需填写

### 日历聚合配置

```python
self.calendar_sync = {
    "days_ahead": 2,
    "archive_days_before": 10,
}
```

字段说明：

- `days_ahead`：聚合哪一天的 booking 记录
- `archive_days_before`：归档多少天前的旧 booking 记录

## .bat 脚本如何配置

打开 `start_server.bat`：

```bat
@echo off
setlocal
cd /d "%~dp0"
set "PYTHON_EXE=python"
set "WAIT_SECONDS=180"
"%PYTHON_EXE%" main.py
timeout /t %WAIT_SECONDS% /nobreak
"%PYTHON_EXE%" write_to_calendar.py
```

可修改项：

- `PYTHON_EXE=python`：如果 Python 已加入环境变量，保持默认即可
- 如果没有加入环境变量，把它改成完整路径，例如：

```bat
set "PYTHON_EXE=D:\Python311\python.exe"
```

- `WAIT_SECONDS=180`：抢场结束后等待多少秒再执行日历聚合

双击 `start_server.bat` 后，脚本会先执行抢场，再等待，再执行聚合。

## 运行方式

只运行抢场：

```bash
python main.py
```

只运行日历聚合：

```bash
python write_to_calendar.py
```

Windows 双击运行：

- `start_server.bat`

## 日志

抢场日志：

```text
logs/YYYY-MM-DD/main.log
```

如果配置了多个 profile，会分别生成对应名称的日志文件。

聚合日志：

```text
logs/YYYY-MM-DD/calendar_sync.log
```
