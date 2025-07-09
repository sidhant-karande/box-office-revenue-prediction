import requests
import pandas as pd

API_KEY = '24024bccf5f0cd1f8d60f9bacba3cb6d'
movie_list = ["KGF: Chapter 2", "Inception"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_movies = []

for movie_name in movie_list:
    print(f"\n🔍 Searching for: {movie_name}")
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"

    try:
        search_response = requests.get(search_url, headers=headers).json()

        if search_response['results']:
            movie_id = search_response['results'][0]['id']

            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
            details = requests.get(details_url, headers=headers).json()

            title = details.get('title', 'N/A')
            overview = details.get('overview', 'N/A')
            rating = details.get('vote_average', 'N/A')
            release_date = details.get('release_date', 'N/A')
            genres = ", ".join([genre['name'] for genre in details.get('genres', [])])

            budget = details.get('budget', 0)
            revenue = details.get('revenue', 0)

            # Convert to Crores (divide by 10 million)
            budget_cr = round(budget / 1e7, 2)
            revenue_cr = round(revenue / 1e7, 2)

            # Determine verdict
            if revenue == 0:
                verdict = "❓ Unknown"
            elif revenue < budget:
                verdict = "❌ Flop"
            elif revenue <= 1.5 * budget:
                verdict = "✅ Average"
            elif revenue <= 2 * budget:
                verdict = "🎯 Hit"
            else:
                verdict = "🌟 Blockbuster"

            # Print details
            print(f"🎬 Title: {title}")
            print(f"📅 Release Date: {release_date}")
            print(f"⭐ TMDb Rating: {rating}")
            print(f"🎭 Genres: {genres}")
            print(f"📝 Overview: {overview}")
            print(f"💰 Budget: ₹{budget_cr} Cr")
            print(f"📈 Revenue: ₹{revenue_cr} Cr")
            print(f"🏆 Verdict: {verdict}")

            all_movies.append({
                'Title': title,
                'Release Date': release_date,
                'TMDb Rating': rating,
                'Genres': genres,
                'Overview': overview,
                'Budget (Cr)': budget_cr,
                'Revenue (Cr)': revenue_cr,
                'Verdict': verdict
            })

        else:
            print("❌ Movie not found on TMDb.")

    except requests.exceptions.ConnectionError as e:
        print("⚠️ Network Error:", e)
        print("🔁 Try again later or check your internet connection.")

# Save to CSV
if all_movies:
    df = pd.DataFrame(all_movies)
    df.to_csv("movie_data.csv", index=False)
    print("\n✅ movie_data.csv file saved successfully!")

    # Download in Google Colab
    from google.colab import files
    files.download("movie_data.csv")
