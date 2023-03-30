import os
import shutil

# Set in dockerfiles
src_path = "/app/agent_n/web/public/videos"
dst_path = "/app/cache"

def startup():
  # Iterate through all files in the source directory
  for file in os.listdir(src_path):
    # Check if the file is an mp4 video
    if file.endswith(".mp4"):
        # Create the full source and destination file paths
        src_file = os.path.join(src_path, file)
        dst_file = os.path.join(dst_path, file)

        # Copy the file, overwriting if it already exists
        shutil.copy2(src_file, dst_file)