def __init__(self):

    self.light = Light()
    self.music = Music()
    self.tv = TV()

    self.actions = {
        "Open_Palm": self.light_on,
        "Closed_Fist": self.light_off,
        "Thumb_Up": self.music_on,
        "Victory": self.tv_mode
    }