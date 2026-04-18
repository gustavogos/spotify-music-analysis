-- Média por gêneros musicais
SELECT 
    top_genre, AVG(pop) as avg_genre
FROM spotify_tracks
GROUP BY top_genre
ORDER BY avg_genre DESC
LIMIT 10
