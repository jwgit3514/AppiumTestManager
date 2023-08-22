import streamlit as st

from helper.os_helper import call_device

class Device:
    def __init__(self, name: str, device_type: str, port: int):
        self.name = name
        self.device_type = device_type  # TODO: device type class 구현
        self.port = port

def get_device_list():
    '''
    this is dummy
    from call_device() -> None:
    '''
    return [Device('dummy', 'android', 8200), Device('foo', 'ios', 8201)]


st.title("Appium Tester for QA")
st.file_uploader("Choose a file")
devices = get_device_list()
st.selectbox('device', [d.name for d in devices])

package = st.text_input('package', placeholder='package 명을 입력하세요')
activity = st.text_input('activity')


left_pos, middle_pos, right_pos = st.columns([2, 2, 1])
with left_pos:
    st.button('set')

with middle_pos:
    st.button('run', on_click=lambda: st.toast(f'testing '
                                                f'{package or "package_must_be_required"} '
                                                f'{activity or "activity_must_be_required"}'))
with right_pos:
    st.button('save')
