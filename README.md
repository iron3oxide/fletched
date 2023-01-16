Say you want to design an app for a government agency with multiple, let's say 20+ pages (MPA = Multi Page Application). Since Flet is technically SPA (Single Page Application) only, you'll use views and some routing to simulate the MPA behaviour. 

Not every person in the agency should be able to access every page/view. Also, they shouldn't be able to see anything but the login page until they're logged in. The roles defined in the OAuth token the app receives upon login will determine what pages/views a user has access to. 

You'll probably want to design your app in a way that bundles every page/view into its own module. If you used an architecture design pattern (which you definitely should at this scale), obtaining the view requires building its model and presenter or controller as well and thus you need some function or method to obtain the view. 

The way flet routing works ATM, a view will have to be recreated after a route change, so you'll want to match each route of your app to the function or method that creates the appropriate view for it. You'll also want the function/method to return a different view or raise an exception if the user is not authorized to access it. This can create a lot of boilerplate code if you don't have the help of a library.
