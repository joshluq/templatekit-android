import os
import shutil

def move_package_path(module_name, package_name):
    """Move placeholder code to the correct package structure.
    
    Args:
        module_name: 'library' or 'showcase'
        package_name: The actual package name (e.g., com.example.mylib)
    """
    project_root = os.getcwd()
    package_path = package_name.replace('.', os.sep)

    # We may need to move placeholder code for multiple source sets
    source_sets = ['main', 'test', 'androidTest']
    moved_any = False

    for src_set in source_sets:
        src_base = os.path.join(project_root, module_name, 'src', src_set, 'java')
        src_placeholder = os.path.join(src_base, 'package_path_placeholder')
        dst_path = os.path.join(src_base, package_path)

        if not os.path.exists(src_placeholder):
            # no placeholder for this source set — skip
            continue

        # Create destination directory structure
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)

        # Move all files from placeholder to new package path
        for filename in os.listdir(src_placeholder):
            shutil.move(os.path.join(src_placeholder, filename), os.path.join(dst_path, filename))

        # Remove the placeholder directory
        shutil.rmtree(src_placeholder)
        print(f"Moved {src_set} code from placeholder to {package_path} in {module_name}")
        moved_any = True

    if not moved_any:
        print(f"No placeholder directories found for module {module_name}")
        return False

    return True

if __name__ == "__main__":
    package_name = "{{ cookiecutter.package_name }}"
    # Library uses base package
    move_package_path('library', package_name)
    # Showcase uses base package + ".showcase"
    move_package_path('showcase', package_name + '.showcase')