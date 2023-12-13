from gui import AppWindow
from mathwork import Mathwork
from settings import Settings
from utils import Utils

settings = Settings()

mathwork = Mathwork(
    settings=settings
)
app_window = AppWindow(
    settings=settings,
    utils=Utils(
        settings=settings
    )
)
app_window.set_prompts_callbacks(
    homework_callback=lambda prompt: mathwork.get_homework(prompt),
    markdown_callback=lambda prompt: mathwork.get_markdown(prompt)
)
app_window.show()
app_window.exec()
