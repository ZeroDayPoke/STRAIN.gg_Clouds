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
