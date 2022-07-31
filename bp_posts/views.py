import logging

from flask import Flask, Blueprint, render_template, current_app, request
from werkzeug.exceptions import abort

from bp_posts.dao.comment import Comment
from bp_posts.dao.comment_dao import CommentDAO
from bp_posts.dao.post import Post
from bp_posts.dao.post_dao import PostDAO
from config import DATA_PATH_POSTS, DATA_PATH_COMMENTS

bp_posts = Blueprint("bp_posts", __name__, template_folder="templates")
#создаем объект доступа к данным
post_dao = PostDAO(DATA_PATH_POSTS)
comments_dao = CommentDAO(DATA_PATH_COMMENTS)

@bp_posts.route("/")
#все посты
def page_posts_index():
    all_posts = post_dao.get_all()
    return render_template("posts_index.html", posts=all_posts)


@bp_posts.route("/posts/<int:pk>/") #один пост
def page_posts_single(pk):
    post: Post | None = post_dao.get_by_pk(pk)
    comments: list[Comment] = comments_dao.get_comments_by_post_pk(pk)

    if post is None:
        abort(404)

    return render_template("posts_single.html",
                           post=post,
                           comments = comments,
                           comments_len = len(comments)
                        )

@bp_posts.route("/users/<user_name>") #все посты пользователя
def page_posts_by_user(user_name: str):
    posts: list[Post] = post_dao.get_by_poster(user_name)

    if posts == []:
        abort(404, "Такого пользователя не существует")

    return render_template("posts_user-feed.html",
                           posts = posts,
                           user_name = user_name
                           )

@bp_posts.route("/search/") #поиск постов
def page_posts_search():

    query: str = request.args.get("s", "")
    if query == "":
        posts: list = []
    else:
        posts = post_dao.search_in_content(query)

    return render_template("posts_search.html",
                           posts = posts,
                           query = query,
                           posts_len = len(posts)
                           )


