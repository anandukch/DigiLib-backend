import pickle
import os
# file_path = os.path.abspath('popular.pkl')

def get_popular_books():
    try:
        with open (os.getcwd() + '/app/models/popular.pkl'
                   , 'rb') as f:
            print(f)
            df = pickle.load(f)
            return df
    except Exception as e:
        raise e
    
def get_book_by_title(title: str):
    try:
        with open (os.getcwd() + '/app/models/books.pkl'
                   , 'rb') as f:
            df = pickle.load(f)
            return df[df['Book-Title'] == title]
    except Exception as e:
        raise e


def recommend_books(values: list):
    print(values)
    try:
        with open (os.getcwd() + '/app/models/knn_model.pkl'
                   , 'rb') as f:
            model = pickle.load(f)
            book_class = model.predict([values])
            books = pickle.load(open(os.getcwd() + '/app/models/book.pkl', 'rb'))
            # print(books[books['Class'] == book_class[0]])
            return books[books['Class'] == book_class[0]]
            
    except Exception as e:
        raise e

