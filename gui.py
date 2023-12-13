import datetime
import os.path
import sys

import PyQt5
import PyQt5.QtWebEngineWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow

import utils
from settings import Settings


class AppWindow(PyQt5.QtWidgets.QWidget):
    def __init__(self, utils: utils.Utils, settings: Settings):
        self.application = QApplication([])

        self.web_engine_page = PyQt5.QtWebEngineWidgets.QWebEnginePage()
        self.web_engine_page.loadStarted.connect(lambda: self.log_info("Started exporting"))
        self.web_engine_page.loadFinished.connect(lambda: self.log_info("Exporting finished"))

        self.web_engine_page.loadFinished.connect(lambda: self.export_pdf())

        super().__init__()
        self.settings = settings
        self.utils = utils
        self.current_md: str = ""
        self.setWindowTitle("automathwork-alpha")
        self.resize(1010, 760)  # initial window size

        # parent widgets
        self.parent_layout = PyQt5.QtWidgets.QHBoxLayout()

        # left widgets
        self.left_layout = PyQt5.QtWidgets.QVBoxLayout()
        self.parent_layout.addLayout(self.left_layout)

        # right widgets
        self.right_layout = PyQt5.QtWidgets.QVBoxLayout()
        self.parent_layout.addLayout(self.right_layout)

        # right top widgets
        self.right_top_layout = PyQt5.QtWidgets.QHBoxLayout()
        self.right_layout.addLayout(self.right_top_layout)
        self.export_pdf_button_widget = PyQt5.QtWidgets.QPushButton("Export as PDF")
        self.delete_button_widget = PyQt5.QtWidgets.QPushButton("Delete Markdown")
        self.save_button_widget = PyQt5.QtWidgets.QPushButton("Save Markdown")
        self.switch_subject_button = PyQt5.QtWidgets.QComboBox()
        self.export_pdf_button_widget.clicked.connect(lambda: self.export_to_pdf())
        self.save_button_widget.clicked.connect(lambda: self.save_new_markdown())
        self.delete_button_widget.clicked.connect(lambda: self.delete_selected_markdown())
        self.right_top_layout.addWidget(self.switch_subject_button)
        self.right_top_layout.addWidget(self.save_button_widget)
        self.right_top_layout.addWidget(self.delete_button_widget)
        self.right_top_layout.addWidget(self.export_pdf_button_widget)

        # right bottom widgets
        self.right_bottom_layout = PyQt5.QtWidgets.QVBoxLayout()
        self.right_layout.addLayout(self.right_bottom_layout)

        # left paired widgets
        self.history_bar = PyQt5.QtWidgets.QListWidget()
        self.info_widget = PyQt5.QtWidgets.QTextEdit()
        self.info_widget.setReadOnly(True)
        self.info_widget.setMaximumWidth(130)
        self.history_bar.setMaximumWidth(130)
        self.history_bar.currentItemChanged.connect(
            lambda: self.on_histories_selected(self.history_bar.currentItem())
        )

        self.left_layout.addWidget(self.history_bar)
        self.left_layout.addWidget(self.info_widget)

        # right bottom paired widgets
        self.right_paired_layout = PyQt5.QtWidgets.QHBoxLayout()
        self.markdown_view_widget = PyQt5.QtWidgets.QTextEdit()
        self.html_renderer = PyQt5.QtWebEngineWidgets.QWebEngineView()
        self.markdown_view_widget.setMinimumWidth(360)
        self.html_renderer.setMinimumWidth(400)
        self.markdown_view_widget.textChanged.connect(lambda: self.apply_markdown_change_rerender_html())
        self.right_paired_layout.addWidget(self.markdown_view_widget)
        self.right_paired_layout.addWidget(self.html_renderer)
        self.right_bottom_layout.addLayout(self.right_paired_layout)

        # prompt widgets
        self.prompt_input_widget = PyQt5.QtWidgets.QTextEdit()
        self.prompt_input_widget.setMaximumHeight(55)
        self.prompt_input_widget.setFontPointSize(20)
        self.prompt_input_widget.textChanged.connect(lambda: self.prompt_input_widget.setFontPointSize(20))
        self.prompt_send_button_widget = PyQt5.QtWidgets.QPushButton()
        self.prompt_layout = PyQt5.QtWidgets.QHBoxLayout()

        self.prompt_send_button_widget.setFixedSize(60, 55)
        self.prompt_send_button_widget.setText("Send")
        self.prompt_layout.addWidget(self.prompt_input_widget)
        self.prompt_layout.addWidget(self.prompt_send_button_widget)
        self.right_bottom_layout.addLayout(self.prompt_layout)

        # sum
        self.setLayout(self.parent_layout)

        # window widgets initialization
        self.switch_subject_button.currentIndexChanged.connect(lambda: self.change_subject())
        self.index_subjects()
        self.index_markdowns()
        self.render_html()

    def export_pdf(self):
        path = os.path.join(PyQt5.QtWidgets.QFileDialog.getExistingDirectory(), 'output.pdf')
        if not path == 'output.pdf':
            self.web_engine_page.printToPdf(path)

    def set_prompts_callbacks(self, homework_callback, markdown_callback):
        self.prompt_send_button_widget.clicked.connect(
            lambda: self.handle_send_prompts(
                homework_callable=homework_callback,
                markdown_callable=markdown_callback
            ))

    def handle_send_prompts(self, homework_callable, markdown_callable):
        content = self.prompt_input_widget.toPlainText()
        if len(content) > 0:
            self.log_info("Prompt sent")
            self.generate_homework(homework_callable, markdown_callable, content)

    def generate_homework(self, homework_callable, markdown_callable, prompt):
        self.prompt_input_widget.clear()
        homework = homework_callable(prompt)
        self.log_info("Homework generated!")
        self.log_info("Generating markdown...")
        markdown = markdown_callable(homework)
        self.log_info("Markdown generated!")
        utils.write_cache(os.path.join('saves', 'current.md'), markdown)
        self.markdown_view_widget.setMarkdown(markdown)
        self.index_markdowns()
        # send notifications here

    # update the source file
    # render the corresponding web view
    def apply_markdown_change_rerender_html(self):
        utils.write_cache(self.current_md, self.markdown_view_widget.toMarkdown())
        self.rerender_html()

    def rerender_html(self):
        self.utils.get_html(self.current_md, 'cache.html')
        self.html_renderer.reload()

    def render_html(self):
        self.utils.get_html(self.current_md, 'cache.html')
        self.html_renderer.load(QUrl.fromLocalFile(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache.html')))

    def save_new_markdown(self):
        filename = os.path.join('saves', datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S"))
        utils.write_cache(filename, utils.read_cache(os.path.join('saves', 'current.md')))
        self.log_info("file history {} saved".format(filename))
        self.index_markdowns()
        # add notifications here

    def delete_selected_markdown(self):
        if not self.history_bar.hasFocus():
            return
        if self.history_bar.currentItem().text() == 'current.md':
            return
        path = os.path.join('saves', self.history_bar.currentItem().text())
        if os.path.exists(path):
            os.remove(path)
            self.log_info("file history {} removed".format(self.history_bar.currentItem().text()))
            # add notifications here
        self.index_markdowns()

    def index_markdowns(self):
        def file_to_str(string: str):
            if string == 'current.md':
                return sys.float_info.max
            date_time_parts = string.split("-")
            day = int(date_time_parts[0])
            month = int(date_time_parts[1])
            year = int(date_time_parts[2])
            hour = int(date_time_parts[3].split(":")[0])
            minute = int(date_time_parts[3].split(":")[1])
            second = int(date_time_parts[3].split(":")[2])

            dt = datetime.datetime(year, month, day, hour, minute, second)
            return (dt - datetime.datetime(dt.year, 1, 1)).total_seconds()

        file_list = []
        if os.path.exists('saves'):
            for file_name in os.listdir('saves'):
                if os.path.isfile(os.path.join('saves', file_name)):
                    file_list.append(file_name)
        else:
            os.mkdir('saves')
        if len(file_list) > 0:
            self.history_bar.clear()
            file_list.sort(key=file_to_str, reverse=True)
        for history_file in file_list:
            history = PyQt5.QtWidgets.QListWidgetItem(history_file)
            self.history_bar.addItem(history)

    def index_subjects(self):
        self.switch_subject_button.clear()
        default_name = self.settings.get_default_subject_name()
        for subject in self.settings.get_subject_list():
            name = subject.get_name()
            self.switch_subject_button.addItem(name)
        self.switch_subject_button.setCurrentText(default_name)

    def change_subject(self):
        self.settings.set_default_subject(self.switch_subject_button.currentText())
        self.rerender_html()

    def on_histories_selected(self, history: PyQt5.QtWidgets.QListWidgetItem):
        if history is None:
            self.current_md = ""
            self.markdown_view_widget.setMarkdown("")
        else:
            self.current_md = os.path.join('saves', history.text())
            self.markdown_view_widget.setMarkdown(utils.read_cache(os.path.join('saves', history.text())))

    def export_to_pdf(self):
        self.web_engine_page.load(QUrl.fromLocalFile(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache.html')))

    def log_info(self, info):
        self.info_widget.append(info + "\n")

    def log_error(self, error):
        self.info_widget.append(error + "\n")

    def exec(self):
        self.application.exec()


if __name__ == "__main__":
    app = QApplication([])
    window = QMainWindow()
    html_renderer = PyQt5.QtWebEngineWidgets.QWebEngineView()
    html_renderer.load(QUrl.fromLocalFile(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache.html')))
    window.setCentralWidget(html_renderer)
    window.show()
    app.exec()
