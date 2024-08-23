import requests
from bs4 import BeautifulSoup
import os
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for, abort
from flask_login import  current_user, login_required
from werkzeug.utils import secure_filename
from website.models import UserProfile, tradepost
from . import db




views = Blueprint('views', __name__)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@views.route('/', methods=['GET', 'POST'])

def home(): 
    name="Ayanda!"
    return render_template("home.html", Hello='Welcome to Lecture.AI ' + name )

@views.route('/nexus')
def nexus():
    return render_template("nexus.html")

@views.route('/reuse')
def reuse():
    return render_template("reuse.html")

@views.route('/reduce')
def reduce():
    return render_template("reduce.html")

@views.route('/recycle')
def recycle():
    return render_template("recycle.html")



@views.route('/r-trade')
def trade():
    trades = tradepost.query.all()  # Fetch all trades
    for trade in trades:
        print(f"Trade image: {trade.image}") 
    return render_template('r-trade.html', trades=trades)

@views.route('/create-trade', methods=['POST'])
@login_required
def create_trade():
    if request.method == 'POST':
        if not current_user.is_authenticated:  # Ensure the user is authenticated
            flash('You need to be logged in to create a trade!', category='error')
            return redirect(url_for('views.login'))
        
        image = request.files.get('image')
        description = request.form.get('caption')
      
        price = request.form.get('price')
        category = request.form.get('category')
 

        title = request.form.get('title')

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            new_trade = tradepost(
                image=filename,
                description=description,
                title=title, 
                price=float(price) if type == 'Sell' else None,
                category=category,
                
                user_id=current_user.id  # Only access id if current_user is authenticated
            )

            db.session.add(new_trade)
            db.session.commit()
            flash('Trade post created successfully!', category='success')
            return redirect(url_for('views.trade'))

    return redirect(url_for('views.trade'))



@views.route('/blog')
def blog():
    urls = [
        "https://www.bbc.com/future/article/20230317-how-recycling-can-help-the-climate-and-other-facts",
        "https://www.who.int/news-room/fact-sheets/detail/electronic-waste-%28e-waste%29",
        "https://freelancian.co.za/what-can-i-recycle-to-make-money-in-south-africa/"  
    ]

    articles = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  

         
            soup = BeautifulSoup(response.text, 'html.parser')

            article_content = soup.find('article')  

            articles.append({
                'title': soup.title.string if soup.title else 'No Title',
                'html': str(article_content)
            })

        except requests.RequestException as e:
            print(f"Error fetching article from {url}: {e}")
            articles.append({
                'title': 'Error Loading Article',
                'html': "<p>Error loading article</p>"
            })

    return render_template('blog.html', articles=articles)


@views.route('/videos')
def videos():
    video_list = [
        {'title': 'Artificial Intelligence Integrated in Recycling!', 'url': 'https://www.youtube.com/embed/On5WUCUNmfc'}, 
        {'title': 'Make Money Through Waste!', 'url': 'https://www.youtube.com/embed/cQqhKzcHnAg'},  
        {'title': 'AI Making Our Lives Easier!', 'url': 'https://www.youtube.com/embed/KPVSTjfcdng'}
    ]

    return render_template("videos.html", videos=video_list)



@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/certificate')
def certificate():
    url = "https://environmentgo.com/free-online-recycling-courses/#:~:text=Free%20Online%20Recycling%20Courses%201%201.%20Advanced%20Diploma,Electronics%20for%20Recycling%20in%20a%20Circular%20Economy%20"

    try:
        response = requests.get(url)
        response.raise_for_status()  

        
        soup = BeautifulSoup(response.text, 'html.parser')

      
        content = soup.find('main')  

     
        content_html = str(content)

    except requests.RequestException as e:
        print(f"Error fetching certificate data: {e}")
        content_html = "<p>Error loading content</p>"

    return render_template('certificate.html', content_html=content_html)


@views.route('/help')
def help():
    return render_template("help.html")

@views.route('/privacy')
def privacy():
    return render_template("privacy.html")

@views.route('/terms')
def terms():
    return render_template("terms.html")



@views.route('/login')
def login():
    return render_template("login.html")



@views.route('/sign-up')
def sign_up():
    return render_template("sign-up.html")

@views.route('/create-profile', methods=['GET', 'POST'])
@login_required
def createProfile():
    
    
    if request.method == 'POST':
        firstname = request.form.get('firstName')
        lastname = request.form.get('lastName')
        bio = request.form.get('bio')
        location = request.form.get('location')
        workplace = request.form.get('workplace')
        education = request.form.get('education')
        highlights = request.form.get('highlights')
        linkedin = request.form.get('linkedin')
        facebook = request.form.get('facebook')
        instagram = request.form.get('instagram')
        media_type = request.form.get('mediaType')
        category_prefix = request.form.get('categoryPrefix')


        cover_photo = request.files.get('coverPhoto')
        media_uploads = request.files.getlist('mediaUpload')
        
        cover_photo_filename = None
        media_upload_filenames = []
        
        if cover_photo and allowed_file(cover_photo.filename):
            cover_photo_filename = secure_filename(cover_photo.filename)
            cover_photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], cover_photo_filename))
        
        for media_upload in media_uploads:
         if media_upload and allowed_file(media_upload.filename):
            filename = secure_filename(media_upload.filename)
            media_upload.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            media_upload_filenames.append(filename)
            
        
        profile = UserProfile(
            firstname=firstname,
            lastname=lastname,
            bio=bio,
            location=location,
            workplace=workplace,
            education=education,
            highlights=highlights,
            linkedin=linkedin,
            facebook=facebook,
            instagram=instagram,
            cover_photo=cover_photo_filename,
            media_upload=','.join(media_upload_filenames),
            media_type='image' if media_uploads and media_uploads[0].content_type.startswith('image') else 'video', 
            user_id=current_user.id
        )

        db.session.add(profile)
        db.session.commit()
        flash('Profile created successfully!', category='success')
        return redirect(url_for('views.cans'))

    return render_template('create-profile.html')


@views.route('/cans')
def cans():
    profiles = UserProfile.query.all()
    return render_template("cans.html", profiles=profiles)

@views.route('/update-profile/<int:profile_id>', methods=['GET', 'POST'])
@login_required
def update(profile_id):
    profile = UserProfile.query.get_or_404(profile_id)

    if request.method == 'POST':
        profile.firstname = request.form.get('firstName')
        profile.lastname = request.form.get('lastName')
        profile.bio = request.form.get('bio')
        profile.location = request.form.get('location')
        profile.workplace = request.form.get('workplace')
        profile.education = request.form.get('education')
        profile.highlights = request.form.get('highlights')
        profile.linkedin = request.form.get('linkedin')
        profile.facebook = request.form.get('facebook')
        profile.instagram = request.form.get('instagram')

        # Handle cover photo upload
        cover_photo = request.files.get('coverPhoto')
        if cover_photo and allowed_file(cover_photo.filename):
            cover_photo_filename = secure_filename(cover_photo.filename)
            cover_photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], cover_photo_filename))
            profile.cover_photo = cover_photo_filename

        # Handle media uploads
        media_uploads = request.files.getlist('mediaUpload')
        media_filenames = []

        for media in media_uploads:
            if media and allowed_file(media.filename):
                filename = secure_filename(media.filename)
                media.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                media_filenames.append(filename)

        if media_filenames:
            profile.media_upload = ','.join(media_filenames)

        db.session.commit()
        flash('Profile updated successfully!', category='success')
        return redirect(url_for('views.update', profile_id=profile.id))

    return render_template('update-profile.html', profile=profile)



    

@views.route('/Paper_Cardboard')
def Paper_Cardboard():
    return render_template("Paper_Cardboard.html")

@views.route('/plastic')
def plastic():
    return render_template("plastic.html")

@views.route('/Metal_Info')
def MetalInfo():
    return render_template("Metal_Info.html")

@views.route('/GlassInfo')
def GlassInfo():
    return render_template("GlassInfo.html")

@views.route('/Electronics_Info')
def electronics():
    return render_template("Electronics_Info.html")


from flask import request, flash, redirect, url_for

@views.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        # Proceed with saving the file or any other processing
        flash('File allowed and processed successfully!')
        return redirect(url_for('views.index'))
    else:
        flash('File not allowed')
        return redirect(request.url)
    

@views.route('/delete-profile', methods=['POST'])
@login_required
def delete_profile():
    data = request.get_json()  
    profile_id = data.get('profile_id') 
    
  
    profile = UserProfile.query.get_or_404(profile_id)
    
    
    db.session.delete(profile)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Profile deleted successfully!'})