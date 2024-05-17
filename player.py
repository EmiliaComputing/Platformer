import arcade

class Player(arcade.Sprite):
    def __init__(self, filename, scaling):
        super().__init__(filename, scaling)
        self.change_direction()

    #add change of direction
    def change_direction(self):
        self.textures = []

        texture = arcade.load_texture(":resources:images/enemies/frog.png")
        self.textures.append(texture)
        texture = arcade.load_texture(":resources:images/enemies/frog.png",
                                          flipped_horizontally=True)
        self.textures.append(texture)

        self.texture = texture

    def on_update(self, deltatime):
        pass
            
