#класс для обработки комментариев
import json
from json import JSONDecodeError
from bp_posts.dao.comment import Comment

from exceptions.data_exceptions import DataSourseError


class CommentDAO:
    def __init__(self, path):
        self.path = path

    def _load_data(self):
        """загружает данные из json и возвращает список словарей"""
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                posts_data = json.load(file)
        except(FileNotFoundError, JSONDecodeError):
            raise DataSourseError(f"Не удается получить данные из файла {self.path}")
        return posts_data

    def _load_comments(self):
        # возвращает список экземпляров
        comments_data = self._load_data()
        list_of_posts = [Comment(**comment_data) for comment_data in comments_data]
        return list_of_posts

    def get_comments_by_post_pk(self, post_id:int) -> list[Comment]:
        #получает все комментарии к определененому посту по его pk
        comments: list[Comment] = self._load_comments()
        comments_match: list[Comment] = [c for c in comments if c.post_id == post_id]
        return comments_match
