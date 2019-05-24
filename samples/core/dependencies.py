import gzip
import os
import shutil
from google_drive_downloader import GoogleDriveDownloader as gdd

import nltk

from core.path import Path
Path.create_dirs()
nltk.data.path.append(os.path.join(Path.bin, 'ntlk_data'))
nltk.download('stopwords', download_dir=os.path.join(Path.bin, 'ntlk_data'))

class DependenciesDownloader:
    def __init__(self):
        Path.create_bin()
        self.google_word2vec()
        self.ntlk()

    def ntlk(self):
        pass

    def google_word2vec(self):
        if not os.path.exists(Path.w2v_model) and not os.path.exists(Path.google_w2v_model):
            google_w2v_gz = os.path.join(Path.bin, 'GoogleNews-vectors-negative300.bin.gz')
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
            print("%s exists: %s" % (Path.w2v_model,os.path.exists(Path.w2v_model)))
            print("%s exists: %s" % (Path.google_w2v_model,os.path.exists(Path.google_w2v_model)))
