SELECT 
    top_genre, 
    COUNT(*) as musics_per_genres
FROM spotify_tracks
GROUP BY top_genre
ORDER BY musics_per_genres DESC
limit 10
