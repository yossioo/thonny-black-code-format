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
    """
    Apply black format to the current loaded file.

    Using subprocess, black is executed to format .py files displayed in
    Thonny. Whenever this plugin is executed, format_black is called. Depending
    on the result, final_title and final_message is displayed through
    tkinter.messagebox.showinfo().
    """

    workbench = get_workbench()

    def __init__(self) -> None:
        """Prepare the plugin when Thonny is opened."""
        self.load_plugin()

    def format_black(self) -> None:
        """Handle the plugin execution."""
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

                        final_title = message_without_emojis.splitlines()[1]
                        final_message = "\n".join(
                            message_without_emojis.splitlines()[::2]
                        ).capitalize()
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
                final_title = "File not compatible!"
                final_message = (
                    "Looks like this is not a python file. Did you already save it?"
                )

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


run = BlackFormat()
