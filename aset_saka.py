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
st.write('Untuk mengetahui detail aset serta kebedaan aset device.')
st.markdown("-------")

st.header('Detail Aset')

device_name = st.text_input('Jenis Device*', help ='Contoh : Dell Latitude 3450')
pic_name = st.text_input('Nama PIC*', help = 'Nama Penanggung Jawab')
device_type = st.selectbox('Tipe Device', ['PC','Notebook'])
status = st.selectbox('Status Aset',['Sudah Diambil IT','Belum Diambil IT'], key = 'status_aset')


if st.session_state.status_aset == 'Belum Diambil IT':
    letak_aset = st.text_input('Dimana Letak Aset Tersebut?')
else:
    letak_aset = st.text_input('Di Terima oleh siapa?')
    
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
