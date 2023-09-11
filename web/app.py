from module_default import *
import streamlit as st
import pandas as pd
import datetime
import time
import pickle
import extra_streamlit_components as stx
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
from streamlit_server_state import server_state, server_state_lock


class Device:
    def __init__(self, udid: str, device_type: str, port: int):
        self.udid = udid
        self.device_type = device_type  # TODO: device type class 구현
        self.port = port


class Appium_Server:
    def __init__(self, port: int, client: str, openned: bool):
        self.port = port
        self.cliennt = client
        self.openned = openned


class TestScenario():
    def __init__(self, description: str, test_type: int, filename: str,):
        self.description = description
        self.test_type = test_type
        self.filename = filename

    def get_val(self):
        return [self.description, self.filename, self.test_type]


def get_device_list():
    '''
    this is dummy
    from call_device() -> None:
    '''
    device_list = []
    port_num = 0
    for a in call_device():
        device_list.append(Device(a, 'android', 8200+port_num))
        port_num += 1
        pass
    return device_list


class App:
    def __init__(self, cookies):
        st.title("Appium Tester for QA...")

        with server_state_lock['session']:
            if 'session' not in server_state:
                server_state.session = []

        with server_state_lock['appium_server']:
            if 'appium_server' not in server_state:
                server_state.appium_server = [Appium_Server(4723, '', False),
                                              Appium_Server(4724, '', False),
                                              Appium_Server(4725, '', False),
                                              Appium_Server(4726, '', False),
                                              Appium_Server(4727, '', False),
                                              Appium_Server(4728, '', False),
                                              Appium_Server(4729, '', False),
                                              Appium_Server(4730, '', False),]

        with server_state_lock['session']:
            if 'session' not in server_state:
                server_state.session = []

        self.cookies = cookies

        self.file_list = read_filename(
            f'./images/{self.cookies["qa_id"]}')

        if 'test_list' not in st.session_state:
            st.session_state.test_list = []

# c1, c2 = st.columns(2)

# with c1:
#     st.subheader("Get Cookie:")
#     cookie = st.text_input("Cookie", key="0")
#     clicked = st.button("Get")
#     if clicked:
#         value = cookie_manager.get(cookie=cookie)
#         st.write(value)

# with c2:
#     st.subheader("Set Cookie:")
#     cookie = st.text_input("Cookie", key="1")
#     val = st.text_input("Value")
#     if st.button("Add"):
#         cookie_manager.set(cookie, val)  # Expires in a day by default
# with c1:
#     st.subheader("Delete Cookie:")
#     cookie = st.text_input("Cookie", key="2")
#     if st.button("Delete"):
#         cookie_manager.delete(cookie)

    def show_(self):
        devices = get_device_list()

        self.selected = st.selectbox(
            'server', [s.port for s in server_state.appium_server if s.openned == False])
        st.selectbox('device', [d.udid for d in devices])

        st.write(f'{self.selected=}')

        st.write(f'{self.cookies["qa_id"]=}')

        # big_list = ['test_step_01', 'test_step_02', 'test_step_03'
        #             ]

        # col = st.columns([4, 3], gap='medium')

        # with col[0]:
        #     st.write('테스트 시나리오')
        #     rb = st.radio('select', big_list, label_visibility='collapsed', key='rb_1')

        # with col[1]:
        #     st.text_input('Value selected', value=rb, key='ti_1')

    def test(self, selected):
        for s in server_state.appium_server:
            if s.port == selected:
                s.openned = True

    def buttons(self):
        left_pos, middle_pos, right_pos = st.columns([2, 2, 1])
        with left_pos:
            st.button('set')
        # with left_pos:
        #     st.button('test', on_click=lambda: self.test(self.selected))
        with middle_pos:
            st.button('run', on_click=lambda: st.toast(f'testing '))
        with right_pos:
            st.button('save')

    def file_uploader(self):
        uploaded_file = st.file_uploader(
            "Choose a file", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            # To read file as bytes:
            # cu_time = datetime.datetime.now()
            # filename = cu_time.isoformat().replace(':', '_')
            # uploaded_file.name = filename

            save_uploaded_file(
                f'./images/{self.cookies["qa_id"]}', uploaded_file)

            # bytes_data = uploaded_file.getvalue()
            # st.write(bytes_data)

            # # To convert to a string based IO:
            # stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            # st.write(stringio)

            # # To read file as string:
            # string_data = stringio.read()
            # st.write(string_data)

            # Can be used wherever a "file-like" object is accepted:
            # dataframe = pd.read_csv(uploaded_file)
            # st.write(dataframe)

    def dataframe(self):
        data = {
            "description": [],
            "test_type": [],
            "filename": [],
            "image": [],
        }

        # df = pd.DataFrame(data)
        if 'df' not in st.session_state:
            st.session_state.df = data

        edited_df = st.data_editor(data, column_config={
            "description"
            "test_type": st.column_config.SelectboxColumn(label="test_type", options=[0, 1], width="None", required=True,),
            "filename": st.column_config.SelectboxColumn(label="filename", options=self.file_list, width="None",),
            "image": st.column_config.ImageColumn(label='images', help='show selected image')
        }, hide_index=True, num_rows="dynamic", key='data_editor')

        if edited_df is not None:
            self.update_df(edited_df)
            st.session_state.df = edited_df

        self.print_tl()

    def update_df(self, edited_df):
        # for row_1, row_2, row_3, in zip(edited_df['description'], edited_df['test_type'], edited_df['image'],):
        #     st.write(
        #         "INSERT INTO TEST TABLE",
        #         (
        #             row_1,
        #             row_2,
        #             row_3,
        #         ),
        #     )

        st.session_state.test_list = []

        for i in range(len(edited_df['description'])):
            descripion = edited_df['description'][i]
            test_type = int(edited_df['test_type'][i])
            image = edited_df['filename'][i]

            instace = TestScenario(descripion, test_type, image)
            st.session_state.test_list.append(instace)

    def print_tl(self,):
        if st.button('test'):
            for i in range(len(st.session_state.test_list)):
                print('description : ',
                      st.session_state.test_list[i].description)
                print('test_type : ', st.session_state.test_list[i].test_type)
                if st.session_state.test_list[i].test_type == 1:
                    print('image file : ',
                          st.session_state.test_list[i].filename)
                    print('filepath : ' + '/images/' +
                          f'{cookies["qa_id"]}/'+st.session_state.test_list[i].filename)
                print('')

        # print(['/images/'+f'{cookies["qa_id"]}/' +
        #       i.filename for i in st.session_state.test_list])


if __name__ == '__main__':
    cookie_manager = stx.CookieManager()
    cookies = cookie_manager.get_all()
    time.sleep(0.5)

    if 'qa_id' not in cookies:
        st.toast('don\'t have id!!')
        name = st.text_input('이름', placeholder='이름을 입력하세요')
        if st.button('submit'):
            cookie_manager.set('qa_id', name)
    else:
        app = App(cookies)
        app.show_()
        app.file_uploader()
        app.dataframe()
        app.buttons()

    try:
        if not st.session_state.get('connect_check', False):
            st.toast(f'hello {cookies["qa_id"]} :)')
            st.session_state.connect_check = True
    except Exception as e:
        print(f'error : {e}')
