# Gunicorn 配置文件

# 监听地址和端口
bind = "0.0.0.0:5000"

# 工作进程数 (建议设置为 CPU核心数 * 2 + 1)
workers = 4

# 每个工作进程的线程数
threads = 2

# 工作模式
worker_class = "sync"

# 最大并发数
worker_connections = 1000

# 超时设置 (秒)
timeout = 30
keepalive = 2

# 守护进程
daemon = False

# 进程名称
proc_name = "logistics_voucher_api"

# 日志
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"

# PID文件
pidfile = "logs/gunicorn.pid"

# 优雅重启超时时间
graceful_timeout = 30

# 预加载应用
preload_app = True
