from quart_wtf import QuartForm
from wtforms import SearchField, SelectField
from wtforms.validators import InputRequired


class SearchForm(QuartForm):
    city = SearchField(
        "City",
        validators=[InputRequired()],
    )

    temperature_unit = SelectField(
        "Temperature Unit",
        choices=[("celsius", "Celsius"), ("fahrenheit", "Fahrenheit")],
        default="celsius",
        validators=[InputRequired()],
    )

    distance_unit = SelectField(
        "Distance Unit",
        choices=[("kilometres", "Kilometres"), ("miles", "Miles")],
        default="kilometres",
        validators=[InputRequired()],
    )
