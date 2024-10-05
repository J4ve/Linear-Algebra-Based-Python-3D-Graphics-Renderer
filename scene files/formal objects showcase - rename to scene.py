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

        crate1 = Cube(app, tex_id=1, pos=(-3, 0, 0), scale=(1, 1, 1))
        add(crate1)

        crate2 = Cube(app, tex_id=2, pos=(0, 0, 0), scale=(1, 1, 1))
        add(crate2)

        crate3 = Cube(app, tex_id=0, pos=(3, 0, 0), scale=(1, 1, 1))
        add(crate3)
        
        rotating_cube = RotatingCube(app, tex_id=3, pos=(0, 0, -30), scale=(5, 5, 5),)
        add(rotating_cube)


        


        app.camera.selected_object = crate1


    def render(self):
        for obj in self.objects:
            obj.render()
