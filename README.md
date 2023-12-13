# automathwork

automathwork is a GUI application that provides exam and practice generation using generative AI (gpt3.5). This tool
creates subject-specific exams and practice materials with good levels of accuracy and efficiency. With automathwork,
educators and students alike can easily generate comprehensive and customized assessments to enhance learning outcomes.
Whether it's for test preparation or reinforcing subject knowledge, automathwork software provides a seamless and
user-friendly experience for optimized learning.

## Install

### Windows
- Download the automathwork as a zip.
- Unzip it and double-click the `install-windows.bat`.

### MacOS
- Download the automathwork as a zip.
- Unzip it and double-click the `install-macos`.


## Usage

### Windows
- double-click the `launch-windows.bat`.

### MacOS
- double-click the `launch-macos`.

## Configure

### `config/config.json`
```json
{
  "gpt3.5-turbo.key": "xxxx",
  "proxy.address": "127.0.0.1",
  "proxy.port": "7890",
  "subject.default": "AP Physics C: Electricity and Magnetism"
}
```
`gpt3.5-turbo.key` fill your chatgpt3.5 key here.

`proxy.address` proxy address, typically `127.0.0.1`. **_temporary unavailable_**.

`proxy.port` proxy port, typically `7890`. **_temporary unavailable_**.

`subject.default` auto generated field. **DO NOT EDIT BY HAND**.

### `config/subjects.json`
```json
{
  "Precalculus": {
    "homework.prompt": "You are a helpful assistant. You should assist me to design the Precalculus homework. Your answer will be directly used so don't give me any other sentences. You should follow the following format: Question is one line. Question should start with number following by a dot.",
    "markdown.prompt": "You are a helpful assistant. You should only convert the plain texts I give you which might contain math symbols to markdown format. All expressions are braced with two paired $. DO NOT EVER try to parse the contents! Every word I give you is the content. Do not answer the question in the contents I give you.",
    "signature.title": "Calculus Practice",
    "signature.school": "Robinson's kindergarten",
    "signature.teacher": "Robinson",
    "signature.grade": "10",
    "signature.class": "Precalculus I"
  },
  "AP Calculus BC": {
    "homework.prompt": "You are a helpful assistant. You should assist me to design the Advanced Placement Calculus BC practices. Your answer will be directly used so don't give me any other sentences. You should follow the following format: Question is one line. Question should start with number following by a dot.",
    "markdown.prompt": "You are a helpful assistant. You should only convert the plain texts I give you which might contain math symbols to markdown format. All expressions are braced with two paired $. DO NOT EVER try to parse the contents! Every word I give you is the content. Do not answer the question in the contents I give you.",
    "signature.title": "Calculus Practice",
    "signature.school": "Robinson's kindergarten",
    "signature.teacher": "Robinson",
    "signature.grade": "12",
    "signature.class": "AP Calculus BC"
  }
}
```
This is an example file. you can remove/add more subjects following the format above.

`"This field will be the title of the combobox items": {}` this field will be the title of the combobox items.

`homework.prompt` the prompt to generate homework.

`markdown.prompt` the prompt to convert math symbols in generated homework to markdown. recommend to use the provided prompt.

`signature.title` the title of the generated doc(pdf).

`signature.school` the school of the generated doc belongs to.

`signature.teacher` the teacher who owns the generated doc.

`signature.grade` the grade of the doc aims to.

`signature.class` the class of the doc aims to.

## File/Folder Hierarchy

`config` saves the configuration files and binary deps of the app.

`config/config.json` stores the config file for the app.

`config/subjects.json` stores the subjects info for customization.

`config/pandoc` the binary used to convert markdown to html, do not edit or move.

`saves` the directory that stores the saved histories markdown docs.

`saves/current.md` the special markdown file that stores the currently generated contents.

`saves/mm-dd-yyyy-hh:mm:ss` the saved history files with timestamp filenames.
