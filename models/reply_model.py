# models/reply_model.py
from mongoengine import Document, StringField, ReferenceField, ListField

class Reply(Document):
    content = StringField(required=True)
    post = ReferenceField('Post', required=True)  # Use string reference instead of direct import
    likes = ListField(StringField()) # list of user id's that liked the reply
    
    def __str__(self):
        return f'Reply(content={self.content}, post={self.post.title})'
