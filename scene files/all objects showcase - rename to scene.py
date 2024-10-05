from model import *



class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        #ikot sa y axis


        # di gumagalaw
        sean = Cube(app, tex_id=4, pos=(-30, 0, -20), scale=(3, 3, 3))
        add(sean)

        jave = Cube(app, tex_id=5, pos=(-20, 0, -20), scale=(3, 3, 3))
        add(jave)

        gab = Cube(app, tex_id=6, pos=(-10, 0, -20), scale=(3, 3, 3))
        add(gab)

        kenji = Cube(app, tex_id=7, pos=(0, 0, -20), scale=(3, 3, 3))
        add(kenji)

        remar = Cube(app, tex_id=8, pos=(10, 0, -20), scale=(3, 3, 3))
        add(remar)

        carl = Cube(app, tex_id=9, pos=(20, 0, -20), scale=(3, 3, 3))
        add(carl)

        crate1 = Cube(app, tex_id=1, pos=(-2, 0, 0), scale=(1, 1, 1))
        add(crate1)

        crate2 = Cube(app, tex_id=2, pos=(0, 0, 0), scale=(1, 1, 1))
        add(crate2)

        crate3 = Cube(app, tex_id=0, pos=(2, 0, 0), scale=(1, 1, 1))
        add(crate3)
        
        rotating_cube = RotatingCube(app, tex_id=3, pos=(0, 0, -30), scale=(5, 5, 5),)
        add(rotating_cube)

        ak47 = Ak47(app, pos=(-20, -5, -60), scale=(0.2,0.2,0.2), rot=(-5,0,0))
        add(ak47)

        cat = Cat(app, pos=(0, 0, -60), scale=(1, 1, 1))
        add(cat)

        realisticcat = RealCat(app, pos=(20, 0, -60), scale=(1, 1, 1))
        add(realisticcat)

        


        app.camera.selected_object = sean


    def render(self):
        for obj in self.objects:
            obj.render()
