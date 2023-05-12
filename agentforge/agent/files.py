import os
import uuid
from werkzeug.utils import secure_filename

def secure_wav_filename(filename):
    """
    Returns a secure filename for a WAV file using a UUID string.
    """
    # get the file extension
    ext = os.path.splitext(filename)[1]
    # generate a unique filename using UUID
    new_filename = str(uuid.uuid4()) + ext
    # return a secure filename using Werkzeug's secure_filename function
    return secure_filename(new_filename)