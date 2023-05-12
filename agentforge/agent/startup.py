import os
import shutil
from agentforge import VIDEO_SRC_PATH, DST_PATH

def startup():
  # Iterate through all files in the source directory
  for file in os.listdir(VIDEO_SRC_PATH):
    # Check if the file is an mp4 video
    if file.endswith(".mp4"):
        # Create the full source and destination file paths
        src_file = os.path.join(VIDEO_SRC_PATH, file)
        dst_file = os.path.join(DST_PATH, file)

        # Copy the file, overwriting if it already exists
        shutil.copy2(src_file, dst_file)