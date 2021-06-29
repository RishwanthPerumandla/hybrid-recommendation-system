from flask import Flask, render_template, request, url_for, redirect, session, json, jsonify
from datetime import datetime
import pymongo
import json
import base64
from bson.objectid import ObjectId

# set app as a Flask instance
app = Flask(__name__)
# encryption relies on secret keys so they could be run
app.secret_key = "testing"
# connoct to your Mongo DB database
client = pymongo.MongoClient(
    "mongodb+srv://rishi:rishi@cluster0.mhdj6.mongodb.net/recom?retryWrites=true&w=majority")

# get the database name
db = client.get_database('recom')
# get the particular collection that contains the data
records = db.users
likes = db.likes
posts = db.posts

# assign URLs to have a particular route


@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    # if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        # password1 = request.form.get("password1")
        # password2 = request.form.get("password2")
        # if found in database showcase that it's found
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        # if password1 != password2:
        #     message = 'Passwords should match!'
        #     return render_template('index.html', message=message)
        else:
            # hash the password and encode it
            # hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            # assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, }
            # insert it in the record collection
            records.insert_one(user_input)

            # find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            new_user = user_data['name']
            id = user_data['_id']
            session["email"] = new_email
            var1 = ObjectId(id)
            session['_id'] = (str(var1))
            session["name"] = new_user
            # if registered redirect to logged in as the registered user
            return render_template('logged_in.html', email=new_email)
    return render_template('index.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        # password = request.form.get("password")

        # check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            id = email_found['_id']
            name = email_found['name']

            # passwordcheck = email_found['password']
            # encode the password and check if it matches
            # if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
            if email_found:
                session["email"] = email_val
                session["name"] = name
                var1 = ObjectId(id)
                session['_id'] = (str(var1))

                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        name = session["name"]
        id = session['_id']
        # content = posts.find({}).sort("timestamp", 1)
        # content = json.dumps(content)
        # data1 = json.loads(content)
        return render_template('logged_in.html', email=email,  name=name, id=id)
    else:
        return redirect(url_for("login"))


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        session.pop("name", None)
        session.pop("_id", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')


@app.route("/recommendations", methods=["POST", "GET"])
def recommendations():
    from CollaborativeFiltering import recommend

    if "email" in session:
        id = session["_id"]
        var1 = ObjectId(id)
        print(str(var1))
        data1 = recommend(str(var1))
        return render_template('feed.html', data1=json.loads(data1))
    else:
        return redirect(url_for("login"))


@app.route("/feed", methods=["POST", "GET"])
def newsfeed():
    from ContentBasedFiltering import recom
    import glob
    if "email" in session:
        id = session["_id"]
        # likings = likes.find({"user_id": id}, {"post_id": 1, "_id": 0}).sort(
        #     "timestamp", 1).limit(5)
        # get = db.messages.find({'name': request.POST['name']})
        # if likings is not None:
        #     result = list(likings)
        #     print(json.dumps(result))
        # liked = json.dumps(list(likings))
        # print(liked)

        # liked = json.loads(liked)
        data = []

        for post_id in likes.find({"user_id": id}, {"post_id": 1, "_id": 0}).sort(
                "timestamp", 1).distinct("post_id")[0:6]:
            # idvalue = post_id.get('post_id')
            print(post_id)
            content = posts.find_one(
                {"_id": post_id}, {"title": 1, "_id": 0})
            # print(content)
            data.append(content)

        data = json.dumps(data)
        data = json.loads(data)
        # print(data)
        data1 = []
        for title in data:
            if title is not None:
                if title.get('title') is not None:
                    var22 = str(title.get('title'))
                    # print(var22)
                    data2 = recom(str(var22))
                    # print(data2)
                    data1.append(json.loads(data2))

        data1 = json.dumps(data1)
        data1 = json.loads(data1)
        # print(data1)
        return render_template('feed1.html', data1=data1)
    else:
        return redirect(url_for("login"))


@ app.route("/like/<post_id>", methods=["GET"])
def like(post_id):
    if "email" in session:
        # id = session["_id"]
        if request.method == "GET":
            user_id = session["_id"]
            new_email = session["email"]
            timestamp = str(datetime.now())
            liked = {'user_id': user_id, 'post_id': post_id,
                     "timestamp": timestamp}
            # insert it in the record collection
            likes.insert_one(liked)
            return redirect(url_for("recommendations"))
    else:
        return redirect(url_for("login"))
    return redirect(url_for("recommendations"))


@ app.route("/like/contentbased/<post_id>", methods=["GET"])
def ContentBasedLike(post_id):
    if "email" in session:
        # id = session["_id"]
        if request.method == "GET":
            user_id = session["_id"]
            new_email = session["email"]
            timestamp = str(datetime.now())
            liked = {'user_id': user_id, 'post_id': post_id,
                     "timestamp": timestamp}
            # insert it in the record collection
            likes.insert_one(liked)
            return redirect(url_for("newsfeed"))
    else:
        return redirect(url_for("login"))
    return redirect(url_for("newsfeed"))


@ app.route("/upload", methods=["GET", "POST"])
def upload():
    if "email" in session:
        # id = session["_id"]
        if request.method == "POST":
            title = request.form.get("title")
            category = request.form.get("category")
            post_type = "skill"
            image = request.files['image']
            image_string = base64.b64encode(image.read()).decode('utf-8')
            image_string = "data:image/jpeg;base64," + image_string
            # print(image_string)
            post = {'title': title, 'category': category,
                    'post_type': post_type, 'image': image_string}
            # insert it in the posts collection
            posts.insert_one(post)
            return render_template('uploadsuccess.html')
        else:
            return render_template('upload.html')
    else:
        return redirect(url_for("login"))
    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True)
