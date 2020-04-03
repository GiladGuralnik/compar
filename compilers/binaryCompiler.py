from compilers.compiler import Compiler
import os
import subprocess
from exceptions import CompilationError, CombinationFailure
from subprocess_handler import run_subprocess


class BinaryCompiler(Compiler):

    def __init__(self, compiler_name, version, compilation_flags=None, input_file_directory=None, main_c_file=None):
        super().__init__(version, compilation_flags, input_file_directory)
        self._compiler_name = compiler_name
        self._main_c_file = main_c_file

    def initiate_for_new_task(self, compilation_flags, input_file_directory, main_c_file):
        super().initiate_for_new_task(compilation_flags, input_file_directory)
        self.set_main_c_file(main_c_file)

    def get_compiler_name(self):
        return self._compiler_name

    def set_compiler_name(self, compiler_name):
        self._compiler_name = compiler_name

    def get_main_c_file(self):
        return self._main_c_file

    def set_main_c_file(self, main_c_file):
        self._main_c_file = main_c_file

    def compile(self):
        if not self.get_main_c_file():
            raise CompilationError("Missing main_file argument to compile!")
        if not self.get_input_file_directory():
            raise CompilationError("Missing working directory!")
        # Compiling
        try:
            self.run_compiler()
            return True
        except subprocess.CalledProcessError as ex:
            raise CombinationFailure(self._compiler_name +
                                     f' return with {ex.returncode} code: {str(ex)} : {ex.output} : {ex.stderr}')
        except Exception as e:
            raise CompilationError(str(e) + " " + self.get_main_c_file() + " failed to be compiled!")

    def run_compiler(self):
        input_file_path_only = os.path.dirname(self.get_input_file_directory() + os.path.sep)
        dir_name = os.path.basename(input_file_path_only)

        print("Compiling " + self.get_main_c_file())
        command = [self.get_compiler_name(), "-fopenmp"] + self.get_compilation_flags()
        command += [self.get_main_c_file(), "-o", dir_name + ".x"]
        stdout, stderr, ret_code = run_subprocess(command, self.get_input_file_directory())
        print(self._compiler_name + ' compilation output: ' + str(stdout))
        print("Done Compile work")
