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

# Paths setup
ROOT_DIR = abspath(join(dirname(__file__), "..", ".."))
EXTERNAL_REPO_PATH = join(ROOT_DIR, EXTRA_PLUGINS_FOLDER)

# Flag for external plugins
extra_plugins_enabled = EXTRA_PLUGINS.lower() == "true"

# Clone the external repo if required
if extra_plugins_enabled:
    if not os.path.exists(EXTERNAL_REPO_PATH):
        with open(os.devnull, "w") as devnull:
            clone_result = subprocess.run(
                ["git", "clone", EXTRA_PLUGINS_REPO, EXTERNAL_REPO_PATH],
                stdout=devnull,
                stderr=subprocess.PIPE,
            )
            if clone_result.returncode != 0:
                logger.error(f"Error cloning external plugins repository: {clone_result.stderr.decode()}")

    # Handling utils folder
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

    # Install requirements for external plugins
    requirements_path = join(EXTERNAL_REPO_PATH, "requirements.txt")
    if os.path.isfile(requirements_path):
        with open(os.devnull, "w") as devnull:
            install_result = subprocess.run(
                ["pip", "install", "-r", requirements_path],
                stdout=devnull,
                stderr=subprocess.PIPE,
            )
            if install_result.returncode != 0:
                logger.error(f"Error installing requirements for external plugins: {install_result.stderr.decode()}")


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
        external_plugins_dir = join(EXTERNAL_REPO_PATH, "plugins")  # Ensure the 'plugins' folder is here
        plugins_init_path = join(external_plugins_dir, "__init__.py")
        
        # Check for __init__.py in the external plugin folder
        if os.path.isfile(plugins_init_path):
            try:
                sys.path.append(EXTERNAL_REPO_PATH)
                from plugins import PLUGINS_MODULES
                external_modules = [f"{EXTRA_PLUGINS_FOLDER}.{mod}" for mod in PLUGINS_MODULES]
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
            # No __init__.py found in the external repo, fallback to globbing
            external_mod_paths = glob.glob(join(external_plugins_dir, "*.py"))
            external_mod_paths += glob.glob(join(external_plugins_dir, "*/*.py"))
            external_modules = [
                f.replace(EXTERNAL_REPO_PATH, EXTRA_PLUGINS_FOLDER).replace(os.sep, ".")[:-3]
                for f in external_mod_paths
                if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
            ]
            all_modules.extend(external_modules)

    return sorted(all_modules)


def import_plugin_module(module_name):
    """Import the plugin module by its full name."""
    try:
        if '.' in module_name:  # Handle relative imports
            # Provide package context for relative imports
            package = module_name.rsplit('.', 1)[0]  # Get the package part
            full_module_name = module_name.split(".", 1)[-1]  # Module part
            imported_module = importlib.import_module(full_module_name, package)
        else:
            # Absolute import
            imported_module = importlib.import_module(module_name)
        
        logger.info(f"Successfully imported {module_name}")
        return imported_module
    except ModuleNotFoundError as e:
        logger.error(f"Module {module_name} not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error importing module {module_name}: {e}")
        raise


def init():
    # Sample plugin modules
    all_modules = __list_all_modules()

    for all_module in all_modules:
        import_plugin_module(all_module)


# Initialize the modules
init()
