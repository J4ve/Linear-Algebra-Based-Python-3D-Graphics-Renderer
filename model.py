import moderngl as mgl
import numpy as np
import glm


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), shear=(0, 0, 0)):
        self.app = app
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.shear = glm.vec3(shear)
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        
        # translate
        m_model = glm.translate(m_model, self.pos)
       
        # rotate
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        
        # scale
        m_model = glm.scale(m_model, self.scale)

        #shearing
        shearing_matrix = glm.mat4(1.0)  # Identity matrix

        # Modify the shearing matrix to apply shearing along x, y, and z axes
        shearing_matrix = glm.mat4(
            1.0, self.shear.x, self.shear.y, 0.0,
            self.shear.x, 1.0, self.shear.z, 0.0,
            self.shear.y, self.shear.z, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0
        )
        # Multiply the model matrix by the shearing matrix
        m_model *= shearing_matrix

        return m_model

    def render(self):
        self.update()
        self.vao.render()


class RotatingCube(BaseModel):
    def __init__(self, app, vao_name='rotatingcube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), shear=(0, 0, 0)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, shear)
        self.rotation_speed = glm.radians(0.1) # set lng yung speed dito sa parameter na glmradians thingy (degrees per sec)
        self.on_init()

    def update(self):
        delta_time = self.app.clock.get_time()  # nakalagay sa main yung get_time function lol
        angle_change = self.rotation_speed * delta_time  # Calculate angle change based on time
        self.rot += glm.vec3(0, angle_change, 0)  # Increment rotation around the y-axis

        # Update the model matrix with the new rotation
        self.m_model = self.get_model_matrix()
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)

class Cube(BaseModel):
    def __init__(self, app, vao_name='rotatingcube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), shear=(0, 0, 0)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, shear)
        self.rotation_speed = glm.radians(0.0) # set lng yung speed dito sa parameter na glmradians thingy (degrees per sec)
        self.on_init()

    def update(self):
        delta_time = self.app.clock.get_time()  # nakalagay sa main yung get_time function lol
        angle_change = self.rotation_speed * delta_time  # Calculate angle change based on time
        self.rot += glm.vec3(0, angle_change, 0)  # Increment rotation around the y-axis

        # Update the model matrix with the new rotation
        self.m_model = self.get_model_matrix()
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)

class Ak47(BaseModel):
    def __init__(self, app, vao_name='ak47', tex_id='ak47',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.rotation_speed = glm.radians(0.0)  # Set the initial rotation speed here
        self.on_init()

    def update(self):
        delta_time = self.app.clock.get_time()  # Get the time difference
        angle_change = self.rotation_speed * delta_time  # Calculate the angle change based on time

        # Increment the rotation around the y-axis (similar to the rotating cube)
        self.rot += glm.vec3(0, angle_change, 0)

        # Update the model matrix with the new rotation
        self.m_model = self.get_model_matrix()

        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)


class Cat(BaseModel):
    def __init__(self, app, vao_name='cat', tex_id='cat',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.rotation_speed = glm.radians(0.0)  # Set the initial rotation speed here
        self.on_init()

    def update(self):
        delta_time = self.app.clock.get_time()  # Get the time difference
        angle_change = self.rotation_speed * delta_time  # Calculate the angle change based on time

        # Increment the rotation around the y-axis (similar to the rotating cube)
        self.rot += glm.vec3(0, angle_change, 0)

        # Update the model matrix with the new rotation
        self.m_model = self.get_model_matrix()

        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)

class RealCat(BaseModel):
    def __init__(self, app, vao_name='realcat', tex_id='realcat',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.rotation_speed = glm.radians(0.0)  # Set the initial rotation speed here
        self.on_init()

    def update(self):
        delta_time = self.app.clock.get_time()  # Get the time difference
        angle_change = self.rotation_speed * delta_time  # Calculate the angle change based on time

        # Increment the rotation around the y-axis (similar to the rotating cube)
        self.rot += glm.vec3(0, angle_change, 0)

        # Update the model matrix with the new rotation
        self.m_model = self.get_model_matrix()

        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)











