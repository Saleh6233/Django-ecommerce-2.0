# Django E-Commerce Project

## Overview

Welcome to the **Django E-Commerce Project**, a fully featured online store built with Django and Python. This application demonstrates a modular, scalable architecture and includes everything you need to get started:

- **Product Catalogue**  
  Browse, filter, and search products by category, price range, and keywords.

- **Shopping Cart & Checkout**  
  Add items to your cart, adjust quantities, and complete secure checkout with payment integration.

- **User Accounts & Profiles**  
  Register, log in, manage your profile and shipping addresses, reset your password, and view order history.

- **Admin Dashboard**  
  Built-in Django admin plus custom dashboards for managing products, orders, users, and site settings.

- **Responsive Design**  
  Mobile-first UI built with modern HTML5, CSS3, and JavaScript—fully responsive across desktop, tablet, and mobile.

- **Extensible Architecture**  
  Fully modular apps (`account`, `cart`, `payment`, `store`) make it easy to add new features or swap out components.

- **Security & Best Practices**  
  Uses Django’s authentication, CSRF protection, and environment-based settings to keep your secrets safe.

Whether you’re learning Django, prototyping an online store, or building a production-ready e-commerce platform, this project provides a solid foundation and clear examples you can extend to meet your needs.

## Setup Instructions

Follow these steps to set up the project on your local machine:

1. **Ensure Python is installed:**  
   Check by running:
   ```sh
   python --version
   ```
   This project requires Python 3.8 or higher.

2. **Navigate to your project folder:**  
   Open a terminal or command prompt and run:
   ```sh
   cd your-django-project
   ```

3. **Create a virtual environment:**  
   ```sh
   python -m venv venv
   ```

4. **Activate the virtual environment:**  
   - *Windows (CMD or PowerShell):*
     ```sh
     venv\Scripts\activate
     ```
   - *macOS/Linux:*
     ```sh
     source venv/bin/activate
     ```

5. **Install required dependencies:**  
   ```sh
   pip install -r requirements.txt
   ```

6. **Apply migrations:**  
   ```sh
   python manage.py migrate
   ```

7. **Create an admin account (optional):**  
   ```sh
   python manage.py createsuperuser
   ```

8. **Start the Django development server:**  
   ```sh
   python manage.py runserver
   ```

9. **Access the application:**  
   Open a browser and go to `http://127.0.0.1:8000/` to check if everything is working.
   
11. **Also you need to give your email and email app password in settings.py for account and profile to be working. Also paypal account needed for integraton builder**

## Features

- **Product Catalogue:** Browse, filter, and search products by category, price range, and keywords.
- **Shopping Cart & Checkout:** Add items to your cart, adjust quantities, and complete secure checkout with payment integration.
- **User Accounts & Profiles:** Register, log in, manage your profile and shipping addresses, reset your password, and view order history.
- **Admin Dashboard:** Built-in Django admin plus custom dashboards for managing products, orders, users, and site settings.
- **Responsive Design:** Mobile-first UI built with modern HTML5, CSS3, and JavaScript—fully responsive across desktop, tablet, and mobile.
- **Extensible Architecture:** Fully modular apps (`account`, `cart`, `payment`, `store`) make it easy to add new features or swap out components.
- **Security & Best Practices:** Uses Django’s authentication, CSRF protection, and environment-based settings to keep your secrets safe.

## Requirements

- Python 3.8 or higher
- Virtual environment (recommended)

