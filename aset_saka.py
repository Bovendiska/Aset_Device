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
            "private_key_id": "e9815b702481b331e280698d88e6bda83e68805d",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCt7K9jYb4mQGRB\nfocU6PP7tfVRQ5kUKjw9iIhFJw0DZiHWo9VKhDTgGHJdLVrIAGJFlMKz1c45hcBy\n1+AoP5Gp8lxLc8R+66mEjUzslJsU6eMlz+nQOjYlAuiMGa6SNDKH/0D1SD7Bp/dk\nKZRFvHjArKqZvK/9Pz6GPpInk2HhFTCe09vIEzaS0YyepJenhfsQ5lE+E1idVUN/\nTAcpXwKKJqD0xyPh9vJvX7ZMN3YaSd3rxArsHUOmkSLBtjw++iyq6Bs1zUyoqbsl\nf2HelKJm9Qu/glCnSJuphUHxm3inOkBjZu81/YTO4zk2ckGKF422X8ljpvZ2nxXV\naR0bAlutAgMBAAECggEAVgczL6y6sc/65xxvM4wQlspHiAUwNDW561Pb15y7xpkf\nlrwd9chUIR5mfyk+dJwf/7vX3L0eTvyWFxgpk67x3YZ4WYfvQzpM9Lgxuvm8hck0\nplDjnbAVdRQts5LGcyHndrZuyoSMKhzrdPtOEHprnh4qGnYm9NRyGFPd1j6D1SFj\nuFISRaDCR88Rbgt7SE0znE1qPlzYu7LeJn6FIWA4g0PpBv+Iv145pgn0n9MBssbp\nzcA21tVhttkn41kRtFlKC2Xa0rLPFFpMJ0F91utcrErCa1pyikwpHbstblmKm29N\nE7q+UaGAW0UlDbpEctc2s+UasSfAWnzlBwwzOAgtHwKBgQDzTId/X0zpmA4zokpd\n38uyIPKW0KHjPyy/s7EneiwlioEBjtlQhU2PQxnxb4/RpO/aVPKjZPBIed4C9qMP\n/8hn9hOkxjOA7tZJFMGSEzazr6csELfarwKfJgOPSMVhgcqefQlwSzRK131DyNni\nOewGXzd3W+2UqQY1LE64r7BlewKBgQC3AQeba2h4fyEkEtMdGGPSrjMdZq2zm/0a\n48z6BbvLPuyKj+Txeo+MLltInegRVMJJxjmNWO+PaU/Uprhs8QQYf45egss88WhS\n4wP0OJNtbvliPhhAzsuu1GU9Ly8TmLxwzHe84jQEP1aCWtlAH00BLociOOuXqwl5\n1dnRj5G29wKBgQCsRvZzJMJLbhYwTaynCD8uZNIiJJ1dUnCXVeANeh8kfgyXU9Vh\nhOLEnNkT8tE9u7LzQM+HD4RtbY3dP1N7kr0PkFmchZQWqggmO4JNszk6xxhyxWvK\nd749fydqIDdTshoNW7CBSV8/15KlmuVdoXIVmPqnk/qJF56DrFoZwJ4BXQKBgBTa\nfS9ssd7pPbGKo5vxJ47eYty60phg8hqaUsU62gdzCClR9FjACpOCxMwlkkhHTExz\n1iMRO1swOPSWevWPEVRpVKPYa6hqKeUoEU9HEyWpO6nCQalA51zovxCVy9uD0BVa\nd1qCvEKvpP/9sjvoVTIJR0TTD6Wcy9uiTsvefFBJAoGAcq4CRvlueJ5t8GuooJmT\nQcw+vgpEaWy+7PIvyQiFPM4K56Ovo+Oe2NNq6UZHp+UjlFv6oOOpzQi0BJYNxP7H\nGq/JJCFUKFqJ5pZA+sGZ8voczxJojdaOL+Kl4CsazSgtEpypZfq8U3ktXvrE7Ac0\nLzkWKfj2/U9d9iFNqpfHY2U=\n-----END PRIVATE KEY-----\n",
            "client_email": "aset-device@streamlit-aset.iam.gserviceaccount.com",
            "client_id": "117660315058839628089",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/aset-device%40streamlit-aset.iam.gserviceaccount.com",
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
