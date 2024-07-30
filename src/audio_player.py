import subprocess
import os


class AudioPlayer:
    def __init__(self, volume=50):
        self.volume = volume

    def set_volume(self, volume):
        self.volume = volume
        subprocess.run(['amixer', 'sset', 'PCM', f'{self.volume}%'], check=True)

    def play_audio(self, file_path=None):
        if not file_path:
            file_path = self.get_scream_file_path()
        subprocess.run(['mpg123', file_path], check=True)

    def get_scream_file_path(self):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), './assets/scream.mp3'))


if __name__ == '__main__':
    player = AudioPlayer(volume=75)
    player.set_volume(50)
    player.play_audio()
