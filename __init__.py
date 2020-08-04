from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from ratelimiter import RateLimiter

error = False
app = Flask(__name__)
app.static_folder = 'static'
app.template_folder = 'templates'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pass@localhost:3306/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable = False)
    comment = db.Column(db.String(1000), nullable = False)
    def __init__(self, name, comment):
        self.name = name
        self.comment = comment

@app.route('/see')
def see():
    return render_template('see.html')

@app.route('/stay')
def stay():
    return render_template('stay.html')

@app.route('/eat')
def eat():
    return render_template('eat.html')

@app.route('/home')
def redir():
        return redirect('/')


@app.route('/', methods=['GET','POST'])
@RateLimiter(max_calls=10, period=60)   
def postComment():
    comments = db.session.query(Comment).all()
    comments.reverse()
    if request.method == 'POST':
        if len(request.form['form_name']) > 25 or len(request.form['form_name']) < 1 or len(request.form['form_comment']) < 5 or len(request.form['form_name']) > 999:
            error = True
            return render_template('index.html', comments=comments)
        _name = request.form['form_name']
        _comment = request.form['form_comment']

        newcomment = Comment(_name, _comment)
        db.session.add(newcomment)
        db.session.commit()
        comments = db.session.query(Comment).all()
        comments = reversed(comments)
        return render_template('index.html', comments=comments)
    else:
        return render_template('index.html', comments=comments)

@app.route('/del/<commentid>', methods=['POST'])
def delComment(commentid):
    Comment.query.filter_by(id=int(commentid)).delete()
    comments = db.session.query(Comment).all()
    db.session.commit()
    comments = reversed(comments)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug = True)