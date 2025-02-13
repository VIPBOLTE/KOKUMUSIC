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

# Clean up any existing directories
if EXTRA_PLUGINS_FOLDER in os.listdir():
    shutil.rmtree(EXTRA_PLUGINS_FOLDER)

if "utils" in os.listdir():
    shutil.rmtree("utils")

ROOT_DIR = abspath(join(dirname(__file__), "..", ".."))

EXTERNAL_REPO_PATH = join(ROOT_DIR, EXTRA_PLUGINS_FOLDER)

# Check if extra plugins are enabled
extra_plugins_enabled = EXTRA_PLUGINS.lower() == "true"

# If external plugins are enabled, clone the repo and install dependencies
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

    # Handle the utils folder from the external repo
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

    # Add the utils folder to the system path
    if os.path.isdir(utils_target_path):
        sys.path.append(utils_target_path)

    # Install any requirements from the external repo
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
    all_modules = []
    main_repo_plugins_dir = dirname(__file__)

    # Process main repository plugins
    main_mod_paths = glob.glob(join(main_repo_plugins_dir, "*.py"))
    main_mod_paths += glob.glob(join(main_repo_plugins_dir, "*/*.py"))
    main_modules = [
        f.replace(main_repo_plugins_dir, "KOKUMUSIC.plugins").replace(os.sep, ".")[:-3]
        for f in main_mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]
    all_modules.extend(main_modules)

    # Process external plugins if enabled
    if extra_plugins_enabled:
        external_plugins_dir = join(EXTERNAL_REPO_PATH, "plugins")  # Ensure this path is correct
        plugins_init_path = join(external_plugins_dir, "__init__.py")

        # Ensure the plugins directory and init.py exists
        if os.path.isfile(plugins_init_path):
            logger.info(f"Found __init__.py in {external_plugins_dir}")

            try:
                # Add the external repo to the system path
                sys.path.append(EXTERNAL_REPO_PATH)

                # Ensure plugins module can be found
                import plugins

                # Try importing PLUGINS_MODULES from the external repo
                from plugins import PLUGINS_MODULES
                external_modules = [
                    f"{EXTRA_PLUGINS_FOLDER}.{mod}"
                    for mod in PLUGINS_MODULES
                ]
                all_modules.extend(external_modules)
                logger.info(f"Successfully loaded external plugins from PLUGINS_MODULES: {PLUGINS_MODULES}")
            except ImportError as e:
                logger.error(f"Failed to import PLUGINS_MODULES: {e}")
                # Fallback to globbing
                external_mod_paths = glob.glob(join(external_plugins_dir, "*.py"))
                external_mod_paths += glob.glob(join(external_plugins_dir, "*/*.py"))
                external_modules = [
                    f.replace(EXTERNAL_REPO_PATH, EXTRA_PLUGINS_FOLDER).replace(os.sep, ".")[:-3]
                    for f in external_mod_paths
                    if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
                ]
                all_modules.extend(external_modules)
            except Exception as e:
                logger.error(f"Unexpected error loading external plugins: {e}")
        else:
            logger.error(f"__init__.py not found in {external_plugins_dir}")
            # Fallback if __init__.py is missing
            external_mod_paths = glob.glob(join(external_plugins_dir, "*.py"))
            external_mod_paths += glob.glob(join(external_plugins_dir, "*/*.py"))
            external_modules = [
                f.replace(EXTERNAL_REPO_PATH, EXTRA_PLUGINS_FOLDER).replace(os.sep, ".")[:-3]
                for f in external_mod_paths
                if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
            ]
            all_modules.extend(external_modules)

    return sorted(all_modules)


ALL_MODULES = __list_all_modules()

# Expose the modules
__all__ = ALL_MODULES + ["ALL_MODULES"]

# Optional debugging: print the sys.path to check if plugins directory is included
print(sys.path)
