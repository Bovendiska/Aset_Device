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
        creds = Credentials.from_service_account_info(
            st.secrets.to_dict(), # Mengubah semua secrets menjadi dictionary
            scopes=SCOPE
        )
        # Otorisasi gspead
        client = gspread.authorize(creds)

        # Buka spreadsheet berdasarkan nama
        gsheet = client.open(st.secrets["gsheet_name"])

        # Pilih worksheet pertama
        worksheet = gsheet.get_worksheet(0)

        new_row = [
            data.get('Nomor Aset',''),
            data.get('Device',''),
            data.get('PIC',''),
            data.get('Nomor Telpon PIC'),
            data.get('Jenis Device Lama',''),
            data.get('Jenis Device Baru',''),
            data.get('Pemegang Device Lama',''),
            data.get('Pemegang Device Baru','')
        ]

        worksheet.append_row(new_row)

        return True, f"Aset '{data.get('Device'),''}' berhasil disimpan!"
    except Exception as e:
        return False, f"Terjadi kesalahan : {e}"
    
st.set_page_config(layout = 'centered', page_title='Form Aset IT')

st.title('📝 Formulir Input device IT')
st.write('Untuk mengetahui transaksi device lama dan baru')
st.markdown("-------")


st.header('Detail Aset')

device_number = st.text_input('Nomor Device (Device Lama)', help = 'Dilihat pada barcode Aset Device = SFL/../..')
device_name = st.text_input('Jenis Device*', help ='Contoh : Dell Latitude 3450')
pic_name = st.text_input('Nama PIC*', help = 'Nama Pengisi Form')
pic_num = st.text_input('Nomor PIC*', help = 'Nama Pengisi Form')
new_type = st.selectbox('Jenis Device Lama', ['PC','Notebook'])
old_type = st.selectbox('Jenis Device Baru', ['PC','Notebook'])
own_dev_old = st.text_input('Pemegang Device Lama')
own_dev_new = st.text_input('Pemegang Device Baru')  
keterangan = st.text_area("Keterangan Tambahan")

with st.form('asset_form', clear_on_submit = True):
    submit = st.form_submit_button('Simpan Aset ke Google Sheets')

if submit:

    if not device_name or not pic_name or not device_number or not pic_num:
        st.warning('Mohon isi field yang ditandai (*)')
    else:
        payload = {
            'Nomor Aset' : device_number,
            'Device':device_name,
            'PIC' : pic_name,
            'Nomor Telpon PIC': pic_num,
            'Jenis Device Lama':old_type,
            'Jenis Device Baru':new_type,
            'Pemegang Device Lama' : own_dev_old,
            'Pemegang Device Baru': own_dev_new
        }
        with st.spinner('Sedang Mengirimkan data ke Google Sheets....'):
            success, message = submit_gsheet(payload)
        
        if success:
            st.success(message)
        else:
            st.error(message)
