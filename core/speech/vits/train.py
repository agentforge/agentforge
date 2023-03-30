import subprocess

AUDIO_FOLDER_PATH = "../drive/MyDrive/long_audios/"
subprocess.run(f"cp {AUDIO_FOLDER_PATH}/* ./raw_audio/", shell=True)

VIDEO_FOLDER_PATH = "../drive/MyDrive/videos/"
subprocess.run(f"cp {VIDEO_FOLDER_PATH}/* ./video_data/", shell=True)

subprocess.run("python video2audio.py", shell=True)
subprocess.run("python denoise_audio.py", shell=True)
subprocess.run("python long_audio_transcribe.py --languages \"{PRETRAINED_MODEL}\" --whisper_size large", shell=True)
subprocess.run("python short_audio_transcribe.py --languages \"{PRETRAINED_MODEL}\" --whisper_size large", shell=True)

ADD_AUXILIARY = True
PRETRAINED_MODEL = "CJE"

if ADD_AUXILIARY:
    subprocess.run(f"python preprocess_v2.py --add_auxiliary_data True --languages \"{PRETRAINED_MODEL}\"", shell=True)
else:
    subprocess.run(f"python preprocess_v2.py --languages \"{PRETRAINED_MODEL}\"", shell=True)

subprocess.run("tensorboard --logdir \"./OUTPUT_MODEL\"", shell=True)
Maximum_epochs = "40"
subprocess.run(f"python finetune_speaker_v2.py -m \"./OUTPUT_MODEL\" --max_epochs \"{Maximum_epochs}\" --drop_speaker_embed True", shell=True)
