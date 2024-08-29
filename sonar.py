import os
import json


class Sonar:
    def __init__(self, path: str, ignored: list = [".git", "__pycache__", "venv"]) -> None:
        """Initializes Sonar object.

        Args:
            path (str): Path to the directory that will be the starting point of the Sonar object.
            ignored (list, optional): Directories to be ignored. Defaults to [".git", "__pycache__", "venv"].
        """
        self.path = path
        self.ignored = ignored

    def simple_explore(self) -> dict:
        """Recursively explores all directories inside a given path, giving a list of it's contents.

        Returns:
            dict: Returns a dictionary map with this format: {"path/to/directory" : [list, of, items]}
        """
        directory_map = {}
        current_dir = os.getcwd()

        def func(path):
            nonlocal directory_map
            os.chdir(path)
            path = os.getcwd()
            directory_contents = os.listdir()
            directory_map[path] = directory_contents
            for content in directory_contents:
                os.chdir(path)
                abs_path = os.path.join(os.getcwd(), content)
                if content in self.ignored:
                    continue
                elif os.path.isdir(abs_path):
                    func(abs_path)

        func(self.path)

        # Resets path
        os.chdir(current_dir)
        return directory_map

    def complete_explore(self):
        """Recursively explores all directories inside a given path, giving a nested dictionary of it's contents.

        Returns:
            dict: Returns a dictionary with this format: {"path/to/dir": {dir:{items}, file:"content", other:{}}}
        """
        current_dir = os.getcwd()

        def func(path):
            os.chdir(path)
            path = os.getcwd()
            directory_contents = os.listdir()
            # directory_map[path] = directory_contents
            inner_content = {}
            for content in directory_contents:
                os.chdir(path)
                abs_path = os.path.join(os.getcwd(), content)
                if content in self.ignored:
                    continue
                elif os.path.isdir(abs_path):
                    inner_content[content] = func(abs_path)
                elif os.path.isfile(abs_path):
                    with open(abs_path, "r") as file:
                        try:
                            if file.readable():
                                inner_content[abs_path] = file.read()
                            else:
                                inner_content[abs_path] = "*** FILE NOT READABLE ***"
                        except UnicodeDecodeError:
                            inner_content[abs_path] = ""
                else:
                    inner_content[abs_path] = None
            return inner_content

        directories = func(self.path)

        # Resets path
        os.chdir(current_dir)
        return directories

    def seek_files(file_names: list) -> str:
        """Looks for and gathers the content of a group of specific files

        Args:
            file_name (list): _description_

        Returns:
            str: _description_
        """
        raise NotImplementedError("Please make this function when you can.")


if __name__ == "__main__":
    sonar = Sonar("/home/luiz/annoying_site")
    directory_map = sonar.simple_explore()
    with open("sonar.json", "w") as file:
        file.write(json.dumps(directory_map))
