import socket
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tkinter import Tk, Button, Scale
import threading
from scipy.fft import fft, fftfreq

server_ip = '127.0.0.1'
server_port1 = 5000  # クライアント1のポート番号
server_port2 = 5001  # クライアント2のポート番号

# フーリエ変換のためのデータ保存用のリスト
fft_data1 = []
fft_data2 = []

# UDPソケットを作成
server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# ソケットのタイムアウトを設定（ここでは5秒に設定）
server_socket1.settimeout(0.1)
server_socket2.settimeout(0.1)

# サーバーアドレスとポート番号をバインド
server_address1 = (server_ip, server_port1)
server_address2 = (server_ip, server_port2)
server_socket1.bind(server_address1)
server_socket2.bind(server_address2)

print('UDPサーバーを開始しました。')

# グラフの初期化
fig, ax = plt.subplots()
ax2 = ax.twinx()
# プロットの設定
line1, = ax.plot([], [], label='Client 1')
line2, = ax.plot([], [], label='Client 2')
max_data_points = 100  # データ数の上限
ax.set_xlim(0, max_data_points)
ax.set_ylim(-50, 50)
ax2.set_ylim(0, 100)
# ラベルを表示するための初期化
freq_label = ax2.text(0.5, 0.95, "", transform=ax2.transAxes, ha='center', va='top')
ax.legend(loc='upper left')

# データ保存用のリスト
x_data = []
y_data1 = []
y_data2 = []

# アニメーションの更新関数
paused = False  # 一時停止フラグ

def update(frame):
    global x_data, y_data1, y_data2, paused, fft_data1, fft_data2
    if paused:
        return line1, line2

    try:
        # データを受信
        data, address = server_socket1.recvfrom(1024)
        value = float(data.decode())
        print(f'クライアント1から受信しました: {value}')
    except socket.timeout:
        # タイムアウト例外をキャッチし、タイムアウト時の処理を記述
        print('クライアント1からのデータ受信がタイムアウトしました。')
        value = None  # 受信データがない場合はNoneを設定

    # データを追加してグラフを更新
    x_data.append(len(x_data))
    y_data1.append(value)

    # データ数が上限を超えた場合、一番最初のデータを削除し、データを一つずつ前にずらす
    global max_data_points
    if len(x_data) > max_data_points:
        x_data = x_data[1:]
        y_data1 = y_data1[1:]
        x_data = [x - 1 for x in x_data]  # データを一つずつ前にずらす

    # グラフをプロット
    line1.set_data(x_data, y_data1)

    # サンプリングレートの計算
    sampling_rate = 10.0  # 1秒あたりのサンプリング数（Hz）
    time_interval = 1.0 / sampling_rate

    # フーリエ変換を実行
    fft_data1.append(value)

    # データ数が上限を超えた場合、一番最初のデータを削除
    if len(fft_data1) > max_data_points:
        fft_data1 = fft_data1[1:]
    
    if len(fft_data1) > 1:  # データ数が1つ以上ある場合のみフーリエ変換を実行
        fft_result1 = fft(fft_data1, axis=0)
        frequencies1 = fftfreq(len(fft_data1), time_interval)
        positive_frequencies1 = frequencies1[:len(frequencies1) // 2]
        magnitude1 = np.abs(fft_result1[:len(frequencies1) // 2])
        peak_frequency_index1 = np.argmax(magnitude1)
        peak_frequency1 = positive_frequencies1[peak_frequency_index1]
    else:
        peak_frequency1 = 0.0


    # クライアント2のデータを受信
 
    try:
        # データを受信
        data, address = server_socket2.recvfrom(1024)
        value = float(data.decode())
        print(f'クライアント2から受信しました: {value}')
    except socket.timeout:
        # タイムアウト例外をキャッチし、タイムアウト時の処理を記述
        print('クライアント2からのデータ受信がタイムアウトしました。')
        value = None  # 受信データがない場合はNoneを設定

    # データを追加してグラフを更新
    y_data2.append(value)

    # データ数が上限を超えた場合、一番最初のデータを削除し、データを一つずつ前にずらす
    if len(y_data2) > max_data_points:
        y_data2 = y_data2[1:]

    # グラフをプロット
    line2.set_data(x_data, y_data2)

    # フーリエ変換を実行
    fft_data2.append(value)

    # データ数が上限を超えた場合、一番最初のデータを削除
    if len(fft_data2) > max_data_points:
        fft_data2 = fft_data2[1:]
    if len(fft_data2) > 1:  # データ数が1つ以上ある場合のみフーリエ変換を実行
        fft_result2 = fft(fft_data2, axis=0)
        frequencies2 = fftfreq(len(fft_data2), time_interval)
        positive_frequencies2 = frequencies2[:len(frequencies2) // 2]
        magnitude2 = np.abs(fft_result2[:len(frequencies2) // 2])
        peak_frequency_index2 = np.argmax(magnitude2)
        peak_frequency2 = positive_frequencies2[peak_frequency_index2]
    else:
        peak_frequency2 = 0.0

    freq_label.set_text(f"Client 1: {peak_frequency1:.2f} Hz, Client 2: {peak_frequency2:.2f} Hz")
    
    print("Client 1 frequency:", peak_frequency1, "Hz")
    print("Client 2 frequency:", peak_frequency2, "Hz")

    return line1, line2

# アニメーションの作成
animation = FuncAnimation(fig, update, frames=None, interval=0, blit=False)

# グラフを表示する関数
def show_plot():
    global paused, max_data_points

    # 一時停止ボタンのコマンド
    def pause_animation():
        global paused
        paused = True

    # 再開ボタンのコマンド
    def resume_animation():
        global paused
        paused = False

    # Tkinterウィンドウの作成
    root = Tk()
    root.title("Control Panel")

    # 一時停止ボタンの追加
    pause_button = Button(root, text="一時停止", command=pause_animation)
    pause_button.pack()

    # 再開ボタンの追加
    resume_button = Button(root, text="再開", command=resume_animation)
    resume_button.pack()

    def on_x_slider_change(val):
        global max_data_points
        x_range = int(val)
        max_data_points = x_range
        ax.set_xlim(0, max_data_points)
        ax.set_xlabel(f" ({x_range * 10}:ms)")  # Add the unit information to the X-axis label
        fig.canvas.draw_idle()

    x_slider = Scale(root, from_=0, to=2000, orient='horizontal', label="データ数", command=on_x_slider_change)
    x_slider.set(max_data_points)
    x_slider.pack()

    # Y軸スライダーの追加
    def on_y_slider_change(val):
        y_range = int(val)
        y_min = -y_range
        y_max = y_range
        ax.set_ylim(y_min, y_max)
        fig.canvas.draw_idle()

    y_slider = Scale(root, from_=0, to=100, orient='horizontal', label="電圧表示幅", command=on_y_slider_change)
    y_slider.set(50)
    y_slider.pack()

    # Tkinterのメインループを開始
    root.mainloop()

# グラフを表示する関数を非同期で実行
plt_thread = threading.Thread(target=show_plot)
plt_thread.start()

# アニメーションの開始
plt.show()

# ソケットを閉じる
server_socket1.close()
server_socket2.close()

# プロットスレッドが終了するまで待機
plt_thread.join()
