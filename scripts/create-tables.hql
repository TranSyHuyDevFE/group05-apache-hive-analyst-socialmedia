-- Create external table for TikTok category data
CREATE EXTERNAL TABLE IF NOT EXISTS tiktok_category (
  index INT,
  display STRING,
  slug STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\"",
  "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/opt/hive/data/warehouse/tiktok/category';

-- Create external table for TikTok comments data with sentiment analysis
CREATE EXTERNAL TABLE IF NOT EXISTS tiktok_comments (
  username STRING,
  content STRING,
  likes INT,
  video_url STRING,
  sentiment STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\"",
  "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/opt/hive/data/warehouse/tiktok/comments';

-- Create external table for TikTok related videos data
CREATE EXTERNAL TABLE IF NOT EXISTS tiktok_related_videos (
  video_link STRING,
  parrent_video_url STRING,
  title STRING,
  author STRING,
  likes STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\"",
  "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/opt/hive/data/warehouse/tiktok/related_videos';

-- Create external table for TikTok video info data
CREATE EXTERNAL TABLE IF NOT EXISTS tiktok_video_info (
  url STRING,
  thumbnail STRING,
  description STRING,
  likes STRING,
  category STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\"",
  "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/opt/hive/data/warehouse/tiktok/video';

-- Create external table for TikTok video info details data
CREATE EXTERNAL TABLE IF NOT EXISTS tiktok_video_info_details (
  time_published STRING,
  description STRING,
  hashtags STRING,
  video_url STRING,
  username STRING,
  nickname STRING,
  music_title STRING,
  music_link STRING,
  likes STRING,
  comments STRING,
  shares STRING,
  crawl_date STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\"",
  "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/opt/hive/data/warehouse/tiktok/video_info_details';

-- Create external table for TikTok user info details data
CREATE EXTERNAL TABLE IF NOT EXISTS tiktok_user_info_details (
  user_title STRING,
  user_subtitle STRING,
  avatar_url STRING,
  bio STRING,
  username STRING,
  `following` STRING,
  `followers` STRING,
  `likes` STRING,
  first_link_url STRING,
  first_link_text STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\"",
  "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/opt/hive/data/warehouse/tiktok/user_info_details';

