import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

#The next id we can put a post at (also equal to number of posts due to 0-based indexing)
post_id_counter = 3

#The next id we can put a comment at (global variable)
comment_id_counter = 5

#Dictionary containing all posts on server
posts = {
    0: {
        "id": 0,
        "upvotes": 1,
        "title": "My cat is the cutest!",
        "link": "https://i.imgur.com/jseZqNK.jpg",
        "username": "alicia98",
    },
    1: {
        "id": 1,
        "upvotes": 3,
        "title": "Cat loaf",
        "link": "https://i.imgur.com/TJ46wX4.jpg",
        "username": "alicia98",
    
    },
    2: {
        "id": 2,
        "upvotes": 3,
        "title": "Post 3",
        "link": "https://i.imgur.com/TJ46wX4.jpg",
        "username": "monkey",
    
    }
}

comments = {
    0: [ # comments for post_id 0 (first post)
        {
            "id": 0, #comment-id
            "upvotes": 8,
            "text": "Wow, my first Reddit gold!",
            "username": "alicia98"
        },
        {
            "id": 1,
            "upvotes": 3,
            "text": "This is an interesting discussion!",
            "username": "user123"
        },
        {
            "id": 2,
            "upvotes": 12,
            "text": "I couldn't agree more!",
            "username": "bobsmith"
        }
    ],
    1: [ # comments for post_id 1 (second post)
        {
            "id": 3,
            "upvotes": 5,
            "text": "Awesome post!",
            "username": "user123"
        },
        {
            "id": 4,
            "upvotes": 7,
            "text": "Great insights, thanks for sharing!",
            "username": "redditlover"
        }
    ]
}


@app.route("/")
def hello_world():
    return "Hello world!"


# your routes here

#Gets all posts stored in posts datastore
#Note, methods not specified, so default is GET
@app.route("/api/posts/")
def get_all_posts():
    all_posts = {"posts": list(posts.values())} # Make dictionary mapping "posts" to all the posts
    return json.dumps(all_posts), 200 #Return json file of all_posts along with 200 Success status Code

#Stores new post passed in by user (containing a title, link, and username) in posts datastore
@app.route("/api/posts/", methods = ["POST"])
def create_post():
    global post_id_counter
    post_input = json.loads(request.data) #Takes in user-passed dictionary, and saves as json file

    #Grab all 3 values from user inputted dictionary
    title_val = post_input.get("title")
    link_val = post_input.get("link")
    user_val = post_input.get("username")

    if not title_val: #evalutes to None -- must throw 404 error
        return json.dumps({"error":"No Field"}), 400
    if not link_val: #evalutes to None -- must throw 404 error
        return json.dumps({"error":"No Field"}), 400
    if not user_val: #evalutes to None -- must throw 404 error
        return json.dumps({"error":"No Field"}), 400
    
    #initialize a new post to add to posts
    new_post = {
        "id": post_id_counter,
        "upvotes": 1, #default value
        "title": title_val,
        "link": link_val,
        "username": user_val,
    }
    posts[post_id_counter] = new_post #initialize next spot in dictionary with this post
    post_id_counter += 1 #there has been 1 more post added to the dict
    return json.dumps(new_post), 201 #Success status code 201 along with the json-ified new post

#Gets a specific post stored in posts datastore
#Note, methods not specified, so default is GET
@app.route("/api/posts/<int:id>/")
def get_spec_post(id):
    post_spec = posts.get(id)
    if not post_spec: #evalutes to None -- must throw 404 error
        return json.dumps({"error":"Post not found"}), 404
    return json.dumps(post_spec), 200

#Deletes the specific post identified by this url
@app.route("/api/posts/<int:id>/", methods = ["DELETE"])
def delete_post(id):
    post_del = posts.get(id) # post corresponding to that id
    if not post_del: #evalutes to None -- must throw 404 error
        return json.dumps({"error":"Post not found"}), 404
    del posts[id]
    return json.dumps(post_del), 200 #When finish deleting, return the deleted post as a json file, as well as 200 (Success) Status Code
    

#Server gets comments associated with a specific post (note passed in post-id) stored in posts datastore
#Note, methods not specified, so default is GET
@app.route("/api/posts/<int:id>/comments/")
def get_comm_post(id):
    if not posts.get(id): #no post associated with id
        return json.dumps({"error":"Post not found"}), 404
    if id in comments and comments[id]:  # if postid exists in comments dictionary, and if there are any attached comments. 
        return json.dumps({"comments": comments[id]}), 200
    else:
     return json.dumps({"comments": []}), 200  # Return an empty set if no comments exist

                          
#Posts a comment to a specific post stored in posts datastore
@app.route("/api/posts/<int:id>/comments/", methods = ["POST"])
def post_comm(id):
    global comment_id_counter
    if not posts.get(id): #no post associated with id
        return json.dumps({"error":"Post not found"}), 404
    
    comment_input = json.loads(request.data) #Takes in user-passed dictionary, and saves as json file

    #Grab all values from user inputted dictionary
    text_val = comment_input.get("text")
    user_val = comment_input.get("username")

    if not text_val: #evalutes to None -- must throw 404 error
        return json.dumps({"error":"No Field"}), 400
    if not user_val: #evalutes to None -- must throw 404 error
        return json.dumps({"error":"No Field"}), 400
    #Create new comment
    new_comment = {
        "id": comment_id_counter, #the global comment-counter
        "upvotes": 1,  # Assuming new comments start with 0 upvotes
        "text": text_val,
        "username": user_val
    }
    comment_id_counter += 1

    if id in comments and comments[id]:  # if postid exists in comments dictionary, and if there are any attached comments. 
        comments[id].append(new_comment)
    else: #make a new corresponding list and initialize with this comment
        comments[id] = [new_comment]
    return json.dumps(new_comment), 201


# #Posts a comment to a specific post stored in posts datastore
@app.route("/api/posts/<int:pid>/comments/<int:cid>", methods = ["POST"])
def edit_comm(pid, cid):
    if not posts.get(pid): #no post associated with id
        return json.dumps({"error":"Post not found"}), 404 

    comment_input = json.loads(request.data) #Takes in user-passed dictionary, and saves as json file

    #Grab all values from user inputted dictionary
    text_val = comment_input.get("text")

    if pid in comments and comments[pid]:  # comments[pid] is a list of comments associated with the post of id "pid"
        for comment in comments[pid]: # check each comment in list
            if comment["id"] == cid: #the comment has id field equal to comment-id passed in by user
                comment["text"] = text_val
                return comment
    return json.dumps({"error":"No valid/associated comments"}), 404
        
                

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
