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

[![Product Name Screen Shot][product-screenshot]](https://example.com)

There are many great README templates available on GitHub, however, I didn't find one that really suit my needs so I created this enhanced one. I want to create a README template so amazing that it'll be the last one you ever need.

Here's why:
* Your time should be focused on creating something amazing. A project that solves a problem and helps others
* You shouldn't be doing the same tasks over and over like creating a README from scratch
* You should element DRY principles to the rest of your life :smile:

Of course, no one template will serve all projects since your needs may be different. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue.

A list of commonly used resources that I find helpful are listed in the acknowledgements.

### Built With

* [Python](https://python.org)
* [Dask](https://dask.org/)
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

### Launching the app

Once the installation is complete, you can start the application
```sh
python3 ./app.py
```

### Updating job offers

If you want to update the job offers database, follow these steps.

1. Get  [Pole Emploi API identifier and key](https://www.emploi-store-dev.fr/portail-developpeur-cms/home/catalogue-des-api/documentation-des-api/utiliser-les-api.html)

2. Set them as environment variables (POLE_EMPLOI_API_ID and POLE_EMPLOI_API_KEY)
```sh
python3 ./app.py
```

3. Run... (A COMPLETER)

4. Compute the new FastText representations of the offers 
```sh
python3 doc_embeddings/fasttext_embeddings.py
```


<!-- USAGE -->
## Usage


<!-- CONTRIBUTING -->
## Contributing

All contributions are welcome.

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

