import multiprocessing

bind = '0.0.0.0:8080'
workers = multiprocessing.cpu_count()*2 + 1
print(workers)
timeout = 30
worker_connections = 1000
