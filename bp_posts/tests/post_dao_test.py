import pytest
from _pytest.capture import capfd

from bp_posts.dao.post import Post
from bp_posts.dao.post_dao import PostDAO


def check_fields(post):
    fields = ["poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"]
    for field in fields:
        assert hasattr(post, field), f"Нет поля {field}"


class TestPostsDAO:

    @pytest.fixture
    def post_dao(self):
        post_dao_instance = PostDAO("post_mock.json")
        return post_dao_instance

### функция получения всех

    def test_get_all_types(self, post_dao):
        posts = post_dao.get_all()
        assert type(posts) == list, "Incorrect type for result"
        post: Post = post_dao.get_all()[0]
        assert type(post) == Post, "Incorrect type for result single item"

    def test_get_all_fields(self, post_dao):
        posts = post_dao.get_all()
        post: Post = post_dao.get_all()[0]
        check_fields(post)


    def test_get_all_correct_ids(self,  post_dao):
        posts = post_dao.get_all()
        correct_pks = {1, 2, 3}
        pks = set([post.pk for post in posts])
        assert pks == correct_pks, "не совпадают полученные id"


### функция получения одного по pk


    def test_get_by_pk_types(self, post_dao):
        post = post_dao.get_by_pk(1)
        assert type(post) == Post, "Incorrect type for result single item"

    def test_get_by_pk_fields(self, post_dao):
        post = post_dao.get_by_pk(1)
        check_fields(post)


    def test_get_by_pk_none(self, post_dao):
        post = post_dao.get_by_pk(999)
        assert post is None, "Should be None for non existent pk"


    @pytest.mark.parametrize("pk", [1, 2, 3])
    def test_get_by_pk_correct_id(self, post_dao, pk):
        post = post_dao.get_by_pk(pk)
        assert post.pk == pk, f"Incorrect post.pk for requestion post with pk ={pk}"


### функция получения постов по вхождению строки

    def test_search_in_content_types(self, post_dao):
        posts = post_dao.search_in_content("ага")
        assert type(posts) == list, "Incorrect type for result"
        post: Post = post_dao.get_all()[0]
        assert type(post) == Post, "Incorrect type for result single item"

    def test_search_in_content_fields(self, post_dao):
        posts = post_dao.search_in_content("ага")
        post: Post = post_dao.get_all()[0]
        check_fields(post)

    def test_search_in_content_not_found(self, post_dao):
        posts = post_dao.search_in_content("999D9999")
        assert posts == [] , "Should be [] for not subbstring not found"

    @pytest.mark.parametrize("s, expected_pks", [
        ("ага", {1}),
        ("вышел", {2}),
        ("на", {1, 2, 3})
    ])
    def test_search_in_content_results(self, post_dao, s, expected_pks):
        posts = post_dao.search_in_content(s)
        pks = set([post.pk for post in posts])
        assert pks == expected_pks, f"Incirrect result searching for {s}"

### функция получения постов по имени автора

    def test_get_by_poster_types(self, post_dao):
        posts = post_dao.get_by_poster("999D9999")
        assert type(posts) == list, "Incorrect type for result"
        post: Post = post_dao.get_all()[0]
        assert type(post) == Post, "Incorrect type for result single item"

    def test_get_by_poster_fields(self, post_dao):
        posts = post_dao.get_by_poster("leo")
        post: Post = post_dao.get_all()[0]
        check_fields(post)

    def test_get_by_poster_not_found(self, post_dao):
        posts = post_dao.get_by_poster("leo")
        assert posts == [] , "Should be [] for not subbstring not found"

    @pytest.mark.parametrize("poster, name", [
        ("leo", "leo"),
        ("johnny", "johnny"),
        ("hank", "hank")
    ])
    def test_get_by_poster_results(self, post_dao, poster, name):
        posts = post_dao.get_by_poster(poster)
        result_of_poster = set([post.poster_name for post in posts])
        assert result_of_poster == name, f"Incirrect result searching for {name}"

