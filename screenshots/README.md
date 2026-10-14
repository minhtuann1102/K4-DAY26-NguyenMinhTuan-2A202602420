# Minh chứng chạy lab

Mọi ảnh được tạo từ **code ở commit này**, ngày 2026-10-14, trên Windows 11 (bước 01–03: Python 3.11, `mcp` 2.3.0; lab 04: Python 3.13, `mcp` 1.28.1 khi chạy local theo `uv.lock`, 1.30.0 trong Docker).

## Hai loại ảnh — đọc kỹ

| Loại | Ảnh | Cách tạo |
|---|---|---|
| **Ảnh chụp trình duyệt thật** | `04c`, `04d` | Chrome điều khiển bằng Playwright mở ADK web UI (`adk web`), gõ câu hỏi, chụp màn hình |
| **Ảnh render từ output lệnh** | `01`, `02`, `03a`, `03b`, `03c`, `04a`, `04b` | Chạy lệnh thật, lưu nguyên stdout, rồi dựng thành trang kiểu terminal và chụp bằng Chrome |

Loại thứ hai **không phải ảnh chụp cửa sổ terminal của hệ điều hành**. Để kiểm chứng, output gốc chưa chỉnh sửa
của từng ảnh nằm ở [`logs/`](logs/) cùng tên. Mỗi ảnh có caption ghi lệnh chạy và thời điểm chụp.
Nếu giảng viên yêu cầu ảnh chụp terminal thật, hãy chạy lại các lệnh bên dưới và chụp màn hình.

## Mục lục

| Ảnh | Bước | Lệnh | Chứng minh điều gì |
|---|---|---|---|
| [01-function-calling.png](01-function-calling.png) | 01 | `python weather_function_calling.py` (trong `01-function-calling/`) | Model yêu cầu `get_weather`, **app tự thực thi**, model tổng hợp câu trả lời. Tên thành phố không dấu (`Ha Noi`, `Da Nang`) vẫn ra đúng dữ liệu mock |
| [02-mcp-basics.png](02-mcp-basics.png) | 02 | `python weather_client.py` (trong `02-mcp-basics/`) | Client khám phá tool bằng `list_tools` rồi `call_tool` qua stdio |
| [03a-auth.png](03a-auth.png) | 03a | `MCP_AUTH_PORT=8100 python auth_server.py` + `python auth_client.py` + 2 lệnh `curl` | Không token / token sai → `401`; token hợp lệ → gọi tool được |
| [03b-registry.png](03b-registry.png) | 03b | `python registry_client.py` | Agent tìm tool theo tag, chọn `get_weather_v2` (version cao nhất, không deprecated) và tự kết nối |
| [03c-versioning.png](03c-versioning.png) | 03c | `python versioned_client.py` | v1 (deprecated) và v2 chạy song song, `server://info` công bố migration |
| [04a-mcp-server-local.png](04a-mcp-server-local.png) | 04 | `PORT=8085 python weather.py` + `python smoke_test.py` | MCP server Streamable HTTP có 3 tool, gọi WeatherAPI thật |
| [04b-docker.png](04b-docker.png) | 04 | `docker build` / `docker run -e PORT=8080` + `python smoke_test.py http://localhost:8086/mcp` | Image build từ Dockerfile chạy đúng ở chế độ giống Cloud Run (`PORT=8080`) với `mcp` 1.30.0 |
| [04c-adk-web-ui.png](04c-adk-web-ui.png) | 04 | `adk web` → chat với `weather_agent` | Agent ADK tự gọi `get_current_weather` + `get_forecast` qua `McpToolset`, trả lời tiếng Việt |
| [04d-adk-web-tool-call.png](04d-adk-web-tool-call.png) | 04 | (cùng phiên trên) | Chi tiết một lần gọi tool: tham số `city: "Hanoi"` gửi sang MCP server |

Log build Docker đầy đủ (không cache, 345 dòng): [`logs/04b-docker-build-full.txt`](logs/04b-docker-build-full.txt).

## Chưa làm được

- **Deploy lên Cloud Run:** máy chưa cài `gcloud` và bước này cần tài khoản GCP của bạn. Dockerfile đã được build và chạy
  trong Docker local với `PORT=8080` — cách Cloud Run chạy container — nhưng chưa có ảnh dịch vụ trên Cloud Run.
  Khi deploy xong, đặt `MCP_SERVER_URL=https://<service>.run.app/mcp` trong `04-lab/mcp-client/.env` và chụp thêm ADK web.

## Ghi chú khi chạy lại

- `auth_server.py` mặc định dùng cổng 8000, trùng với `adk web`. Đặt `MCP_AUTH_PORT=8100` và `MCP_AUTH_SERVER_URL=http://localhost:8100/mcp` nếu cần chạy cùng lúc.
- Nếu khởi động lại MCP server khi `adk web` đang chạy, phải khởi động lại `adk web` (lỗi `Session terminated` do ADK giữ session cũ).
- Log của `weather.py` không ghi URL request của `httpx`, vì WeatherAPI nhận API key qua query string `?key=` và sẽ lộ key vào log.
