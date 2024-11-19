# models/post_model.py
from mongoengine import Document, StringField, ListField, ReferenceField

class Post(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    replies = ListField(ReferenceField('Reply'))  # Use string reference instead of direct import
    likes = ListField(StringField())  #List to store user Id of those who liked the post
    
    def __str__(self):
        return f'Post(title={self.title}, content={self.content})'
