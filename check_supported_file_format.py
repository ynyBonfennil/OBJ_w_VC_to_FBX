"""
This script is from the following article.
https://qiita.com/segur/items/75428cb98b8a28c687e3
"""

import FbxCommon


if __name__ == "__main__":
    manager, scene = FbxCommon.InitializeSdkObjects()

    # supported file format for FbxImporter
    print("Supported File Format for FbxImporter")
    for pFileFormat in range(manager.GetIOPluginRegistry().GetReaderFormatCount()):
        description = manager.GetIOPluginRegistry().GetReaderFormatDescription(pFileFormat)
        print(pFileFormat, description)
    
    # supported file format for FbxExporter
    print("")
    print("Supported File Format for FbxExporter")
    for pFileFormat in range(manager.GetIOPluginRegistry().GetWriterFormatCount()):
        description = manager.GetIOPluginRegistry().GetWriterFormatDescription(pFileFormat)
        print(pFileFormat, description)
