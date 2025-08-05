-- Remove TikTok views first
DROP VIEW IF EXISTS v_top_hashtags;
DROP VIEW IF EXISTS v_trending_music;
DROP VIEW IF EXISTS v_trending_videos;
DROP VIEW IF EXISTS v_top_category_trending;


-- Remove TikTok tables 
DROP TABLE IF EXISTS tiktok_comments;
DROP TABLE IF EXISTS tiktok_related_videos;
DROP TABLE IF EXISTS tiktok_video_info_details;
DROP TABLE IF EXISTS tiktok_user_info_details;
DROP TABLE IF EXISTS tiktok_video_info;
DROP TABLE IF EXISTS tiktok_category;

