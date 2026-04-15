# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**TuneFinder 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 
 

This system suggests up to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is designed for classroom exploration to demonstrate how content-based recommendation systems work. It is not intended for real-world use or production music platforms.


---

## 3. How the Model Works  

Explain your scoring approach in simple language.  


**TuneFinder 1.0** compares each song in the catalog to a user's taste profile using a simple point-based scoring system. For every song, it checks three things:

- If the song's genre matches the user's favorite genre, it earns 2 points
- If the song's mood matches the user's favorite mood, it earns 1 point
- The song earns up to 1 additional point based on how close its energy level is to the user's target energy

Once every song has a score, the system sorts them from highest to lowest and returns the top results. Each recommendation includes an explanation of why it was suggested, such as "genre match (+2.0), energy similarity (0.95)."


---

## 4. Data  

Describe the dataset the model uses.  


- The catalog contains 20 songs stored in `data/songs.csv`
- Genres represented: pop, lofi, rock, jazz, ambient, synthwave, indie pop, electronic
- Moods represented: happy, chill, intense, relaxed, moody, focused
- 10 songs were in the original starter file; 10 additional songs were added to improve diversity
- The dataset reflects a bias toward Western popular music styles and does not include classical, country, hip-hop, or world music

---

## 5. Strengths  

Where does your system seem to work well  


- Works well for users with clear, common preferences like "chill lofi" or "high-energy pop"
- Recommendations are fully explainable, every suggestion includes a reason
- Simple and transparent scoring makes it easy to understand and debug
- Fast performance even without any machine learning

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 
 

- Genre match is worth twice as much as mood match, which can create a "filter bubble" where users only see one genre
- The catalog is very small (20 songs), so niche genres like ambient or electronic have very few options
- Energy similarity can reward songs that are close in energy even if they feel completely different
- The system does not consider tempo, valence, danceability, or acousticness in scoring
- Users with conflicting preferences (e.g., high energy but chill mood) may get unexpected results
- The dataset does not represent many global music styles, making it biased toward certain listener types

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 


A weight shift experiment was also considered: doubling the energy weight and halving the genre weight would likely surface more cross-genre results based on vibe rather than category.

---

## 8. Future Work  

Ideas for how you would improve the model next.  


- Add support for more features in scoring, such as tempo range preferences and valence
- Expand the catalog to hundreds of songs across more genres and cultures
- Implement collaborative filtering to learn from multiple users' listening history
- Add diversity balancing so the top results include songs from different genres
- Build a Streamlit UI so users can interactively adjust their taste profile and see results change in real time


---

## 9. Personal Reflection  

A few sentences about your experience.  


Building TuneFinder taught me how recommendation systems transform raw data into personalized suggestions through simple math. I was surprised by how reasonable the results felt even with such a basic scoring system, it shows that a few well-chosen rules can go a long way. The biggest insight was discovering how small weight decisions, like making genre worth 2x more than mood, can unintentionally limit what users discover. This made me think about how real platforms like Spotify might struggle with the same problem at a much larger scale, and why human oversight in AI systems still matters even when the algorithm seems to be working correctly.
