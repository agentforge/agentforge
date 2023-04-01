import os
import json
from historica.config import Config

class Avatar:
    def __init__(self, folder_path='/avatars'):
        self.avatar_config = {}
        self.config = Config(None)
        self.load_avatars(self.config.CONFIG_DIR + folder_path)

    def load_avatars(self, folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.json'):
                with open(os.path.join(folder_path, file_name), 'r') as f:
                    avatar_data = json.load(f)
                    avatar_key = avatar_data.get('avatar')
                    if avatar_key:
                        self.avatar_config[avatar_key] = avatar_data

    def get_avatar(self, avatar_key):
        return self.avatar_config.get(avatar_key)

    def set_avatar(self, avatar_key, avatar_data):
        self.avatar_config[avatar_key] = avatar_data

def main():
    avatar_instance = Avatar()
    makhno_avatar = avatar_instance.get_avatar('makhno')
    print(makhno_avatar)

if __name__ == '__main__':
    main()
