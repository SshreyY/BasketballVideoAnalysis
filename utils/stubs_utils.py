import os
import pickle

def save_stub(stub_path, object):
    if not os.path.exists(os.path.dirname(stub_path)):
        os.makedirs(os.path.dirname(stub_path))

    if stub_path is not None:
        with open(stub_path, "wb") as f:
            pickle.dump(object, f)

def read_stub(read_from_stub, stub_path):
    if read_from_stub and stub_path is not None and os.path.exists(stub_path):
        with open(stub_path, "rb") as f:
            object = pickle.load(f)
            # Clean up any numpy types in the loaded data
            object = _clean_numpy_types(object)
            return object
    return None

def _clean_numpy_types(obj):
    """Recursively convert numpy types to Python types in the object."""
    import numpy as np
    
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, list):
        return [_clean_numpy_types(item) for item in obj]
    elif isinstance(obj, dict):
        return {_clean_numpy_types(key): _clean_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, tuple):
        return tuple(_clean_numpy_types(item) for item in obj)
    else:
        return obj