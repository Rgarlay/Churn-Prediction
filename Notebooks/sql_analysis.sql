use churn_db

alter table churn
drop column signup_date

select * from churn

DELIMITER $$
CREATE PROCEDURE all_records()
BEGIN
    SELECT * FROM churn;
END$$
DELIMITER ;

SELECT column_name
FROM information_schema.columns
WHERE table_name = 'churn'
---------------------------------------------------------
## General Analysis

call all_records();

-- How many records are there
select count(*) from churn

-- > 125,000

--  What is the overall churn rate? --

select sum(case when churned = 1 then 1 else 0 end) as yes_churned,
sum(case when churned = 0 then 1 else 0 end) as no_churned, 
avg(churned) as ratio_yes_to_no 
from churn

-- 0.51 churn rate

-- How many unique customers are in the dataset?
select count(distinct customer_id)as unique_customer from churn
-- All are unique

-- Are there duplicate customer IDs?
SELECT *
FROM churn
WHERE
    customer_id IS NULL OR  age IS NULL OR  location IS NULL OR  subscription_type IS NULL OR  payment_plan IS NULL
    OR  num_subscription_pauses IS NULL OR  payment_method IS NULL OR  customer_service_inquiries IS NULL OR  signup_date IS NULL
    OR  weekly_hours IS NULL OR  average_session_length IS NULL OR  song_skip_rate IS NULL OR  weekly_songs_played IS NULL 
    OR  weekly_unique_songs IS NULL OR  num_favorite_artists IS NULL OR  num_platform_friends IS NULL OR  num_playlists_created IS NULL
    OR  num_shared_playlists IS NULL OR  notifications_clicked IS NULL OR churned IS NULL;
-- None

-- How does churn rate vary across different age groups?

with cte_1 as 
(SELECT
    CASE
        WHEN age BETWEEN 18 AND 24 THEN '18–24'
        WHEN age BETWEEN 25 AND 34 THEN '25–34'
        WHEN age BETWEEN 35 AND 44 THEN '35–44'
        WHEN age BETWEEN 45 AND 54 THEN '45–54'
        WHEN age BETWEEN 55 AND 64 THEN '55–64'
        WHEN age BETWEEN 65 AND 79 THEN '65–79'
        ELSE 'Unknown'
    END AS age_group, churned
FROM churn)
select 
	age_group, 
	avg(churned) as churn_to_not_ratio
from cte_1
group by age_group 
order by churn_to_not_ratio desc
-- > Higest: - 65-79 & 18-24 : - 0.62
-- > Lowest: - 45-54 & 35-44: - 0.40

-- Which locations have the highest churn rates?
select 
	location, 
    avg(churned) as churn_to_not_ratio 
from churn
group by location
order by churn_to_not_ratio 
desc
-- Which subscription types have the lowest churn rates?
select 
	subscription_type, 
    avg(churned) as churn_to_not_ratio 
from churn
group by subscription_type
order by churn_to_not_ratio 
desc
-- Free --> Student --> Family --> Premium (max to least churn late)

-- How does payment plan (monthly vs annual) impact churn?
select 
	payment_plan, 
    avg(churned) as churn_to_not_ratio 
from churn
group by payment_plan
order by churn_to_not_ratio 
desc
-- No impact on churn. Its about 51%.

-- Do customers with more subscription pauses churn more frequently?
select 
	num_subscription_pauses, 
    avg(churned) as churn_to_not_ratio 
from churn
group by num_subscription_pauses
order by churn_to_not_ratio 
desc

-- > Threshold is 2. Above 2 pauses, churn rate is over 64%, below it, its about 42%.

-- Does churn vary by payment method?
select 
	payment_method, 
    sum(churned)/count(churned) as churn_to_not_ratio 
from churn
group by payment_method
order by churn_to_not_ratio 
desc
-- > Most churn are from Apple pay. Least are from Credit card, but difference is only 2%.

-- Is lower content variety associated with higher churn?
-- People who listen to more or less singers or songs variety.
call all_records()

select max(num_favorite_artists),min(num_favorite_artists) from churn

WITH cte_1 AS (
    SELECT
        CASE
            WHEN num_favorite_artists BETWEEN 0 AND 10 THEN '0-10'
            WHEN num_favorite_artists BETWEEN 11 AND 20 THEN '11-20'
            WHEN num_favorite_artists BETWEEN 21 AND 30 THEN '21-30'
            WHEN num_favorite_artists BETWEEN 31 AND 40 THEN '31-40'
            ELSE '41-49'
        END AS artists_group,
        churned
    FROM churn
)
SELECT
    artists_group,
    COUNT(*) AS total_users,
    SUM(churned) AS churned_users,
    ROUND(AVG(churned), 3) AS churn_rate
FROM cte_1
GROUP BY artists_group
ORDER BY churn_rate DESC;
-- > It;s less than 0.1% change, no considerable change.

-- Do churned users spend fewer weekly hours on the platform?

call all_records()

SELECT
    churned,
    COUNT(*) AS users,
    Round(AVG(weekly_hours),2) AS avg_weekly_hours
FROM churn
GROUP BY churned;

-- > 9 hours difference in average weekly watch time.

-- Is a higher song skip rate associated with increased churn?

SELECT
    churned,
    COUNT(song_skip_rate) AS users,
    ROUND(AVG(song_skip_rate),2) AS avg_skip_rate
FROM churn
WHERE song_skip_rate IS NOT NULL
GROUP BY churned;

-- > 10% difference.

-- Do churned users play fewer songs per week?

SELECT
    churned,
    COUNT(weekly_songs_played) AS users,
    ROUND(AVG(weekly_songs_played),3) AS avg_weekly_songs
FROM churn
WHERE weekly_songs_played IS NOT NULL
GROUP BY churned;
-- > Almost no difference.

-- Do churned users listen to fewer unique songs?

SELECT
    churned,
    COUNT(weekly_unique_songs) AS users,
    ROUND(AVG(weekly_unique_songs), 2) AS avg_unique_songs
FROM churn
WHERE weekly_unique_songs IS NOT NULL
GROUP BY churned;

-- > Almost nodifference. 

-- Do churned users engage with fewer favorite artists?

SELECT
    churned,
    COUNT(num_favorite_artists) AS users,
    ROUND(AVG(num_favorite_artists), 2) AS avg_favorite_artists
FROM churn
WHERE num_favorite_artists IS NOT NULL
GROUP BY churned;
-- > Almost no difference.

-- Do users with platform friends churn less than those without?
call all_records()

select max(num_platform_friends),min(num_platform_friends) from churn

WITH cte_friends AS (
    SELECT
        CASE
            WHEN num_platform_friends BETWEEN 0 AND 20 THEN '0-20'
            WHEN num_platform_friends BETWEEN 21 AND 50 THEN '11-50'
            WHEN num_platform_friends BETWEEN 51 AND 100 THEN '51-100'
            ELSE '101-199'
        END AS friends_group,
        churned
    FROM churn
)

SELECT
    friends_group,
    COUNT(*) AS total_users,
    SUM(churned) AS churned_users,
    ROUND(AVG(churned), 3) AS churn_rate
FROM cte_friends
GROUP BY friends_group
ORDER BY churn_rate DESC;


-- > ~1% difference max.

-- Does creating more playlists reduce churn?

SELECT
    MIN(num_playlists_created) AS min_playlists_created,
    MAX(num_playlists_created) AS max_playlists_created
FROM churn
WHERE num_playlists_created IS NOT NULL;
-- range is (0,99)

SELECT
    CASE
        WHEN num_playlists_created BETWEEN 0 AND 24 THEN '0–24'
        WHEN num_playlists_created BETWEEN 25 AND 49 THEN '25–49'
        WHEN num_playlists_created BETWEEN 50 AND 74 THEN '50–74'
        WHEN num_playlists_created BETWEEN 75 AND 99 THEN '75–99'
        ELSE 'Unknown'
    END AS playlist_bin,
    COUNT(*) AS users,
    AVG(churned) * 100 AS churn_percent
FROM churn
WHERE num_playlists_created IS NOT NULL
GROUP BY playlist_bin
ORDER BY playlist_bin desc;
-- >   Almost same for all.

-- Are users who share playlists less likely to churn?

select max(num_shared_playlists),min(num_shared_playlists) from churn

-- Grouped based on share vs no shared.
SELECT
    CASE
        WHEN num_shared_playlists > 0 THEN 'Shares Playlists'
        ELSE 'Does Not Share'
    END AS share_status,
    COUNT(*) AS users,
    ROUND(AVG(churned), 3) AS churn_rate
FROM churn
GROUP BY share_status;
-- > About 1.5% difference, no significant. ALso, class class highly imbalanced.

-- Grouped by how many shared
WITH cte_shared_playlists AS (
    SELECT
        CASE
            WHEN num_shared_playlists BETWEEN 0 AND 5 THEN '0-5'
            WHEN num_shared_playlists BETWEEN 6 AND 15 THEN '6-15'
            WHEN num_shared_playlists BETWEEN 16 AND 30 THEN '16-30'
            ELSE '31-49'
        END AS shared_playlists_group,
        churned
    FROM churn
)

SELECT
    shared_playlists_group,
    COUNT(*) AS total_users,
    SUM(churned) AS churned_users,
    ROUND(AVG(churned), 3) AS churn_rate
FROM cte_shared_playlists
GROUP BY shared_playlists_group
ORDER BY churn_rate DESC;


-- Do churned users make more customer service inquiries?

SELECT
    customer_service_inquiries AS inquiry_level,
    COUNT(*) AS users,
    AVG(churned) * 100 AS churn_percent
FROM churn
WHERE customer_service_inquiries IN ('Low', 'Medium', 'High')
GROUP BY inquiry_level
ORDER BY churn_percent desc;

-- > Very interesting. Almost 23% difference each side.

-- Are churned users less likely to click notifications?

SELECT
    churned,
    COUNT(notifications_clicked) AS users,
    ROUND(AVG(notifications_clicked), 3) AS avg_notifications_clicked
FROM churn
WHERE notifications_clicked IS NOT NULL
GROUP BY churned;

-- > difference of 2. 

-- Is churn higher among new users compared to long-tenure users?


-- Does engagement drop significantly before churn occurs?
-- Which behaviors are most strongly associated with retention?
-- Which users should be prioritized for churn-prevention efforts?

-- Which customer segments have the highest churn risk?
WITH cte_1 AS (
    SELECT
        CASE
            WHEN num_favorite_artists BETWEEN 0 AND 10 THEN '0-10'
            WHEN num_favorite_artists BETWEEN 11 AND 20 THEN '11-20'
            WHEN num_favorite_artists BETWEEN 21 AND 30 THEN '21-30'
            WHEN num_favorite_artists BETWEEN 31 AND 40 THEN '31-40'
            ELSE '41-49'
        END AS artists_group,
        churned,
        weekly_hours,
        song_skip_rate,
        customer_service_inquiries
    FROM churn
)
SELECT
    artists_group,
    CASE
        WHEN weekly_hours < 2 THEN 'Low Engagement'
        WHEN weekly_hours BETWEEN 2 AND 5 THEN 'Medium Engagement'
        ELSE 'High Engagement'
    END AS engagement_level,
    CASE
        WHEN song_skip_rate < 0.2 THEN 'Low Skip'
        WHEN song_skip_rate < 0.5 THEN 'Medium Skip'
        ELSE 'High Skip'
    END AS skip_rate_level,
    customer_service_inquiries AS inquiry_level,
    COUNT(*) AS users,
    ROUND(AVG(churned), 3) AS churn_rate
FROM cte_1
GROUP BY artists_group, engagement_level, skip_rate_level, inquiry_level
ORDER BY churn_rate DESC;

-- A summary of which factors are most important in churning.





