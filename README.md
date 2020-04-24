<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">An application to improve job offers recommendation</h3>

  <p align="center">
    by Romain Avouac and Jaime Costa Centena
  <br /><br />
  </p>
</p>

![Application interface](https://raw.githubusercontent.com/avouacr/3A-ENSAE-projet-info/master/images_readme/main.png "Application interface")

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

By default, the app runs with the job offers data from the current (04/24/2020) Pole Emploi database. If you want to update the data with the new job offers, follow these steps :

1. Get  the [Pole Emploi API developper identifier and key](https://www.emploi-store-dev.fr/portail-developpeur-cms/home/catalogue-des-api/documentation-des-api/souscrire-api.html;JSESSIONID_JAHIA=C8EFB919489B2A8430C18600687F35E6)

2. Set them as environment variables (POLE_EMPLOI_API_ID and POLE_EMPLOI_API_KEY).

```sh
export POLE_EMPLOI_API_ID="YOUR POLE EMPLOI API DI"
export POLE_EMPLOI_API_KEY="YOUR POLE EMPLOI API KEY"
```

The above procedure does not store the variables. If you wish to conserve these variables persistently, you might find ressources in the following links for [Linux](https://unix.stackexchange.com/questions/117467/how-to-permanently-set-environmental-variables), [Windows](https://www.computerhope.com/issues/ch000549.htm) and [Mac](https://medium.com/@youngstone89/setting-up-environment-variables-in-mac-os-28e5941c771c).


3. Query Pole Emploi API
```sh
 python3 API_query/api_query.py
```
By default this queries for offers published during the last two years (365x2 days), you can change this through the ```num_days_lookback``` variable in the API_query/api_query.py script.

4. Compute the new FastText representations of the offers 
```sh
python3 doc_embeddings/fasttext_embeddings.py
```


<!-- USAGE -->
## Usage

The interface of the application is voluntarily minimalistic. The first and mandatory step for users is to complete their profile (general information, official certification, education, experiences and self-presentation). Then, they can can either :
- download a professional looking resume filled with all the information they provided ;
- check the job offers that best match their profile.


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

