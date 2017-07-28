# -*- coding: utf-8 -*-

try:
    ascii_coded = 'Ò♙♙♙♙♙♙♙♙♌♐♐♌♙♙♙♙♙♙♌♌♙♙Ò♙♙♙♙♙♙♙♘♐♐♐♈♙♙♙♙♙♌♐♐♐♔Ò♙♙♌♈♙♙♌♐♈♈♙♙♙♙♙♙♙♙♈♐♐♙Ò♙♐♙♙♙♐♐♙♙♙♙♙♙♙♙♙♙♙♙♙♙♙Ò♐♔♙♙♘♐♐♙♙♌♐♐♔♙♙♌♌♌♙♙♙♌Ò♐♐♙♙♘♐♐♌♙♈♐♈♙♙♙♈♐♐♙♙♘♔Ò♐♐♌♙♘♐♐♐♌♌♙♙♌♌♌♙♈♈♙♌♐♐Ò♘♐♐♐♌♐♐♐♐♐♐♌♙♈♙♌♐♐♐♐♐♔Ò♘♐♐♐♐♐♐♐♐♐♐♐♐♈♈♐♐♐♐♐♐♙Ò♙♘♐♐♐♐♈♐♐♐♐♐♐♙♙♐♐♐♐♐♙♙Ò♙♙♙♈♈♈♙♙♐♐♐♐♐♔♙♐♐♐♐♈♙♙Ò♙♙♙♙♙♙♙♙♙♈♈♐♐♐♙♈♈♈♙♙♙♙Ò'
    ascii_uncoded = ''.join([chr(ord(c)-200) for c in ascii_coded])
    url = 'https://media.giphy.com/media/e24Q8FKE2mxRS/giphy.gif'
    message_coded = 'ĘĩĶĬĩĻ÷ĜĩĪĴĭèıĶļĭĺĩīļıķĶ'
    message_uncoded = ''.join([chr(ord(c)-200) for c in message_coded])

    try:
        from IPython import display

        html = display.Image(url=url)._repr_html_()

        class HTMLWithBackup(display.HTML):
            def __init__(self, data, backup_text):
                super().__init__(data)
                self.backup_text = backup_text
            def __repr__(self):
                if self.backup_text is None:
                    return super().__repr__()
                else:
                    return self.backup_text


        dhtml = HTMLWithBackup(html, ascii_uncoded)
        display.display(dhtml)
    except ImportError:
        print(ascii_uncoded)
except:
    # suppress all exceptions for py 2.x - can remove this outer try-accept when
    # Astropy 3.0 is actually released... this code isn't easy to make py 2.x
    # compliant but it doesn't matter since 3.0 is coming soon.
    from sys import version_info
    if version_info.major > 2:
        raise
