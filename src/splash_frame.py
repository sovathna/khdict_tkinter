import tkinter as tk
from tkinter import ttk
import requests
import zipfile
import os
import sys
import pathlib
import uuid
import threading
import dbm
import concurrent.futures
import time


class SplashFrame(ttk.Frame):

    def __init__(self, master=None, on_downloaded=None):
        super().__init__(master=master)
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.columnconfigure(0, weight=1)
        self.rowconfigure([0, 4], weight=1)

        self.on_downloaded = on_downloaded

        self.label_title = ttk.Label(self)
        self.label_title.grid(row=1, column=0)

        self.progress_bar = ttk.Progressbar(
            self, mode='indeterminate', orient=tk.HORIZONTAL, maximum=1)
        self.progress_bar.grid(row=2, column=0, sticky=tk.EW, padx=64, pady=16)
        self.progress_bar.start()
        self.label_sub_title = ttk.Label(self, text='Loading...')
        self.label_sub_title.grid(row=3, column=0, sticky=tk.E, padx=64)

        # if self._should_download():
        self.label_title['text'] = 'កំពុងទាញយកយកទិន្នន័យលើកដំបូង សូមមេត្តារង់ចាំ...!'
        threading.Thread(target=self._download_db_file).start()
        # else:
        #     self._set_progress_value(1)

    def _set_progress_value(self, value=1.0):
        self.progress_bar.stop()
        self.progress_bar['mode'] = 'determinate'
        self.progress_bar['value'] = value
        self.label_sub_title['text'] = '{:.0f}%'.format(value*100)

    def _on_downloaded(self):
        if self.on_downloaded:
            self.on_downloaded()

    def _should_download(self):
        return os.path.exists(f'{self._appDataDir()}{os.pathsep}data.sqlite')

    def _download_db_file(self):
        db_url = 'https://raw.githubusercontent.com/sovathna/database/main/data.zip'
        response = requests.get(db_url, stream=True)

        tmp_file_name = self._tmpFile()
        print('tmp file:', tmp_file_name)
        size = int(response.headers.get('content-length', 0))
        with open(tmp_file_name, 'wb') as fd:
            total_downloaded = 0
            last = time.perf_counter()
            for chunk in response.iter_content(chunk_size=1024*8):
                fd.write(chunk)
                total_downloaded = total_downloaded + len(chunk)
                now = time.perf_counter()
                if now - last >= 0.2:
                    last = now
                    self._set_progress_value(total_downloaded/size)
            self._set_progress_value(1.0)
            self._extract_db_file(tmp_file_name)

    def _extract_db_file(self, filename):

        with zipfile.ZipFile(filename) as zip:
            data_dir = self._appDataDir()
            print(data_dir)
            zip.extractall(data_dir)
            self._on_downloaded()

    def _tmpFile(self):
        tmp_file_name = str(uuid.uuid4())
        if sys.platform == 'win32':
            return f"{os.getenv('TEMP')}\\{tmp_file_name}.tmp"
        else:
            return f'/var/tmp/{tmp_file_name}'

    def _appDataDir(self):
        if sys.platform == 'win32':
            return f"{os.getenv('APPDATA')}\\io.github.sovathna.khdicttkinter"
        elif sys.platform == 'linux':
            return f'{pathlib.Path().home()}/.local/share/io.github.sovathna.khdicttkinter'
        else:
            return f'{pathlib.Path().home()}/Library/Application Support/io.github.sovathna.khdicttkinter'
