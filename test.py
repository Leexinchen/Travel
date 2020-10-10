from aip import AipSpeech


result  = client.synthesis('0.4米', 'zh', 1, {'vol': 5,'per':0})
# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('0.4米.wav', 'wb') as f:
        f.write(result)