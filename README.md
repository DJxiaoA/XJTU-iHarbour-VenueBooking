# 场地预约系统（VenueBooking）

本仓库是一个面向体育场馆预约场景的自动化工具集，由 `client/` 与 `server/` 两个子项目共同组成。系统围绕同一套场馆预约站点运行：客户端负责执行预约流程并记录预约结果，服务端在此基础上承担预约结果聚合、日历写入与历史记录归档等服务侧处理任务。

`client` 和 `server` 均为独立的 Python 自动化程序，通过外部场馆系统、Notion 数据库以及可选的 PushPlus 推送服务协同工作。

## 项目架构

```text
.
├─client/
│  ├─Config_example.py
│  ├─Config.py
│  ├─funcs.py
│  ├─main.py
│  ├─start_client.bat
│  └─README.md
├─server/
│  ├─Config_example.py
│  ├─Config.py
│  ├─funcs.py
│  ├─main.py
│  ├─write_to_calendar.py
│  ├─start_server.bat
│  └─README.md
└─README.md
```

## 核心功能

- 基于 Selenium 自动打开场馆系统登录页并获取预约所需会话 Cookie。
- 按配置的放号时间等待进入预约窗口，支持立即执行模式与无界面模式。
- 查询指定日期与时段的候选场地，解析可用场地编号并并发尝试预约。
- 通过 `ddddocr` 识别滑块验证码，自动构造轨迹并提交预约请求。
- 通过 `profile_names` 同时运行多个账号配置，实现多账号并发预约。
- 在生产模式下将预约成功结果写入 Notion 的 booking 数据库。
- 在服务端将 booking 数据库中的预约记录按日期、时段聚合写入 calendar 数据库，并可选发送 PushPlus 推送。
- 按日期输出运行日志，分别记录预约过程与日历聚合过程。

## 技术栈

- Python
- Selenium WebDriver
- Requests
- Beautiful Soup 4
- lxml
- ddddocr
- Pillow
- Notion API（`notion-client`）
- PushPlus API（服务端可选）
- Windows 批处理脚本（`.bat`）

## 子项目说明

| 子项目 | 主要入口 | 职责 |
| --- | --- | --- |
| `client/` | `main.py`、`start_client.bat` | 执行预约流程，完成登录、候选场地查询、验证码识别、并发预约与 booking 数据库写入。 |
| `server/` | `main.py`、`write_to_calendar.py`、`start_server.bat` | 复用预约流程，并在预约结束后执行 booking 结果聚合、calendar 数据库写入、旧 booking 记录归档与可选 PushPlus 推送。 |

### 客户端

`client` 子项目聚焦于预约执行本身。程序会读取 `Config.py` 中启用的 profile，按账号配置逐个或并发运行，完成以下流程：

1. 打开统一认证登录入口并建立场馆系统会话。
2. 等待放号时间，或在测试模式 / 立即执行模式下直接继续。
3. 打开目标场地页面，查询目标日期与时段的候选场地。
4. 并发尝试预约所有候选场地。
5. 在生产模式下将成功结果写入 Notion booking 数据库。

### 服务端

`server` 子项目包含两条职责线：

1. `main.py` 负责执行与客户端同类的预约流程。
2. `write_to_calendar.py` 负责从 booking 数据库读取目标日期的预约记录，按时段聚合后写入 calendar 数据库，并归档早于阈值日期的旧 booking 记录。

`start_server.bat` 会先执行预约流程，再等待 `WAIT_SECONDS`（默认 `180` 秒）后执行日历聚合流程。

## 安装说明

### 环境要求

- Python 3.10 或更高版本
- Google Chrome
- 可正常启动 Chrome 的 Selenium 运行环境

### 安装依赖

仓库当前未提供统一的 `requirements.txt`，可根据源码中的实际依赖安装：

```bash
python -m pip install selenium requests beautifulsoup4 lxml ddddocr pillow notion-client
```

## 配置说明

### 配置文件

两个子项目均使用各自目录下的 `Config.py` 作为运行配置文件。建议先分别复制配置模板：

- `client/Config_example.py` -> `client/Config.py`
- `server/Config_example.py` -> `server/Config.py`

`Config.py` 已在 `.gitignore` 中排除，适合仅在本地保存账号、令牌与数据库标识等敏感信息。

### 通用配置项

`client/Config.py` 与 `server/Config.py` 均包含以下核心配置块：

- `site`
  - `base_url`：场馆系统根地址。
  - `login_url`：统一认证登录入口。
  - `venue_url`：正式预约场地页面。
  - `test_venue_url`：测试场地页面。
  - `booking_open_time`：放号时间，包含 `hour`、`minute`、`second`、`millisecond`。
  - `headless`：是否以无界面模式运行浏览器。
  - `run_immediately`：是否启动后立即执行，不等待放号时间。
  - `request_timeout_seconds`：HTTP 请求超时时间。
  - `captcha_offset`：滑块识别结果的补偿偏移量。
  - `notification_delay_range_seconds`：预约成功后写入 Notion 前的随机等待区间。
- `profiles`
  - `username`：登录账号。
  - `password`：登录密码。
  - `record_name`：写入 Notion 时使用的记录标识。
  - `days_ahead`：预约目标日期相对当前日期的偏移天数。
  - `venue_target`：`production` 表示正式场地，`test` 表示测试场地。
  - `priority_time_period`：目标预约时段，格式示例为 `19:01-20:00`。
- `profile_names`
  - 指定本次启用的 profile 列表；列表中有多个 profile 时，程序会并发执行。

### 集成配置

`client` 与 `server` 都依赖 Notion booking 数据库写入预约结果，相关配置位于：

```python
self.integrations = {
    "notion": {
        "token": "YOUR_NOTION_TOKEN",
        "booking_database_id": "YOUR_BOOKING_DATABASE_ID",
    }
}
```

`server` 额外需要以下配置：

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

self.calendar_sync = {
    "days_ahead": 2,
    "archive_days_before": 10,
}
```

- `calendar_database_id`：服务端聚合结果写入的日历数据库。
- `pushplus.token`：PushPlus 推送令牌；留空时仅写入 Notion，不发送推送。
- `pushplus.topic`：PushPlus 主题。
- `calendar_sync.days_ahead`：聚合 booking 数据库中哪一天的记录。
- `calendar_sync.archive_days_before`：归档多少天前的旧 booking 记录。

### Notion 数据库字段约定

根据代码实现，系统对 Notion 数据库字段名称有固定约定：

**booking 数据库**

| 字段名 | 用途 |
| --- | --- |
| `Scheduled date` | 预约日期 |
| `Order date` | 下单日期 |
| `Time period` | 预约时段 |
| `Venue Number` | 场地编号列表 |
| `Student ID` | 记录标识 |

**calendar 数据库**

| 字段名 | 用途 |
| --- | --- |
| `名称` | 聚合后的标题 |
| `日期` | 日历起止时间 |
| `标签` | 场地与人员标签 |

## 运行方式

### 运行客户端

```bash
cd client
python main.py
```

Windows 环境下也可直接执行：

```bat
client\start_client.bat
```

### 运行服务端预约流程

```bash
cd server
python main.py
```

### 运行服务端日历聚合流程

```bash
cd server
python write_to_calendar.py
```

### 一键运行服务端完整流程

```bat
server\start_server.bat
```

该脚本会按以下顺序执行：

1. 运行 `server/main.py` 执行预约。
2. 等待 `WAIT_SECONDS` 指定的秒数，默认值为 `180`。
3. 运行 `server/write_to_calendar.py` 执行日历聚合与旧记录归档。

## 前后端协作方式与接口概述

- 场馆预约系统：负责登录、场地查询与预约提交。
- Notion booking 数据库：保存预约结果。
- Notion calendar 数据库：保存服务端聚合后的日历记录。
- PushPlus：服务端可选通知渠道。

### 预约流程涉及的外部接口

预约流程主要依赖以下站点页面或接口：

- `site.login_url`：统一认证登录入口。
- `site.venue_url` / `site.test_venue_url`：正式场地与测试场地页面。
- `/product/findtime.html`：查询某日可用时段。
- `/product/price.html`：拉取目标时段价格 / 关联信息。
- `/seat/seat.html`：获取可用场地与座位标识。
- `/gen`：获取滑块验证码数据。
- `/order/book.html`：提交预约请求。

### 数据协作关系

1. `client` 或 `server/main.py` 完成预约后，在生产模式下将成功结果写入 booking 数据库。
2. `server/write_to_calendar.py` 按 `days_ahead` 读取 booking 数据库中的目标日期记录。
3. 服务端按时段聚合同一天的预约结果，写入 calendar 数据库。
4. 服务端归档超过 `archive_days_before` 的旧 booking 记录。
5. 如已配置 PushPlus 令牌，服务端在写入 calendar 数据库后发送推送通知。

## 日志与输出

- 客户端预约日志：`client/logs/YYYY-MM-DD/<profile>.log`
- 服务端预约日志：`server/logs/YYYY-MM-DD/<profile>.log`
- 服务端聚合日志：`server/logs/YYYY-MM-DD/calendar_sync.log`

日志文件按日期归档；启用多个 profile 时，会分别生成对应名称的预约日志。

## 使用说明与注意事项

- 建议在各子项目目录内执行命令，以保持配置文件路径与日志输出位置一致。
- 当前仓库未提供自动化测试脚本、容器化配置或部署脚本，运行方式以本地 Python 执行为主。
- 生产模式下，预约成功后会直接写入 Notion booking 数据库；仅测试流程时，应使用测试场地或调整相应配置。
- `client` 与 `server` 的配置文件彼此独立；如需两端行为一致，应同步维护相同或兼容的参数。
- 场馆系统地址、登录入口、场地页面与数据库字段均来自当前代码实现；若目标系统页面结构或接口发生变化，应同步调整配置或代码。

## 作者信息

Jiahui Wang
