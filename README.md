# Book-Recommendation-system

📚 Book Recommendation System

Welcome to the Book Recommendation System! 🌟 This dynamic web application is designed to help you discover your next favorite read. With personalized recommendations based on various criteria, you'll find books tailored just for you!

📋 Table of Contents

1.Dataset Information
2.Features
3.Technologies Used
4.Installation
5.Usage
6.How It Works
7.Contributors

📊 Dataset Information

The dataset contains 11,128 rows  with the following 12 columns:

bookID
title
authors
average_rating
isbn
isbn13
language_code
num_pages
ratings_count
text_reviews_count
publication_date
publisher


✨ Features

1.Search by Book Title: Get recommendations based on your favorite book. 📖

2.Search by Minimum Rating: Discover top-rated books that meet your rating criteria. ⭐

3.Search by Publisher: Find books published by your favorite publishers. 🏢

4.Search by Author: Get recommendations based on your favorite authors. ✍️

5.Live Search Suggestions: As you type a book title, suggestions will appear to help you find the right book quickly. 🔍

6.Responsive Design: The application is designed to work seamlessly on various devices. 📱💻

⚙️ Technologies Used

1.Flask: A lightweight WSGI web application framework in Python.

2.Pandas: For data manipulation and analysis.

3.NumPy: For numerical computations.

4.Scikit-learn: For implementing machine learning algorithms for book recommendations.

5.HTML/CSS: For front-end development and styling.

6.JavaScript: For dynamic content updates and user interaction.

🛠️ Installation
To set up the project locally, follow these steps:

Clone the repository:

git clone https://github.com/Harshit130127/Machinelearning_based_Bookrecommendation.git
cd Machinelearning_based_Bookrecommendation

Install the required packages:

pip install -r requirements.txt

Prepare the dataset:
Place your books.csv file in the dataset directory.

Run the application:
python app.py

Access the application in your browser at http://127.0.0.1:5000 after run python app.py

💻 Usage
Navigate to the home page.

Use the search forms to find book recommendations based on title, rating, publisher, or author.

View the recommendations displayed on a new page.

🔍 How It Works

The application uses a collaborative filtering approach with a nearest neighbors algorithm to recommend books based on user input:

Data Preparation: The dataset is cleaned and processed using Pandas, with relevant features extracted for modeling.

Recommendation Logic:

1. By Title:Checks if the input title exists in the dataset, retrieves its index, and creates a feature vector. It then uses a nearest neighbors model to find similar titles, including the original book in the recommendations, and limits the output to a maximum of 30 titles.

2. By Rating:Filters the dataset for books that meet or exceed a specified minimum average rating, sorts these books in descending order by their ratings, and returns a list of the top 100 books that match the criteria.

3. By Publisher:Retrieves books published by a specified publisher. If the number of books is less than 30, it constructs a feature vector based on the input publisher and average values for continuous features to find similar publishers. It then recommends additional books from those publishers, ensuring the total recommendations do not exceed 30.

4. By Author:Filters books by a specified author and retrieves their titles. If the number of books is less than 30, it constructs a feature vector to find similar authors and recommends additional titles from those authors, again ensuring the total does not exceed 30 recommendations.

User Interface: Built with HTML/CSS for structure and styling, enhanced with JavaScript for dynamic interactions.

🤝 Contributors

This project is maintained by:
Harshit Mishra 👤
Harshit Khandelwal 👤
Harshvardhan Singh Shekhawat 👤
Mayank Upadhyay 👤
Krishna Kumar 👤
Mohit Kumar 👤

