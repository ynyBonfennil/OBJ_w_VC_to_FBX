# Wavefront OBJ with Vertex Color to FBX

Python script to convert Wavefront OBJ with Vertex Color to FBX. Texture coordinate is not supported.

## Prerequisites

### FBX SDK Python Biindings

This script requires FBX SDK Python Bindings, which can be downloaded from Autodesk developer network.

- [Autodesk FBX Software Developer Kit](https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-2)

It might be confusing because there is a SDK named "FBX Python SDK" along with FBX Python Bindings. In short, we're not going to use FBX Python SDK here because it supports only Python 2.7 and Python 3.3 (which is out of date for 2021). Instead, by using FBX Python Bindings, you can build Python SDK for your own Python version. If you build it with Python3.9, then you can get Python SDK for Python 3.9.

Once you download FBX SDK and FBX Python Bindings, install FBX SDK first, then install FBX Python Bindings. There are some documentation for building them inside their downloaded files.

### Other libraries

- trimesh
- numpy

## How wo use

Run the following comamnd.

```sh
$ python ./OBJ_w_VC_to_FBX.py {input file path} {output file path}
```

### FBX binary / FBX ascii

FBX SDK supports multiple file format for importing and exporting (it also supports .obj, although it doesn't read vertex colors of it). If you want to export as FBX ascii, please change the following line.

```py
# export as FBX binary
FbxCommon.SaveScene(manager, scene, output_path, pFileFormat=0)

# export as FBX ascii
FbxCommon.SaveScene(manager, scene, output_path, pFileFormat=1)
```

Which `pFileFormat` value corresponds to which file format can vary depending on your FBX SDK versions. You can also check it by running `check_supported_file_format.py`.

## Reference

<http://docs.autodesk.com/FBX/2014/ENU/FBX-SDK-Documentation/index.html?url=files/GUID-452768B5-7A4F-45BD-AC37-DC1A034DCF3B.htm,topicNumber=d30e10431>
