from backend.api_v1.posts.models_sql import Post


def format_feed(users_posts: list[Post], communities_posts: list[Post]):
    unique