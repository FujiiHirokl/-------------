import socket
import time
import numpy as np

server_ip = '127.0.0.1'
server_port = 5091

# TCPソケットを作成
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# サーバに接続
client_socket.connect((server_ip, server_port))

# サイン波のパラメータ
amplitude = 10.0  # 振幅
frequency = 1.0  # 周波数（1秒ごとに変化）

counter = 0

while True:
    # サイン波の値を計算
    t = counter / 10.0  # 時間（秒）
    value = amplitude * np.sin(2 * np.pi * frequency * t)

    # サーバに値を送信
    message = str(value) + '\n'  # データを改行コードで区切って送信
    client_socket.send(message.encode())

    # カウンタをインクリメント
    counter += 1

    # 1秒待機
    time.sleep(0.01)

# ソケットを閉じる（通常はここに到達しない）
client_socket.close()
