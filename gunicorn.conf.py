from multiprocessing import cpu_count
import os

bind = f"0.0.0.0:{os.environ.get('BACKEND_PORT')}"
workers = 2  # (cpu_count() * 2) + 1
worker_class = "uvicorn.workers.UvicornWorker"
capture_output = True
loglevel = "debug"
proxy_headers = True
forwarded_allow_ips = "*"
