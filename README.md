# JAIPUR GUIDE
#### Video Demo:  https://youtu.be/Gn9LUTz1kEk
#### History:

Jaipur is a city of Rajasthan in India, also known as the Pink City.
Planned by Vidyadhar Bhattacharya, Jaipur holds the distinction of being the first planned city of India. Renowned globally for its coloured gems, the capital city of Rajasthan combines the allure of its ancient history with all the advantages of a metropolis. The bustling modern city is one of the three corners of the golden triangle that includes Delhi, Agra and Jaipur.

Jaipur traces back its origins to 1727 when it was established by Jai Singh II, the Raja of Amber. He shifted his capital from Amber to the new city because of the rapidly-growing population and an increasing water scarcity. Noted architect Vidyadhar Bhattacharya used the established principles of Vastu Shastra to build the city.

#### Description:

jaipur guide<br>
    |<br>
    |--> static<br>
    |       |--> css --> style.css<br>
    |       |--> img --> all images<br>
    |<br>
    |--> templates<br>
    |       |--> add.html<br>
    |       |--> contact.html<br>
    |       |--> facts.html<br>
    |       |--> index.html<br>
    |       |--> layout.html<br>
    |       |--> more_info.html<br>
    |       |--> tourist_place.html<br>
    |<br>
    |--> application.py<br>
    |--> config.json<br>
    |--> Travel.db<br>

I used flask and sqlite3 database for backend and html, CSS and JavaScript for frontend. This website will guide tourists to find and locate amazing places to visit in Jaipur. I have categorized places to make interface user friendly so that they can bifurcate according to their preferences. Description, history and facts about places which makes place more interesting to visit. People can find best and suitable time to visit places. People can able to explore some hidden gems of Jaipur.
This site will provide collective knowledge about a place giving major information to users. With collection of photo captured at that location which make this website more useful than other related.

--> Static: It contains static files like css file and img folder contaning all the images used in website.

--> Templates: This folder contains all the .html file which work as template for the website.

--> config.json: This file contains website configuration such as admin email-id, password, image folder path, etc.

--> Travel.db: This is a sqlite3 database containing Jaipur and User Table.
                |->Jaipur table stores information that is used in category pages. Columns are name, image, tag, desc.
                |->User table stores the information about the user who submit contact form. Columns are username, email, contact, suggestion.

--> application.py: This is a controller of website. It contains different routes to handle different page request and giving back proper response. It has home page, facts page, tourist places (containing all places), category page (according to user preference), detail page, add page and contact page.
                    |-> Category page has a dynamic route to handle multiple request without post or get method. Category method then make a query to Jaiput table in database according to the request and sends back the response to the user.
                    |-> Add page contains a form containing fields required to a place. If admin submits the form by his email_id then the place is directly added to the website else the data is stored in database for evaluation.
                    |-> Contact page also contains the form for any suggestion and query. All the details filled by user are stored in Users table. After submition User receives the thank you mail and admin receives the mail, containing the user information and query.
