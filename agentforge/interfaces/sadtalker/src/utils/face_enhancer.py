import os
import torch 

from gfpgan import GFPGANer

from tqdm import tqdm

from agentforge.interfaces.sadtalker.src.utils.videoio import load_video_to_cv2



def enhancer(images, method='gfpgan', bg_upsampler='realesrgan'):
    print('face enhancer....')
    if os.path.isfile(images): # handle video to images
        images = load_video_to_cv2(images)

    # ------------------------ set up GFPGAN restorer ------------------------
    if  method == 'gfpgan':
        arch = 'clean'
        channel_multiplier = 2
        model_name = 'GFPGANv1.4'
        url = 'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth'
    elif method == 'RestoreFormer':
        arch = 'RestoreFormer'
        channel_multiplier = 2
        model_name = 'RestoreFormer'
        url = 'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/RestoreFormer.pth'
    elif method == 'codeformer':
        arch = 'CodeFormer'
        channel_multiplier = 2
        model_name = 'CodeFormer'
        url = 'https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth'
    else:
        raise ValueError(f'Wrong model version {method}.')


    # ------------------------ set up background upsampler ------------------------
    if bg_upsampler == 'realesrgan':
        if not torch.cuda.is_available():  # CPU
            import warnings
            warnings.warn('The unoptimized RealESRGAN is slow on CPU. We do not use it. '
                          'If you really want to use it, please modify the corresponding codes.')
            bg_upsampler = None
        else:
            from basicsr.archs.rrdbnet_arch import RRDBNet
            from realesrgan import RealESRGANer
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
            bg_upsampler = RealESRGANer(
                scale=2,
                model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth',
                model=model,
                tile=400,
                tile_pad=10,
                pre_pad=0,
                half=True)  # need to set False in CPU mode
    else:
        bg_upsampler = None

    # determine model paths
    model_path = os.path.join('gfpgan/weights', model_name + '.pth')

    if not os.path.isfile(model_path):
        model_path = os.path.join('checkpoints', model_name + '.pth')
    
    if not os.path.isfile(model_path):
        # download pre-trained models from url
        model_path = url

    restorer = GFPGANer(
        model_path=model_path,
        upscale=2,
        arch=arch,
        channel_multiplier=channel_multiplier,
        bg_upsampler=bg_upsampler)

    # ------------------------ restore ------------------------
    restored_img = [] 
    for idx in tqdm(range(len(images)), 'Face Enhancer:'):
        
        # restore faces and background if necessary
        cropped_faces, restored_faces, r_img = restorer.enhance(
            images[idx],
            has_aligned=False,
            only_center_face=False,
            paste_back=True)
        
        restored_img += [r_img]
       
    return restored_img
