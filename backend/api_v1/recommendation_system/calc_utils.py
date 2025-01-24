import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def tfidf_similarity(games_a, games_b, all_games):
    vectorizer = TfidfVectorizer(vocabulary=all_games)
    tfidf_matrix = vectorizer.fit_transform([' '.join(games_a), ' '.join(games_b)])
    return (tfidf_matrix * tfidf_matrix.T).A[0, 1]

def tfidf_similarity2(all_users_games):
    all_games_texts = [' '.join(games) for games in all_users_games.values()]
    vectorizer_games = TfidfVectorizer()
    tfidf_matrix_games = vectorizer_games.fit_transform(all_games_texts)
    return tfidf_matrix_games

def euclidean_similarity(user_a, user_b, weights):
    distance = np.sqrt(sum(weights[attr] * (user_a[attr] - user_b[attr]) ** 2 for attr in weights))
    return 1 / (1 + distance)  # Нормализация в [0,1]

def jaccard_similarity(set_a, set_b):
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union else 0

def calculate_similarity(user_vector, candidate_vector):
    """
    Вычисляет схожесть двух игроков с помощью косинусного сходства.
    """
    user_vector = np.array(user_vector).reshape(1, -1)
    candidate_vector = np.array(candidate_vector).reshape(1, -1)
    return cosine_similarity(user_vector, candidate_vector)[0][0]