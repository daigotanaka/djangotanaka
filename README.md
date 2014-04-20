# djangotanaka

A Django based web site

## Install

    virtualenv env --distribute
    source env/bin/activate
    pip install -r requirements

## Run

    source venv/bin/activate
    foreman start

## Posting, retrieving, and editing articles

### Post a new article

    python post draft/my-article.txt

### Retrieving a new article 

    python get --slug my-article 

### Editing an existing article 

    python patch draft/my-article 

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
