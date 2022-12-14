CREATE TABLE IF NOT EXISTS views (
    user_id         String,
    movie_id        String,
    frame           Int64,
    time_created    DateTime
)
    Engine=MergeTree()
    ORDER BY user_id;
