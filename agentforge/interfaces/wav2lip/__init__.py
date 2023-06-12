from .resource import Wav2LipModel
from .hparams import hparams as hp
from . import audio
from . import face_detection
from .models import Wav2Lip

__all__ = [
'Wav2LipModel',
'Wav2Lip',
'hp',
'audio',
'face_detection',
'Wav2Lip'
]