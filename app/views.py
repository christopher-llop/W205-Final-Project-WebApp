from flask import render_template, flash, redirect, session
from app import app
from .forms import LoginForm, PostForm
from config import POSTS_PER_PAGE, MAX_PAGES_DISPLAYED
from .query import dead_query, query, ranked_query, fetch_details

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:CurrentPage>', methods=['GET', 'POST'])
def index(CurrentPage = 1):
    form = PostForm()
    if form.validate_on_submit():
        #flash('Search requested for Keywords="%s"' % (form.post.data))
        #return redirect('/index')
        #posts = dead_query(form.post.data)
        #posts = list(query(form.post.data))
        #posts = list(ranked_query(form.post.data))
        print form.sliderField1.data
        print form.sliderField2.data
        print form.sliderField3.data
        print form.sliderField4.data
        flash(form.sliderField4.data)
        posts = dead_query(query_string="test1")
        #print posts
        session['posts'] = posts[0:400]

    if 'posts' in session:
        posts = session['posts']
        print "Restoring Posts from Cookie"
    else:
        posts = []
        print "No Cookie"
    ResultsCount = len(posts)
    TotalPages = ResultsCount // POSTS_PER_PAGE
    if (ResultsCount % POSTS_PER_PAGE > 0):
        TotalPages += 1

    posts = posts[POSTS_PER_PAGE * (CurrentPage - 1):POSTS_PER_PAGE * CurrentPage]
    post_data = fetch_details(posts)

    return render_template('index.html',
                           title='Home',
                           posts=post_data,
                           form=form,
                           ResultsCount=ResultsCount,
                           TotalPages=TotalPages,
                           CurrentPage=CurrentPage,
                           MaxPage=MAX_PAGES_DISPLAYED)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form)