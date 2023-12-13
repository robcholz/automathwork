class Subject:
    def __init__(self, name, fields):
        self.fields = fields
        self.name = name

    def get_name(self):
        return self.name

    def get_homework_prompt(self):
        return self.fields['homework.prompt']

    def get_markdown_prompt(self):
        return self.fields['markdown.prompt']

    def get_signature_title(self):
        return self.fields['signature.title']

    def get_signature_school(self):
        return self.fields['signature.school']

    def get_signature_teacher(self):
        return self.fields['signature.teacher']

    def get_signature_grade(self):
        return self.fields['signature.grade']

    def get_signature_class(self):
        return self.fields['signature.class']
