from thonny import get_workbench
from tkinter.messagebox import showinfo
import subprocess
import sys
import os

name = "thonny-black-format"

ERROR = "Error!"
SUCCESS = "All done!"

NO_TEXT_TO_FORMAT = (ERROR, "There is no text to format.")
PACKAGE_NOT_FOUND = (
    ERROR,
    "Could not find Black package. Is it installed and on your PATH?",
)
NOT_COMPATIBLE = (
    "File not compatible!",
    "Looks like this is not a python file. Did you already save it?",
)

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
    """
    Apply black format to the current loaded file.

    Using subprocess, black is executed to format .py files displayed in
    Thonny. Whenever this plugin is executed, format_black is called. Depending
    on the result, final_title and final_message is displayed through
    tkinter.messagebox.showinfo().
    """

    def __init__(self) -> None:
        """Get the workbench to be later used to detect the file to format."""
        self.workbench = get_workbench()

    def format_black(self) -> None:
        """Handle the plugin execution."""
        self.editor = self.workbench.get_editor_notebook().get_current_editor()

        try:
            self.filename = self.editor.get_filename()
        except AttributeError:
            final_title = NO_TEXT_TO_FORMAT[0]
            final_message = NO_TEXT_TO_FORMAT[1]
        else:
            if self.filename is not None and self.filename[-3:] == ".py":
                self.editor.save_file()

                format_code = subprocess.run(
                    [get_interpreter_for_subprocess(), "-m", "black", self.filename,],
                    capture_output=True,
                    text=True,
                )

                if format_code.stderr.find("No module named black") != -1:
                    final_title = PACKAGE_NOT_FOUND[0]
                    final_message = PACKAGE_NOT_FOUND[1]
                else:
                    # Emojis are not supported in Tkinter.
                    message_without_emojis = format_code.stderr.encode(
                        "ascii", "ignore"
                    ).decode()
                    if format_code.returncode != 0:
                        """
                        Black error message structure:
                            1. error: cannot format file_name.py: ... (Error detail)
                            2. Oh no!
                            3. 1 file failed to reformat.
                        """

                        final_title = "Oh no!"
                        final_message = "\n".join(
                            message_without_emojis.splitlines()[::2]
                        )

                        final_message = final_message[0].upper() + final_message[1:]

                    else:
                        self.editor._load_file(self.filename, keep_undo=True)

                        """
                        Black success message structure:
                            A) When a file is reformatted:
                                1. reformatted file_name.py
                                2. All done!
                                3. 1 file reformatted.
                            * A.1 is not shown in final_message.

                            B) When the file is not changed:
                                1. All done!
                                2. 1 file left unchanged.
                        """

                        final_title = "All done!"
                        final_message = message_without_emojis.splitlines()[-1]

            else:
                final_title = NOT_COMPATIBLE[0]
                final_message = NOT_COMPATIBLE[1]

        showinfo(title=final_title, message=final_message)

    def load_plugin(self) -> None:
        """
        Load the plugin on runtime.

        Using self.workbench.add_command(), the plugin is registered in Thonny
        with all the given arguments.
        """
        self.workbench.add_command(
            command_id="format_black",
            menu_name="tools",
            command_label="Format with Black",
            handler=self.format_black,
            default_sequence="<Control-Alt-c>",
            extra_sequences=["<<CtrlAltCInText>>"],
        )


if get_workbench() is not None:
    run = BlackFormat().load_plugin()
