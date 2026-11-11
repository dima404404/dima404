# Проверка, свободен ли поддомен is-a.dev
import socket

for name in ["dima404", "dima404404", "dmitry", "dima"]:
    host = name + ".is-a.dev"
    try:
        ip = socket.gethostbyname(host)
        print(host, "->", ip, "ЗАНЯТ")
    except socket.gaierror:
        print(host, "-> свободен (NXDOMAIN)")
