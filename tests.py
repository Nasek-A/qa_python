from main import BooksCollector
import pytest 

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2 
        # books_rating - нет такого списка, у нас есть books_genre, тут поправлю.
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
    
    # Параметризованная проверка допустимых длин названия:
    # 1 символ, обычное название и граничное значение в 40 символов
    @pytest.mark.parametrize('name', ['A', 'Гарри Поттер', 'Удивительное путешествие Нильса с гусями'])
    def test_add_new_book_valid_name_book_added(self, name):
        collector = BooksCollector()

        collector.add_new_book(name)

        assert name in collector.get_books_genre()

    # Параметризованная проверка недопустимых длин названия:
    # пустая строка и название из 41 символа - книга не добавляется
    @pytest.mark.parametrize('name', ['', 'Алиса в Стране чудес. Алиса в Зазеркалье.'])
    def test_add_new_book_invalid_name_length_book_not_added(self, name):
        collector = BooksCollector()

        collector.add_new_book(name)

        assert collector.get_books_genre() == {}

    # Одну и ту же книгу нельзя добавить дважды: в словаре остаётся одна запись
    def test_add_new_book_same_book_twice_added_once(self):
        collector = BooksCollector()

        collector.add_new_book('Дюна')
        collector.add_new_book('Дюна')

        assert len(collector.get_books_genre()) == 1

    # Книга добавляется без жанра (пустая строка)
    def test_add_new_book_new_book_has_no_genre(self):
        collector = BooksCollector()
 
        collector.add_new_book('Дюна')
 
        assert collector.get_book_genre('Дюна') == ''

    # Параметризованная проверка: каждый жанр из списка доступных можно установить книге
    @pytest.mark.parametrize('genre', ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'])
    def test_set_book_genre_valid_genre_genre_set(self, genre):
        collector = BooksCollector()

        collector.add_new_book('Дюна')

        collector.set_book_genre('Дюна', genre)
 
        assert collector.get_book_genre('Дюна') == genre

    # Жанра нет в списке доступных - жанр не устанавливается, остаётся пустая строка
    def test_set_book_genre_unknown_genre_genre_not_set(self):
        collector = BooksCollector()

        collector.add_new_book('Дюна')
 
        collector.set_book_genre('Дюна', 'Драма')
 
        assert collector.get_book_genre('Дюна') == ''

    # Книги нет в словаре - установить ей жанр нельзя, и новая запись не появляется
    def test_set_book_genre_book_not_in_collection_nothing_added(self):
        collector = BooksCollector()
 
        collector.set_book_genre('Дюна', 'Фантастика')
 
        assert collector.get_books_genre() == {}

    # Для книги, которой нет в словаре, get_book_genre возвращает None
    def test_get_book_genre_unknown_book_returns_none(self):
        collector = BooksCollector()
 
        assert collector.get_book_genre('Несуществующая книга') is None

    # Метод возвращает только книги нужного жанра, книги других жанров не попадают в список

    def test_get_books_with_specific_genre_returns_only_books_of_that_genre(self):
        collector = BooksCollector()

        collector.add_new_book('Дюна')
        collector.add_new_book('Оно')
        collector.add_new_book('Марсианин')

        collector.set_book_genre('Дюна', 'Фантастика')
        collector.set_book_genre('Оно', 'Ужасы')
        collector.set_book_genre('Марсианин', 'Фантастика')
 
        assert collector.get_books_with_specific_genre('Фантастика') == ['Дюна', 'Марсианин']

    # Параметризованная проверка: если книг такого жанра нет
    # (или жанра нет в списке доступных), возвращается пустой список     
    @pytest.mark.parametrize('genre', ['Комедии', 'Драма'])
    def test_get_books_with_specific_genre_no_matching_books_returns_empty_list(self, genre):
        collector = BooksCollector()

        collector.add_new_book('Дюна')

        collector.set_book_genre('Дюна', 'Фантастика')

        assert collector.get_books_with_specific_genre(genre) == []

    # Метод возвращает текущий словарь: книга с жанром и книга без жанра
    def test_get_books_genre_returns_current_dictionary(self):
        collector = BooksCollector()

        collector.add_new_book('Дюна')
        collector.add_new_book('Оно')

        collector.set_book_genre('Дюна', 'Фантастика')
 
        assert collector.get_books_genre() == {'Дюна': 'Фантастика', 'Оно': ''}

    # Параметризованная проверка: книги жанров без возрастного рейтинга подходят детям
    @pytest.mark.parametrize('genre', ['Фантастика', 'Мультфильмы', 'Комедии'])
    def test_get_books_for_children_genre_without_age_rating_book_included(self, genre):
        collector = BooksCollector()

        collector.add_new_book('Книга')

        collector.set_book_genre('Книга', genre)
 
        assert 'Книга' in collector.get_books_for_children()

    # Параметризованная проверка: книги с возрастным рейтингом (Ужасы, Детективы)
    # отсутствуют в списке книг для детей
    @pytest.mark.parametrize('genre', ['Ужасы', 'Детективы'])
    def test_get_books_for_children_genre_with_age_rating_book_excluded(self, genre):
        collector = BooksCollector()

        collector.add_new_book('Книга')

        collector.set_book_genre('Книга', genre)
 
        assert 'Книга' not in collector.get_books_for_children()

    # Книга без жанра не попадает в список книг для детей
    def test_get_books_for_children_book_without_genre_excluded(self):
        collector = BooksCollector()

        collector.add_new_book('Книга')
 
        assert collector.get_books_for_children() == []

    # Книга, которая есть в словаре, добавляется в избранное
    def test_add_book_in_favorites_book_in_collection_added(self):
        collector = BooksCollector()

        collector.add_new_book('Дюна')
 
        collector.add_book_in_favorites('Дюна')
 
        assert collector.get_list_of_favorites_books() == ['Дюна']

    # Повторно добавить книгу в избранное нельзя: в списке остаётся одна запись
    def test_add_book_in_favorites_same_book_twice_added_once(self):
        collector = BooksCollector()

        collector.add_new_book('Дюна')
 
        collector.add_book_in_favorites('Дюна')
        collector.add_book_in_favorites('Дюна')
 
        assert collector.get_list_of_favorites_books() == ['Дюна']

    # Книгу, которой нет в словаре books_genre, в избранное добавить нельзя
    def test_add_book_in_favorites_book_not_in_collection_not_added(self):
        collector = BooksCollector()
 
        collector.add_book_in_favorites('Дюна')
 
        assert collector.get_list_of_favorites_books() == []

     # Книга удаляется из избранного, другие книги в списке остаются
    def test_delete_book_from_favorites_book_in_favorites_removed(self):
        collector = BooksCollector()

        collector.add_new_book('Дюна')
        collector.add_new_book('Оно')

        collector.add_book_in_favorites('Дюна')
        collector.add_book_in_favorites('Оно')
 
        collector.delete_book_from_favorites('Дюна')
 
        assert collector.get_list_of_favorites_books() == ['Оно']

    # Удаление книги, которой нет в избранном, не меняет список и не вызывает ошибку
    def test_delete_book_from_favorites_book_not_in_favorites_list_unchanged(self):
        collector = BooksCollector()

        collector.add_new_book('Дюна')

        collector.add_book_in_favorites('Дюна')
 
        collector.delete_book_from_favorites('Оно')
 
        assert collector.get_list_of_favorites_books() == ['Дюна']

     # У только что созданного экземпляра список избранного пуст
    def test_get_list_of_favorites_books_new_collector_returns_empty_list(self):
        collector = BooksCollector()
 
        assert collector.get_list_of_favorites_books() == []
