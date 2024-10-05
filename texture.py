import pygame as pg
import moderngl as mgl


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/img.png')
        self.textures[1] = self.get_texture(path='textures/img_1.png')
        self.textures[2] = self.get_texture(path='textures/img_2.png')
        self.textures[3] = self.get_texture(path='textures/mcdiamond.png')
        self.textures[4] = self.get_texture(path='textures/seanmc.png')
        self.textures[5] = self.get_texture(path='textures/jave.png')
        self.textures[6] = self.get_texture(path='textures/gab.png')
        self.textures[7] = self.get_texture(path='textures/kenji.png')
        self.textures[8] = self.get_texture(path='textures/remar.png')
        self.textures[9] = self.get_texture(path='textures/carl.png')
        self.textures['ak47'] = self.get_texture(path='objects/ak47/color.tga')
        self.textures['cat'] = self.get_texture(path='objects/cat/20430_cat_diff_v1.jpg')
        self.textures['realcat'] = self.get_texture(path='objects/realcat/Cat_diffuse.jpg')


    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # AF
        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
