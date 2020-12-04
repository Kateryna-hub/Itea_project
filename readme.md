Technology stack

Python3
MongoDB
Mongoengine
Flask
Flask restful
Telebot
Google cloud
Nginx
Gunicorn
Marhsmallow
DB entities

Products

Name
Description
{Category}
Price
Availability
Picture
Discount in percent
Categories

Name
Description
{parent}
[{subcategories}]
Users

telegram id (PC)
Phone number
Nickname
Basket

Orders

news

Title
Content
Date of publication
#Lesson 12

Create an abstract collection. It must contain two fields, created and modified, and store the date and time in them. created - object creation time, modified - last update time. We place the logic over time in the save method.
Initialize the bot. Describe the / start handler. At startup, greet the user. Create the texts module, which will store the text permanently.