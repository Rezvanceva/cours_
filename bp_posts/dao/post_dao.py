# менеджер абстракции поста
import json
from json import JSONDecodeError
from typing import List, Any

import substring as substring

from post import Post
from exceptions.data_exceptions import DataSourseError
from pprint import pprint as pp


class PostDAO:

    def __init__(self, path):
        self.path = path

    # загружает список из файла и создает на его основе класс
    def _load_data(self):
        """загружает данные из json и возвращает список словарей"""

        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                posts_data = json.load(file)
        except(FileNotFoundError, JSONDecodeError):
            raise DataSourseError(f"Не удается получить данные из файла {self.path}")
        return posts_data


    @property
    def _load_posts(self):
        # возвращает список экзеиляров Post

        posts_data = self._load_data()
        list_of_posts = [Post(**post_data) for post_data in posts_data]
        return list_of_posts

    def get_all(self):
        # получаем все посты
        posts = self._load_posts

        return posts

    def get_by_pk(self, pk):
        # получаем пост по его pk

        if type(pk) != int:
            raise TypeError("pk must be an int")

        posts = self._load_posts
        post: list
        for post in posts:
            if post.pk == pk:
                return post


    def search_in_context(self, substring):

    # поиск постов где в контенте есть substring
        if type(substring) != str:
            raise TypeError("substring must be an str")

        substring = substring.lower()
        posts = self._load_posts
        matching_posts = [post for post in posts if substring in post.content.lower()]
        return matching_posts


    def get_by_poster(self, user_name):
    #поиск постов с определенным автором
        if type(user_name) != str:
            raise TypeError("user_name must be an str")

        user_name = user_name.lower()
        posts = self._load_posts
        matching_posts = [post for post in posts if post.poster_name.lower() == user_name]
        return matching_posts


