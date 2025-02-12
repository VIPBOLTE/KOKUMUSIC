import glob
import importlib
import logging
import os
import shutil
import subprocess
import sys
from os.path import abspath, dirname, isfile, join

from config import EXTRA_PLUGINS, EXTRA_PLUGINS_FOLDER, EXTRA_PLUGINS_REPO
from KOKUMUSIC import LOGGER

logger = LOGGER(__name__)

# Check and remove previous extra plugin folder if it exists
if EXTRA_PLUGINS_FOLDER in os.listdir():
    shutil.rmtree(EXTRA_PLUGINS_FOLDER)

# Check and remove "utils" folder if it exists
if "utils" in os.listdir():
    shutil.rmtree("utils")

# Set root directory
ROOT_DIR = abspath(join(dirname(__file__), "..", ".."))

# Path to external plugin repository
EXTERNAL_REPO_PATH = join(ROOT_DIR, EXTRA_PLUGINS_FOLDER)

# Check if extra plugins are enabled
extra_plugins_enabled = EXTRA_PLUGINS.lower() == "true"

# Clone the external plugin repository if extra plugins are enabled and not already cloned
if extra_plugins_enabled:
    if not os.path.exists(EXTERNAL_REPO_PATH):
        with open(os.devnull, "w") as devnull:
            clone_result = subprocess.run(
                ["git", "clone", EXTRA_PLUGINS_REPO, EXTERNAL_REPO_PATH],
                stdout=devnull,
                stderr=subprocess.PIPE,
            )
            if clone_result.returncode != 0:
                logger.error(
                    f"Error cloning external plugins repository: {clone_result.stderr.decode()}"
                )

    # Move "utils" from external repo to main repo if it exists
    utils_source_path = join(EXTERNAL_REPO_PATH, "utils")
    utils_target_path = join(ROOT_DIR, "utils")
    if os.path.isdir(utils_source_path):
        if not os.path.exists(utils_target_path):
            os.rename(utils_source_path, utils_target_path)
        else:
            for root, dirs, files in os.walk(utils_source_path):
                relative_path = os.path.relpath(root, utils_source_path)
                target_dir = os.path.join(utils_target_path, relative_path)
                os.makedirs(target_dir, exist_ok=True)
                for file in files:
                    source_file = os.path.join(root, file)
                    target_file = os.path.join(target_dir, file)
                    if not os.path.exists(target_file):
                        os.rename(source_file, target_file)

    if os.path.isdir(utils_target_path):
        sys.path.append(utils_target_path)

    # Install requirements from "requirements.txt" in external repo if it exists
    requirements_path = join(EXTERNAL_REPO_PATH, "requirements.txt")
    if os.path.isfile(requirements_path):
        with open(os.devnull, "w") as devnull:
            install_result = subprocess.run(
                ["pip", "install", "-r", requirements_path],
                stdout=devnull,
                stderr=subprocess.PIPE,
            )
            if install_result.returncode != 0:
                logger.error(
                    f"Error installing requirements for external plugins: {install_result.stderr.decode()}"
                )


def __list_all_modules():
    # Get the main repo directory for plugins
    main_repo_plugins_dir = dirname(__file__)
    work_dirs = [main_repo_plugins_dir]

    if extra_plugins_enabled:
        logger.info("Loading extra plugins...")
        work_dirs.append(join(EXTERNAL_REPO_PATH, "plugins"))

    all_modules = []

    # Loop through all plugin directories and find Python modules
    for work_dir in work_dirs:
        mod_paths = glob.glob(join(work_dir, "*.py"))
        mod_paths += glob.glob(join(work_dir, "*/*.py"))

        modules = [
            (
                (
                    (f.replace(main_repo_plugins_dir, "KOKUMUSIC.plugins")).replace(
                        EXTERNAL_REPO_PATH, EXTRA_PLUGINS_FOLDER
                    )
                ).replace(os.sep, ".")
            )[:-3]  # Remove the ".py" extension
            for f in mod_paths
            if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
        ]
        all_modules.extend(modules)

    return all_modules


# Get all modules from both main repo and external plugins
ALL_MODULES = sorted(__list_all_modules())

# Import the PLUGINS_MODULES from your plugin initialization file
from plugins import PLUGINS_MODULES  # Update the path as per your repo structure

# Combine the modules from main repo and external plugins
ALL_MODULES += PLUGINS_MODULES

# Define __all__ for public interface
__all__ = ALL_MODULES + ["ALL_MODULES"]

# Now, dynamically import and run each module
for module_name in ALL_MODULES:
    try:
        # Dynamically import the module
        module = importlib.import_module(module_name)
        logger.info(f"Successfully imported module: {module_name}")
        
        # If the module has an 'initialize' method (or another method you want to run)
        if hasattr(module, 'initialize'):
            module.initialize()  # Initialize the module if it has such a method
        else:
            logger.warning(f"Module {module_name} does not have an 'initialize' method.")
            
    except Exception as e:
        logger.error(f"Failed to load module {module_name}: {str(e)}")
