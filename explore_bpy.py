import bpy

bpy.app.binary_path = "/usr/bin/blender"


print(bpy.ops.wm.read_factory_settings())
print(bpy.ops.wm.read_homefile())
print(list(bpy.data.objects))
print(bpy.data.objects[0].name)
print(bpy.data.objects[1].name)
bpy.data.objects[1].name = "Hi"
print(bpy.data.objects[1].name)

mesh = bpy.data.meshes.new(name="MyMesh")

print(list(bpy.data.objects))
