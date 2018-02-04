# Requirement 


## The system shall be used by parents who are seeking schools for their chidren.

## The system must be able to display welcome information, introductions at the home page.

## The system must be able to display school information.

## The system must be able to filter schools in a specfic area.

## The system must be able to filter schools according to users' requests/inputs.

## The parents shall be able to add a school into watchlist.

## The system must be able to notify parents if there is change of school in their watchlist.

## The system must be able to provide comparing method given a list of schools. 

## The system must be able to interact with users to retrive users' requirments.


# 2. (Optional)
## The system shall be used by teachers from the perspective school.

## The teachers shall be able to update information of their schools.


## Home Page
### Functional Requirement

1. First row to show parent a jumbotron about the system.
2. The second row should display a navigation bar for user to go to other pages. 
3.  Scroll bar at the right of the screen in the case of more information to be display.
4. Display any updated info from schools.
5.  From third row on wards, each row will display 4 banner.
6.  User will be able to click on banner to display a modal of the updated info.
7.  By clicking on non modal space, the modal should disappear. 
8.  On the modal, school name should be display.
9.  On the modal, the displayed school name should be clickable thus allow user to navigate to full info about school on our system. 
10.  On the modal, any other keyword should be clickable too. Example course info should there be one.

### Non Functional Requirement

1. 80% of the user should be able to learn how to use the interface in 2 minutes.
2. The system should be able to consistently updating any new info.
3. There may be legal issues involving privacy of information, intellectual property rights, export of restricted technologies, etc. Those information should be declared in the system.
4. User information should be protected thus eliminate the risk of leaking user information.
5. The system should be responsive so any action from user will react in under 2 ms in good network condition.
6. All processing should be done on the server side so not to cause performance issue on user's device.  

## Comparison between schools

###ADD/REMOVE SCHOOLS
1. User can add schools to a comparison list from School Information Page.
2. User can remove a school from the table.
3. User can add a school to Favorite list from the table.

###TABLE DISPLAY
1. When entering display, create a table of all schools in the comparison list with their details as columns.
2. Preferable features of a school are Highlighted. (For features that are hard to compare, just leave them.)
3. User can sort any feature column. (Number: dec/asc order; String: alphabetical order)


###REQUIREMENTS TOWARDS FOLLOWING AND PUSHING SERVICE
1.	User must be able to select what kind of organisation they want to follow whether child care or kindergarten and so on. 
2.	User must be able to follow as many kinds of kindergartens or child care services as possible when they are interested in a specific type of kindergarten.
3.	User must be able to follow a certain type of kindergarten or child care services to receive their relevant data or messages.
4.	User must be able to unfollow certain kindergarten or child care services when they are not interested in it.
5.	User must be enabled with the ability of choosing some certain kindergartens or child care services that they have followed to form some certain groups based on users’ need.
6.	User must be able to give different priorities to different groups.
7.	User must be able to give different priorities to the members(schools) inside each group.
8.	User must be able to see the kindergarten’s or child care services’ home page and information after following a specific kindergarten. 
9.	User must have the choice to choose whether to receive the pushing service or not.
10.	The pushing service must provide information towards the kindergarten or child care services name, latest information about the kindergarten.
11. User must be able to select which kind of pushing message they want for each kind of groups they have made before.
12.	Pushing message must have different tags including messages about new classes, message about new vacancies, messages about new teachers, messages about new teaching plan and so on.
13.	User must be able to choose what kind of pushing message they want to receive.
14.	User must be able to receive the information about their followed kindergarten or child care services immediately.
15.	The application must be able to send pushing message to the user whenever the user is opening the application or not.
16.	User must be able to see the previous pushing messages up to whatever day they want.
17.	When different information towards different kindergartens or child care services are received at the same time. The kindergartens or child care services with higher priorities must be given the priority to display the pushing messages following with pushing messages towards lower priority kindergartens or child care services.
