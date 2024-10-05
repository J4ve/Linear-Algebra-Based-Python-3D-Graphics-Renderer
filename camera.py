import glm
import pygame as pg


FOV = 50  # deg
NEAR = 0.1
FAR = 100
SPEED = 0.005
SENSITIVITY = 0.04


class Camera:
    def __init__(self, app, position=(0, 0, 4), yaw=-90, pitch=0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        # view matrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        self.m_proj = self.get_projection_matrix()
        self.mouse_locked = True  # Initially lock the mouse control
        self.toggle_pressed = False  # Flag to check if toggle key is pressed
        self.toggle_key = pg.K_SPACE  # Assign the toggle key (SPACE key) to a variable
        self.toggle_cooldown = 500  # Cooldown time in milliseconds (adjust as needed)
        self.last_toggle_time = 0  # Initialize the last toggle time
        self.object_switch_cooldown = 500  # Cooldown time for object selection in milliseconds
        self.last_object_switch_time = 0  # Initialize the last object switch time



    def cycle_selected_object(self, objects):
        current_time = pg.time.get_ticks()
        keys = pg.key.get_pressed()

        if keys[pg.K_PAGEUP] or keys[pg.K_LEFT]:
            self.handle_object_switch(objects, -1)

        elif keys[pg.K_PAGEDOWN] or keys[pg.K_RIGHT]:
            self.handle_object_switch(objects, 1)

    def handle_object_switch(self, objects, direction):
        current_time = pg.time.get_ticks()

        if current_time - self.last_object_switch_time > self.object_switch_cooldown:
            if self.selected_object is None:
                self.selected_object = objects[0]
            else:
                index = objects.index(self.selected_object)
                index = (index + direction) % len(objects)
                self.selected_object = objects[index]

            self.last_object_switch_time = current_time

    def rotate(self):
        if not self.mouse_locked:
            return  # If the mouse is locked, don't update camera rotation
        
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def toggle_mouse_lock(self):
        current_time = pg.time.get_ticks()  # Get the current time in milliseconds
        keys = pg.key.get_pressed()

        if keys[self.toggle_key] and current_time - self.last_toggle_time > self.toggle_cooldown:
            self.mouse_locked = not self.mouse_locked
            pg.mouse.set_visible(not self.mouse_locked)
            pg.event.set_grab(self.mouse_locked)
            self.last_toggle_time = current_time  # Update the last toggle time


    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()
        
        self.toggle_mouse_lock()  # Moved outside of event loop

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    # Add an exit condition if needed
                    pg.quit()
                    sys.exit()

        # Call cycle_selected_object to cycle through selected objects
        self.cycle_selected_object(self.app.scene.objects)
        self.handle_user_input()  # Handle user input for object manipulation

    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_e]:
            self.position += self.up * velocity
        if keys[pg.K_q]:
            self.position -= self.up * velocity

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)

    def handle_user_input(self):
        keys = pg.key.get_pressed()
        # Check if selected_object is not None before manipulating it
        if self.selected_object is not None:
            # Reset everything
            if keys[pg.K_TAB]:
                self.selected_object.scale = glm.vec3(1, 1, 1)
                self.selected_object.rot = glm.vec3(0, 0, 0)
                self.selected_object.shear = glm.vec3(0, 0, 0)
            # Translation controls
            if keys[pg.K_i]:
                # Move the selected object up along the y-axis
                self.selected_object.pos += glm.vec3(0, 0.1, 0)
            if keys[pg.K_k]:
                # Move the selected object down along the y-axis
                self.selected_object.pos += glm.vec3(0, -0.1, 0)
            if keys[pg.K_j]:
                # Move the selected object left along the x-axis
                self.selected_object.pos += glm.vec3(-0.1, 0, 0)
            if keys[pg.K_l]:
                # Move the selected object right along the x-axis
                self.selected_object.pos += glm.vec3(0.1, 0, 0)
            if keys[pg.K_o]:
                # Move the selected object forward along the z-axis
                self.selected_object.pos += glm.vec3(0, 0, -0.1)
            if keys[pg.K_u]:
                # Move the selected object backward along the z-axis
                self.selected_object.pos += glm.vec3(0, 0, 0.1)

            # Rotation controls
            if keys[pg.K_r]:
                # Rotate the selected object around the x-axis
                self.selected_object.rot += glm.vec3(0.1, 0, 0)
            if keys[pg.K_t]:
                # Rotate the selected object around the y-axis
                self.selected_object.rot += glm.vec3(0, 0.1, 0)
            if keys[pg.K_y]:
                # Rotate the selected object around the z-axis
                self.selected_object.rot += glm.vec3(0, 0, 0.1)
            if keys[pg.K_f]:
                # Rotate the selected object around the x-axis reverse
                self.selected_object.rot -= glm.vec3(0.1, 0, 0)
            if keys[pg.K_g]:
                # Rotate the selected object around the y-axis reverse
                self.selected_object.rot -= glm.vec3(0, 0.1, 0)
            if keys[pg.K_h]:
                # Rotate the selected object around the z-axis reverse
                self.selected_object.rot -= glm.vec3(0, 0, 0.1)
            

            # Scaling controls
            if keys[pg.K_z]:
                # Increase the scale of the selected object
                self.selected_object.scale += glm.vec3(0.1, 0.1, 0.1)
            if keys[pg.K_x]:
                # Decrease the scale of the selected object
                self.selected_object.scale -= glm.vec3(0.1, 0.1, 0.1)
            if keys[pg.K_F1]:
                # Increase the scale of the selected object x axis
                self.selected_object.scale += glm.vec3(0.1, 0, 0)
            if keys[pg.K_F2]:
                # Increase the scale of the selected object y axis
                self.selected_object.scale += glm.vec3(0, 0.1, 0)
            if keys[pg.K_F3]:
                # Increase the scale of the selected object z axis
                self.selected_object.scale += glm.vec3(0, 0, 0.1)
            if keys[pg.K_F4]:
                # Decrease the scale of the selected object x axis
                self.selected_object.scale -= glm.vec3(0.1, 0, 0)
            if keys[pg.K_F5]:
                # Decrease the scale of the selected object y axis
                self.selected_object.scale -= glm.vec3(0, 0.1, 0)
            if keys[pg.K_F6]:
                # Decrease the scale of the selected object z axis
                self.selected_object.scale -= glm.vec3(0, 0, 0.1)
            # Shearing controls
            if keys[pg.K_1]:
                # Shear the selected object around the x-axis
                self.selected_object.shear += glm.vec3(0.1, 0, 0)
            if keys[pg.K_2]:
                # Shear the selected object around the y-axis
                self.selected_object.shear += glm.vec3(0, 0.1, 0)
            if keys[pg.K_3]:
                # Shear the selected object around the z-axis
                self.selected_object.shear += glm.vec3(0, 0, 0.1)
            if keys[pg.K_4]:
            # Shear the selected object around the x-axis reverse
                self.selected_object.shear -= glm.vec3(0.1, 0, 0)
            if keys[pg.K_5]:
                # Shear the selected object around the y-axis reverse
                self.selected_object.shear -= glm.vec3(0, 0.1, 0)
            if keys[pg.K_6]:
                # Shear the selected object around the z-axis reverse
                self.selected_object.shear -= glm.vec3(0, 0, 0.1)


    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()
        self.toggle_mouse_lock()
        self.handle_user_input()  # New method to handle user input for object manipulation
