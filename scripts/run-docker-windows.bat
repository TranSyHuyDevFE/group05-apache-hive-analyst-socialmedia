@echo off
setlocal enabledelayedexpansion

:: Configuration
set "TARGET_DIR_DATA=volumes\warehouse\tiktok"
set "TARGET_DIR_SCRIPT=volumes\warehouse"
set "SRC_DIR=cleaned_data"

:: Colors for output
set "RED=[31m"
set "GREEN=[32m"
set "YELLOW=[33m"
set "NC=[0m"

:: Function to print error messages
:error_exit
    echo %RED%[ERROR] %~1%NC%
    exit /b 1

:: Function to print info messages
:info
    echo %GREEN%[INFO] %~1%NC%
    exit /b 0

:: Check if docker is running
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    call :error_exit "Docker is not running. Please start Docker and try again."
)

:: Check if hiveserver2 container is running
docker ps | findstr /i "hiveserver2" >nul
if %ERRORLEVEL% neq 0 (
    call :error_exit "HiveServer2 container is not running. Please start the container and try again."
)

:: Check if source directory exists
if not exist "%SRC_DIR%" (
    call :error_exit "Source directory '%SRC_DIR%' does not exist. Please check the path and try again."
)

:: Step 1: Create folders in warehouse for each table
call :info "Creating directory structure in warehouse..."

:: Table names and their corresponding files
set "tbl_names=category comments related_videos video video_info_details user_info_details"
set "tbl_files=category.csv comments.csv related_videos.csv video_info.csv video_info_details.csv user_info_details.csv"

:: Create directories for each table
for %%t in (%tbl_names%) do (
    if not exist "%TARGET_DIR_DATA%\%%~t" (
        mkdir "%TARGET_DIR_DATA%\%%~t"
        if %ERRORLEVEL% neq 0 (
            call :error_exit "Failed to create directory: %TARGET_DIR_DATA%\%%~t"
        )
    )
)

call :info "Directory structure created successfully"

:: Step 2: Copy each data file to its folder
call :info "Copying data files to warehouse..."

for /d %%d in ("%SRC_DIR%\*") do (
    set "dir_name=%%~nxd"
    if exist "%TARGET_DIR_DATA%\!dir_name!" (
        xcopy /E /Y "%%~d" "%TARGET_DIR_DATA%\!dir_name!\" >nul
        if !ERRORLEVEL! gtr 0 (
            echo %YELLOW%[WARNING] Failed to copy data for table: !dir_name!%NC%
        )
    ) else (
        echo %YELLOW%[WARNING] No target directory found for: !dir_name!%NC%
    )
)

call :info "Data files copied successfully"

:: Step 3: Copy scripts folder to warehouse
call :info "Updating scripts in warehouse..."

if not exist "scripts" (
    call :error_expt "Scripts directory not found. Please run from the project root directory."
)

if exist "%TARGET_DIR_SCRIPT%\scripts" (
    rmdir /S /Q "%TARGET_DIR_SCRIPT%\scripts"
    if %ERRORLEVEL% neq 0 (
        call :error_exit "Failed to remove old scripts"
    )
)

xcopy /E /I /Y "scripts" "%TARGET_DIR_SCRIPT%\scripts" >nul
if %ERRORLEVEL% gtr 0 (
    call :error_exit "Failed to copy scripts to warehouse"
)

call :info "Scripts updated successfully"

:: Step 4: Execute Hive scripts
call :info "Executing Hive scripts..."

:: Check if script files exist in container
docker exec hiveserver2 test -f "/opt/hive/data/warehouse/scripts/remove-db-structure.hql"
if %ERRORLEVEL% neq 0 (
    call :error_exit "Hive script remove-db-structure.hql not found in container"
)

:: Remove existing database structure
call :info "Removing existing database structure..."
docker exec -i hiveserver2 beeline -u jdbc:hive2://localhost:10000 -f /opt/hive/data/warehouse/scripts/remove-db-structure.hql
if %ERRORLEVEL% neq 0 (
    echo %YELLOW%[WARNING] Failed to remove database structure. Continuing anyway...%NC%
)

:: Create tables
call :info "Creating tables..."
docker exec -i hiveserver2 beeline -u jdbc:hive2://localhost:10000 -f /opt/hive/data/warehouse/scripts/create-tables.hql
if %ERRORLEVEL% neq 0 (
    call :error_exit "Failed to create tables"
)

:: Create views
call :info "Creating views..."
docker exec -i hiveserver2 beeline -u jdbc:hive2://localhost:10000 -f /opt/hive/data/warehouse/scripts/create-views.hql
if %ERRORLEVEL% neq 0 (
    call :error_exit "Failed to create views"
)

call :info "Hive scripts executed successfully"

:: Step 5: Test sentiment analysis setup
call :info "Testing sentiment analysis setup..."

call :info "Counting comments with sentiment analysis..."
docker exec -i hiveserver2 beeline --silent=true --outputformat=tsv2 -u jdbc:hive2://localhost:10000 -e "
    SELECT 'Comments with sentiment analysis:' as description, 
           COUNT(*) as total_comments 
    FROM tiktok_comments 
    WHERE sentiment IS NOT NULL;" 2>nul | findstr /v /i /c:"rows selected"

call :info "Sentiment summary dashboard preview:"
docker exec -i hiveserver2 beeline --silent=true --outputformat=tsv2 -u jdbc:hive2://localhost:10000 -e "
    SELECT * FROM v_sentiment_summary_dashboard;" 2>nul | head -n 6

:: Print completion message
echo.
echo %GREEN%All steps completed successfully!%NC%
echo.
echo %YELLOW%=== Dashboard Views Available ===%NC%
echo - v_top10_trending_videos: Top 10 trending videos by engagement
echo - v_top10_videos_sentiment_analysis: Detailed sentiment analysis per video
echo - v_sentiment_summary_dashboard: Overall sentiment summary
echo - v_video_sentiment_details: Video ranking with sentiment breakdown
echo - v_sentiment_by_time: Sentiment trends over time
echo.
echo %GREEN%Sentiment analysis dashboard is ready!%NC%

endlocal
exit /b 0
