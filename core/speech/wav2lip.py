import sys
import subprocess

class Wav2Lip():
  def __init__(self):
    pass

  def run(self, mp4_file, wav_file, output_file):
      wav2lip_path = "/app/Wav2Lip/inference.py"
      checkpoint_path = "/app/checkpoints/your-checkpoint.pth"  # Replace with your checkpoint path
      
      cmd = [
          "python",
          wav2lip_path,
          "--checkpoint_path",
          checkpoint_path,
          "--face",
          mp4_file,
          "--audio",
          wav_file,
          "--outfile",
          output_file,
      ]
      
      try:
          subprocess.run(cmd, check=True)
          print("Wav2Lip completed successfully.")
          return output_file
      except subprocess.CalledProcessError as e:
          print(f"Wav2Lip failed with error code {e.returncode}.")
          return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python wav2lip_wrapper.py <input_video.mp4> <input_audio.wav>")
        sys.exit(1)

    wav = Wav2Lip()
    input_video = sys.argv[1]
    input_audio = sys.argv[2]
    
    wav.run(input_video, input_audio)