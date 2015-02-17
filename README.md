<!--markdown-->
# kawaraban

A Django based web site that let you focus on writing.

1. **Write in your favorite editor**

    Create and edit posts with your favorite text editor, and post them with
    a single command, rather than opening a web browser:

        python post.py some-article.txt

2. **Use [markdown](http://en.wikipedia.org/wiki/Markdown/#Example) instead of
cumbersome HTML.**

    Draft written in Markdown is more legible than HTML, and produces cleaner
    HTML than wysiwyg HTML editors.

3. **Beafutiful preset layouts is just one keyword away**

    Like [cover photo](http://daigotanaka.org/full-width-cover)
    or [carousel](http://daigolab.org) layouts? This can be done just adding a
    keyword "coverphoto" or "carousel" (or
    [both](http://daigotanaka.org/our-garden-in-spring) if you want to be
    greedy)

## How to use

### Install git and get source code

1. Follow [this instruction](https://help.github.com/articles/set-up-git) to
set up github
2. Get the source code

        git clone git@github.com:daigotanaka/kawaraban.git
        mv djanotanaka my_website

### Install Python

Mac OSX users should follow
[this guide](http://docs.python-guide.org/en/latest/starting/install/osx/)

1. Install [Python](https://www.python.org/downloads/)
2. Install [pip](http://pip.readthedocs.org/en/latest/installing.html)
3. Install Python packages

        pip install virtualenv
        virtualenv env
        source env/bin/activate
        pip install -r requirements

### Deploy on Heroku

1. Create [a Heroku account](https://devcenter.heroku.com/articles/quickstart)
and install [the Heroku toolbelt](https://toolbelt.heroku.com/)
2. Create an Heroku app and add PostgreSQL

        heroku login
        heroku apps:create your_heroku_app_name
        heroku addons:add heroku-postgresql:dev --app your_heroku_app_name

3. Edit my_website/.git/config to add heroku as the remote repository
Add this at the end of the file:

        [remote "heroku"]
            url = git@heroku.com:your_heroku_app_name.git
            fetch = +refs/heads/*:refs/remotes/heroku/*

4. Deploy

        heroku config:set HEROKU=TRUE
        git push heroku master
        heroku ps:scale web=1
        heroku run python manage.py syncdb

It will ask you to create an account.

5. Useful Heorku add-ons

MemCachier:

        heroku addons:add memcachier

PG Backups:

        heroku addons:add pgbackups:auto-week

New Relic:
New Relic is a monitoring tool, and it can be used to ping the server periodically
so the free Dyno won't go to sleep.

        heroku addons:add newrelic:stark

After deploying the app, go to

        https://addons-sso.heroku.com/apps/your-heroku-app-name/addons/newrelic

Choose to set up New Relic APM, select Python for the agent to install, and
follow the rest of the instruction:

        https://docs.newrelic.com/docs/agents/python-agent/hosting-services/python-agent-heroku

## Run the server locally

### Set up [PostgreSQL](http://www.postgresql.org/download/)

### Set environment variables (do it once)

    LOCAL_POSTGRES_DBNAME=your_db_name
    LOCAL_POSTGRES_PASSWORD=your_db_password
    LOCAL_POSTGRES_USERNAME=your_db_username
    export LOCAL_POSTGRES_DBNAME
    export LOCAL_POSTGRES_PASSWORD
    export LOCAL_POSTGRES_USERNAME

### Start server

    source venv/bin/activate
    foreman start

*Point browser to 0.0.0.0:5000 to view site

## Posting, retrieving, and updating articles

### Set environment variables (do it once)

    DJANGO_USERNAME=your_django_username
    DJANGO_API_KEY=your_django_api_key
    export DJANGO_USERNAME
    export DJANGO_API_KEY

### Posting a new article

Posting a new article:

    python post.py draft/my-article.txt

Posting with parameters:

    python post.py draft/my-article.txt --title="My first article"

### Retrieving a new article

    python get.py --slug my-article

### Updating an existing article

    python patch.py draft/my-article.txt

Make the article public:

    python patch.py draft/my-article.txt --status "public"

The article is "private" by default.

Change the title:

    python patch.py draft/my-article.txt --title "New Title"

Change the slug:

    python patch.py draft/my-article.txt --slug "new-slug"

## Markdown with goodies

### Cover photo layout

Example: http://www.daigotanaka.org/full-width-cover/

Draft:

    <!--markdown coverphoto-->
    ![Cover photo high res image](http://mysite.com/image.jpg)

    ![Mobile low res image](http://mysite.com/image-low.jpg)

    ## Article title

    Text begins here...


### Carousel layout

Example: http://daigotanaka.org/landing/

Draft:

    <!--markdown carousel-->
    ## Article title

    Intro text outside carousel

    A paragraph that is converted to slide #1

    A paragraph that is converted to slide #2

    ...

### Combine cover photo and carousel layouts

Example: http://www.daigotanaka.org/our-garden-in-spring/

Draft:

    <!--markdown coverphoto carousel-->
    ![Cover photo high res image](http://mysite.com/image.jpg)

    ![Mobile low res image](http://mysite.com/image-low.jpg)

    ## Article title

    Intro text outside carousel

    A paragraph that is converted to slide #1

    A paragraph that is converted to slide #2

    ...

### Advanced: Use R

1. Use heroku-buildpack-multi:

```
heroku config:add BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git
```

2. Activate installation of rpy2 in requirements.txt

3. Set environmental variables

```
heroku config:set PATH=/app/vendor/pg/bin:/app/vendor/R/bin:/app/vendor/gcc-4.3/bin:/app/.heroku/python/bin:/usr/local/bin:/usr/bin:/bin
heroku config:set LD_LIBRARY_PATH=/app/.heroku/vendor/lib:/app/.heroku/python/lib::/app/vendor/R/lib64/R/modules:/app/vendor/R/lib64/R/lib:/app/vendor/gcc-4.3/lib64:/app/vendor/pg/lib
```

4. Add rpy2 to requirements.txt

```
rpy2==2.3.10
```

5. Commit the changes, and push the changes to heroku

```
git add requirements.txt
heroku config:set BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git
git push heroku master
```

![real kawaraban](https://farm8.staticflickr.com/7554/15684812578_bee3192ca0_o.png)
