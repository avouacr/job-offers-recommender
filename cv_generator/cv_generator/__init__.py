import datetime
import json
import logging
import os

import jsonschema
import yaml

from .model import BasicInfo, ContactInfo, ExperienceItem, EducationItem, LanguageItem, CertificationItem
from .theme import BaseTheme


class CV:
    lang = ''
    last_update = None
    basic = BasicInfo()
    contact = ContactInfo()
    experience = []
    education = []
    awards = []
    publications = []
    languages = []
    courses = []
    projects = []
    skills = []
    logger: logging.Logger

    def __init__(self, logger):
        self.logger = logger

    def load(self, cv_file_path, cv_schema_path):
        cv_raw = self._load_raw_data(cv_file_path)
        self._validate_raw_data(cv_raw, cv_schema_path)
        self.lang = cv_raw['lang']
        self.last_update = datetime.datetime.strptime(cv_raw['last_update'], '%Y-%m-%d').date()
        self.basic = self.basic.load(cv_raw['basic'])
        self.contact = self.contact.load(cv_raw['contact']) if 'contact' in cv_raw else None
        self.experience = [
            ExperienceItem().load(experience_item) for experience_item in cv_raw['experience']
        ] if 'experience' in cv_raw else []
        self.education = [
            EducationItem().load(education_item) for education_item in cv_raw['education']
        ] if 'experience' in cv_raw else []
        self.awards = [
            AwardItem().load(awards_item) for awards_item in cv_raw['awards']
        ] if 'awards' in cv_raw else []
        self.publications = [
            PublicationItem().load(publications_item) for publications_item in cv_raw['publications']
        ] if 'publications' in cv_raw else []
        self.languages = [
            LanguageItem().load(languages_item) for languages_item in cv_raw['languages']
        ] if 'languages' in cv_raw else []
        self.certifications = [
            CertificationItem().load(certifications_item) for certifications_item in cv_raw['certifications']
        ] if 'certifications' in cv_raw else []
        self.informatique = [
            CertificationItem().load(certifications_item) for certifications_item in cv_raw['informatique']
        ] if 'certifications' in cv_raw else []
        self.autres = [
            CertificationItem().load(certifications_item) for certifications_item in cv_raw['autres']
        ] if 'autres' in cv_raw else []

        self.courses = [
            CourseItem().load(courses_item) for courses_item in cv_raw['courses']
        ] if 'courses' in cv_raw else []
        self.projects = [
            ProjectItem().load(projects_item) for projects_item in cv_raw['projects']
        ] if 'projects' in cv_raw else []
        self.skills = [
            SkillItem().load(skills_item) for skills_item in cv_raw['skills']
        ] if 'skills' in cv_raw else []
        return self

    def _load_raw_data(self, cv_file_path):
        """Loads the input JSON or YAML file

        Loads the input data inside the `self._cv_file` attribute of the class.

        Args:
            cv_file_path (str): path the the input JSON or YAML file.
        """
        # file_extension = os.path.splitext(os.path.basename(cv_file_path))[1]
        # if file_extension not in ['.json', '.yaml']:
        #     self.logger.error('The extension of the input file is not compatible.')
        #     exit()
        # if not os.path.exists(cv_file_path):
        #     self.logger.error(
        #         'It has not been possible to read the input file. Make sure that you provide a path relative to the '
        #         'execution folder or, if not, provide an absolute path to your JSON or YAML file.'
        #     )
        #     exit()
        dict = {
            "lang": "fr-FR",
            "last_update": "2020-04-11",
            "basic": {
                "name": "Jean",
                "surnames": "Dupont",
                "residence": "Brest",
                "disponibilite_geographique": "Bretagne",
                "biography": "Je désire mettre mon savoir-faire au service de votre boulangerie traditionnelle reconnue pour la qualité de ses produits. J’ai acquis des connaissances techniques, de la préparation du pain depuis le pétrissage de la pâte au défournement, en passant par la fermentation et le façonnage jusqu’à la cuisson. J’ai bénéficié de nombreux conseils professionnels pour maîtriser cet art et je sais organiser mon travail dans les règles d’hygiène les plus strictes. Habile, rigoureux(se) et robuste, je suis prêt(e) à travailler en horaires décalés qui n’ôtent en rien mon sourire et mon amabilité naturelle"
            },
            "contact": {
                "email": "paul_dupont@gmail.com",
                "phone": "(+33) 600 00 00 00"
            },
            "experience": [
                {
                    "institution": "Bon Pain Brest Boulange",
                    "position": "Stagiaire",
                    "date_start": "2019-12-01",
                    "date_end": "2020-05-31",
                    "description": "Préparation du pain, pétrissage, défournement. Gestion d'un boulangerie, comptabilité, RH."
                },

                {
                    "institution": "Universidad Politécnica de Cataluña",
                    "position": "Research Fellow",
                    "date_start": "2018-12-01",
                    "date_end": "2019-05-31",
                    "description": "Obtuve una beca del Gobierno español para realizar una estancia en el departamento de mi elección. Elegí el departamento VEU, dirigido por el Prof. Antonio Bonafonte y enfocado en el desarrollo de tecnologías relacionadas con la voz.\nTrabajé bajo la supervisión del Dr. Santiago Pascual en sistemas de síntesis de voz, publicando el paper \"Problem-agnostic speech embeddings for multi-speaker text-to-speech with SampleRNN\", aceptado como presentación oral en el décimo ISCA Speech Synthesis Workshop."
                }
            ],
            "education": [
                {
                    "institution": "L'Ecole des Pros Brest",
                    "degree": "Certificat d'aptitude professionnelle (CAP)",
                    "major": "Boulangerie",
                    "date_start": "2020-02-01",
                    "date_end": "2020-07-31",
                    "description": "Reconversion boulanger. Les RNN m'ont saoûlé."
                },
                {
                    "institution": "ETH Zürich",
                    "degree": "Estudiante de Intercambio",
                    "major": "Computer Vision Laboratory",
                    "date_start": "2019-02-01",
                    "date_end": "2019-07-31",
                    "description": "Trabajando en video inpainting bajo la supervisión de Sergi Caelles, el Dr. Martin Danelljan, el Prof. Xavier Giró-i-Nieto y el Prof. Luc Van Gool."
                }
            ],
            "languages": [
                {
                    "name": "Français : langue maternelle"
                },
                {
                    "name": "Catalan : B2"
                },
                {
                    "name": "Serbo-croate : night-club level"
                }
            ],
            "certifications": [
                {
                    "name": "Patissier spécialiste"
                },
                {
                    "name": "Permis B"
                }
            ],
            "informatique": [
                {
                    "name": "Microsoft Office"
                },
                {
                    "name": "Logiciels comptabilité"
                }
            ],
            "autres": [
                {
                    "name": "Passionné de pêche"
                }
            ]

        }
        return dict

    def dump(self, cv_file_path):
        cv_raw = CV._dump_cleaner({
            'lang': self.lang,
            'last_update': self.last_update,
            'basic': self.basic.__dict__,
            'contact': self.contact.__dict__,
            'experience': [item.__dict__ for item in self.experience],
            'education': [item.__dict__ for item in self.education],
            'awards': [item.__dict__ for item in self.awards],
            'publications': [item.__dict__ for item in self.publications],
            'languages': [item.__dict__ for item in self.languages],
            'certifications': [item.__dict__ for item in self.certifications],
            'informatique': [item.__dict__ for item in self.informatique],
            'autres': [item.__dict__ for item in self.autres],
            'courses': [item.__dict__ for item in self.courses],
            'projects': [item.__dict__ for item in self.projects],
            'skills': [item.__dict__ for item in self.skills],
        })
        cv_raw_json = json.dumps(cv_raw, indent=2, ensure_ascii=False, default=CV._dump_handler)
        cv_raw_yaml = yaml.dump(json.loads(cv_raw_json), allow_unicode=True, sort_keys=False)
        open(cv_file_path + '.json', 'wt').write(cv_raw_json)
        open(cv_file_path + '.yaml', 'wt').write(cv_raw_yaml)

    def _validate_raw_data(self, cv_raw, cv_schema_path):
        """Validates input CV data using `cv.schema.json`.

        Validates the input CV file using the schema provided in `cv.schema.json`, which follows the JSONSchema
        protocol.

        Args:
            cv_schema_path (str): path to the 'cv.schema.json' schema file
        """
        if not os.path.exists(cv_schema_path):
            self.logger.error(
                'The file cv.schema.json has not been found. Verify that you have not deleted it accidentally.'
            )
            exit()
        jsonschema.validate(cv_raw, json.load(open(cv_schema_path)))

    def get_age(self):
        today = datetime.date.today()
        return today.year - self.basic.birthday.year - (
                (today.month, today.day) < (self.basic.birthday.month, self.basic.birthday.day)
        )

    def get_language_score(self, language_level):
        return {'A1': 40, 'A2': 50, 'B1': 60, 'B2': 70, 'C1': 80, 'C2': 90, 'Native': 100}[language_level]

    def get_skills_categories(self):
        categories_list = []
        for item in self.skills:
            if item.category is not None and item.category not in categories_list:
                categories_list.append(item.category)
        return categories_list

    def filter_skills_by_category(self, category):
        return [item for item in self.skills if (category is None or item.category == category)]

    @staticmethod
    def _dump_cleaner(cv_raw):
        cv_raw_cleaned = {}
        for k, v in cv_raw.items():
            if type(cv_raw[k]) == dict:
                cv_raw_cleaned[k] = CV._dump_cleaner(cv_raw[k])
            if type(cv_raw[k]) == list:
                cv_raw_cleaned[k] = [CV._dump_cleaner(list_item) for list_item in cv_raw[k]]
            elif v is not None and v != -1 and v != '':
                cv_raw_cleaned[k] = v
        return cv_raw_cleaned

    @staticmethod
    def _dump_handler(o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        elif isinstance(o, model.LinkItem):
            return {'anchor': o.anchor, 'href': o.href}
