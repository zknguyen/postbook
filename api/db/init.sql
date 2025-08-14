CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    firebase_uid VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE TABLE follows (
    follow_id SERIAL PRIMARY KEY,
    follower_id INT NOT NULL,
    CONSTRAINT fk_follower FOREIGN KEY (follower_id)
    REFERENCES users(user_id),
    followee_id INT NOT NULL,
    CONSTRAINT fk_followee FOREIGN KEY (followee_id)
    REFERENCES users(user_id)
);

CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id)
    REFERENCES users(user_id),
    text_content TEXT NOT NULL,
    num_likes INT NOT NULL DEFAULT 0,
    media_url VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp
);
CREATE INDEX idx_created_at ON posts (created_at);

CREATE TABLE likes (
    like_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id)
    REFERENCES users(user_id),
    post_id INT NOT NULL,
    CONSTRAINT fk_post FOREIGN KEY (post_id)
    REFERENCES posts(post_id),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id)
    REFERENCES users(user_id),
    post_id INT NOT NULL,
    CONSTRAINT fk_post FOREIGN KEY (post_id)
    REFERENCES posts(post_id),
    text_content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE TABLE feeds (
    feed_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id)
    REFERENCES users(user_id),
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE TABLE feed_posts (
    feed_post_id SERIAL PRIMARY KEY,
    feed_id INT NOT NULL,
    CONSTRAINT fk_feed FOREIGN KEY (feed_id)
    REFERENCES feeds(feed_id),
    post_id INT NOT NULL,
    CONSTRAINT fk_post FOREIGN KEY (post_id)
    REFERENCES posts(post_id)
);

INSERT INTO users (username, first_name, last_name, email, firebase_uid) VALUES
('admin', 'ADMIN', '', 'admin@postbook.com', 'abc123');

INSERT INTO feeds (user_id) VALUES
((SELECT user_id FROM users WHERE username='admin'));

INSERT INTO posts (user_id, text_content) 
VALUES
((SELECT user_id FROM users WHERE username='admin'), 'This is my first post'),
((SELECT user_id FROM users WHERE username='admin'), 'This is my second post');

INSERT INTO comments (user_id, post_id, text_content)
VALUES
((SELECT user_id FROM users WHERE username='admin'), 
 (SELECT post_id FROM posts WHERE text_content='This is my first post'), 
 'This is a comment on the first post'),
((SELECT user_id FROM users WHERE username='admin'), 
 (SELECT post_id FROM posts WHERE text_content='This is my second post'), 
 'This is a comment on the second post');