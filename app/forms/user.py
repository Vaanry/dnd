from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Regexp, Length


class RegistrationForm(Form):

    username = StringField(
        "Имя пользователя",
        validators=[
            DataRequired(message="Обязательное поле"), 
            Length(3, 20, message="Имя должно быть от 3 до 20 символов"), 
            Regexp(r"^[а-яА-ЯёЁa-zA-Z0-9_]+$", message="Разрешены буквы английского и русского алфавита, цифры и знак нижнего подчёркивания."),
            ],
    )

    password = PasswordField(
        "Введите пароль",
        validators=[
            DataRequired(message="Обязательное поле"), 
            Length(8, 20, message="Минимальная длина 8 символов, максимальная 20"),
            Regexp(r"^[a-zA-Z0-9]+/*#_$", message="Разрешены буквы английского алфавита и цифры."),
            ],
    )