class NewsArticle:
    def __init__(self, title, content, publish_date, source, url=None, author=None, tags=None):
        self.title = title
        self.content = content
        self.publish_date = publish_date
        self.source = source
        self.url = url
        self.author = author
        self.tags = tags  # This could be a list of keywords or categories

    def to_dict(self):
        """Converts the article object to a dictionary."""
        return self.__dict__
        
    @classmethod
    def from_dict(cls, article_dict):
        """Creates an article object from a dictionary."""
        return cls(**article_dict)
