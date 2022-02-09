# Diary of a Journal: isqa8210_travelblog




#Additional Features/Items
    - Custom Management Functions
        - seed
            - python manage.py seed
            - Uses faker to add up to 25 users, up to 25 posts for each, and up to 10 commetns for each post.
            - Uses image generator to randomly provide image links (https://picsum.photos/)
        - cleanup
            - python manage.py cleanup
            - Deletes all posts, comments and REGULAR users
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
    - Added Custom Template Tags
        - blog_url
            - Create the right url for using in pagination and sorting links
        - activesort
            - add appropriate styling to sorting buttons
        - popovertext
            - create truncated text html for use with BS popover
    - Config changes
        - Created .env to move secret_key and un/pw for SendGrid into non-repository file.  Set up environment variables in heroku to provide this information.
        - Added additional security checks to CRUD methods to make sure the user was a superuser, NOT just logged in.
    - UI Changes
        - Added Sort by post date, # of comments, and last comment date for front page
        - Added searching for front page, post list, and comment list
        - Added pagination for post list, and comment list
    - Added styled Change password page to front end
        - /accounts/password_change
        - Linked in dropdown menu next to logout
    - Set up SendGrid integration
    - Set up styled "forgot my password" feature
    - Added favorites table
        - Added JS (ajax) and styling


##Attributes:
###Password Reset
Used this tutorial: https://learndjango.com/tutorials/django-password-reset-tutorial
 
###Bootstrap Theme:
https://bootstrap.build/app/project/KFEuubTyXwQL

###Bootstrap Popover:
https://getbootstrap.com/docs/5.0/components/popovers/ 

###Box Shadow:
https://html-css-js.com/css/generator/box-shadow/

