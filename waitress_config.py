# Waitress 配置文件 (Windows 服务器专用)

# 监听地址和端口
host = "0.0.0.0"
port = 5000

# 线程数
threads = 4

# 连接队列大小
backlog = 2048

# 请求超时(秒)
channel_timeout = 120

# 清理间隔
cleanup_interval = 30

# 最大请求体大小 (字节)
max_request_body_size = 1073741824  # 1GB

# 最大请求头大小 (字节)
max_request_header_size = 262144  # 256KB
