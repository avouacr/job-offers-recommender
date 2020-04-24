<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">An application to improve job offers recommendation</h3>

  <p align="center">
    by Romain Avouac and Jaime Costa Centena
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
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

![Application interface](https://raw.githubusercontent.com/avouacr/3A-ENSAE-projet-info/master/images_readme/main.png "Application interface")

### Built With

* [Python](https://python.org)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [fastText](https://github.com/facebookresearch/fastText/tree/master/python)
* [cv_generator](https://github.com/davidalvarezdlt/) (allthough with significant modifications)




<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Clone the repo
```sh
git clone https://github.com/avouacr/3A-ENSAE-projet-info.git
```
2. Create a virtual environment inside the cloned directory and activate it
```sh
python3 -m venv ./venv
source venv/bin/activate
```
3. Install required libraries
```sh
pip install -r requirements.txt
```
4. Download input data for the application
```sh
python3 ./download_data.py
```

### Launching the app

Once the installation is complete, you can start the application
```sh
python3 ./app.py
```

### Updating the job offers database

If you want to update the job offers database, follow these steps :

1. Get  [Pole Emploi API identifier and key](https://www.emploi-store-dev.fr/portail-developpeur-cms/home/catalogue-des-api/documentation-des-api/utiliser-les-api.html)

2. Set them as environment variables (POLE_EMPLOI_API_ID and POLE_EMPLOI_API_KEY)
```sh
A COMPLETER
```

3. Query Pole Emploi API
```sh
python3 A COMPLETER
```

4. Compute the new FastText representations of the offers 
```sh
python3 doc_embeddings/fasttext_embeddings.py
```


<!-- USAGE -->
## Usage




<!-- CONTRIBUTING -->
## Contributing

All contributions are welcome. You can either [report a bug](https://github.com/avouacr/3A-ENSAE-projet-info/issues) or contribute directly using the following typical workflow :


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


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Miguel Grinberg's "Flask Mega-Tutorial"](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* [Best README template](https://github.com/othneildrew/Best-README-Template)
* [Template mo](templatemo.com/)

