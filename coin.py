import arcade

class Coin(arcade.Sprite):
    def __init__(self, filename, scaling):
        super().__init__(filename, scaling)

    def on_update(self, deltatime):
        pass
