from thonny import get_workbench
from tkinter.messagebox import showinfo
import subprocess
import sys
import os

name = "thonny-black-format"

# Temporary fix: this function comes from thonny.running, but importing that
# module may conflict with outdated Thonny installations from some Linux
# repositories.
# TODO: change this with thonny.running.get_interpreter_for_subprocess when
# possible and change Thonny version required.
_console_allocated = False


def get_interpreter_for_subprocess(candidate=None):
    if candidate is None:
        candidate = sys.executable

    pythonw = candidate.replace("python.exe", "pythonw.exe")
    if not _console_allocated and os.path.exists(pythonw):
        return pythonw
    else:
        return candidate.replace("pythonw.exe", "python.exe")


class BlackFormat:
    workbench = get_workbench()

    def __init__(self):
        return self.load_plugin()

    def format_black(self):
        self.editor = self.workbench.get_editor_notebook().get_current_editor()
        try:
            self.filename = self.editor.get_filename()
        except AttributeError:
            final_title = "Error!"
            final_message = "There is no text to format."
        else:
            if self.filename is not None and self.filename[-3:] == ".py":
                self.editor.save_file()
                try:
                    format_code = subprocess.run(
                        [
                            get_interpreter_for_subprocess(),
                            "-m",
                            "black",
                            self.filename,
                        ],
                        capture_output=True,
                        text=True,
                    )
                except FileNotFoundError:
                    final_title = "Error!"
                    final_message = "Could not find Black package. Is it installed and on your PATH?"
                else:
                    if format_code.returncode != 0:
                        final_title = "Error!"
                        try:
                            error_found = format_code.stderr.split("error:")[
                                1
                            ].split("\n")[0]
                        except IndexError:
                            error_found = format_code.stderr.split("Error:")[
                                1
                            ].split("\n")[0]

                        final_message = error_found
                    else:
                        self.editor._load_file(self.filename, keep_undo=True)
                        final_title = "Success!"
                        final_message = "Code formatted succesfully."

            else:
                final_title = "File not compatible!"
                final_message = "Looks like this is not a python file. Did you already save it?"

        showinfo(title=final_title, message=final_message)

    def load_plugin(self):
        self.workbench.add_command(
            command_id="format_black",
            menu_name="tools",
            command_label="Format with Black",
            handler=self.format_black,
            default_sequence="<Control-Alt-c>",
            extra_sequences=["<<CtrlAltCInText>>"],
        )


run = BlackFormat()
