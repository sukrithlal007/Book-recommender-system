from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)


# @app.before_first_request
# def do_something_only_once():
#     print('111111')


@app.route('/')
def index():
    books_present = list(popular_df['Book-Title'])
    return render_template('recommend.html',present_books = books_present)


@app.route('/recommend')
def recommend_ui():
    books_present = list(popular_df['Book-Title'])
    return render_template('recommend.html',present_books = books_present)

@app.route('/recommend_books',methods=['post','get'])
def recommend_books():
    user_input = request.args.get('user_input')
    try:
        index = np.where(pt.index == user_input)[0][0]
    except IndexError as ie:
        books_present = list(popular_df['Book-Title'])
        return render_template('recommend.html',present_books = books_present,book_name = user_input)
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    # print(data)

    books_present = list(popular_df['Book-Title'])
    return render_template('recommend.html',present_books = books_present ,book_name = user_input,data=data)

if __name__ == '__main__':
    app.run(debug=True)