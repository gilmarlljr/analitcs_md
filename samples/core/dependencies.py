import gzip
import os
import shutil

import requests
from google_drive_downloader import GoogleDriveDownloader as gdd

import nltk

from core.path import Path

Path.create_dirs()
nltk.data.path.append(os.path.join(Path.bin_dir, 'ntlk_data'))
nltk.download('stopwords', download_dir=os.path.join(Path.bin_dir, 'ntlk_data'))
nltk.download('punkt', download_dir=os.path.join(Path.bin_dir, 'ntlk_data'))
java_path = "C:/Program Files (x86)/Java/jdk1.8.0_191/bin/java.exe"
os.environ['JAVAHOME'] = java_path
from clint.textui import progress


class DependenciesDownloader:
    def __init__(self):
        Path.create_bin()
        # self.google_word2vec()
        self.ntlk()
        self.stanford_models()

    def ntlk(self):
        pass

    def google_word2vec(self):
        if not os.path.exists(Path.w2v_model) and not os.path.exists(Path.google_w2v_model):
            google_w2v_gz = os.path.join(Path.bin_dir, 'GoogleNews-vectors-negative300.bin.gz')
            google_w2v_gz_size = 1647046227
            if not os.path.exists(google_w2v_gz) or (
                    os.path.exists(google_w2v_gz) and os.stat(google_w2v_gz).st_size != google_w2v_gz_size):
                gdd.download_file_from_google_drive(file_id='0B7XkCwpI5KDYNlNUTTlSS21pQmM',
                                                    dest_path=google_w2v_gz,
                                                    showsize=True,
                                                    overwrite=True)
            print("Unziping %s... " % google_w2v_gz)
            with gzip.open(google_w2v_gz, 'rb') as f_in:
                with open(Path.google_w2v_model, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print("Done")
        else:
            print("%s exists: %s" % (Path.w2v_model, os.path.exists(Path.w2v_model)))
            print("%s exists: %s" % (Path.google_w2v_model, os.path.exists(Path.google_w2v_model)))

    def stanford_models(self):
        if not os.path.exists(Path.stanford_models_dir):
            file_pos = os.path.join(Path.bin_dir, 'stanford-pos.zip')
            file_pos_size = 26260468
            if not os.path.exists(file_pos):
                url_pos = 'https://nlp.stanford.edu/software/stanford-postagger-2018-10-16.zip'
                request = requests.get(url_pos, stream=True)
                with open(file_pos, "wb") as pos:
                    total_length = int(request.headers.get('content-length'))
                    for ch in progress.bar(request.iter_content(chunk_size=1024),
                                           expected_size=(total_length / 1024) + 1, label='stanford-pos.zip', ):
                        if ch:
                            pos.write(ch)
                print(os.stat(file_pos).st_size)

            file_ner = os.path.join(Path.bin_dir, 'stanford-ner.zip')
            file_ner_size = 180358328
            if not os.path.exists(file_ner):
                url_ner = 'https://nlp.stanford.edu/software/stanford-ner-2018-10-16.zip'
                request = requests.get(url_ner, stream=True)
                with open(file_pos, "wb") as ner:
                    total_length = int(request.headers.get('content-length'))
                    for ch in progress.bar(request.iter_content(chunk_size=1024),
                                           expected_size=(total_length / 1024) + 1, label='stanford-ner.zip', ):
                        if ch:
                            ner.write(ch)
                print(os.stat(file_ner).st_size)

            # print("Unziping %s... " % google_w2v_gz)
            # with gzip.open(google_w2v_gz, 'rb') as f_in:
            #     with open(Path.google_w2v_model, 'wb') as f_out:
            #         shutil.copyfileobj(f_in, f_out)
            print("Done")
        # else:
        # print("%s exists: %s" % (Path.w2v_model, os.path.exists(Path.w2v_model)))
        # print("%s exists: %s" % (Path.google_w2v_model, os.path.exists(Path.google_w2v_model)))


if __name__ == '__main__':
    DependenciesDownloader()
