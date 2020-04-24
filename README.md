<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">A matching application for Pôle Emploi job offers</h3>

  <p align="center">
    by Romain Avouac and Jaime Costa Centena
    <br />
    <br />
    <br />
    <a href="https://github.com/avouacr/3A-ENSAE-projet-info/issues">Report Bug</a>
    ·
    <a href="https://github.com/avouacr/3A-ENSAE-projet-info/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Installation](#installation)
  * [Start the app](#start-app)
  * [Query the Pole Emploi API](#query-api)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

There are many great README templates available on GitHub, however, I didn't find one that really suit my needs so I created this enhanced one. I want to create a README template so amazing that it'll be the last one you ever need.

Here's why:
* Your time should be focused on creating something amazing. A project that solves a problem and helps others
* You shouldn't be doing the same tasks over and over like creating a README from scratch
* You should element DRY principles to the rest of your life :smile:

Of course, no one template will serve all projects since your needs may be different. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue.

A list of commonly used resources that I find helpful are listed in the acknowledgements.

### Built With
This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [Python](https://python.org)
* [Dask](https://dask.org/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [fastText](https://github.com/facebookresearch/fastText/tree/master/python)
* [cv_generator (allthough with significant alterations)](https://github.com/davidalvarezdlt/)




<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Clone the repo
```sh
git clone https://github.com/avouacr/3A-ENSAE-projet-info.git
```
2. Create a virtual environment inside the project directory
```sh
python -m venv ./venv
```
3. Install required libraries
```sh
pip install -r requirements.txt
```
4. Download input data for the application
```sh
python3 ./download_data.py
```

### Start the app

Once the installation is completed, you can simply start the application
```sh
python3 ./app.py
```

### Query the Pole Emploi API

If you want to update the job offers database, follow these steps.

1. Get  [Pole Emploi API identifier and key](https://www.emploi-store-dev.fr/portail-developpeur-cms/home/catalogue-des-api/documentation-des-api/utiliser-les-api.html)

2. Set them as environment variables (POLE_EMPLOI_API_ID and POLE_EMPLOI_API_KEY)
```sh
python3 ./app.py
```

3. Run... (A COMPLETER)



<!-- CONTRIBUTING -->
## Contributing

Contributions are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Romain Avouac - [avouacr](https://github.com/avouacr) - romain.avouac@ensae.fr

Jaime Costa Centena - [JCCen](https://github.com/JCCen) - jaime.costa.centena@ensae.fr 

Project Link: [https://github.com/avouacr/3A-ENSAE-projet-info](https://github.com/avouacr/3A-ENSAE-projet-info)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Miguel Grinberg's "Flask Mega-Tutorial"](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* [Best README template](https://github.com/othneildrew/Best-README-Template)

