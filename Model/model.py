
# - bookID: Unique identification number fro each book
# - title: Name under which book was published
# - authors: Name of the Authors of the book
# - average_rating: Avarage rating of the book recevied in total.
# - isbn: International standarded book number
# - isbn13: 13 digit isbn to identify the book
# - language_code: Primary Language of the book
# - num_pages: Number of pages the book containes
# - ratings_count: Total Number of ratings the book recevied.
# - text_reviews_count: Total number of written reviews recevied.
# - publication_date: Date when the book was first published
# - publisher: Name of the Pulishers



import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv(r"dataset/books.csv", on_bad_lines = 'skip')


df.drop(['bookID', 'isbn', 'isbn13'], axis = 1, inplace = True)



df['year'] = df['publication_date'].str.split('/')
df['year'] = df['year'].apply(lambda x: x[2])

df['year'] = df['year'].astype('int')

df.to_csv(r'dataset/cleaned_data.csv',index=False)

df=pd.read_csv(r'dataset/cleaned_data.csv')

df[df['year'] == 2020][['title', 'authors','average_rating','language_code','publisher' ]]


df.groupby(['year'])['title'].agg('count').sort_values(ascending = False).head(20)


df[df.average_rating == df.average_rating.max()][['title','authors','language_code','publisher']]


publisher = df['publisher'].value_counts()[:20]
publisher

df.head(5)


def num_to_obj(x):
    if x >0 and x <=1:
        return "between 0 and 1"
    if x > 1 and x <= 2:
        return "between 1 and 2"
    if x > 2 and x <=3:
        return "between 2 and 3"
    if x >3 and x<=4:
        return "between 3 and 4"
    if x >4 and x<=5:
        return "between 4 and 5"
df['rating_obj'] = df['average_rating'].apply(num_to_obj)



rating_df = pd.get_dummies(df['rating_obj'])     #one hot encoding
rating_df.head()


language_df = pd.get_dummies(df['language_code'])
language_df.head()


features = pd.concat([rating_df,language_df, df['average_rating'],
                    df['ratings_count'], df['title']], axis = 1)
features.set_index('title', inplace= True)
features.head()

from sklearn.preprocessing import StandardScaler


scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

features_scaled

# # Model Building


from sklearn import neighbors

import traceback



model = neighbors.NearestNeighbors(n_neighbors=10, algorithm = 'ball_tree',
                                  metric = 'euclidean')
model.fit(features_scaled)
dist, idlist = model.kneighbors(features_scaled)


def normalize_title(title):
    """ Normalize title by removing extra spaces and standardizing format """
    # Convert to lowercase
    title = title.lower()
    
    # Remove extra spaces, including around special characters
    title = re.sub(r'\s+', ' ', title)  # Replace multiple spaces with single space
    title = re.sub(r'\s*([\(\)\[\]#,:])\s*', r'\1', title)  # Remove spaces around special characters
    
    # Remove any non-essential punctuation
    title = re.sub(r'[^\w\s\(\)\[\]#,:-]', '', title)
    
    return title.strip()

def BookRecommender(book_name):
    book_list_info = []
    
    try:
        # Normalize input
        normalized_input = normalize_title(book_name)
        
        # Normalize dataset titles for comparison
        if 'normalized_title' not in df.columns:
            df['normalized_title'] = df['title'].apply(normalize_title)
        
        # Debug output
        print(f"Original Input: {book_name}")
        print(f"Normalized Input: {normalized_input}")
        
        # Try different matching strategies
        
        # First try exact match
        exact_match = df[df['normalized_title'] == normalized_input]
        
        
        if exact_match.empty:
            # Remove everything after and including parentheses or brackets
            base_title = re.split(r'[\(\[\{]', normalized_input)[0].strip()
            book_id_row = df[df['normalized_title'].str.contains(re.escape(base_title), na=False, case=False)]
        else:
            book_id_row = exact_match
            
        
        if book_id_row.empty:
            # Remove special characters and try partial match
            simplified_input = re.sub(r'[^\w\s]', '', normalized_input)
            simplified_titles = df['normalized_title'].apply(lambda x: re.sub(r'[^\w\s]', '', x))
            book_id_row = df[simplified_titles.str.contains(simplified_input, na=False, case=False)]

        print(f"Matched Rows:\n{book_id_row[['title', 'authors']].head()}")

        if not book_id_row.empty:
            book_id = book_id_row.index[0]
            
            # Add original book
            book_list_info.append(f"{df.iloc[book_id].title} by {df.iloc[book_id].authors}")
            
            # Add recommendations
            for newid in idlist[book_id]:
                if newid != book_id:
                    recommended_title = df.iloc[newid].title
                    recommended_author = df.iloc[newid].authors
                    book_list_info.append(f"{recommended_title} by {recommended_author}")
        else:
            print(f"Book '{book_name}' not found in the database.")
            # Show similar titles for debugging
            print("\nSimilar titles in database:")
            similar_words = book_name.lower().split()
            for word in similar_words:
                if len(word) > 3:  # Only check for words longer than 3 characters
                    similar = df[df['normalized_title'].str.contains(word, na=False, case=False)]
                    if not similar.empty:
                        print(f"\nTitles containing '{word}':")
                        print(similar['title'].head().tolist())
        
    except Exception as e:
        print(f"Error in BookRecommender: {str(e)}")
        traceback.print_exc()  # Print full error traceback
        
    return book_list_info


def recommend_by_rating(min_rating):
    filtered_books = df[df['average_rating'] >= min_rating]
    
    top_books = filtered_books.sort_values(by='average_rating', ascending=False).head(125)  # Get top 125 books
    
    book_list_info = [f"{row['title']} by {row['authors']}" for index, row in top_books.iterrows()]
    
    return book_list_info


def recommend_by_publisher(publisher_name):
    filtered_books = df[df['publisher'].str.lower() == publisher_name.lower()]
    
    top_books = filtered_books.sort_values(by='average_rating', ascending=False).head(30)  #get top 25 books
    
    book_list_info = [f"{row['title']} by {row['authors']}" for index, row in top_books.iterrows()]
    
    return book_list_info


def normalize_author(author):
    """ Normalize author name by removing unwanted characters and converting to lowercase. """
    return re.sub(r'[^\w\s#():""-]', '', author).lower().strip()


def recommend_by_author(author_name):
    author_list_info = []
    
    # Normalize input
    normalized_input = normalize_author(author_name)
    
    # Normalize dataset authors for comparison
    df['normalized_authors'] = df['authors'].apply(normalize_author)
    
    # Check if the input contains special characters
    if re.search(r'[^\w\s#():""-]', author_name): 
        print("Input contains special characters.")
        # Use str.contains instead of str.extract
        author_id_row = df[df['normalized_authors'].str.contains(re.escape(normalized_input), na=False, case=False)]
    else:
        # Logic for simple string inputs
        print("Input is a simple string.")
        author_id_row = df[df['normalized_authors'].str.contains(re.escape(normalized_input), na=False, case=False)]
    
    if not author_id_row.empty:
        author_id = author_id_row.index[0]
        
        author_list_info.append(f"{df.iloc[author_id].title} by {df.iloc[author_id].authors}")
        
        # Assuming `idlist` is defined similarly to the BookRecommender function
        for newid in idlist[author_id]:
            if newid != author_id:
                recommended_title = df.iloc[newid].title
                recommended_author = df.iloc[newid].authors
                author_list_info.append(f"{recommended_title} by {recommended_author}")
                
    else:
        print(f"Author '{author_name}' not found in the database.")
    
    return author_list_info

