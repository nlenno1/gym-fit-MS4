# Testing

# Manual Testing

## Features Testing
Find all my manual testing criteria, procedure and outcomes in my [Manual Testing Document](gym-fit-manual-testing-document.pdf)

## User Stories

For full details on the User Stories testing, please see my [User Stories Testing Document](gym-fit-user-stories-testing-document.pdf)

## Peer Review

I requested peer review feedback from my friends, family and the Code Institute slack community. Below you can find any issues or suggestions from my peers and any changes I made in response to the feedback. Apart from that logged below, all other peer review feedback was positive.

|Peer |Feedback Received |Action Taken |
|-----|-----|-----|
|Hollie Coote |Can only see 5 days in advance on the Classes this Week page |Altered the view to include the entire week plus 1 day |
|Anya McDonald |Class description seems too close to the image on the Class Details page |Added addition padding to this text section |
|Anya McDonald |2nd image on the home page seems out of place |Updated design |
|Anya McDonald |Would like some more about opening hours  |Added opening hours to the home page |
|Laila (Slack) |500 response when adding a package to their bag as a guest  |Added login_required decorator to prompt user to sign in/up to purchase a package |
|Tayla Joel |Would like to be able to sign in using social media accounts  |Added to the future development features list |
|Frannie Yip (Slack) |Missed the sent message notification. Maybe redirect to a different page to make it clearer the message has been sent  |Changed message redirect to the home page |

## Responsive Design 

After researching the most commonly used screen resolutions ([Screen Resolutions Research Link](https://www.browserstack.com/guide/responsive-design-breakpoints)), I tested the responsive design on all the pages in this project at the resolutions widths of:

![Resolutions Image](responsive-test-resolutions.jpg)

as they are the very common resolutions. I carried out the tests using a combination of the [Browser Stack Responsive Design Tester](https://www.browserstack.com/responsive), [Media Genesis RESPONSIVE WEB DESIGN CHECKER](https://responsivedesignchecker.com/) and [Chrome Dev Tools](https://developer.chrome.com/docs/devtools/). 

I also added 2560 × 1440 screen resolution into the tests to enable site display durability as this resolution is becoming more widely used.

Here are the results to these tests:
![Responsive Design Test Results](gymfit-responsive-testing-results.png)

During testing, I realised the Admin Messages table was acting responsively however this led to the table being horizontally scrollable, at smaller screen widths, which was hampering the UX. To correct this I refactored the Admin Message display to a custom design which was more responsive, before running my responsive tests again.

For device responsive testing I used:
- A Samsung Galaxy S10 (360px) as it is roughly in the middle of the range of screen sizes I tested for mobile, 
- A Samsung Galaxy Tab 4 Tablet (800px) as again it is roughly in the middle of the range of tablet screen resolutions test 
- A full HD 15" laptop and full HD 32" monitor (1920x1080).

## Browser Testing

I manually tested the project on the Browsers Firefox (version 94), Chrome (version 96) and Edge (version 95) on my Windows 10 machine and called a peer to talk them through testing the page on Safari (version 15.1), so I could manually test all browsers on desktop.

All features and designs were as expected.

# Automated Testing

## Performance - Lighthouse
I tested the Performance, Accessibility, Best Practices and SEO of GymFit using [Lighthouse](https://developers.google.com/web/tools/lighthouse) in Chrome Developer Tools.

|Page | Lighthouse result |
| --- | --- |
|Home | ![Lighthouse Result for Home](gymfit-lighthouse-home.jpg) |
|Our Classes | ![Lighthouse Result for Home](gymfit-lighthouse-our-classes.jpg) |
|Join Us | ![Lighthouse Result for Home](gymfit-lighthouse-class-access-packages.jpg) |

The results from all pages were similar to the results shown, for desktop and mobile. The main performance degradation happened when displaying images but especially the instructor images as they are being hosted remotely and I can not control the size of the hosted images. To solve this issue, the images could be stored in the project AWS storage. The model allows for external URLs to be used for the image and I wanted to test for the worst possible scenario after deployment.

The best practice issues have all come from the Stripe import. There is now an updated application for the Stripe system, which might remove these issues, that can be implemented in future releases.

![Lighthouse Best Practice Issues for all pages](gymfit-lighthouse-best-practice-issues.jpg)

## Colour Tester - A11y

To test the color contrast on GymFit I used [A11y the Color Contrast Accessibility Validator](https://color.a11y.com/). After testing a few pages, there were no issues found. Here is the result from the Classes this Week page as it contained all the color combinations that have been used in the project.

![Image of Color Validator Result](gymfit-a11y-color-test.jpg)

# Validation

### HTML

Find all my HTML validation, please see my [HTML Validation Document](gym-fit-html-validation-document.pdf)

### CSS

All the CSS files on the project were validated using the The W3C CSS Validation Service
(https://jigsaw.w3.org/css-validator/). They were tested through direct input top remove the errors and warnings generated by external files.

Through testing I found 2 color declarations that were missing the # symbol before the hex value and both of these were corrected. 

After these corrections, all CSS files passed validation.

<a href="http://jigsaw.w3.org/css-validator/check/referer">
    <img style="border:0;width:88px;height:31px"
        src="http://jigsaw.w3.org/css-validator/images/vcss-blue"
        alt="Valid CSS!" />
    </a>
</p>

### JavaScript

I validated the JavaScript in the project using BeautifyTools’ JavaScript Validator. The only issues found were a few missing semicolons and definition issues cause by using elements from bootstrap or functions being defined but not called as they are called by inline functions.

After correcting the semi colons issues, all the JS passed the validation

### Python

To validate the Python code used in this project, I ran manual checks to confirm all print statements and commented out code were removed while checking relevance of the comments on the code. 

During development I had [pylint](https://pylint.org/) installed on my workspace which highlighted any problems which were correct as and when they arrose.

I also used the [Black Code Formatter](https://black.readthedocs.io/en/stable/) to format and beautify the code. 