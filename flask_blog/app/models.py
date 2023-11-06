from App import db
from datetime import datetime
import re
from time import time

def slugify(s):
    pattern = r"[^\w+]"
    return re.sub(pattern, '-', s)

posts_tags = db.Table('posts_tags',
                      db.Column('post_id', db.Integer,
                      db.ForeignKey('post.id')),
                      db.Column('tag_id', db.Integer,
                      db.ForeignKey('tag.id'))
                      )

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140)) 
    slug = db.Column(db.String(140), unique=True) 
    body = db.Column(db.Text)
    filepath = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.now())
    tags = db.relationship('Tag', secondary='posts_tags', 
                           backref=db.backref('posts'),
                           lazy='dynamic')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()
    
    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)
        else:
            self.slug = str(int(time()))

    def __repr__(self):
        return f"<post id: {self.id} title: {self.title} body: {self.body}>"
    
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140)) 
    slug = db.Column(db.String(140), unique=True)
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = slugify(self.title)
        
    def __repr__(self):
        return f"<Tag id: {self.id} title: {self.title}>"