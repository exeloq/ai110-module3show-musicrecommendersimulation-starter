# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

GrooveMatrix
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
It will generate a sorted list of song recommendations that match the user's profile card based on a set of complicated vector math.
- What assumptions does it make about the user  
This model assumes the user does not intend to exit their 'genre comfort zone', and will not suggest songs outside of their favorite genre. 
- Is this for real users or classroom exploration  
Currently it isn't ready for real users because of it's simplicity and small dataset.
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)
Genre is used as a hard filter before scoring begins. Mood is evaluated as a categorical match. Energy, acousticness, valence, danceability, and tempo are all evaluated as continuous variables using a proximity formula. Artist is used in the planned diversity penalty during the ranking phase. Title and id are display and for identification only.

- What user preferences are considered
The UserProfile stores seven preferences: favorite_genre, favorite_mood, target_energy, target_acousticness, target_valence, target_danceability, and target_tempo_bpm. Each one maps directly to a feature in the Song object and contributes its own component to the final score.

- How does the model turn those into a score
Genre filters the candidate pool first. Then for each remaining song, mood is compared as a binary match worth up to 1.5 points. The five continuous features are each scored using the formula Weight x (1 - abs(user_target - song_value)), which produces a value between 0 and 1 scaled by the feature's weight. All components are summed into a single total score, songs are sorted highest to lowest, and the top k results are returned with a per-component breakdown explaining each score.

- What changes did you make from the starter logic
The starter used a simple points system where genre match added 2.0 points and mood match added 1.0 point, with a rough energy similarity bonus. We replaced this entirely with a weighted proximity model that evaluates five continuous dimensions instead of one, treats genre as a hard filter rather than a bonus, replaces the boolean likes_acoustic field with a float target, and adds targets for valence, danceability, and tempo that the original system did not consider at all.

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
There are 20 songs in total in the catalog.
- What genres or moods are represented 
The dataset represents 10 genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, r&b, classical, edm, metal, country, reggae, soul, funk, and latin. The dataset represents 16 moods: happy, chill, intense, relaxed, moody, focused, uplifting, romantic, peaceful, euphoric, angry, nostalgic, melancholic, sad, playful, and festive.
- Did you add or remove data  
I prompted Claude to add 10 songs to the dataset.
- Are there parts of musical taste missing in the dataset  
There is no field for lyrics, language, or theme. It also disregards the name of the artist in suggesting songs. There is also no "listening context" field, which might be crucial in finding the right song for the right situation. You don't want to be suggested the same songs for working out an studying.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results
The system works great for users whose favorite genre is present more than others in the catalog and whose mood preference has at least one match. The "High-Energy Pop" profile we made as a stress test is the clearest example: pop has three candidates, the mood "happy" exists in the catalog, and the continuous targets are specific enough that the proximity formula produces meaningfully different scores between songs rather than a tie.

- Any patterns you think your scoring captures correctly
The proximity formula correctly rewards closeness on all five continuous dimensions, so a song that is slightly off on every feature scores lower than a song that is a strong match on a lot of features. The system also correctly separates acousticness as its own dimension rather than assuming high energy always means low acoustic.

- Cases where the recommendations matched your intuition
The "Chill Lofi" profile returns songs with high acousticness and low energy no top, which matches what a lofi listener would expect. The "Deep Intense Rock" profile outputs Storm Runner correctly since it is the only rock song and its attributes closely align with high energy and low acousticness targets. The "Mood With No Match in Genre" edge case test also behaved as we expected: the jazz song still appeared in results but with zero mood points, making sure the system degrades gracefully rather than crashing or returning random output.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider
The system has no concept of lyrical content, listening context, or artist name. A user who only listens to French music or exclusively wants new releases has no way to tune the tool, and the system would treat those songs identically to anything else in the catalog.

- Genres or moods that are underrepresented
Most genres in the catalog have only one song, meaning the scoring formula has almost nothing to compare within those genres. A reggae or funk listener gets a single result. Moods like "peaceful," "festive," and "euphoric" each appear once, so any user whose favorite mood is not "chill" or "happy" will almost always receive a mood mismatch on every result.

- Cases where the system overfits to one preference
Because energy has a weight of 1.5, a user with a very specific energy target will consistently see that dimension in their score breakdown despite how well other features match. The edge case test "Impossible Lofi" demonstrates this: the system still returns lofi songs even though every continuous target is the opposite of what lofi songs offer, because there are simply no other candidates after the genre filter runs.

- Ways the scoring might unintentionally favor some users
Users whose favorite genre is pop benefit from having three songs in the catalog, giving the formula more meaningful candidates to rank. Users whose favorite mood is "happy" as well, since those moods appear more.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
