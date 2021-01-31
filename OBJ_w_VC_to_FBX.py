import sys
import os
import traceback
import trimesh
import numpy as np

import FbxCommon
from fbx import *


def create_fbx_mesh_node(manager: FbxManager, scene: FbxScene, mesh: trimesh.base.Trimesh):

    # create node and its attribute
    fbx_mesh = FbxMesh.Create(manager, "Mesh")
    fbx_mesh_node = FbxNode.Create(manager, "Mesh_Node")
    fbx_mesh_node.SetNodeAttribute(fbx_mesh)
    fbx_mesh_node.SetShadingMode(FbxNode.eFullShading)

    # add material
    black = FbxDouble3(0, 0, 0)
    white = FbxDouble3(1, 1, 1)
    fbx_surface_phong = FbxSurfacePhong.Create(manager, "material")
    fbx_surface_phong.Reflection.Set(black)     # TODO: It seems these property settings returns false (fails)
    fbx_surface_phong.Specular.Set(black)
    fbx_surface_phong.Bump.Set(white)
    fbx_mesh_node.AddMaterial(fbx_surface_phong)

    # Add Control Points (Vertices)
    fbx_mesh.InitControlPoints(len(mesh.vertices))
    for i, v in enumerate(mesh.vertices):
        fbx_mesh.SetControlPointAt(FbxVector4(v[0], v[1], v[2], 1.0), i)

    # Add Polygon
    for i, f in enumerate(mesh.faces):
        fbx_mesh.BeginPolygon(0)
        for val in f:
            fbx_mesh.AddPolygon(val)
        fbx_mesh.EndPolygon()

    # Create Layer
    fbx_mesh.CreateLayer()
    layer = fbx_mesh.GetLayer(0)

    # set normals
    fbx_mesh_normals = FbxLayerElementNormal.Create(fbx_mesh, "")
    fbx_mesh_normals.SetMappingMode(FbxLayerElement.eByControlPoint)
    fbx_mesh_normals.SetReferenceMode(FbxLayerElement.eDirect)
    for normal in mesh.vertex_normals:
        fbx_mesh_normals.GetDirectArray().Add(FbxVector4(normal[0], normal[1], normal[2], 1.0))
    layer.SetNormals(fbx_mesh_normals)

    # set vertex colors
    fbx_mesh_vc = FbxLayerElementVertexColor.Create(fbx_mesh, "")
    fbx_mesh_vc.SetMappingMode(FbxLayerElement.eByControlPoint)
    fbx_mesh_vc.SetReferenceMode(FbxLayerElement.eDirect)
    for vc in mesh.visual.vertex_colors:
        fbx_mesh_vc.GetDirectArray().Add(FbxColor(vc[0]/255, vc[1]/255, vc[2]/255))
    layer.SetVertexColors(fbx_mesh_vc)

    # LayerElementPolygonGroup
    # fbx_mesh_polygroups = FbxLayerElementPolygonGroup.Create(fbx_mesh, "")
    # fbx_mesh_polygroups.SetMappingMode(FbxLayerElement.eByPolygon)
    # fbx_mesh_polygroups.SetReferenceMode(FbxLayerElement.eIndex)
    # for _ in range(len(mesh.faces)):
    #     fbx_mesh_polygroups.GetIndexArray().Add(0)
    # layer.SetPolygonGroups(fbx_mesh_polygroups)

    # LayerElementMaterial
    # fbx_mesh_material = FbxLayerElementMaterial.Create(fbx_mesh, "")
    # fbx_mesh_material.SetMappingMode(FbxLayerElement.eByPolygon)
    # fbx_mesh_material.SetReferenceMode(FbxLayerElement.eIndexToDirect)
    # layer.SetMaterials(fbx_mesh_material)

    return fbx_mesh_node

if __name__ == "__main__":

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # check if the extension is .fbx
    output_ext = os.path.splitext(output_path)[-1]
    if output_ext != ".fbx":
        try:
            raise Exception("Unsupported file extension {0}".format(output_ext))
        except:
            traceback.print_exc()
            exit(0)
    
    # load mesh
    mesh = trimesh.load_mesh(input_path)

    # initialize fbx manager and scene
    manager, scene = FbxCommon.InitializeSdkObjects()
    
    # create mesh node and add to the scene
    fbx_mesh_node = create_fbx_mesh_node(manager, scene, mesh)
    scene.GetRootNode().AddChild(fbx_mesh_node)

    # export
    FbxCommon.SaveScene(manager, scene, output_path, pFileFormat=0)
