import os
import sys
import torch
from time import strftime
from agentforge.interfaces.sadtalker.src.utils.preprocess import CropAndExtract
from agentforge.interfaces.sadtalker.src import Audio2Coeff
from agentforge.interfaces.sadtalker.src.facerender import AnimateFromCoeff
from agentforge.interfaces.sadtalker.third_part.GFPGAN import GFPGANer
from agentforge.interfaces.sadtalker.third_part.GPEN import FaceEnhancement

class SadTalker():
  def __init__(self) -> None:
      
    # Read environment variables
    driven_audio = os.environ.get('DRIVEN_AUDIO', './examples/driven_audio/bus_chinese.wav')
    source_video = os.environ.get('SOURCE_VIDEO', './examples/source_image/input.mp4')

    self.checkpoint_dir = os.environ.get('CHECKPOINT_DIR', './checkpoints')
    self.result_dir = os.environ.get('RESULT_DIR', './results')
    self.batch_size = int(os.environ.get('BATCH_SIZE', 1))
    self.enhancer_region = os.environ.get('ENHANCER', 'lip')
    
    cpu = os.environ.get('CPU', 'False').lower() in ['true', '1', 'yes']

    self.use_DAIN = os.environ.get('USE_DAIN', 'False').lower() in ['true', '1', 'yes']

    # Remaining variables
    save_dir = os.path.join(self.result_dir, strftime("%Y_%m_%d_%H.%M.%S"))
    os.makedirs(save_dir, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() and not cpu else "cpu"
    current_code_path = sys.argv[0]
    current_root_path = os.pathCropAndExtract.split(current_code_path)[0]
    os.environ['TORCH_HOME'] = os.path.join(current_root_path, self.checkpoint_dir)

    path_of_lm_croper = os.path.join(current_root_path, self.checkpoint_dir, 'shape_predictor_68_face_landmarks.dat')
    path_of_net_recon_model = os.path.join(current_root_path, self.checkpoint_dir, 'epoch_20.pth')
    dir_of_BFM_fitting = os.path.join(current_root_path, self.checkpoint_dir, 'BFM_Fitting')
    wav2lip_checkpoint = os.path.join(current_root_path, self.checkpoint_dir, 'wav2lip.pth')

    audio2pose_checkpoint = os.path.join(current_root_path, self.checkpoint_dir, 'auido2pose_00140-model.pth')
    audio2pose_yaml_path = os.path.join(current_root_path, 'src', 'config', 'auido2pose.yaml')

    audio2exp_checkpoint = os.path.join(current_root_path, self.checkpoint_dir, 'auido2exp_00300-model.pth')
    audio2exp_yaml_path = os.path.join(current_root_path, 'src', 'config', 'auido2exp.yaml')

    free_view_checkpoint = os.path.join(current_root_path, self.checkpoint_dir, 'facevid2vid_00189-model.pth.tar')

    mapping_checkpoint = os.path.join(current_root_path, self.checkpoint_dir, 'mapping_00109-model.pth.tar')
    facerender_yaml_path = os.path.join(current_root_path, 'src', 'config', 'facerender_still.yaml')

    # init model
    print(path_of_net_recon_model)
    self.preprocess_model = CropAndExtract(path_of_lm_croper, path_of_net_recon_model, dir_of_BFM_fitting, device)

    print(audio2pose_checkpoint)
    print(audio2exp_checkpoint)
    self.audio_to_coeff = Audio2Coeff(audio2pose_checkpoint, audio2pose_yaml_path, audio2exp_checkpoint, audio2exp_yaml_path, wav2lip_checkpoint, device)

    print(free_view_checkpoint)
    print(mapping_checkpoint)
    self.animate_from_coeff = AnimateFromCoeff(free_view_checkpoint, mapping_checkpoint, facerender_yaml_path, device)

    self.restorer_model = GFPGANer(model_path='checkpoints/GFPGANv1.3.pth', upscale=1, arch='clean',
                              channel_multiplier=2, bg_upsampler=None)
    self.enhancer_model = FaceEnhancement(base_dir='checkpoints', size=512, model='GPEN-BFR-512', use_sr=False,
                                    sr_model='rrdb_realesrnet_psnr', channel_multiplier=2, narrow=1, device=device)


  def load(self, source_video: str):
    # crop image and extract 3dmm from image
    first_frame_dir = os.path.join(self.save_dir, 'first_frame_dir')
    os.makedirs(first_frame_dir, exist_ok=True)
    print('3DMM Extraction for source image')
    first_coeff_path, crop_pic_path, crop_info = self.preprocess_model.generate(source_video, first_frame_dir)
    if first_coeff_path is None:
        print("Can't get the coeffs of the input")
        return

  def synthesizer(self, text, filename, speaker_wav=None, speaker_idx=0):
    # audio2ceoff
    batch = get_data(first_coeff_path, audio_path, device)
    coeff_path = audio_to_coeff.generate(batch, save_dir)
    # coeff2video
    data = get_facerender_data(coeff_path, crop_pic_path, first_coeff_path, audio_path, batch_size, device)
    tmp_path, new_audio_path, return_path = animate_from_coeff.generate(data, save_dir, pic_path, crop_info,
                                                                        restorer_model, enhancer_model, enhancer_region)
    torch.cuda.empty_cache()
    if args.use_DAIN:
        import paddle
        from src.dain_model import dain_predictor
        paddle.enable_static()
        predictor_dian = dain_predictor.DAINPredictor(args.dian_output, weight_path=args.DAIN_weight,
                                                      time_step=args.time_step,
                                                      remove_duplicates=args.remove_duplicates)
        frames_path, temp_video_path = predictor_dian.run(tmp_path)
        paddle.disable_static()
        save_path = return_path[:-4] + '_dain.mp4'
        command = r'ffmpeg -y -i "%s" -i "%s" -vcodec copy "%s"' % (temp_video_path, new_audio_path, save_path)
        os.system(command)
    os.remove(tmp_path)
