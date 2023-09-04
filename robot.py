import pyaudio
import wave
import numpy as np
import speech_recognition as SR
from gtts import gTTS
from IPython.display import Audio
from pydub import AudioSegment
from pydub.playback import play

class ChatRobot():
    QA = {
        "無法辨識":"請你再說一次",
        "你好":"你好",
        "123牽著手":"四五六抬起頭",
        "789":"我們一起私奔到月球",
        }
    
    def __init__(self,
                 language = "zh-TW",
                 FORMAT = pyaudio.paInt16,
                 channels = 2,
                 chunk = 1024,
                 rate = 44100,
                 record_seconds = 30,
                 output_filename = "robotListen.wav",
                #  microphone = 1,
                 threshhold = 95):
        # 語言
        self.LANGUAGE = language
        # 錄音參數
        self.FORMAT = FORMAT    # 音頻樣本格式(paFloat32、paInt32、paInt24、paInt16、paInt8、paUInt8、paCustomFormat)
        self.CHANNELS = channels    # 聲道數量
        self.CHUNK = chunk    # 音頻流中的幀大小，指每次讀取音頻數據的大小
        self.RATE = rate    # 取樣頻率(Hz)(44100 ( CD )、48000 ( DVD )、22050、24000、12000 和 11025)
        self.RECORD_SECONDS = record_seconds    # 錄音秒數
        self.OUTPUT_FILENAME = output_filename    # 錄音儲存檔名
        # self.MICROPHONE = microphone    # 選擇麥克風
        self.THRESHHOLD = threshhold
    
    def setLang(self, lang):
        self.LANGUAGE = lang
    
    def listen2audio(self):
        # 建立 pyaudio 物件
        pa = pyaudio.PyAudio()

        # 開啟錄音串流
        stream = pa.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK,
                        # input_device_index=self.MICROPHONE,
                        )
        frames = []  # 建立聲音串列
        last_non_silent_time = 0

        # 開始錄音
        # print("=== 開始錄音 ===")
        try:
            for i in range(0, int(self.RATE/self.CHUNK * self.RECORD_SECONDS)):
                print(("錄音中"+("."*(i%10))).ljust(16),'\r',end='')
                data = stream.read(self.CHUNK)
                # 轉換音訊數據為 numpy 數組            
                audio_data = np.frombuffer(data, dtype=np.int16)
                # 計算音量
                volume = np.abs(audio_data).max()
                if volume > 900:
                    last_non_silent_time = i
                if i - last_non_silent_time > self.THRESHHOLD:
                    break
                frames.append(data)  # 將聲音紀錄到串列中
        except:
            pass

        # 關閉錄音串流
        stream.stop_stream()  # 停止錄音
        stream.close()  # 關閉串流
        pa.terminate()  # 關閉音訊設備
        # print("=== 錄音結束 ===")

        # 將錄音數據保存為 wav 檔
        with wave.open(self.OUTPUT_FILENAME, "wb") as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(pa.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b"".join(frames))
        # print(f"錄音檔案已儲存為 {OUTPUT_FILENAME}")

    def audio2word(self):
        r = SR.Recognizer()  # 用於辨識語音
        with SR.AudioFile(self.OUTPUT_FILENAME) as source:  # 開啟音檔
            audio = r.record(source)  # 讀取語音內容

        return r.recognize_google(audio, language=self.LANGUAGE)  # 將讀取到的音頻傳遞給 googlem 語音識別引擎進行辨識，並返回字串
    
    def speak(self):
        try:        
            text = self.audio2word()
        except:        
            text = "無法辨識"
        # 將文字轉換為語音
        tts = gTTS(ChatRobot.QA.get(text, "我還不夠聰明，等變聰明了再回答你"), lang=self.LANGUAGE)

        tts.save("robotSay.wav")
        # 打開音檔
        sound = AudioSegment.from_file("robotSay.wav")
        # 播放
        play(sound)