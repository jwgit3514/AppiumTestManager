import subprocess

def call_device() -> None:
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)

    device_list = []
    lines = result.stdout.strip().splitlines()
    for line in lines[1:]:
        device_info = line.strip().split('\t')
        if len(device_info) == 2 and device_info[1] == 'device':
            device_list.append(device_info[0])

    if not device_list:
        print("is empty!!")
        device_list = ['']
        return device_list
    else:
        return device_list
