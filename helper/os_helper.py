import subprocess

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