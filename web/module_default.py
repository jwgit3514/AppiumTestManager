import os
import sys
import warnings
import streamlit as st
import re
import subprocess
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# warnings.simplefilter(action='ignore', cetegory=FutureWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)


def split_filename(filename) -> str:
    file_num = re.findall(r"\d+", filename)
    return int(file_num[0])+1


def read_filename(path) -> str:
    file_list = os.listdir(path)
    # print("file_list : ".format(file_list))
    return sorted(file_list, reverse=False)


def convert_filename(filepath, filename) -> None:
    file_list = read_filename(filepath)
    if not file_list:
        return 'uploaded_1.jpg'
    else:
        last_num = split_filename(file_list[-1])
        return f'uploaded_{str(last_num)}.jpg'


def call_device() -> None:
    # adb devices 명령어 실행
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)

# 명령어 실행 결과에서 디바이스 목록 추출
    device_list = []
    lines = result.stdout.strip().splitlines()
    for line in lines[1:]:  # 첫 번째 줄은 헤더이므로 건너뜁니다.
        device_info = line.strip().split('\t')
        if len(device_info) == 2 and device_info[1] == 'device':
            device_list.append(device_info[0])

    if not device_list:
        print("is empty!!")
        device_list = ['None']
        return device_list
    else:
        return device_list


def save_uploaded_file(filepath, file):
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    file.name = convert_filename(filepath, file.name)

    with open(os.path.join(filepath, file.name), 'wb') as f:
        f.write(file.getbuffer())

    return st.success('complete file upload')


if __name__ == '__main__':
    list = read_filename('./images/홍정원')
    print(list)
