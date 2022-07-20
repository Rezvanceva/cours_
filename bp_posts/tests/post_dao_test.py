import pytest

from bp_posts.dao.post import Post
from bp_posts.dao.post_dao import PostDAO

class TestPostsDAO:

    @pytest.fixture
    def post_dao(self):
        post_dao_instance = PostDAO("./bp_posts/tests/post_mock.json")
        return post_dao_instance

    def test_get_all_types(self, post_dao):

        posts = post_dao.get_all()
        assert type(posts) == list, "Incorrect type for result"

        post: Post = post_dao.get_all()[0]
        assert type(post) == Post, "Incorrect type for result single item"

    def test_get_all_fields(self,post_dao):

        posts = post_dao.get_all()
        post: Post = post_dao.get_all()[0]