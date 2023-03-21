from os import listdir, path
import numpy as np
import cv2, os
from core.wav2lip import audio
import subprocess
from tqdm import tqdm
import torch, face_detection
from models import Wav2Lip
import platform

class Wav2LipModel():
  def __init__(self, checkpoint_path, opts={}) -> None:
    MyNamespace = type('MyNamespace', (object,), {})
    self.args = MyNamespace()
    self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
    self.checkpoint_path = checkpoint_path
    self.outfile = opts['outfile'] if 'outfile' in opts else 'results/result_voice.mp4'
    
    self.static = False if 'static' not in opts else opts['static']
    self.fps = 25.0 if 'fps' not in opts else opts['fps']
    
    self.pads = opts['pads'] if 'pads' in opts else [0, 10, 0, 0]
    
    self.face_det_batch_size = 16 if 'face_det_batch_size' not in opts else opts['face_det_batch_size']
    self.wav2lip_batch_size = 128 if 'wav2lip_batch_size' not in opts else opts['wav2lip_batch_size']
    
    self.resize_factor = 1 if 'resize_factor' not in opts else opts['resize_factor']
    
    self.crop = opts['crop'] if 'crop' in opts else [0, -1, 0, -1]
    
    self.box = opts['box'] if 'box' in opts else [-1, -1, -1, -1]
    
    self.rotate = False if 'rotate' not in opts else opts['rotate']
    self.nosmooth = False if 'nosmooth' not in opts else opts['nosmooth']

    self.mel_step_size = 16
    print('Using {} for inference.'.format(self.device))

    self.model = self.load_model(self.args.checkpoint_path)
    print ("Model loaded")

    if os.path.isfile(self.args.face) and self.args.face.split('.')[1] in ['jpg', 'png', 'jpeg']:
      self.args.static = True

  def run(self, opts={}):
    self.args.face = opts['face'] if 'face' in opts else 'results/test.mp4'
    self.args.audio = opts['audio'] if 'audio' in opts else 'results/test.wav'
    self.args.outfile = opts['outfile'] if 'outfile' in opts else 'results/result_voice.mp4'
    self.main()

  def get_smoothened_boxes(boxes, T):
    for i in range(len(boxes)):
      if i + T > len(boxes):
        window = boxes[len(boxes) - T:]
      else:
        window = boxes[i : i + T]
      boxes[i] = np.mean(window, axis=0)
    return boxes

  def face_detect(self, images):
    detector = face_detection.FaceAlignment(face_detection.LandmarksType._2D, 
                        flip_input=False, device=self.device)

    batch_size = self.args.face_det_batch_size
    
    while 1:
      predictions = []
      try:
        for i in tqdm(range(0, len(images), batch_size)):
          predictions.extend(detector.get_detections_for_batch(np.array(images[i:i + batch_size])))
      except RuntimeError:
        if batch_size == 1: 
          raise RuntimeError('Image too big to run face detection on GPU. Please use the --resize_factor argument')
        batch_size //= 2
        print('Recovering from OOM error; New batch size: {}'.format(batch_size))
        continue
      break

    results = []
    pady1, pady2, padx1, padx2 = self.args.pads
    for rect, image in zip(predictions, images):
      if rect is None:
        cv2.imwrite('temp/faulty_frame.jpg', image) # check this frame where the face was not detected.
        raise ValueError('Face not detected! Ensure the video contains a face in all the frames.')

      y1 = max(0, rect[1] - pady1)
      y2 = min(image.shape[0], rect[3] + pady2)
      x1 = max(0, rect[0] - padx1)
      x2 = min(image.shape[1], rect[2] + padx2)
      
      results.append([x1, y1, x2, y2])

    boxes = np.array(results)
    if not self.args.nosmooth: boxes = self.get_smoothened_boxes(boxes, T=5)
    results = [[image[y1: y2, x1:x2], (y1, y2, x1, x2)] for image, (x1, y1, x2, y2) in zip(images, boxes)]

    del detector
    return results 

  def datagen(self, frames, mels):
    img_batch, mel_batch, frame_batch, coords_batch = [], [], [], []

    if self.args.box[0] == -1:
      if not self.args.static:
        face_det_results = self.face_detect(frames) # BGR2RGB for CNN face detection
      else:
        face_det_results = self.face_detect([frames[0]])
    else:
      print('Using the specified bounding box instead of face detection...')
      y1, y2, x1, x2 = self.args.box
      face_det_results = [[f[y1: y2, x1:x2], (y1, y2, x1, x2)] for f in frames]

    for i, m in enumerate(mels):
      idx = 0 if self.args.static else i%len(frames)
      frame_to_save = frames[idx].copy()
      face, coords = face_det_results[idx].copy()

      face = cv2.resize(face, (self.args.img_size, self.args.img_size))
        
      img_batch.append(face)
      mel_batch.append(m)
      frame_batch.append(frame_to_save)
      coords_batch.append(coords)

      if len(img_batch) >= self.args.wav2lip_batch_size:
        img_batch, mel_batch = np.asarray(img_batch), np.asarray(mel_batch)

        img_masked = img_batch.copy()
        img_masked[:, self.args.img_size//2:] = 0

        img_batch = np.concatenate((img_masked, img_batch), axis=3) / 255.
        mel_batch = np.reshape(mel_batch, [len(mel_batch), mel_batch.shape[1], mel_batch.shape[2], 1])

        yield img_batch, mel_batch, frame_batch, coords_batch
        img_batch, mel_batch, frame_batch, coords_batch = [], [], [], []

    if len(img_batch) > 0:
      img_batch, mel_batch = np.asarray(img_batch), np.asarray(mel_batch)

      img_masked = img_batch.copy()
      img_masked[:, self.args.img_size//2:] = 0

      img_batch = np.concatenate((img_masked, img_batch), axis=3) / 255.
      mel_batch = np.reshape(mel_batch, [len(mel_batch), mel_batch.shape[1], mel_batch.shape[2], 1])

      yield img_batch, mel_batch, frame_batch, coords_batch

  def _load(self, checkpoint_path):
    if self.device == 'cuda':
      checkpoint = torch.load(checkpoint_path)
    else:
      checkpoint = torch.load(checkpoint_path,
                  map_location=lambda storage, loc: storage)
    return checkpoint

  def load_model(self, path):
    model = Wav2Lip()
    print("Load checkpoint from: {}".format(path))
    checkpoint = self._load(path)
    s = checkpoint["state_dict"]
    new_s = {}
    for k, v in s.items():
      new_s[k.replace('module.', '')] = v
    model.load_state_dict(new_s)

    model = model.to(self.device)
    return model.eval()

  def main(self):
    if not os.path.isfile(self.args.face):
      raise ValueError('--face argument must be a valid path to video/image file')

    elif self.args.face.split('.')[1] in ['jpg', 'png', 'jpeg']:
      full_frames = [cv2.imread(self.args.face)]
      fps = self.args.fps

    else:
      video_stream = cv2.VideoCapture(self.args.face)
      fps = video_stream.get(cv2.CAP_PROP_FPS)

      print('Reading video frames...')

      full_frames = []
      while 1:
        still_reading, frame = video_stream.read()
        if not still_reading:
          video_stream.release()
          break
        if self.args.resize_factor > 1:
          frame = cv2.resize(frame, (frame.shape[1]//self.args.resize_factor, frame.shape[0]//self.args.resize_factor))

        if self.args.rotate:
          frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)

        y1, y2, x1, x2 = self.args.crop
        if x2 == -1: x2 = frame.shape[1]
        if y2 == -1: y2 = frame.shape[0]

        frame = frame[y1:y2, x1:x2]

        full_frames.append(frame)

    print ("Number of frames available for inference: "+str(len(full_frames)))

    if not self.args.audio.endswith('.wav'):
      print('Extracting raw audio...')
      command = 'ffmpeg -y -i {} -strict -2 {}'.format(self.args.audio, 'temp/temp.wav')

      subprocess.call(command, shell=True)
      self.args.audio = 'temp/temp.wav'

    wav = audio.load_wav(self.args.audio, 16000)
    mel = audio.melspectrogram(wav)
    print(mel.shape)

    if np.isnan(mel.reshape(-1)).sum() > 0:
      raise ValueError('Mel contains nan! Using a TTS voice? Add a small epsilon noise to the wav file and try again')

    mel_chunks = []
    mel_idx_multiplier = 80./fps 
    i = 0
    while 1:
      start_idx = int(i * mel_idx_multiplier)
      if start_idx + self.mel_step_size > len(mel[0]):
        mel_chunks.append(mel[:, len(mel[0]) - self.mel_step_size:])
        break
      mel_chunks.append(mel[:, start_idx : start_idx + self.mel_step_size])
      i += 1

    print("Length of mel chunks: {}".format(len(mel_chunks)))

    full_frames = full_frames[:len(mel_chunks)]

    batch_size = self.args.wav2lip_batch_size
    gen = self.datagen(full_frames.copy(), mel_chunks)

    for i, (img_batch, mel_batch, frames, coords) in enumerate(tqdm(gen, 
                        total=int(np.ceil(float(len(mel_chunks))/batch_size)))):
      if i == 0:
        frame_h, frame_w = full_frames[0].shape[:-1]
        out = cv2.VideoWriter('temp/result.avi', 
                    cv2.VideoWriter_fourcc(*'DIVX'), fps, (frame_w, frame_h))

      img_batch = torch.FloatTensor(np.transpose(img_batch, (0, 3, 1, 2))).to(self.device)
      mel_batch = torch.FloatTensor(np.transpose(mel_batch, (0, 3, 1, 2))).to(self.device)

      with torch.no_grad():
        pred = self.model(mel_batch, img_batch)

      pred = pred.cpu().numpy().transpose(0, 2, 3, 1) * 255.
      
      for p, f, c in zip(pred, frames, coords):
        y1, y2, x1, x2 = c
        p = cv2.resize(p.astype(np.uint8), (x2 - x1, y2 - y1))

        f[y1:y2, x1:x2] = p
        out.write(f)

    out.release()

    command = 'ffmpeg -y -i {} -i {} -strict -2 -q:v 1 {}'.format(self.args.audio, 'temp/result.avi', self.args.outfile)
    subprocess.call(command, shell=platform.system() != 'Windows')

if __name__ == '__main__':
  pass
  # w2lip = Wav2Lip2()
