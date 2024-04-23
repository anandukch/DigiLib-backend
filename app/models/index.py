import pickle
import os

# file_path = os.path.abspath('popular.pkl')


def get_popular_books():
    try:
        with open(os.getcwd() + "/app/models/popular.pkl", "rb") as f:
            print(f)
            df = pickle.load(f)
            return df
    except Exception as e:
        raise e


def get_book_by_title(title: str):
    try:
        with open(os.getcwd() + "/app/models/books.pkl", "rb") as f:
            df = pickle.load(f)
            return df[df["Book-Title"] == title]
    except Exception as e:
        raise e

import pandas as pd
def recommend_books(values: list):
    
    try:
        with open(os.getcwd() + "/app/models/knn_model2.pkl", "rb") as f:
            model = pickle.load(f)
            # check if the all the values are 0
            
            book_class = model.predict([values])
            books = pickle.load(open(os.getcwd() + "/app/models/book.pkl", "rb"))
            print(book_class[0])

            extra_books = []
            true_results = []
            if book_class[0] != "Poetry" and values[9] == 1:
                extra_books.append(books[books["CLASS"] == "Poetry"].sample(5))
            if book_class[0] != "History" and values[3] == 1:
                extra_books.append(books[books["CLASS"] == "History"].sample(5))
            if book_class[0] != "Comic" and (values[6] == 1 or values[8]==1):
                extra_books.append(books[books["CLASS"] == "Comic"].sample(5))
            if book_class[0] != "Biography" and values[0] == 1:
                extra_books.append(books[books["CLASS"] == "Biography"].sample(5))
                        
            # Extract true results
            true_results = books[books["CLASS"] == book_class[0]]

            # Take 5 random books from extra books
            # if extra_books:
            #     extra_books = pd.concat(extra_books)

            # # Take 5 random books from true results
            # true_results = true_results[:5]

            # # Append extra books to true results
            # combined_books = true_results.append(extra_books, ignore_index=True)

            # print(combined_books)
            
            return true_results[:10],extra_books

    except Exception as e:
        raise e
