from vbo import VBO
from shader_program import ShaderProgram


class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        # rotating cube vao
        self.vaos['rotatingcube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['rotatingcube'])
        
        #original cube na vao
        self.vaos['cube'] = self.get_vao(
        program=self.program.programs['default'],
        vbo = self.vbo.vbos['cube'])

        #ak47 vao
        self.vaos['ak47'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['ak47'])
        
        #cat vao
        self.vaos['cat'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['cat'])
        
        #real cat vao
        self.vaos['realcat'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['realcat'])

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()