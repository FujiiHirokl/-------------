import socket
import time
import numpy as np

server_ip = '127.0.0.1'
server_port = 5001

# UDPソケットを作成
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# サイン波のパラメータ
amplitude = 5.0  # 振幅
frequency = 1.0  # 周波数（1秒ごとに変化）

counter = 0

while True:
    # サイン波の値を計算
    t = counter / 10.0  # 時間（秒）
    value = amplitude * np.sin(2 * np.pi * frequency * t)

    # サーバに値を送信
    message = str(value).encode()
    client_socket.sendto(message, (server_ip, server_port))

    # カウンタをインクリメント
    counter += 1

    # 1秒待機
    time.sleep(0.05)

# ソケットを閉じる（通常はここに到達しない）
client_socket.close()
