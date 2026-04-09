# VenueBooking

西安交通大学 创新港巨构 羽毛球场地预约

## 作者

Jiahui Wang

## 说明

本项目仅供学习与交流使用。 如需参考、修改或二次开发，请保留原作者信息。

## 项目简介

本项目用于登录体育场馆系统、等待放号、查询可用场地并提交预约。

项目主入口：

- `main.py`：按 `Config.py` 中的 `self.profile_names` 依次并发运行预约任务
- `start_client.bat`：Windows 一键启动脚本

## 目录说明

- `Config.py`：统一配置文件，登录信息、预约参数、Notion 配置都在这里
- `funcs.py`：预约流程实现
- `main.py`：程序入口
- `start_client.bat`：Windows 启动脚本

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
- `record_name`：写入 Notion 时使用的姓名
- `priority_time_period`：目标预约时段

常用字段说明：

- `days_ahead`：预约几天后的场地，`2` 表示预约两天后
- `venue_target`：`production` 为正式场地，`test` 为测试场地

## 如何配置同时预约的账号数

程序会对 `self.profile_names` 中列出的 profile 并发执行。

如果只预约一个账号，保持默认即可：

```python
self.profile_names = ["main"]
```

如果要同时预约多个账号，可以复制 `main` 配置块并改名，例如：

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
        "priority_time_period": "19:01-20:00",
    },
}

self.profile_names = ["main", "main2"]
```

并发账号数就等于 `self.profile_names` 的数量。

## 其他常用配置

`Config.py` 中的 `self.site` 可调整以下参数：

- `venue_url`：正式场地页面
- `test_venue_url`：测试场地页面
- `booking_open_time`：放号时间
- `headless`：`True` 表示无界面运行，`False` 表示显示浏览器
- `run_immediately`：`True` 表示不等待放号时间，启动后立即执行
- `notification_delay_range_seconds`：预约成功后写入 Notion 前的随机等待时间

`self.integrations["notion"]` 用于 Notion booking 数据库：

```python
self.integrations = {
    "notion": {
        "token": "YOUR_NOTION_TOKEN",
        "booking_database_id": "YOUR_BOOKING_DATABASE_ID",
    }
}
```

如果不需要写入 Notion，可以保留结构但填写你自己的测试配置，或者自行修改代码跳过该步骤。

## .bat 脚本如何配置

打开 `start_client.bat`：

```bat
@echo off
setlocal
cd /d "%~dp0"
set "PYTHON_EXE=python"
"%PYTHON_EXE%" main.py
```

可修改项：

- `PYTHON_EXE=python`：如果你的 Python 已加入环境变量，保持默认即可
- 如果没有加入环境变量，把它改成完整路径，例如：

```bat
set "PYTHON_EXE=D:\Python311\python.exe"
```

双击 `start_client.bat` 后，脚本会进入当前目录并执行 `main.py`。

## 运行方式

命令行运行：

```bash
python main.py
```

Windows 双击运行：

- `start_client.bat`

## 日志

运行日志会写入：

```text
logs/YYYY-MM-DD/main.log
```

如果配置了多个 profile，会分别生成对应名称的日志文件。
