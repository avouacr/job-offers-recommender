import datetime


class BasicInfo:
    name = None
    surnames = None
    profession = None
    birthday = None
    birthplace = None
    residence = None
    marital_status = None
    biography = None
    hobbies = None
    permis = None
    disponibilite_geographique = None

    def load(self, basic_info_dict):
        self.name = basic_info_dict['name']
        self.surnames = basic_info_dict['surnames']
        self.residence = basic_info_dict['residence'] if 'residence' in basic_info_dict else None
        self.biography = basic_info_dict['biography']
        self.disponibilite_geographique = basic_info_dict[
            'disponibilite_geographique'] if 'disponibilite_geographique' in basic_info_dict else None

        return self


class ContactInfo:
    email = ''
    phone = ''

    def load(self, contact_info_dict):
        self.email = contact_info_dict['email']
        self.phone = contact_info_dict['phone']
        return self


class ExperienceItem:
    institution = ''
    position = ''
    date_start = None
    date_end = None
    description = ''

    def load(self, experience_item_dict):
        self.institution = experience_item_dict['institution']
        self.position = experience_item_dict['position']
        self.date_start = datetime.datetime.strptime(experience_item_dict['date_start'], '%Y-%m-%d').date()
        self.date_end = datetime.datetime.strptime(experience_item_dict['date_end'], '%Y-%m-%d').date() \
            if 'date_end' in experience_item_dict else None
        self.description = experience_item_dict['description'].rstrip() if 'description' in experience_item_dict else ''
        return self


class EducationItem:
    institution = ''
    degree = ''
    major = ''
    date_start = None
    date_end = None
    description = ''
    gpa = -1
    gpa_max = -1
    performance = -1
    promotion_order = ''

    def load(self, education_item_dict):
        self.institution = education_item_dict['institution']
        self.degree = education_item_dict['degree']
        self.major = education_item_dict['major'] if 'major' in education_item_dict else ''
        self.date_start = datetime.datetime.strptime(education_item_dict['date_start'], '%Y-%m-%d').date()
        self.date_end = datetime.datetime.strptime(education_item_dict['date_end'], '%Y-%m-%d').date() \
            if 'date_end' in education_item_dict else None
        self.description = education_item_dict['description'].rstrip() if 'description' in education_item_dict else ''
        self.gpa = education_item_dict['gpa'] if 'gpa' in education_item_dict else -1
        self.gpa_max = education_item_dict['gpa_max'] if 'gpa_max' in education_item_dict else -1
        self.performance = education_item_dict['performance'] if 'performance' in education_item_dict else -1
        self.promotion_order = education_item_dict['promotion_order'] \
            if 'promotion_order' in education_item_dict else ''
        return self



class LanguageItem:
    name = ''

    def load(self, language_item_dict):
        self.name = language_item_dict['name']
        return self

class CertificationItem:
    name = ''

    def load(self, certification_item_dict):
        self.name = certification_item_dict['name']
        return self


class LinkItem:
    anchor = ''
    href = ''

    def load(self, link_item_dict):
        self.anchor = link_item_dict['anchor']
        self.href = link_item_dict['href']
        return self
