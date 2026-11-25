-- FitPlan database schema for PostgreSQL / Supabase.
-- Generated from app/models.py. The app also creates these tables itself on first start,
-- so running this file by hand is optional.

CREATE TYPE sex AS ENUM ('male', 'female');
CREATE TYPE activitylevel AS ENUM ('sedentary', 'light', 'moderate', 'active', 'very_active');
CREATE TYPE goal AS ENUM ('cut', 'maintain', 'bulk');
CREATE TYPE mealtype AS ENUM ('breakfast', 'lunch', 'dinner', 'snack');

CREATE TABLE "user" (
	id SERIAL NOT NULL, 
	email VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	hashed_password VARCHAR NOT NULL, 
	username VARCHAR, 
	is_private BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_user_email ON "user" (email);
CREATE UNIQUE INDEX ix_user_username ON "user" (username);

CREATE TABLE customexercise (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	name_ar VARCHAR NOT NULL, 
	name_en VARCHAR NOT NULL, 
	muscle VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "user" (id)
);
CREATE INDEX ix_customexercise_user_id ON customexercise (user_id);

CREATE TABLE follow (
	follower_id INTEGER NOT NULL, 
	followee_id INTEGER NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (follower_id, followee_id), 
	FOREIGN KEY(follower_id) REFERENCES "user" (id), 
	FOREIGN KEY(followee_id) REFERENCES "user" (id)
);
CREATE INDEX ix_follow_followee_id ON follow (followee_id);

CREATE TABLE food (
	id SERIAL NOT NULL, 
	name_ar VARCHAR NOT NULL, 
	name_en VARCHAR NOT NULL, 
	calories FLOAT NOT NULL, 
	protein FLOAT NOT NULL, 
	carbs FLOAT NOT NULL, 
	fat FLOAT NOT NULL, 
	serving_g FLOAT NOT NULL, 
	serving_ar VARCHAR NOT NULL, 
	serving_en VARCHAR NOT NULL, 
	owner_id INTEGER, 
	kind VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES "user" (id)
);
CREATE INDEX ix_food_owner_id ON food (owner_id);

CREATE TABLE profile (
	user_id INTEGER NOT NULL, 
	sex sex NOT NULL, 
	age INTEGER NOT NULL, 
	height_cm FLOAT NOT NULL, 
	weight_kg FLOAT NOT NULL, 
	activity_level activitylevel NOT NULL, 
	goal goal NOT NULL, 
	tdee_override INTEGER, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (user_id), 
	FOREIGN KEY(user_id) REFERENCES "user" (id)
);

CREATE TABLE savedmeal (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "user" (id)
);
CREATE INDEX ix_savedmeal_user_id ON savedmeal (user_id);

CREATE TABLE waterlog (
	user_id INTEGER NOT NULL, 
	day DATE NOT NULL, 
	ml INTEGER NOT NULL, 
	PRIMARY KEY (user_id, day), 
	FOREIGN KEY(user_id) REFERENCES "user" (id)
);

CREATE TABLE weightlog (
	user_id INTEGER NOT NULL, 
	day DATE NOT NULL, 
	weight_kg FLOAT NOT NULL, 
	PRIMARY KEY (user_id, day), 
	FOREIGN KEY(user_id) REFERENCES "user" (id)
);

CREATE TABLE workoutplan (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	split VARCHAR NOT NULL, 
	is_active BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "user" (id)
);
CREATE INDEX ix_workoutplan_user_id ON workoutplan (user_id);

CREATE TABLE mealentry (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	food_id INTEGER NOT NULL, 
	day DATE NOT NULL, 
	meal_type mealtype NOT NULL, 
	grams FLOAT NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "user" (id), 
	FOREIGN KEY(food_id) REFERENCES food (id)
);
CREATE INDEX ix_mealentry_day ON mealentry (day);
CREATE INDEX ix_mealentry_food_id ON mealentry (food_id);
CREATE INDEX ix_mealentry_user_id ON mealentry (user_id);

CREATE TABLE planday (
	id SERIAL NOT NULL, 
	plan_id INTEGER NOT NULL, 
	weekday INTEGER NOT NULL, 
	day_type VARCHAR NOT NULL, 
	title VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(plan_id) REFERENCES workoutplan (id) ON DELETE CASCADE
);
CREATE INDEX ix_planday_plan_id ON planday (plan_id);

CREATE TABLE recipe (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	food_id INTEGER NOT NULL, 
	servings INTEGER NOT NULL, 
	total_weight_g FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "user" (id), 
	FOREIGN KEY(food_id) REFERENCES food (id)
);
CREATE INDEX ix_recipe_food_id ON recipe (food_id);
CREATE INDEX ix_recipe_user_id ON recipe (user_id);

CREATE TABLE savedmealitem (
	id SERIAL NOT NULL, 
	saved_meal_id INTEGER NOT NULL, 
	food_id INTEGER NOT NULL, 
	grams FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(saved_meal_id) REFERENCES savedmeal (id), 
	FOREIGN KEY(food_id) REFERENCES food (id)
);
CREATE INDEX ix_savedmealitem_food_id ON savedmealitem (food_id);
CREATE INDEX ix_savedmealitem_saved_meal_id ON savedmealitem (saved_meal_id);

CREATE TABLE planexercise (
	id SERIAL NOT NULL, 
	plan_day_id INTEGER NOT NULL, 
	exercise_key VARCHAR NOT NULL, 
	sets INTEGER NOT NULL, 
	reps VARCHAR NOT NULL, 
	position INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(plan_day_id) REFERENCES planday (id) ON DELETE CASCADE
);
CREATE INDEX ix_planexercise_plan_day_id ON planexercise (plan_day_id);

CREATE TABLE recipeingredient (
	id SERIAL NOT NULL, 
	recipe_id INTEGER NOT NULL, 
	food_id INTEGER NOT NULL, 
	grams FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(recipe_id) REFERENCES recipe (id), 
	FOREIGN KEY(food_id) REFERENCES food (id)
);
CREATE INDEX ix_recipeingredient_food_id ON recipeingredient (food_id);
CREATE INDEX ix_recipeingredient_recipe_id ON recipeingredient (recipe_id);

CREATE TABLE workoutlog (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	plan_day_id INTEGER, 
	day DATE NOT NULL, 
	notes VARCHAR, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "user" (id), 
	FOREIGN KEY(plan_day_id) REFERENCES planday (id)
);
CREATE INDEX ix_workoutlog_day ON workoutlog (day);
CREATE INDEX ix_workoutlog_plan_day_id ON workoutlog (plan_day_id);
CREATE INDEX ix_workoutlog_user_id ON workoutlog (user_id);

CREATE TABLE setlog (
	id SERIAL NOT NULL, 
	workout_log_id INTEGER NOT NULL, 
	exercise_key VARCHAR NOT NULL, 
	set_number INTEGER NOT NULL, 
	weight_kg FLOAT NOT NULL, 
	reps INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(workout_log_id) REFERENCES workoutlog (id) ON DELETE CASCADE
);
CREATE INDEX ix_setlog_exercise_key ON setlog (exercise_key);
CREATE INDEX ix_setlog_workout_log_id ON setlog (workout_log_id);

CREATE TABLE workoutlike (
	user_id INTEGER NOT NULL, 
	workout_log_id INTEGER NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (user_id, workout_log_id), 
	FOREIGN KEY(user_id) REFERENCES "user" (id), 
	FOREIGN KEY(workout_log_id) REFERENCES workoutlog (id)
);
CREATE INDEX ix_workoutlike_workout_log_id ON workoutlike (workout_log_id);

-- Supabase: the app connects as the table owner. Block the public API roles completely
-- (these tables hold password hashes): RLS on with no policies, and no grants.
ALTER TABLE "user" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "user" FROM anon, authenticated;
ALTER TABLE "customexercise" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "customexercise" FROM anon, authenticated;
ALTER TABLE "follow" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "follow" FROM anon, authenticated;
ALTER TABLE "food" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "food" FROM anon, authenticated;
ALTER TABLE "profile" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "profile" FROM anon, authenticated;
ALTER TABLE "savedmeal" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "savedmeal" FROM anon, authenticated;
ALTER TABLE "waterlog" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "waterlog" FROM anon, authenticated;
ALTER TABLE "weightlog" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "weightlog" FROM anon, authenticated;
ALTER TABLE "workoutplan" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "workoutplan" FROM anon, authenticated;
ALTER TABLE "mealentry" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "mealentry" FROM anon, authenticated;
ALTER TABLE "planday" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "planday" FROM anon, authenticated;
ALTER TABLE "recipe" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "recipe" FROM anon, authenticated;
ALTER TABLE "savedmealitem" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "savedmealitem" FROM anon, authenticated;
ALTER TABLE "planexercise" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "planexercise" FROM anon, authenticated;
ALTER TABLE "recipeingredient" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "recipeingredient" FROM anon, authenticated;
ALTER TABLE "workoutlog" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "workoutlog" FROM anon, authenticated;
ALTER TABLE "setlog" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "setlog" FROM anon, authenticated;
ALTER TABLE "workoutlike" ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE "workoutlike" FROM anon, authenticated;
