import glob
import importlib
import os
import shutil
import subprocess
import sys
from os.path import abspath, dirname, isfile, join

from config import EXTRA_PLUGINS, EXTRA_PLUGINS_FOLDER, EXTRA_PLUGINS_REPO
from KOKUMUSIC import LOGGER

logger = LOGGER(__name__)

# Cleanup previous installations
if EXTRA_PLUGINS_FOLDER in os.listdir():
    shutil.rmtree(EXTRA_PLUGINS_FOLDER)

if "utils" in os.listdir():
    shutil.rmtree("utils")

ROOT_DIR = abspath(join(dirname(__file__), "..", ".."))
EXTERNAL_REPO_PATH = join(ROOT_DIR, EXTRA_PLUGINS_FOLDER)
sys.path.insert(0, ROOT_DIR)

extra_plugins_enabled = EXTRA_PLUGINS.lower() == "true"

# Clone external repository
if extra_plugins_enabled:
    if not os.path.exists(EXTERNAL_REPO_PATH):
        result = subprocess.run(
            ["git", "clone", EXTRA_PLUGINS_REPO, EXTERNAL_REPO_PATH],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"Clone failed: {result.stderr}")

    # Handle utils directory
    utils_src = join(EXTERNAL_REPO_PATH, "utils")
    utils_dest = join(ROOT_DIR, "utils")
    if os.path.exists(utils_src):
        shutil.rmtree(utils_dest, ignore_errors=True)
        shutil.copytree(utils_src, utils_dest)
        sys.path.append(utils_dest)

    # Install requirements
    req_file = join(EXTERNAL_REPO_PATH, "requirements.txt")
    if os.path.isfile(req_file):
        result = subprocess.run(
            ["pip", "install", "-r", req_file],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"Requirements error: {result.stderr}")

def __list_all_modules():
    local_plugins_dir = join(ROOT_DIR, "KOKUMUSIC", "plugins")
    external_plugins_dir = join(EXTERNAL_REPO_PATH, "plugins")
    
    search_dirs = [local_plugins_dir]
    if extra_plugins_enabled:
        search_dirs.append(external_plugins_dir)

    all_modules = []
    
    for plugins_dir in search_dirs:
        if not os.path.exists(plugins_dir):
            continue
            
        # Find all Python files recursively
        for py_path in glob.glob(join(plugins_dir, "**/*.py"), recursive=True):
            if "__init__.py" in py_path:
                continue

            # Convert path to module format
            rel_path = os.path.relpath(py_path, plugins_dir)
            module_name = rel_path.replace(os.sep, ".")[:-3]  # Remove .py
            
            if plugins_dir == local_plugins_dir:
                full_module = f"KOKUMUSIC.plugins.{module_name}"
            else:
                full_module = f"{EXTRA_PLUGINS_FOLDER}.plugins.{module_name}"
            
            all_modules.append(full_module)

    return sorted(all_modules)

ALL_MODULES = __list_all_modules()

# Dynamic import from external plugins' __init__.py
if extra_plugins_enabled:
    try:
        # Import from external plugins directory
        external_plugins = importlib.import_module(f"{EXTRA_PLUGINS_FOLDER}.plugins")
        if hasattr(external_plugins, "PLUGINS_MODULES"):
            ALL_MODULES.extend(external_plugins.PLUGINS_MODULES)
            logger.info(f"Loaded {len(external_plugins.PLUGINS_MODULES)} external plugins")
    except Exception as e:
        logger.error(f"External plugins init error: {str(e)}")

__all__ = ALL_MODULES + ["ALL_MODULES"]
