from handlers import parse_item


def test_calories_after_description():
    assert parse_item("chicken salad 350") == (350, "chicken salad")


def test_calories_before_description():
    assert parse_item("350 chicken salad") == (350, "chicken salad")


def test_no_description_defaults_to_food():
    assert parse_item("250") == (250, "food")


def test_no_number_returns_none():
    assert parse_item("no numbers here") is None


def test_strips_separators_around_description():
    assert parse_item("- 120 coffee -") == (120, "coffee")
