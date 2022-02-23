# Donorlist
Created By George Tims and Rushabh Shah

## Inspiration

The American Red Cross supplies roughly 40% of the nation's blood. Unfortunately, the pandemic has caused canceled blood drives, scared away potential donors, and made it difficult for the organization to retain and attract employees. As a result, the Red Cross has recently stated that its supplies have reached critically low levels.  Our goal with Donorlist is to alleviate this shortage by facilitating direct connections between geographically proximate donors and donees.

## What it does

The site lets potential donors and donees input both their blood type and city to view nearby blood type matches. Donees in need of blood can then reach out to potential donors either on a one-to-one basis or en masse to arrange a donation. 

## How we built it

We built the site predominantly using the full stack python-based web framework Django, with Bootstrap and JavaScript providing some additional styling and functionality on the front end. We leveraged the Geopy library and the OpenCage API to calculate the user's latitude and longitude based on their inputted city, as well as calculate the distance between different users to filter nearby blood type matches. 

## Challenges we ran into

Early on, we had a problem with excessive API calls, which resulted in the "view donors" page taking several seconds to load. We were using the API to calculate the exact distance (based on realistic travel routes) between the user and every other user in the database. This resulted in a large number of requests per page load, which inevitably slowed it down and would prevent the site from scaling in the future. To fix this, we created latitude and longitude fields in the user (profile) database, pulling these values just once on sign up and storing them. For the "view donors" page we then used a function in Geopy that calculated the "as the crow flies" distance between two users based on their longitude and latitude. As most people can't fly, this is a less accurate measure than that provided by the API call, but it is a sufficiently accurate approximation for our purposes and made page loads instant. 

## Accomplishments that we're proud of

This was the first Django project either of us had ever done, and so we're very happy to have an MVP that carries out the basic functionality desired in a reasonably attractive manner.

## What we learned

Django has a reputation as being one of the less flexible web frameworks, particularly in relation to something like Flask or Node. We learned how to leverage core Django functionality while also extending and customizing it to meet the needs of our project. For example, Django provides robust authentication with its built-in User model, but this User model did not have necessary fields like City, Blood Type etc. While it was finicky, we used a separate model (Profile) with a one-to-one relationship with User to take advantage of Django's authentication without compromising on our desired user model. We also gained more experience with using an ORM rather than SQL to perform database operations.

## What's next for Donorly - the blood donor matching site.

There is a lot of room for extension in this project. The following is just a shortlist:

- City and Age Validation
- Hospital Integration 
- Expanding into other areas with shortages, like bone marrow