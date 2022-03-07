# BabaShop Ecommerce Django Project
This project is about an online shop which supplier can register and sell their products. Each supplier can set more than one shop with defferent type of products. Supplier can also post articles about their product in blog of the BabaShop website.
Customers can buy from each shop and the supplier can check the customer order in his dashboard.

## Features
This web application contains:
* register with email / phone / username
* Supplier login / logout 
* Customer login / logout
* Forget password with phone number and OTP
* All users can see products
* Logged users can add products to cart
* All supplier have a dashboard
* Each dashboard contains charts, costomers list, orders list, products list and shops list
* Suppliers can define shop and product in their dashboard
* There are three type of users:
    * Admin
    * Supplier
    * Customer
* Admin permissions:
    * Create shop
    * Create product
    * Create post
    * Delete / edit shop
    * Delete / edit product
    * Delete / edit post
    * Create supplier / customer
    * Delete / edit custoemr or supplier
    * ...
* Supplier permissions:
    * Access to a dashboard with useful reports and charts
    * Create shop
    * Create product
    * Create post
    * Delete / edit shop
    * Delete / edit product
    * Delete / edit post
* Customer permissions:
    * login/ logout/ register/ ...
    * put an order
    * delete from cart
There are 3 types of discount:
* Product discount
* An item of order discount
* Total order discount

The shop Contain 3 sections:
* Shop section that mostly related to supplier
* Order section that mostly related to customer
* Blog section that only supplier can post and customer just can read and leave a comment
It is possible to search in blog base on name of post and their content

## Technologies
 * Python
 * Django
 * AJAX
 * JQuery
 * HTML
 * CSS
 * Bootstrap
 * Javascript
 * Celery
 * OTP

### Some pages of Babashop website

#### Register:
![register](https://user-images.githubusercontent.com/90003763/157060447-43cee7f4-fbd6-4040-b686-1a17159c1d83.png)

#### Login:
![login](https://user-images.githubusercontent.com/90003763/157060111-f6d42a30-e4ed-4a2d-ba74-5f598cca21fb.png)

#### Supplier Dashboard:
![plot](./images/dashboard.png)

#### Swagger Api:
![swagger](https://user-images.githubusercontent.com/90003763/157058762-dc1f3ce6-6b18-4f15-a8a4-751ccbe31ddb.png)

#### Blog:
![blog](https://user-images.githubusercontent.com/90003763/157055213-d1e18597-a37e-4fc0-b8b8-9dc214b982a3.png)
