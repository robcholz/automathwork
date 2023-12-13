import datetime
import subprocess


def write_cache(file_path, contents):
    try:
        with open(file_path, "w") as file:
            file.truncate()
            file.flush()
            file.write(contents)
    except FileNotFoundError:
        return


def read_cache(file_path):
    try:
        with open(file_path, "r") as file:
            contents = file.read()
            return contents
    except FileNotFoundError:
        return ""


class Utils:
    def __init__(self, settings):
        self.settings = settings
        self.pandoc_path = settings.get_pandoc_path()

    def get_html(self, md_file, output_html):
        if not read_cache(md_file) == "":
            subprocess.run([self.pandoc_path, '--mathjax', '-s', md_file, '-o' + output_html],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL
                           )
            content = ""
            try:
                with open(output_html, 'r') as file:
                    content = file.read()
            except FileNotFoundError:
                pass
            try:
                with open(output_html, 'w') as w_file:
                    w_file.write(self.get_inject() + content)
            except FileNotFoundError:
                pass

    def get_inject(self):
        return "<header>" \
               "<h1>{}</h1>" \
               "</header>" \
               "<h5>UUID: {}</h5>" \
               "<h5>Teacher: {}</h5>" \
               "<h5>{} for grade {} of {}</h5>".format(self.settings.get_default_subject().get_signature_title(),
                                                       datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
                                                       self.settings.get_default_subject().get_signature_teacher(),
                                                       self.settings.get_default_subject().get_signature_school(),
                                                       self.settings.get_default_subject().get_signature_grade(),
                                                       self.settings.get_default_subject().get_signature_class())
