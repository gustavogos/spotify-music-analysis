import pandas as pd
import sqlite3

#==================================
# CONFIG
# =================================
DATA_PATH = "data/"
DB_PATH = "database/music.db"
# =================================
# LOAD DATA
# =================================
df_music = pd.read_csv(f"{DATA_PATH}spotify_top_music.csv")
df_vars = pd.read_csv(f"{DATA_PATH}spotify_top_music_vars.csv")

# =================================
# EXPLORE DATA
# =================================
def explore_data(df, name):
    print(f"\n==== {name} ====")
    print(df.head())
    print("\nINFO:")
    print(df.info())
    print("\nCOLUNAS:")
    print(df.columns)
    print("\nDESCRIBE:")
    print(df.describe())
    print("\nNULOS:")
    print(df.isnull().sum())

explore_data(df_music, "MUSIC")
explore_data(df_vars, "VARS")


# ====================================
# CLEANING
# ====================================
df_music.columns = df_music.columns.str.lower().str.replace(" ", "_")

print("\n=== COLUNAS PADROZINADAS ===")
print(df_music.columns)

print("\n=== DUPLICADOS ===")
print(df_music.drop_duplicates().sum())

df_music = df_music.drop_duplicates()

print("\n=== TOP GENEROS ===")
print(df_music["top_genre"].value_counts().head(10))

# ====================================
# DATABASE
# ====================================
conn = sqlite3.connect('DB_PATH')
cursor = conn.cursor()

df_music.to_sql('spotify_tracks', conn, if_exists='replace', index=False)

cursor.execute("SELECT * FROM spotify_tracks LIMIT 5")
rows = cursor.fetchall()

print("\n=== DADOS NO SQLITE ===")
for row in rows:
    print(row)

# =========================
#  QUERIES
# =========================
def run_query(query, title):
    cursor.execute(query)
    rows = cursor.fetchall()
    print("\n=== {title} ===")
    for row in rows:
        print(row)

# TOP 10 artistas mais frequentes 
run_query("""
SELECT artist, COUNT(*) as total_tracks
FROM spotify_tracks
GROUP BY artist
ORDER BY total_tracks DESC
LIMIT 10
""", "TOP 10 ARTISTAS")

# Artistas mais populares
run_query("""
SELECT artist, AVG(pop) as avg_popularity
FROM spotify_tracks
GROUP BY artist
ORDER BY avg_popularity DESC
LIMIT 10
""", "ARTISTAS MAIS POPULARES")

# Top gêneros 
run_query("""
SELECT 
    top_genre, 
    COUNT(*) as musics_per_genres
FROM spotify_tracks
GROUP BY top_genre
ORDER BY musics_per_genres DESC
limit 10
""", "TOP GENEROS")

# MÉDIA POR GENEROS 
run_query("""
SELECT 
    top_genre, AVG(pop) as avg_genre
FROM spotify_tracks
GROUP BY top_genre
ORDER BY avg_genre DESC
LIMIT 10
""", "MÉDIA DOS GENEROS")

# Ranking de qualidade (popularidade média por genero)
run_query("""
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
""", "RANKING DE QUALIDADE")

# ====================================
# EXPORT
# ====================================
df_music.to_csv(f"{DATA_PATH}spotify_clean.csv", index=False)

# ====================================
# CLOSE
# ====================================
conn.close()
