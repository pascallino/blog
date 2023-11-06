from  App import app
import views
from App import db
from posts.blueprint import posts

app.register_blueprint(posts, url_prefix='/blog')


if __name__ == '__main__':
    app.run()