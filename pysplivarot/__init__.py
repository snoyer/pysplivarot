try :
    from _pysplivarot import *
except ImportError as e :
    import os
    txt_path = os.path.join(os.path.dirname(__file__), 'ld_library_path')
    if os.path.isfile(txt_path):
        ld_library_path = open(txt_path).read().strip()
        raise ImportError(
            str(e) + ' (library path was `%s` at compile time)' % ld_library_path
        )
    else:
        raise
