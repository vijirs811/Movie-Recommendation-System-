import pandas as pd
from django.shortcuts import render
from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split

def index(request):
    return render(request, 'index.html')

def generate_recommendations(request):
    if request.method == 'POST':
        user_id = int(request.POST['user_id'])
        
        # Load data from CSV files
        ratings = pd.read_csv('rating.csv')
        movies = pd.read_csv('Movie_Id_Titles.csv')

        # Load Data into Surprise
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(ratings[['user_id', 'item_id', 'rating']], reader)

        # Split the dataset into training and testing sets
        trainset, _ = train_test_split(data, test_size=0.2)

        # Choose Collaborative Filtering Algorithm
        sim_options = {'name': 'cosine', 'user_based': True}
        model = KNNBasic(sim_options=sim_options)

        # Train the Model
        model.fit(trainset)

        # Generate Recommendations
        user_inner_id = trainset.to_inner_uid(user_id)
        user_neighbors = model.get_neighbors(user_inner_id, k=5)
        user_neighbors = [trainset.to_raw_uid(inner_id) for inner_id in user_neighbors]
        top_n_recommendations = movies.set_index('item_id').loc[[trainset.to_raw_iid(inner_id) for inner_id in user_neighbors]]['title'].values

        return render(request, 'recommendations.html', {'user_id': user_id, 'recommendations': top_n_recommendations})
    
    return render(request, 'index.html')
