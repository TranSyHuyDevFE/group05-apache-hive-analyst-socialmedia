

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

-- Create external table for TikTok comments data
CREATE EXTERNAL TABLE IF NOT EXISTS tiktok_comments (
  user_info STRING,
  content STRING,
  likes INT,
  `timestamp` STRING,
  video_url STRING
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
  author STRING,
  description STRING,
  hashtags STRING,
  music STRING,
  engagement STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\"",
  "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/opt/hive/data/warehouse/tiktok/video_info_details';
