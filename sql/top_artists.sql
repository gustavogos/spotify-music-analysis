SELECT artist, COUNT(*) as total_tracks
FROM spotify_tracks
GROUP BY artist
ORDER BY total_tracks DESC
LIMIT 10;