#
#
# test of the new Model and Basemodel for MongoDB
#

from mongo_model_post_test import Post


p = Post.init("posts")

print dir(p)
p.title = "test"
print p.title