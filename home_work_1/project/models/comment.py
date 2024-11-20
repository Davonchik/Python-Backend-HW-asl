from datetime import datetime
import functools


class Comment:
    def __init__(self, author_id: int, text: str) -> None:
        self.author_id = author_id
        self.text = text
        self.create_data = datetime.now()
        self.update_data = self.create_data
        self.like_count = 0

    def update_event(func: callable) -> None:
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.update_data = datetime.now()
        return wrapper

    @update_event
    def edit_comment(self, new_text: str) -> None:
        self.text = new_text

    @update_event
    def like(self) -> None:
        self.like_count += 1

    @update_event
    def dislike(self) -> None:
        self.like_count -= 1

    def __repr__(self) -> str:
        return f"Author: {self.author_id}, Text: {self.text}, Like: {self.like_count}"
