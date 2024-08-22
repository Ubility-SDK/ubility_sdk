import re

def upload_local_file(params):
    try:
        if "file" in params and "fileName" in params and "size" in params:
            return {
                "file_binary_data":params["file"],
                "file_name":params["fileName"],
                "file_extension":params['extension'],
                "file_size":params["size"]
            }
    except Exception as error:
        raise Exception(error)
        