**_Link to GitHub_**: https://github.com/IRepeva/ugc_sprint_2

# UGC project 

## Introduction
The project contains UGC service and a databases performance analysis tool.

For code quality check CI with MyPy and wemake_python_styleguide linters was set up.
Telegram notifications for push and pull requests were added for easy deployment tracking.

## Database research

### Description
**db_research** is a tool for database comparison and performance analysis. 

In current project Clickhouse and Vertica databases were compared and 
MongoDB performance was estimated, but the same approach can be used for 
any other databases

### Get started

 - To run the service and configure MongoDB - `make run_and_config_db_research`.
 - To run service without mongodb configuration - `make run_db_research`

To repeat researches from this project:
1. Compare Clickhouse and Vertica - run `db_research/clickhouse_vs_vertica.py` file
2. Analyze MongoDB performance - run `db_research/mongodb/run.py` file

## MongoDB research results
### Input:
- Size of each table (likes, reviews, bookmarks): 50000
- Time required: 200 ms

### Results
#### Load time:
 - Likes - 69.19
 - Reviews - 58.89
 - Bookmarks - 65.56
 - ReviewLikes - 64.85

#### Read operations on existing data

| Request                                           | Average time (10 iterations), ms |
|---------------------------------------------------|----------------------------------|
| get_user_likes                                    | 2.6                              |
| get_movie_likes                                   | 2.8                              |
| get_user_bookmarks                                | 2.2                              |
| get_average_movie_rating                          | 7.7                              |
| get_review_with_sort                              | 32.7                             |

#### Read operations on incoming data

| Request                  | Average time (10 iterations), ms |
|--------------------------|----------------------------------|
| get_user_likes           | 18.1                             |
| get_movie_likes          | 1.5                              |
| get_average_movie_rating | 1.8                              |


### Conclusion
MongoDB satisfies performance requirements and can be used as a storage for 
likes, reviews and bookmarks data 

## UGC service

### Description
API allows to work with likes, reviews and bookmarks information. 
MongoDB is used as data storage.

**_Base service capabilities_**:
 - Add, edit or delete movie rating
 - Add, edit, delete or like/dislike film review
 - Add or delete movie to bookmarks
 - Get user's liked movies
 - Get film's detailed information:
   - number of likes
   - number of dislikes
   - average film rating based on all users' ratings


### Get started
Create file **.env** based on **.env.example** inside ugc folder

 - To run service and configure mongodb - `make run_and_config_ugc`
 - To run service only - `make run_and_config_ugc`
 - To configure mongodb - `make run_and_config_ugc`
 - To fill db with test data - `make fill_mongo_test_data`
 - To authorize and try API - generate token with `user_id` field 
and secret from **.env** file
      
      example:
      ```
      jwt.encode({"user_id": "115"}, "test_Pups_secret", algorithm="HS256")
      ```

More detailed information about service's endpoints is available 
[here](http://0.0.0.0:8000/api/openapi) after project start (`make run_and_config_ugc`)
