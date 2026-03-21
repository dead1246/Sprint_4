import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


# add_new_book
@pytest.mark.parametrize('name', [
    'Книга 1',
    'Название до 40 символов'
])
def test_add_new_book_valid(collector, name):
    collector.add_new_book(name)
    assert name in collector.books_genre


@pytest.mark.parametrize('name', [
    '',
    'a' * 41
])
def test_add_new_book_invalid_length(collector, name):
    collector.add_new_book(name)
    assert name not in collector.books_genre


def test_add_new_book_duplicate(collector):
    collector.add_new_book('Дюна')
    collector.add_new_book('Дюна')
    assert len(collector.books_genre) == 1


def test_add_new_book_has_empty_genre(collector):
    collector.add_new_book('Солярис')
    assert collector.get_book_genre('Солярис') == ''


# set_book_genre / get_book_genre
def test_set_book_genre_valid(collector):
    collector.add_new_book('Оно')
    collector.set_book_genre('Оно', 'Ужасы')
    assert collector.get_book_genre('Оно') == 'Ужасы'


def test_set_book_genre_invalid_genre(collector):
    collector.add_new_book('Оно')
    collector.set_book_genre('Оно', 'Роман')
    assert collector.get_book_genre('Оно') == ''


# get_books_with_specific_genre
def test_get_books_with_specific_genre(collector):
    collector.add_new_book('Дюна')
    collector.add_new_book('Шрек')
    collector.set_book_genre('Дюна', 'Фантастика')
    collector.set_book_genre('Шрек', 'Мультфильмы')

    assert collector.get_books_with_specific_genre('Фантастика') == ['Дюна']


# get_books_genre
def test_get_books_genre_returns_dict(collector):
    collector.add_new_book('Книга')
    assert collector.get_books_genre() == {'Книга': ''}


# get_books_for_children
def test_get_books_for_children_excludes_age_rating(collector):
    collector.add_new_book('Оно')
    collector.add_new_book('Шрек')
    collector.set_book_genre('Оно', 'Ужасы')
    collector.set_book_genre('Шрек', 'Мультфильмы')

    result = collector.get_books_for_children()

    assert 'Оно' not in result
    assert 'Шрек' in result


# add_book_in_favorites / delete_book_from_favorites / get_list_of_favorites_books
def test_add_book_in_favorites(collector):
    collector.add_new_book('Дюна')
    collector.add_book_in_favorites('Дюна')
    assert 'Дюна' in collector.favorites


def test_add_book_in_favorites_no_duplicates(collector):
    collector.add_new_book('Дюна')
    collector.add_book_in_favorites('Дюна')
    collector.add_book_in_favorites('Дюна')
    assert collector.favorites == ['Дюна']


def test_delete_book_from_favorites(collector):
    collector.add_new_book('Дюна')
    collector.add_book_in_favorites('Дюна')
    collector.delete_book_from_favorites('Дюна')
    assert 'Дюна' not in collector.favorites


def test_get_list_of_favorites_books(collector):
    collector.add_new_book('Дюна')
    collector.add_book_in_favorites('Дюна')
    assert collector.get_list_of_favorites_books() == ['Дюна']