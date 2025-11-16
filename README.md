# SwipeFlix: Smart Movie Recommendation App
![proj_gif](https://github.com/user-attachments/assets/e9b044bc-3296-4028-9b1a-7c2649e3e478)

## Inspiration
Choosing a movie shouldn’t feel like homework. We wanted something fast, fun, and addictive. SwipeFlix was inspired by the idea that preferences can be learned extremely quickly if the system is reactive enough.  
So we built a recommender that adapts **every time you swipe**.

## Project Overview
**SwipeFlix** is an intelligent movie-recommendation app that works like Tinder for movies.  
Users swipe **like** or **dislike**, and the system instantly updates its understanding of their taste.

It does this by:

- Tracking liked genres, actors, countries, and decades  
- Computing a probability score using feature ratios (likes/dislikes)  
- Picking new movies using a weighted scoring system  
- Mixing **90% smart picks** with **10% exploration**, where exploration starts at **50%** and decays by **5% per movie**  
- Generating insights like *“You seem to like 90s crime movies starring Brad Pitt”*  
- Showing a dynamic **likelihood bar** for how much you’ll enjoy the next movie  

Over time, the recommendations become sharper, more personalized, and surprisingly accurate.

## How we built it
The frontend was built using **HTML, CSS, JavaScript, and TailwindCSS**.  

The backend was built using **Flask**, and the core recommendation engine is a **Bayesian-style scoring model** that transforms the like to dislike ratio of movie features into a probability estimate using a logistic function.
This converts the user’s historical like/dislike behavior into a continuous probability from 0 to 1.

## Challenges we ran into
- Ensuring the probability system stayed stable when data was sparse  
- Handling movies with features the user had never rated before  
- Preventing the system from getting stuck in a genre “feedback loop”  
- Designing an exploration system that’s both smart and unpredictable  
- Managing the removal and cycling of movies from the recommendation pool  
- Making the learning updates fast enough to feel instant during swipes  

## Accomplishments that we're proud of
- We built a fully functioning adaptive recommender from scratch
- The probability model actually behaves realistically and self-corrects 
- Insights like *“You seem to like…”* turned out surprisingly accurate
- The explore–exploit balance (50% → 10% decay) created natural diversity  
- It genuinely *feels fun* to swipe through movies and watch it learn

## What we learned
- Logistic models are fantastic for real-time personalization  
- Small weights (like 0.5 for country) dramatically affect recommendation stability  
- Exploration is essential, or the system becomes too confident too early  
- Users respond really well to explanations (“You seem to like…”)  
- Building a good recommender = balancing stats, intuition, and UX

## What's next for SwipeFlix
- Add a “why this movie” explanation for transparency  
- Build persistent user profiles and long-term preference memory  
- Introduce collaborative filtering to blend personal + global trends  
- Add trailer previews, watchlists, and social features  
- Release a mobile app version for smoother swiping
