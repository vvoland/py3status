# -*- coding: utf-8 -*-
"""
Display output of a given script.

Display output of any executable script set by `script_path`.
Only the first two lines of output will be used. The first line is used
as the displayed text. If the output has two or more lines, the second
line is set as the text color (and should hence be a valid hex color
code such as #FF0000 for red).
The script should not have any parameters, but it could work.

Configuration parameters:
    cache_timeout: how often we refresh this module in seconds
        (default 15)
    format: see placeholders below (default '{output}')
    script_path: script you want to show output of (compulsory)
        (default None)
    strip_output: shall we strip leading and trailing spaces from output
        (default False)

Format placeholders:
    {output} output of script given by "script_path"

i3status.conf example:

```
external_script {
    format = "my name is {output}"
    script_path = "/usr/bin/whoami"
}
```

@author frimdo ztracenastopa@centrum.cz

SAMPLE OUTPUT
{'full_text': 'script output'}

example
{'full_text': 'It is now: Wed Feb 22 22:24:13'}
"""

import re
STRING_ERROR = 'missing script_path'


class Py3status:
    """
    """
    # available configuration parameters
    cache_timeout = 15
    format = '{output}'
    script_path = None
    strip_output = False

    def post_config_hook(self):
        if not self.script_path:
            raise Exception(STRING_ERROR)

    def external_script(self):
        output_lines = None
        response = {}
        response['cached_until'] = self.py3.time_in(self.cache_timeout)
        try:
            output = self.py3.command_output(self.script_path, shell=True)
            output_lines = output.splitlines()
            if len(output_lines) > 1:
                output_color = output_lines[1]
                if re.search(r'^#[0-9a-fA-F]{6}$', output_color):
                    response['color'] = output_color
        except self.py3.CommandError as e:
            # something went wrong show error to user
            output = e.output or e.error
            self.py3.error(output)

        if output_lines:
            output_text = output_lines[0]
            if self.strip_output:
                output_text = output_text.strip()
        else:
            output_text = ''

        response['full_text'] = self.py3.safe_format(
            self.format, {'output': output_text})
        return response


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)
