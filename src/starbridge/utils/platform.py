import os


def patch_for_homebrew_libs():
    os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = (
        f"{os.getenv('HOMEBREW_PREFIX', '/opt/homebrew')}/lib/"
    )
