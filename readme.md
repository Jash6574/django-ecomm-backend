# Django E-Commerce Backend

This is the backend for an e-commerce platform built with Django and Django Rest Framework (DRF), supporting product management, user authentication, cart functionality, checkout with Stripe, and order history tracking. 

## Features

- **User Registration & Login** (JWT authentication)
- **Product Management** (Create, Update, Delete, View)
- **Cart Management** (Add, View, Remove Items)
- **Order Checkout with Stripe Payment**
- **Order History Tracking**
  
## API Endpoints

### Authentication

- `POST /auth/register/` - Register a new user
- `POST /auth/login/` - Login for users, provides JWT token
- `POST /auth/token/` - Obtain JWT token pair
- `POST /auth/token/refresh/` - Refresh the JWT token pair

### Product Management (Admin Only)

- `POST /api/products/add/` - Add a new product to the inventory
- `GET /api/products/all/` - View all products
- `GET /api/products/<int:id>/` - Get details of a specific product
- `PUT /api/products/update/<int:id>/` - Update the details of an existing product
- `DELETE /api/products/delete/<int:id>/` - Delete a product from the catalog

### Cart Management

- `POST /api/cart/add/` - Add a product to the cart
- `GET /api/cart/` - View all items in the cart
- `POST /api/cart/remove/` - Remove an item from the cart

### Order Checkout and History

- `POST /api/order/checkout/` - Place an order and proceed to Stripe checkout
- `GET /api/order/history/` - View all past orders

## Setup Instructions

### Prerequisites
- Python 3.8+  
- Django 3.x
- Django REST Framework
- Stripe API keys (for checkout)
- PostgreSQL or any preferred database

### Installing

1. Clone the repository
    ```bash
    git clone https://github.com/Jash6574/django-ecomm-backend.git
    cd django-ecomm-backend
    ```

2. Create a virtual environment and activate it
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

4. Configure your database and update the `settings.py` file in the Django project with your credentials.
   
5. Create `.env` file for sensitive variables (like Stripe API key, secret keys, etc.). Ensure that your file looks like this:

    ```
    STRIPE_SECRET_KEY=<Your Secret Key>
    DATABASE_URL=postgres://user:password@localhost/dbname
    ```

6. Run migrations
    ```bash
    python manage.py migrate
    ```

7. Create a superuser to access the Django admin panel (optional):
    ```bash
    python manage.py createsuperuser
    ```

8. Run the development server:
    ```bash
    python manage.py runserver
    ```

### Testing the API
You can test the API using Postman or curl by sending requests to the available endpoints.

### Stripe Configuration

For order checkout functionality using Stripe, you'll need to set up Stripe with the following:
1. Create a Stripe account (if you haven’t already) at [Stripe](https://stripe.com/).
2. Get your **Publishable Key** and **Secret Key** from the Stripe dashboard and add it to your `.env` file.

Example:
```
STRIPE_SECRET_KEY=sk_test_1234567890abcdef
STRIPE_PUBLIC_KEY=pk_test_1234567890abcdef
```

## GitHub Repository

You can access the project repository on GitHub at the following link:

[GitHub Repository](https://github.com/Jash6574/django-ecomm-backend.git)

## License

This project is open-source and available under the MIT License.

## Conclusion

This backend provides essential features for an e-commerce application and can be customized further according to specific needs or expanded to a full-fledged e-commerce solution.
