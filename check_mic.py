import pyaudio

# 創建PyAudio對象
p = pyaudio.PyAudio()

# 獲取可用的音頻設備數據
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

# 列出可用的麥克風設備
for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("麥克風ID {0}: {1}".format(i, p.get_device_info_by_host_api_device_index(0, i).get('name')))

# 關閉PyAudio對象
p.terminate()