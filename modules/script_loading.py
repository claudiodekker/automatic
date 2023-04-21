import os
import importlib.util
import modules.errors as errors


def load_module(path, ignore_errors: bool = False):
    module_spec = importlib.util.spec_from_file_location(os.path.basename(path), path)
    module = importlib.util.module_from_spec(module_spec)
    try:
        module_spec.loader.exec_module(module)
    except Exception as e:
        if not ignore_errors:
            errors.display(e, f'Module load: {path}')
    return module


def preload_extensions(extensions_dir, parser):
    if not os.path.isdir(extensions_dir):
        return

    for dirname in sorted(os.listdir(extensions_dir)):
        preload_script = os.path.join(extensions_dir, dirname, "preload.py")
        if not os.path.isfile(preload_script):
            continue
        try:
            module = load_module(preload_script, ignore_errors = True)
            if hasattr(module, 'preload'):
                module.preload(parser)
        except Exception as e:
            errors.display(e, f'Extension preload: {preload_script}')
