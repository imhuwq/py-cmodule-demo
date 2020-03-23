import os
import pathlib
from setuptools import setup
from setuptools import Extension
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):

    def __init__(self, name):
        super().__init__(name, sources=[])


class BuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        cwd = pathlib.Path().absolute()

        build_temp = f"{pathlib.Path(self.build_temp)}/{ext.name}"
        os.makedirs(build_temp, exist_ok=True)
        extdir = pathlib.Path(self.get_ext_fullpath(ext.name))
        extdir.mkdir(parents=True, exist_ok=True)

        config = "Debug" if self.debug else "Release"
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(extdir.parent.absolute()),
            "-DCMAKE_BUILD_TYPE=" + config
        ]

        build_args = [
            "--config", config,
            "--", "-j8"
        ]

        os.chdir(build_temp)
        self.spawn(["cmake", f"{str(cwd)}/{ext.name}"] + cmake_args)
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
        os.chdir(str(cwd))


mymath = CMakeExtension("mymath")

setup(name="demo",
      version="1.1",
      description="This is a demo package",
      packages=["demo"],
      ext_modules=[mymath],
      cmdclass={"build_ext": BuildExt}
      )
