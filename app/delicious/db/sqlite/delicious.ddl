CREATE TABLE "users" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                      "name" varchar(255) NOT NULL UNIQUE,
                      "created_at" datetime,
                      "updated_at" datetime);

CREATE TABLE "urls" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                     "url" varchar(255) NOT NULL UNIQUE,
                     "created_at" datetime,
                     "updated_at" datetime);

CREATE TABLE "tags" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                     "tag" varchar(255) NOT NULL UNIQUE,
                     "created_at" datetime,
                     "updated_at" datetime);


CREATE TABLE "extendeds" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                          "extended" text,
                          "user_id" integer,
                          "url_id" integer,
                          "created_at" datetime,
                          "updated_at" datetime,
                          FOREIGN KEY("url_id") REFERENCES urls("id"),
                          FOREIGN KEY("user_id") REFERENCES users("id")
                          );

CREATE TABLE "descriptions" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                             "description" text,
                             "url_id" integer,
                             "created_at" datetime,
                             "updated_at" datetime,
                             FOREIGN KEY("url_id") REFERENCES urls("id")
                            );

CREATE TABLE "url_dates" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                          "url_date" datetime,
                          "url_id" integer,
                          "user_id" integer,
                          "created_at" datetime,
                          "updated_at" datetime,
                          FOREIGN KEY("url_id") REFERENCES urls("id"),
                          FOREIGN KEY("user_id") REFERENCES users("id")
                          );

CREATE TABLE "user_url_tags" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                              "user_id" integer,
                              "url_id" integer,
                              "tag_id" integer,
                              "created_at" datetime,
                              "updated_at" datetime,
                              FOREIGN KEY("url_id") REFERENCES urls("id"),
                              FOREIGN KEY("user_id") REFERENCES users("id")
                              );

