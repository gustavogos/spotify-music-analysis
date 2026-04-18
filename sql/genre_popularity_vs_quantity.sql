-- Ranking de qualidade (popularidade média por genero)
SELECT 
    top_genre,
    COUNT(*) AS total_musicas,
    ROUND(AVG(pop), 2) AS media_popularity
FROM
    spotify_tracks
GROUP BY
    top_genre
ORDER BY
    media_popularity DESC