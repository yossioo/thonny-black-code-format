import unittest
from unittest import mock

from pathlib import Path

import thonnycontrib.thonny_black_format as plugin

tests_folder = Path(__file__).parent


class TestPlugin(unittest.TestCase):
    def test_plugin(self):
        """
        Test that `show_info` is displaying the correct messages and
        `load_plugin` is called with the expected arguments.
        """
        with mock.patch(
            "thonnycontrib.thonny_black_format.get_workbench"
        ) as mock_workbench:
            filename = (
                mock_workbench.return_value.get_editor_notebook.return_value.get_current_editor.return_value.get_filename
            )

            black_plugin = plugin.BlackFormat()

            with mock.patch(
                "thonnycontrib.thonny_black_format.showinfo"
            ) as mock_showinfo:
                filename.side_effect = AttributeError

                black_plugin.format_black()
                mock_showinfo.assert_called_with(
                    title=plugin.NO_TEXT_TO_FORMAT[0],
                    message=plugin.NO_TEXT_TO_FORMAT[1],
                )

                filename.side_effect = None

                filename.return_value = "notcompatible"
                black_plugin.format_black()
                mock_showinfo.assert_called_with(
                    title=plugin.NOT_COMPATIBLE[0], message=plugin.NOT_COMPATIBLE[1]
                )

                filename.return_value = str(Path(f"{tests_folder}/unchanged.py"))
                black_plugin.format_black()
                mock_showinfo.assert_called_with(
                    title=plugin.SUCCESS, message="1 file left unchanged."
                )

                filename.return_value = str(Path(f"{tests_folder}/with_errors.py"))
                black_plugin.format_black()
                mock_showinfo.assert_called_with(
                    title="Oh no!",
                    message=f"Error: cannot format {filename()}: Cannot parse: 1:12: print(Hello world!)\n1 file failed to reformat.",
                )

                filename.return_value = str(Path(f"{tests_folder}/successful.py"))
                black_plugin.format_black()
                mock_showinfo.assert_called_with(
                    title="All done!", message="1 file reformatted."
                )

                with mock.patch(
                    "thonnycontrib.thonny_black_format.subprocess"
                ) as mock_subprocess:
                    mock_subprocess.sdterr = "No module named black"
                    black_plugin.format_black()
                    mock_showinfo.assert_called_with(
                        title=plugin.PACKAGE_NOT_FOUND[0],
                        message=plugin.PACKAGE_NOT_FOUND[1],
                    )

                black_plugin.load_plugin()
                mock_workbench.return_value.add_command.assert_called_with(
                    command_id="format_black",
                    menu_name="tools",
                    command_label="Format with Black",
                    handler=black_plugin.format_black,
                    default_sequence="<Control-Alt-c>",
                    extra_sequences=["<<CtrlAltCInText>>"],
                )


if __name__ == "__main__":
    unittest.main()
