import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation

server_ip = '127.0.0.1'
server_port = 5091

# TCPソケットを作成
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ソケットをIPアドレスとポートにバインド
server_socket.bind((server_ip, server_port))

# 接続待機
server_socket.listen()

print(f"サーバーが起動しました。クライアントからの接続を待機しています...")

# クライアントからの接続を受け付ける
client_socket, client_address = server_socket.accept()

print(f"クライアントが接続しました。")

# グラフデータを保持するリストと上限
max_data_points = 100
x_data = []
y_data1 = []

# グラフの設定
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    global x_data, y_data1

    # クライアントからデータを受信
    raw_data = client_socket.recv(1024).decode().strip()

    # 受信したデータを表示
    if raw_data:
        print(f"受信データ: {raw_data}")
        # データを改行コードで分割して、個々のデータを取り出す
        data_points = raw_data.split('\n')
        for data in data_points:
            value = float(data)
            # データをリストの先頭に追加
            x_data.insert(0, len(x_data))
            y_data1.insert(0, value)
            # データ数が上限を超えた場合、一番最初のデータを削除し、データを一つずつ前にずらす
            if len(x_data) > max_data_points:
                x_data = x_data[1:]
                y_data1 = y_data1[1:]
                x_data = [x - 1 for x in x_data]  # データを一つずつ前にずらす

    # グラフを更新
    line.set_data(x_data, y_data1)
    ax.relim()
    ax.autoscale_view()
    return line,

# アニメーションを設定
ani = animation.FuncAnimation(fig, animate, init_func=init, interval=100)

try:
    # グラフ表示開始
    plt.show()
except KeyboardInterrupt:
    print("プログラムが停止されました。")
finally:
    # ソケットを閉じる
    server_socket.close()
    client_socket.close()
