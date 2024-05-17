import arcade

class Enemy2(arcade.Sprite):
    def __init__(self, filename, scaling):
        super().__init__(filename, scaling)
        self.change_direction()

    def change_direction(self):
        texture = arcade.load_texture(":resources:images/enemies/bee.png")
        self.textures.append(texture)
        texture = arcade.load_texture(":resources:images/enemies/bee.png",
                                          flipped_horizontally=True)
        self.textures.append(texture)

        self.texture = texture

    def on_update(self, deltatime):
        pass
