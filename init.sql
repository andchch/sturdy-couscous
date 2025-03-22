-- alembic_version определение

CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);


-- genres определение

CREATE TABLE genres (
	name VARCHAR NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	PRIMARY KEY (id)
);


-- users определение

CREATE TABLE users (
	username VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	hashed_password VARCHAR NOT NULL, 
	gender VARCHAR(6), 
	dob DATETIME, 
	avatar_url VARCHAR NOT NULL, 
	description VARCHAR, 
	timezone VARCHAR, 
	id INTEGER NOT NULL, 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username)
);

CREATE UNIQUE INDEX ix_users_email ON users (email);


-- game_playtimes определение

CREATE TABLE game_playtimes (
	user_id INTEGER NOT NULL, 
	game_name VARCHAR NOT NULL, 
	playtime_hours FLOAT NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
	CONSTRAINT uq_user_game_playtime UNIQUE (user_id, game_name)
);


-- steam_profiles определение

CREATE TABLE steam_profiles (
	user_id INTEGER NOT NULL, 
	steam_id VARCHAR NOT NULL, 
	steam_name VARCHAR NOT NULL, 
	steam_avatar VARCHAR NOT NULL, 
	profile_url VARCHAR NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
	UNIQUE (steam_id), 
	UNIQUE (user_id)
);


-- user_contacts определение

CREATE TABLE user_contacts (
	user_id INTEGER NOT NULL, 
	telegram VARCHAR, 
	steam VARCHAR, 
	discord VARCHAR, 
	id INTEGER NOT NULL, 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
	UNIQUE (user_id)
);


-- user_follows определение

CREATE TABLE user_follows (
	follower_id INTEGER NOT NULL, 
	followed_id INTEGER NOT NULL, 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	PRIMARY KEY (follower_id, followed_id), 
	FOREIGN KEY(followed_id) REFERENCES users (id), 
	FOREIGN KEY(follower_id) REFERENCES users (id), 
	CONSTRAINT uq_user_follow UNIQUE (follower_id, followed_id)
);


-- user_genre_association определение

CREATE TABLE user_genre_association (
	user_id INTEGER NOT NULL, 
	genre_id INTEGER NOT NULL, 
	FOREIGN KEY(genre_id) REFERENCES genres (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);


-- user_infos определение

CREATE TABLE user_infos (
	user_id INTEGER NOT NULL, 
	purpose VARCHAR, 
	preferred_communication VARCHAR, 
	preferred_days VARCHAR, 
	preferred_time VARCHAR, 
	id INTEGER NOT NULL, 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
	UNIQUE (user_id)
);


-- user_ratings определение

CREATE TABLE user_ratings (
	id INTEGER NOT NULL, 
	rater_id INTEGER NOT NULL, 
	rated_id INTEGER NOT NULL, 
	rating VARCHAR(11) NOT NULL, 
	comment VARCHAR, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(rated_id) REFERENCES users (id) ON DELETE CASCADE, 
	FOREIGN KEY(rater_id) REFERENCES users (id) ON DELETE CASCADE, 
	CONSTRAINT uq_user_rating UNIQUE (rater_id, rated_id)
);


-- user_weights определение

CREATE TABLE user_weights (
	user_id INTEGER NOT NULL, 
	purpose_weight FLOAT NOT NULL, 
	self_assessment_lvl_weight FLOAT NOT NULL, 
	preferred_communication_weight FLOAT NOT NULL, 
	preferred_platforms_weight FLOAT NOT NULL, 
	playtime_weight FLOAT NOT NULL, 
	hours_per_week_weight FLOAT NOT NULL, 
	preferred_days_weight FLOAT NOT NULL, 
	preferred_genres_weight FLOAT NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
	UNIQUE (user_id)
);