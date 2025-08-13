import streamlit as st
import pandas as pd
import numpy as np
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime


SCOPE =[
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def submit_gsheet(data):
    try:
        # Memuat credentials dari st.secrets
        
        creds_dict = {
          "type": "service_account",
          "project_id": "streamlit-aset",
          "private_key_id": "ab7bbf62e1454c17448573afc1efd4736f896803",
          "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCwzHAFDwJqkqFo\n63lsvdSWWNVIqCjr7GepGddctgONXygtdDgDafBCK2dGJIORifsRI1V8pZXlhvXA\nSnFnLI8ueydasb5s5KJ20sV0E9TK4t0ZdNujareG2HMS1OxmH1fxf6vvxABjujYD\nch54o+1C32B6B/i6edsPKjBhJrjLmNrvGiQ8eHNrZ/MQAYUTOPIACVE4KNqKwoS9\njud0o/mP/feFTgyuoGm5Hx3QmXbVxD4AR2i6Bs2xfRVnAebRAAp3W+5MXD3hegAf\nJ6C6VmqLMltvxlNRQmpa9D0PsZ1pLaJFGeh5Djrd7PeAMYwRHKvgtWk9VUW/qZkx\nsFPcAc8NAgMBAAECggEABym9RyMwyp8WvZC+ym5VgOLn/0na4JYjLAmBPX8dXTqz\n/sV06ISACLpH9KJRl1GzE6JuGf7+d/50Ef6iIhc+1NgGA+lsKO7Je012VQnhpvey\nlA+1P2V5OpQl82cfjdKqxjzRO0Via6f1fMXAoMwpdnpk5wTQKcP6oV5o9+Kw/YSq\nRZLWfPJsov1IZxGzxel1poLSweX1ykc7uCQYMyg44xJvBDriqE/uk6ZSOe+LyQJe\nH8txth+WxilfGMaewWhT4spkc3cOzz+i5TD0fYFFaqXuan3HPWx5ryU99ZZEAF8f\nROX7v+gd2U30jeudPEs1NoA0q5VPYqqXJuaYB3A8KQKBgQDySBMs10qb0aB8vmAa\npfeEZo7rR2ZQV1QoYlBSQJCK7SPKbM+TVd6hxD/+tVgZNCpw6RTCP24Yhe4HPKuQ\nR1C0FaDiM8MwLNRT/tE1mMe0W2zcvnP13ZL7OIuLfwllZVEZKJnoKAJHkbRWMx57\n8YGn7xoAm5QlXPl3xz/d11YPZQKBgQC6zyws/1PSHQ2KYxI1s7wn0tij0Ow4Xybr\nTOvHlDT6xJDYgHXndIPlELh40WB8W4SgK7P8yTExwm5GMOutqw9P6SPAmDMFuNip\nLaIDQAwB82Iu/alzoadG3tSqcm8iSO3mglwfFTYbOGEKZyl2w4M/v26bxmrQ5Tu0\nnWTTcGkqiQKBgHuq5n7A9chLXAvQcOWpSYo/fzwBGexwZvimFjGl2yHOobI1kE64\nSgdwUOoGTo2u3ur7TilIjz3dPv5arYfbnwoM8C4GFd+FQmwNaWReM7GP6SVT4YTi\nMKAi4Le3hGhJKvgYjVa+9UrqyI4nUawaPgAmP7OHtjrMFlpZTfRCch8xAoGAQnjl\npz1TfjiIUO3f1OwXz7PfEquM4qI5HxFH9MRv9atsPx221p1HMYM5oQQf6SBHmRbz\n/Mc6khI1WxSdSDbORAkZh7agsTCNJ+Xs+GsZ2rfYABCS82paM4Wm9t+xW+nHfXZ1\ngTny/syY+zKqNnBri4t6uENqTtrC3AoFjpc5VMECgYEA0Me78WUaZihHmW9St2/0\ngQfoIOEO/9QwOUp7HiGjNVx0gZjPPQ1E6kyO0RA18DTDN4s8+lwFhqw8Lj9utz0h\nO1H8HCGI0Wc4+1O8wFVtyw3m6p3hp4OW1F22jCWqFaHV/w/ODEJ1emOdEu4xxB0b\n7PRr1RKcIuqYa0l53oLgzTI=\n-----END PRIVATE KEY-----\n",
          "client_email": "device-aset@streamlit-aset.iam.gserviceaccount.com",
          "client_id": "115929604801669675664",
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://oauth2.googleapis.com/token",
          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
          "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/device-aset%40streamlit-aset.iam.gserviceaccount.com",
          "universe_domain": "googleapis.com"
        }

        creds = Credentials.from_service_account_info(creds_dict, scopes =SCOPE)

        # Otorisasi gspead
        client = gspread.authorize(creds)

        # Buka spreadsheet berdasarkan nama
        gsheet = client.open("Aset_SAKA")

        # Pilih worksheet pertama
        worksheet = gsheet.get_worksheet(0)

        new_row = [
            data.get('Device',''),
            data.get('PIC',''),
            data.get('Jenis Device',''),
            data.get('Status',''),
            data.get('Letak Aset',''),
            data.get('Keterangan','')
        ]

        worksheet.append_row(new_row)

        return True, f"Aset '{data.get('Device'),''}' berhasil disimpan!"
    except Exception as e:
        return False, f"Terjadi kesalahan : {e}"
    
st.set_page_config(layout = 'centered', page_title='Form Aset IT')

st.title('📝 Formulir Input Aset IT')
st.write('Data dari formulir ini akan langsung tersimpan di Google Sheets.')
st.markdown("-------")

st.header('Detail Aset')

device_name = st.text_input('Jenis Device*', help ='Contoh : Dell Latitude 3450')
pic_name = st.text_input('Nama PIC*')
device_type = st.selectbox('Tipe Device', ['PC','Notebook'])
status = st.selectbox('Status Aset',['Sudah Diambil IT','Belum Diambil IT'], key = 'status_aset')


if st.session_state.status_aset == 'Belum Diambil IT':
    letak_aset = st.text_input('Dimana Letak Aset Tersebut?')
else:
    letak_aset = ''
    
keterangan = st.text_area("Keterangan Tambahan")

with st.form('asset_form', clear_on_submit = True):
    submit = st.form_submit_button('Simpan Aset ke Google Sheets')

if submit:

    if not device_name or not pic_name:
        st.warning('Mohon isi field yang ditandai (*)')
    else:
        payload = {
            'Device':device_name,
            'PIC' : pic_name,
            'Jenis Device': device_type,
            'Status': status,
            'Letak Aset' : letak_aset,
            'Keterangan': keterangan
        }
        with st.spinner('Sedang Mengirimkan data ke Google Sheets....'):
            success, message = submit_gsheet(payload)
        
        if success:
            st.success(message)
        else:
            st.error(message)
