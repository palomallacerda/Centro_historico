from enum import Enum
from pathlib import Path
from object import Object
import os

class Flag(Enum):
    o = 0
    v = 1
    vn = 2
    vt = 3
    f = 4

class Loader:

    def __init__(self):
        self.objects = []

    def load_from_file(self, file_name: str):
        v = []
        vt = []
        vn = []

        tam_v = 0
        tam_vt = 0
        tam_vn = 0

        file_path = Path(__file__).parent.parent / "Centro_historico" / file_name
        with open(file_path, "r") as file:
            while (line := file.readline()):
                first_space_location = line.find(" ")
                flag = line[0:first_space_location]
                parsed_line = line[first_space_location + 1:].split(" ")

                if flag == Flag.o.name:
                    object_name = parsed_line[0].replace('\n', "")
                    self.objects.append(Object(object_name))
                    tam_v += len(v)
                    tam_vt += len(vt)
                    tam_vn += len(vn)

                    del v
                    del vt
                    del vn

                    v = []
                    vt = []
                    vn = []


                elif flag == Flag.v.name:
                    l = [float(n) for n in parsed_line] # [x, y, z] in blender
                    l[1], l[2] = l[2], l[1] # [x, -y, z] => [x, z, -y] opengl
                    l[0] = -l[0] # this fix the inverted screen bug
                    v.append(l)

                elif flag == Flag.vn.name: # [nx, ny, nz]
                    l = [float(n) for n in parsed_line]
                    vn.append(l)

                elif flag == Flag.vt.name:
                    l = [float(n) for n in parsed_line] # [s, t]
                    vt.append(l)

                elif flag == Flag.f.name:
                    # trim the last \n if it exists
                    parsed_line[-1] = parsed_line[-1].replace('\n', "")

                    # a face is three vertices v/vt/vn in the form
                    # [../../.., ../../.., ../../.., ...]

                    face_vertices = []
                    face_normals = []
                    face_textures = []

                    for vertex in parsed_line:
                        # vertex = v/vt/vn

                        l = []
                        for n in vertex.split("/"):
                            if n == "": # if the vt is empty
                                n = None
                            else:
                                n = int(n) - 1 
                            l.append(n)

                        face_vertices.append(v[ l[0] - tam_v])
                        face_normals.append(vn[ l[2] - tam_vn])

                        if l[1] is not None:
                            face_textures.append(vt[ l[1] - tam_vt])
                        else:
                            face_textures.append(None)

                    self.objects[-1].faces.append([face_vertices, face_textures,
                    face_normals])
