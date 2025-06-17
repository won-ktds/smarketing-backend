INSERT INTO members (member_id, user_id, password, name, business_number, email, created_at, updated_at)
VALUES
  (DEFAULT, 'testuser1', '$2a$10$27tA6hwHt4N94WzZm/xqv.smgDi3c6cVp.Pu8gVyfqlEdwTPI8r7y', '김소상', '123-45-67890', 'test1@smarketing.com', NOW(), NOW()),
  (DEFAULT, 'testuser2', '$2a$10$27tA6hwHt4N94WzZm/xqv.smgDi3c6cVp.Pu8gVyfqlEdwTPI8r7y', '이점주', '234-56-78901', 'test2@smarketing.com', NOW(), NOW()),
  (DEFAULT, 'testuser3', '$2a$10$27tA6hwHt4N94WzZm/xqv.smgDi3c6cVp.Pu8gVyfqlEdwTPI8r7y', '박카페', '345-67-89012', 'test3@smarketing.com', NOW(), NOW()),
  (DEFAULT, 'cafeowner1', '$2a$10$27tA6hwHt4N94WzZm/xqv.smgDi3c6cVp.Pu8gVyfqlEdwTPI8r7y', '최카페', '456-78-90123', 'cafe@smarketing.com', NOW(), NOW()),
  (DEFAULT, 'restaurant1', '$2a$10$27tA6hwHt4N94WzZm/xqv.smgDi3c6cVp.Pu8gVyfqlEdwTPI8r7y', '정식당', '567-89-01234', 'restaurant@smarketing.com', NOW(), NOW())
ON CONFLICT (user_id) DO NOTHING;

-- 이메일 중복 방지를 위한 추가 체크
INSERT INTO members (member_id, user_id, password, name, business_number, email, created_at, updated_at)
VALUES
  (DEFAULT, 'bakery1', '$2a$10$27tA6hwHt4N94WzZm/xqv.smgDi3c6cVp.Pu8gVyfqlEdwTPI8r7y', '김베이커리', '678-90-12345', 'bakery@smarketing.com', NOW(), NOW()),
  (DEFAULT, 'chicken1', '$2a$10$27tA6hwHt4N94WzZm/xqv.smgDi3c6cVp.Pu8gVyfqlEdwTPI8r7y', '한치킨', '789-01-23456', 'chicken@smarketing.com', NOW(), NOW()),
  (DEFAULT, 'pizza1', '$2a$10$27tA6hwHt4N94WzZm/xqv.smgDi3c6cVp.Pu8gVyfqlEdwTPI8r7y', '이피자', '890-12-34567', 'pizza@smarketing.com', NOW(), NOW()),
  (DEFAULT, 'dessert1', '$2a$10$27tA6hwHt4N94WzZm/xqv.smgDi3c6cVp.Pu8gVyfqlEdwTPI8r7y', '달디저트', '901-23-45678', 'dessert@smarketing.com', NOW(), NOW()),
  (DEFAULT, 'beauty1', '$2a$10$27tA6hwHt4N94WzZm/xqv.smgDi3c6cVp.Pu8gVyfqlEdwTPI8r7y', '미뷰티샵', '012-34-56789', 'beauty@smarketing.com', NOW(), NOW())
ON CONFLICT (user_id) DO NOTHING;
