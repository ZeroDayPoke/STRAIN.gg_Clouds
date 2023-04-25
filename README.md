# STRAIN.gg_Clouds

STRAIN.gg_Clouds is a web application for exploring, filtering, and sorting strains of cannabis 
based on parameters like concentration, terpene profiles, effects, and more. Users can also create 
accounts and save their favorite strains.

## Features

- Browse and explore strains of cannabis
- Filter and sort strains based on various parameters
- Create a user account and save favorite strains

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.7 or higher
- Flask 2.0.2 or higher
- npm 6.14.15 or higher

### Installation

1. Clone the repository:
```git clone https://github.com/ZeroDayPoke/STRAIN.gg_Clouds.git```

2. Install dependencies:
```cd STRAIN.gg_Clouds```
```pip3 install -r requirements.txt```

4. Set environment variables:
```export FLASK_APP=app/main.py```
```export FLASK_DEBUG=1```

5. Create mySQL Database:
```cat setup/dev.sql | sudo mysql```

6. Create NGINX Server:
```./setup/nginx```

7. Run the application:
```flask run```


Open your browser and visit `http://127.0.0.1:5000` to access the application.

Note: Frontend libraries like Bootstrap, jQuery, and Popper.js are included in the 'app/static/lib' directory.

## Built With

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - User authentication and authorization
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - Database management
- [Flask-Migrate](https://flask-migrate.readthedocs.io/) - Database migrations
- [MySQL](https://www.mysql.com/) - Database used for the application
- [Bootstrap](https://getbootstrap.com/) - Frontend library for styling
- [jQuery](https://jquery.com/) - JavaScript library for DOM manipulation

## Contributing

We welcome contributions to STRAIN.gg_Clouds! If you would like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bugfix (`git checkout -b feature/my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push the branch to your fork (`git push origin feature/my-new-feature`)
5. Create a new Pull Request

## License

This project is licensed under zugzug License :P

## Authors

- **Chris Stamper** - *Phase 1* - [ZeroDayPoke](https://github.com/ZeroDayPoke)
- **Taylor Woodson** - *Phase 1* - [WoodsonTD](https://github.com/WoodsonTD)
- **Johanna Avila** - *Phase 1* - [jobabyyy](https://github.com/jobabyyy)

See also the list of [contributors] **you could be here!**

## Architecture

```
├── 22-04-2023.tar.gz
├── app
│   ├── __init__.py
│   ├── config.py
│   ├── console.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── engine
│   │   │   ├── __init__.py
│   │   │   └── dbstorage.py
│   │   ├── store.py
│   │   ├── strain.py
│   │   └── user.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── app_routes.py
│   │   └── web_routes.py
│   ├── static
│   │   ├── images
│   │   │   ├── favicon.ico
│   │   │   ├── header.png
│   │   │   ├── logo.ico
│   │   │   ├── strain_images
│   │   │   │   └── gg.png
│   │   │   └── team
│   │   ├── lib
│   │   │   ├── bootstrap.min.css
│   │   │   ├── bootstrap.min.css.map
│   │   │   ├── bootstrap.min.js
│   │   │   ├── bootstrap.min.js.map
│   │   │   ├── bootstrap_two.js
│   │   │   ├── jquery.min.js
│   │   │   ├── popper.min.js
│   │   │   ├── popper.min.js.map
│   │   │   └── popper_two.js
│   │   ├── scripts
│   │   │   ├── stores.js
│   │   │   └── strains.js
│   │   ├── strainggPresentation.pdf
│   │   ├── strainggPresentation.pptx
│   │   └── styles
│   │       └── richard.css
│   ├── templates
│   │   ├── 404.html
│   │   ├── about.html
│   │   ├── account.html
│   │   ├── base.html
│   │   ├── contact.html
│   │   ├── faq.html
│   │   ├── index.html
│   │   ├── presentation.html
│   │   ├── signin.html
│   │   ├── signup.html
│   │   ├── stores.html
│   │   └── strains.html
│   └── utils
│       ├── __init__.py
│       └── helpers.py
├── backup.sql
├── migrations
│   └── inbound.csv
├── raw_research.txt
├── requirements.txt
├── setup
│   ├── backupsql
│   ├── dev.sql
│   ├── nginx
│   └── ufw
├── strain_attributes.py
├── temp
│   ├── README.md
│   ├── index.html
│   ├── package-lock.json
│   └── style.css
└── tests
    ├── __init__.py
    ├── test_app.py
    ├── test_console.py
    ├── test_models
    │   ├── __init__.py
    │   ├── test_base.py
    │   ├── test_engine
    │   │   ├── __init__.py
    │   │   └── test_dbstorage.py
    │   ├── test_strain.py
    │   └── test_user.py
    ├── test_routes
    │   ├── test_app_routes.py
    │   └── test_web_routes.py
    └── test_utils
        └── test_helpers.py

21 directories, 72 files
```
