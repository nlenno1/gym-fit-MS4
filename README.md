# **Gym Fit - Group Fitness E-Commerce Platform**

This project is designed to fufill the needs of a gym or fitness center looking to move thier booking system online and to help them grow their online sales.

![Live Project Representation Image](#)

[Link to Live Project](#)

This is the last of the Milestone Projects that make up the Full Stack Web Development Program at The Code Institute. The main requirements of this project are to *"build a full-stack framework based around business logic used to control a centrally-owned dataset"* using the technologies: **HTML**, **CSS**, **Javascript**, **Python+Django** with a relational database and using the Stripe payments system.

This e-commerce platform allows a small to medium size fitness business to transition from in person to online sales of products and class admittance, and will drive a growth in sales with the opportunity to support fully online operation. Working fully online can be an avenue for business development however the need for this functionality/ability was emphasized most recently by the COVID pandemic where many in person businesses were forced to move online.

## **STRATEGY**

### **Project Goals**

- Develop an e-commerce website to promote a fitness class business and to move their booking system online to improve productivity and efficiency in the booking system to increase customer sales and customer retention
- Create an Admin access account on the platform to allow the company to make the required changes to the data sets in the database
- Produce a secure and comprehensive backend structure, including database hosting any data stored online
- Build a smart and responsive web app to enable users to view displayed information easily
- Handle any errors in such a way to help the user understand the issue and provide an easy form of contact if any error should persist

### **Business Goals**

- Sell more classes online and start selling subscriptions or class access token packages
- Increase class attendance by assisting users to view, change or cancel their bookings with tokens refunded if applicable
- Streamline the booking system to reduce admin work and move towards a cashless business
- Expand the business by easily adding more classes and instructors when required
- Allow customers to find out more information about all the services provided by the business
- Be able to develop the platform later on to add more features including Instructor portals (including personalized schedules), attendance lists (with first time attendees and customer medical conditions to be aware of), mailing lists etc

### **User Demographic**

- Aged 18 to 45
- All genders and ethnicities
- Enjoy fitness and strive for a healthier lifestyle
- Live, work or are visiting in travelling distance from the business
- Interested in building and being an active part of a fitness community
- Comfortable using web apps and online payment systems

### **Value for the User/Customer**

- Easier access to class schedule and a more efficient booking system
- Friendly and intuitive interface
- Convenient email updates to any changes made to classes they are booked on to
- Secure storage of personal information to assist in more efficient payments
- Possibility to access more information about the company and services provided
- Track payments and classes attended
- Read other customer reviews of class and ability to share their personal views with others in their own review
- Opportunity to purchase subscriptions or class access token packages which were unavailable before

## **User Stories**

My user stories are broken up into categories indicated by their ID number. A **Guest** is a Non-Account Holder and a **Customer** is an Account Holder

| ID | Category Name |
| --- | --- |
| 01 | Class Booking |
| 02 | Shopping Bag and Checkout |
| 03 | User Account |
| 04 | Miscellaneous |
| 05 | Admin |

![Spreadsheet of User Stories](readme/assets/gym-fit-user-stories.png)

## **SCOPE**

### **Production Feature Planning Table**

After the initial planning session, an importance viability assessment was performed on all the features suggested and below are the results of this. I-V marks range from 1 to 5

| ID | Feature                                                                                          | Importance | Viability |
|----|--------------------------------------------------------------------------------------------------|------------|-----------|
| 01 | Register, Confirm, Update information in and Delete a User Account with confirmation emails      | 5          | 5         |
| 02 | Sign In and Out                                                                                  | 5          | 5         |
| 03 | Sign In and Out with other social media accounts                                                 | 3          | 4         |
| 04 | Recover account if login information is lost                                                     | 5          | 5         |
| 05 | View User's personal information, upcoming and previous classes and order history                | 5          | 5         |
| 06 | Update User's Personal Information                                                               | 5          | 5         |
| 07 | Create, View, Edit and Delete Class Categories                                                   | 5          | 5         |
| 08 | Schedule, View, Edit and Delete Classes                                                          | 5          | 5         |
| 09 | Filter classes by category, date, trainer, time, ability level and favourite class category list | 5          | 3         |
| 10 | Manage User's personal favourite class category list                                             | 4          | 5         |
| 11 | Schedule weekly classes until a set date or for a certain number of weeks                        | 3          | 3         |
| 12 | Book onto or add a class to the shopping bag                                                     | 5          | 5         |
| 13 | Delete a class booking with refund if required                                                   | 5          | 4         |
| 14 | View fully booked or almost full classes                                                         | 5          | 5         |
| 15 | Add customers to waiting lists if a class is full, with email notification on space opening up    | 3          | 5         |
| 16 | Purchase multiple classes with a weekly interval with a specified number of weeks                | 2          | 3         |
| 17 | Create, View, Edit and Delete Class Access Packages (Tokens or Unlimited)                        | 5          | 5         |
| 18 | Create, View, Edit and Delete Class Access Packages for specific class categories                | 3          | 5         |
| 19 | Create, View, Edit and Delete Instructor Profiles                                                | 4          | 5         |
| 20 | Allow Instructors to Update their publicly visible profiles and manage their classes             | 2          | 2         |
| 21 | Add purchasable items to the shopping bag                                                        | 5          | 5         |
| 22 | Securely process a purchase for items in the shopping bag                                        | 5          | 5         |
| 23 | View order confirmation on purchase completion with a confirmation email                         | 5          | 5         |
| 24 | Validate all User input                                                                          | 5          | 5         |
| 25 | Contact system with FAQs                                                                         | 5          | 5         |
| 26 | Links to business social media accounts                                                          | 5          | 5         |

![Importance Viability Graph](readme/assets/gym-fit-importance-viability-graph.png)

The graph shows an axis of up to 6 however data scores range from 1 to 5 making a 5,5 the highest possible.

Not all users will be able to access all features.

#### **I-V Analysis Conclusion**

After the analysis of the features suggested, all features will be implemented **apart** from feature **3, 11, 15, 16, 18, 20**. These have been removed due to complexity and time restraints mainly but have been added to the list of features for future releases.

**Feature 15 and 18** have been removed because time restraints have limited the amount of features that can be added. These features are possible however the importance category carries more weight in this instance.

**Feature 9** has been **included** in this release however it has been **amended**. The feature will now:

    "Filter classes by class category, date and favourite class category list only while sorting classes chronologically"

Removed functionality can be included in a later release.

The selected website functionality can be broken down into 3 general permission levels using what features users are allowed to access.

### 1. Permission Level 1 - Guest User/Not logged in

At this level, Users can;

- View all basic information about the business,
- View all individual classes available for purchase,
- Add any individual class to their bag,
- Purchase the contents of the bag, by entering their information, and receive confirmation of the transaction on completion,
- Create an account, either separately or as part of the checkout procedure,

### 2. Permission Level 2 - User Logged In/Customer

At this level, Users can;

- Do everything from Permission Level 1,
- View all data stored in relation to their account, including basic details, address and order/class order history
- Update their account information, via their account Profile page
- Add classes to their favourite lists
- Buy class tokens or a subscription
- Leave rating on classes attended

### 3. Permission Level 3 - Admin

At this level, Users can;

- Do everything from Permission Level 1 and 2
- Create, View, Edit or Delete classes and class categories
- View details about the classes and attendees
- Manage instructor profiles
- Receive customer communications

## **STRUCTURE**

## Topology

This diagram explains how the pages will be linked or accessed from each other. The red lines are Admin only access pathways. All the blue elements are accessible at all times from the navbar element.

![Topology Diagram](readme/assets/gym-fit-topology-diagram.png)

## Database Schema

To deliver the required functionality, I have used a relational database to store and access any associated data.

SQLlite was used in the development phase and Postgres, as provided by Heroku, was used in live production.

This diagram shows the database models and the relationship between them.

![Database Structure and Schema Diagram](readme/assets/gym-fit-db-schema.png)

Color Key for app that contains the model:

- Yellow - checkout
- Purple - classes
- Green - products
- Orange - profiles
- Grey - allauth
- Red - instructors
- Pink - reviews
- Blue - contact

### **Model Descriptions**

**User** - Provied by AllAuth application and contains basic user information including username, email etc. This model does not link to any other model but if filled by the Order model on occasion.

**UserProfile** - Stores more detail about a User and is created when the User signs up for a profile. Contains default informtion, used in Order and ContactMessage froms, as well as details about the classes the User has booked on to and the Users class packages, for example the amount of tokens they have to use and the package expiry date. This model is uses ClassCategory for its fav_class_category field and SingleExerciseClass for its classes field which are both ManyToManyFields

**SingleExerciseClass** - Model for all the single exercise class events that can be booked onto using a one time payment or class access package. The model including details like the class location, start time, instructor, price etc. This model is uses ClassCategory for its category ForeignKeyField, Instructor for its instructor ForeignKeyField and User for its participants ManyToManyField

**ClassCategory** - Model for the categories of exercise classes that are offered by GymFit. This model includes detail about the categories required equipment and a short description of the class category. This does't use any other model and was created first.

**ClassCategoryReview** - Model contains all the information for a review of a exercise class category like the review author, subject, rating etc. This mode uses the User model for its author field and ClassCategory model for its review_subject field which are both ForeignKeys.

**ClassAccessPackage** - Model for a type or puchasable product that will allow users access to book onto single exercise classes having unlimited access or a limited number of tokens attributed to their UserProfile. This model contains details such as the type of package, price, package duration until expiry etc. This model doesn't use any other models as the data contained with in it is generally used to alter the information in the UserProfile after purchase.

**Order** - Model that contains all the data related to a single user purchase of a Class Access Package and/or Single Exercise Classes. This model includes shipping details, order total price and the Stripe PID. This model uses the UserProfile model through a ForeignKey field.

**OrderLineItem** - A model for individual items in an order including what the item type and what order it belongs to." This model used the SingleExerciseClass, ClassAccessPackage and Order models as ForeignKeys.

**Instructor** - This model contains the information about the instructors that work at GymFit like their description and if they will be shown on the website. This model uses the ClassCategory for its can_lead_classes ManyToManyField.

**ContactMessage** - Model for storing all the messages sent from the contact page to admin including information like senders name, email address and the message. This model doesn't use any other model as the data is stored as strings as there is not the functionality to reply on the site.

In the database, the OrderLineItem model is not necessary however, it has been included for code reusability and to speed up future develpment.

## **SKELETON**

### **Wireframes**

[Link to all the Wireframe designs for this project](readme/assets/wireframes.md)

### **Design Alterations**

### **Design Decisions**

## **FEATURES**

This is a full, page by page, breakdown of all the features & elements that have been implemented for the first production release of the Gym Fit E-Commerce platform.

### Multi Page Elements

**User Feedback** - All User Feedback messages will come in the form of "Toasts" supplied by Boostrap and displayed on the bottom right of the screen. These Toasts change heading color and contents depending on the message displayed

**Navbar**
- Logo - to establish identity and act as a home button
- "Our Classes" - links to Class Category display to show the user what class types are on offer
- "Book Classes" Dropdown Menu which links to:
    - "Classes This Week" which allows the user to see and filter all the classes this week
    - "Classes By Day" which allows the user to search for classes on individual days and filter the classes found
- "Join Now" - Links to the "Join Us" page which shows the user the Class Access Packages the company has to offer
- "Contact" - Links to the Contact page

**Top Navbar**
- "My Account" - When a User is signed in this links to the Users profile page but when the User is a Guest it is a dropdown menu which links too
    - Register to allow the User to create an Account or 
    - Sign In to allow a User to sign into an existing account
- Shopping Cart Icon - Links to the Users current bag display

At Mobile screen widths, the Navbar links will be contained in a full screen menu which can be toggled with a button on the Navbar.

**Footer**
- Logo - to establish identity and act as a home button
- Links to socials for promotion and to encourage user engaguement
- Address of GymFit

### home App

**/**
- Our Team Display - Display generated from Instructor models in the database. Each model has a display_on_site field which determines which instructors are show. A maximum of 8 instructors will be displayed
- Map and Links section - Links to GymFit instagram account and location on GoogleMaps. Image provided to represent use of GoogleMaps API.

### classes App

**All Class Categories - /classes/our_classes/**
- Card Display of Individual Class Categories which includes:
    - Average Rating display data generated from ClassCategory Model,
    - Heart Icon Button to Add or Remove the Class Category from the Users Favourite Class Categories list,
    - "View Class Details" button links to /classes/class_category/<category_id> for the specific Class Category
- "Add Class Category" Button (ADMIN) - Link to classes/class_category/add

**Class Category Details - /classes/class_category/<category_id>/**
- Class Category details including Name, Representation Image, Average Ratings and Description
- Heart Icon Button to Add or Remove the Class Category from the Users Favourite Class Categories list,
- "Update Class Category" Button (ADMIN) - links to /classes/class_category/<category_id>/edit
- "Delete Class Category" Button (ADMIN) - deletes the selected Class Category after a confirmation check
- Class Category Reviews section which displays all reviews left for the class ordered newest to oldest. If user has left a review, a delete review button is displayed beside their review if they wish to remove it.
- "Write a Review" Button - links to Add Category Review to allow a user to add a review

**Add a Class Category - classes/class_category/add** (ADMIN)
- ClassCategoryForm displayed using Crispy Forms with labels
- Cancel button - Links to All Class Categories
- "Add Class Category" Button - Validates form and adds new Class Category to the database, redirecting to the Class Category Details for the Category just created

**Edit a Class Category - classes/class_category/<category_id>/edit** (ADMIN)
- ClassCategoryForm which is filled with current Category data, displayed using Crispy Forms with labels
- Cancel button - Links to Class Category Details for the class you were editing
- "Edit Class Category" Button - Validates form, updates the Class Category in the database and redirects to the Class Category Details for the Category just edited

**Classes this Week - /classes/classes_this_week/**
- Single Exercise Class Display - Individual Responsive display items for the scheduled classes from the current date until 8 days in the future (to include the same day a week later). If no classes are scheduled, the date will not display. These display items include:
    - Details about the event including date, start time, ability level, location, cost(in tokens or currency depending on user package status) etc
    - Add to Bag button - Adds the selected class to the users shopping bag
    - Book with Tokens button - Books the user onto the class by adding the user to the class participants and the class to the users classes and updates the users package status
    - Edit Class (ADMIN) - links to the Edit Single Exercise Class page
    - Cancel Class Button (ADMIN) - deletes the selected Single Exercise Class after a confirmation check, sends a notification to all participants and refunds tokens
- "Filter By" Dropdown Menu - On selection filters the classes displayed by any single Class Category or using the categories in the Users Favourite Category List
- "Classes By Day" Button - links to Classes by Day

**Classes by Day - /classes/classes_by_day/**

- Single Exercise Class Display - Same as Classes this Week
- "Filter By" Dropdown Menu - On selection filters the classes displayed using any single Class Category or using the categories in the Users Favourite Category List
- "Classes on" Date Select -  On selection filters the classes displayed using the chosen date
- "Classes This Week" Button - links to Classes this Week

**Schedule a Single Exercise Class - /classes/single_class/add/** (ADMIN)
- SingleExerciseClassForm displayed using Crispy Forms with labels
- Cancel button - Links to Profile as that is the only place you can schedule a class from
- "Schedule Class" Button - Validates form and adds new Single Exercise Class to the database, redirecting to Classes This Week

**Update a Single Exercise Class - /classes/single_class/edit/** (ADMIN)
- SingleExerciseClassForm which is filled with current Exercise Class data, displayed using Crispy Forms with labels
- Cancel button - Links to Class Category Details for the class you were editing
- Edit Class Category Button - Validates form, updates the Class Category in the database and redirects to the redirecting to Classes This Week

### products App

**View Class Access Packages - /products/class_access_packages/**
- Display for Token Packages including a repesentation image, package name, popover with more information and package price, ordered by price
- Display for Unlimited Use Packages including a repesentation image, package name, popover with more information, package expiry and package price
- Edit Class (ADMIN) - links to the Edit Class Access Package page
- Delete Package Button (ADMIN) - deletes the selected Class Access Package after a confirmation check and redirects to View Class Access Packages
- Add a Tokens Package / Add an Unlimited Package (ADMIN) - links to Add a Class Access Package

**Add a Class Access Package - classes/class_category/add/** (ADMIN)
- ClassAccessPackageForm displayed using Crispy Forms with labels
- Cancel button - Links to Profile
- "Add Access Package" Button - Validates form and adds new Class Access Package to the database, redirecting to View Class Access Packages

**Edit a Class Access Package - classes/class_category/<package_id>/edit/** (ADMIN)
- ClassCategoryForm which is filled with current Category data, displayed using Crispy Forms with labels including JS check on value of select to see if Class Tokens should be disabled or not
- Cancel button - Links to Class Category Details for the class you were editing
- "Edit Class Category" Button - Validates form, updates the Class Category in the database and redirects to the Class Category Details for the Category just edited

### contact App

**Contact Page - /contact/**
- ContactMessageForm displayed using Crispy Forms with labels. If user is annonomous then name and email inputs are provided. If user is signed in then these details are provided from the database.
- Cancel button - Links to Home
- "Send Message" Button - Validates form, saves data to database and display sent message user feedback after reloading the page

### profiles App

### bag App

### checkout App

### reviews App

### instructors App

### **CRUD Table**

### **Defensive Programming**

### **Error Handling**

### **Features for Future Releases**

- Sign In and Out with other social media accounts
- Add customers to waiting lists if a class is full, with email notification on space opening up
- Purchase multiple classes with a weekly interval with a specified number of weeks
- Create, View, Edit and Delete Class Access Packages for specific class categories
- Allow Instructors to Update their publicly visible profiles and manage their classes
- Automated subscription payment service
- Messaging system to allow admin to respond to customers with accounts
- Add accessory products to the store like apparel, water bottles etc
- Refactor Profile into seperate pages to allow redirection to specific sections

## **TESTING**

View the [Testing Document](readme/assets/testing.md)

## **BUGS AND ISSUES**

## **DEPLOYMENT**

## **TECHNOLOGY USED**

<details>
<summary> Languages and Libraries</summary>

- [Django](https://www.djangoproject.com/) - Python Framework
- [HTML5](https://developer.mozilla.org/en-US/docs/Glossary/HTML5) - Programming Language
- [CSS 3](https://developer.mozilla.org/en-US/docs/Web/CSS) - Programming Language
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - Programming Language
- [Python](https://www.python.org/) - Programming Language
- [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) - Templating Language
- [jQuery](https://jquery.com/) - JavaScript Library
- [Bootstrap v5](https://getbootstrap.com/) - Library Import
- [Google Fonts](https://fonts.google.com/) - Typography Import
- [Font Awesome](https://fontawesome.com/) - Icon provider
- [AOS](https://github.com/michalsnik/aos) - Scroll Animation Library

</details>

<details>
<summary> IDE and Version Control</summary>

- [Git Pod](https://gitpod.io/) - IDE (Integrated Development Environment)
- [Git](https://git-scm.com/) - Version Control Tool
- [Github](https://github.com/) - Cloud based hosting service to manager my Git Repositories
- [Code Institute GitPod Template](https://github.com/Code-Institute-Org/gitpod-full-template) - Provides GitPod extensions to help with code production
</details>

<details>
<summary> Design and Development</summary>

- [Google Chrome Development Tools](https://developer.chrome.com/docs/devtools/) - Design/Development Tools
- [Figma](https://www.figma.com/) - Wireframe designer software
- [Balsamiq](https://balsamiq.com/) - Wireframe designer software
- [Coolors](https://coolors.co/) - Colour scheme generator
- [Lucid App](https://lucid.app/) - Diagram creator
- [Draw.io](https://app.diagrams.net/) - Flow chart creator
</details>

<details>
<summary> Validation and Testing</summary>

- [CSS Beautifier](https://www.freeformatter.com/css-beautifier.html) - Beautifying CSS Code
- [JavaScript Validator](https://beautifytools.com/javascript-validator.php) - Validating JS code
- [Lambda Test](https://www.lambdatest.com/) - Browser Testing Cloud Service
- [Am I Responsive?](http://ami.responsivedesign.is/) - Webpage Breakpoint visualizer and image generator
- [Black](https://black.readthedocs.io/en/stable/)- Code Formatter
</details>

<details>
<summary> Documentation</summary>

- [TinyPNG](https://tinypng.com/) - Image Compression
- [CompressPNG](https://compresspng.com/) - Image Compression
- [Markdown Table Generator](https://www.tablesgenerator.com/markdown_tables) - Markdown Table Production
</details>

## **CREDITS**

### **Code snippets**

### **Resources**

### **Content**

### **Media**

Gym Fit logo designed by [Hollie Coote](https://www.linkedin.com/in/hollie-coote-38306a146/?originalSubdomain=uk)

Images sourced from:

- [Pexels](https://www.pexels.com)
- [Pixabay](https://www.pixabay.com)
- [Unslapsh](https://www.unsplash.com)

### **Acknowledgements**
