  
CREATE TABLE actress_info ( 
--   id INT(20) NOT NULL AUTO_INCREMENT ,
 actress_id VARCHAR(40),
 actress VARCHAR(300),
 actress_page VARCHAR(4000),
 total_vids INT,
 PRIMARY KEY (actress_id));
 

CREATE TABLE video_info (
--  actress VARCHAR(300),
--  actress_page VARCHAR(4000),
 video_id VARCHAR(40),
 title VARCHAR(4000),
 video_link VARCHAR(4000),
 views INT,
 tags VARCHAR(4000),
 date DATE,
 actress_id VARCHAR(40),
 PRIMARY KEY (video_id, actress_id),
 FOREIGN KEY (actress_id) REFERENCES actress_info(actress_id));
 
 
-- INSERT INTO actress_info (actress_id, actress, actress_page, total_vids)
-- VALUES (MD5('https://jav.guru/actress/meguri/'),'meguri','https://jav.guru/actress/meguri/',200);
 
-- SELECT * FROM actress_info;
 
-- INSERT INTO actress_info (actress_id, actress, actress_page, total_vids)
-- VALUES (MD5('https://jav.guru/actress/meguri/'),'meguri','https://jav.guru/actress/meguri/',220)
-- ON DUPLICATE KEY UPDATE total_vids = 220;
 
-- SELECT * FROM actress_info;

