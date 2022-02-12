# Diary of a Journal: isqa8210_travelblog
https://travelblog-dgh.herokuapp.com/

#Steps to install/run locally
1. Download repository
2. Install python requirements
   1. `pip install -r requirements.txt`
3. Configure environment variables 
   1. Create a .env file in the same folder as manage.py 
   2. Create 3 entries:
      1. SECRET_KEY = '(populate with DJANGO Secret)'
         1. Generate using a web tool Django itself:
            1. https://miniwebtool.com/django-secret-key-generator/
            2. `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`

      2. EMAIL_HOST_USER = '(populate with SMTP username)'
      3. EMAIL_HOST_PASSWORD = '(populate with SMTP password)'
4. Run migrations
   1. `python manage.py migrate`
5. Create a superuser:
   1. `python manage.py createsuperuser`
   2. Follow prompts
6. Optionally, seed the database:
   1. `python manage.py seed`
7. Run Server
   1. `python manage.py runserver`

# Additional Features/Items
- Custom Management Functions
  - seed
    - python manage.py seed
    - Uses faker to add up to 25 users, up to 25 posts for each, and up to 10 commetns for each post.
    - Uses random image site to image links (https://picsum.photos/)
  - cleanup
     - python manage.py cleanup
          - Deletes all posts, comments and REGULAR users (to re-run seed if needed)
  - testemail
      - python manage.py testemail
      - sends a test email (used during SendGrid setup)


- Numerous responsive changes and visual tweaks
    - Added popovers to post list to help the table format better
    - Image fixes for responsiveness
    - Used Crispy Forms for Bootstrap 5 styling
    - Added comment count badge on front page posts
    - Fixed some W3C HTML validation issues
    - Added some icons for author and comments
    - Updated the comments list in the travelblog_post page
    - Added ability to upload image instead of using a URL (but left that ability as well)


- Added Custom Template Tags
    - blog_url
        - Create the right url for using in pagination and sorting links
        - {%blog_url [param] [value] %}
          - param: URL Parameter Name
          - value: value for that parameter
          - adds "?param=value" or "&param=value" to url
    - activesort
        - add appropriate styling to sorting buttons
        - {% activesort [sort] [field] %}
          - sort: the sort of the query (i.e. date or -date)
          - field: the butten this applies to
          - returns either "primary active" or "secondary" to style the sorting buttons appropriately
    - popovertext
        - create truncated text html for use with BS popover
        - {% popovertext text length title %}
          - text: full text
          - length: number of words to retain
          - title: title to show in the popover
          - returns html for the popover with appropriate data- attributes.
      

- Config changes
    - Created .env to move secret_key and un/pw for SendGrid into non-committed files.  
    - Set up environment variables in heroku to provide this information.
    - Added additional security checks to CRUD methods to make sure the user was a superuser, NOT just logged in.
    - Refactor to put views/forms/models in individual files
  

- Query functionality Changes
    - Added Sort by post date, # of comments, and last comment date for front page
    - Added searching for front page, post list, and comment list
    - Added pagination for post list, and comment list
    - Added filtering for favorites 
  

- Added styled Change password page to front end
    - /accounts/password_change
    - Linked in dropdown menu next to logout
    - Set up SendGrid integration
    - Set up styled "forgot my password" feature
  

- Added favorites
  - Added favorites table
  - Added view to handle Ajax of making/removing favorite
  - Added JS (ajax) and styling (button)


## Resources:
### Password Reset
Used this tutorial: https://learndjango.com/tutorials/django-password-reset-tutorial

### Icons:
https://fontawesome.com/icons

### Bootstrap Theme:
https://bootstrap.build/app/project/KFEuubTyXwQL

### Bootstrap Popover:
https://getbootstrap.com/docs/5.0/components/popovers/ 

### Box Shadow:
https://html-css-js.com/css/generator/box-shadow/

