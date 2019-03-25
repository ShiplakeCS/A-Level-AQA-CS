-- Get posts for a particular User based on their suname and publically visible (useful for searching)
-- select Post.* from Post, User where Post.author_id = User.id and (user.surname like '%Dim%' or user.first_name like '%ad%') and post.public = 1;

-- Search for users based on username, first name or surname; return details required to display search results
-- select User.id, User.username, User.first_name, User.surname,  User.bio, User.profile_pic_id, User.dob from User where User.username like '%a%' or User.first_name like '%search%' or User.surname like '%searchi%';

-- Get number of likes for a Post based on the Post's id
select post_id, count(post_id) as 'likes' from PostLike where PostLike.post_id = 2

-- Continue writing SQL queries to execute required functionality for other success criteria of FakeBook, using the test data where necessary.