import cv_generator.cv_generator
import pylatex
from pylatex import Command


class ThemeDeveloper(cv_generator.cv_generator.BaseTheme):
    class BarChart(pylatex.base_classes.Environment):
        _latex_name = 'barchart'

    class EntryList(pylatex.base_classes.Environment):
        _latex_name = 'entrylist'

    def __init__(self, cv, logger):
        super(ThemeDeveloper, self).__init__('developer', cv, logger)

    def format(self):
        self.set_lang()
        self.format_header()
        self.format_experience()
        self.format_education()
        self.format_languages()
        # self.format_languages()
        self.format_certifications()
        self.format_informatique()
        return self.doc

    def format_header(self):
        if len(self.cv.basic.name) + len(self.cv.basic.surnames) > 0:
            with self.doc.create(pylatex.MiniPage(width='0.7\\textwidth', pos='c')):
                self.doc.append(Command('alternativeheadername', self.cv.basic.name + ' ' + self.cv.basic.surnames))

            # self.format_skills()
        self.doc.append(pylatex.HFill())
        with self.doc.create(pylatex.MiniPage(width='0.3\\textwidth', pos='c')):
            # self.doc.append(Command('mobi', self.cv.basic.disponibilite_geographique))
            # self.doc.append(pylatex.NewLine())
            if len(self.cv.contact.email) > 0:
                self.doc.append(Command('icon', ['At', 12, self.cv.contact.email]))
            if len(self.cv.contact.phone) > 0:
                self.doc.append(pylatex.NewLine())
                self.doc.append(Command('icon', ['Phone', 12, self.cv.contact.phone]))
            if len(self.cv.basic.residence) > 0:
                self.doc.append(pylatex.NewLine())
                self.doc.append(Command('icon', ['MapMarker', 12, str(self.cv.basic.residence)]))
            if len(self.cv.basic.disponibilite_geographique) > 0:
                self.doc.append(pylatex.NewLine())
                self.doc.append(Command('mobi', ["Mobilité", self.cv.basic.disponibilite_geographique]))

        if len(self.cv.basic.biography) > 0:
            self.doc.append(pylatex.NewLine())
            self.doc.append(Command('cvsect', ('Présentation')))
            self.doc.append(self.cv.basic.biography)

    def format_experience(self):
        if self.cv.experience and len(self.cv.experience) > 0:
            self.doc.append(pylatex.NewLine())
            self.doc.append(Command('cvsect', ('Expériences professionnelles')))
            entry_list = self.EntryList()
            for experience_item in self.cv.experience:
                experience_item_date_start = experience_item.date_start.strftime('%m/%Y')
                experience_item_date_end = experience_item.date_end.strftime('%m/%Y') \
                    if experience_item.date_end is not None else ('en cours')
                experience_period = '{} - {}'.format(experience_item_date_start, experience_item_date_end)
                experience_item_args = [experience_period, experience_item.position,
                                        experience_item.institution, experience_item.description]
                entry_list.append(Command('entry', experience_item_args))
            self.doc.append(entry_list)

    def format_education(self):
        if self.cv.education and len(self.cv.education) > 0:
            self.doc.append(Command('cvsect', ('Formation')))
            entry_list = self.EntryList()
            for education_item in self.cv.education:
                education_item_date_start = education_item.date_start.strftime('%m/%Y')
                education_item_date_end = education_item.date_end.strftime('%m/%Y') \
                    if education_item.date_end is not None else ('en cours')
                education_period = '{} - {}'.format(education_item_date_start, education_item_date_end)
                education_item_args = [
                    education_period, education_item.degree, education_item.institution, education_item.description
                ]
                entry_list.append(Command('entry', education_item_args))

            self.doc.append(entry_list)

    def format_languages(self):

        if len(self.cv.languages) > 0:
            self.vertical_division_coefficient = 0.95 / (
                    (len(self.cv.languages) > 0) + (len(self.cv.certifications) > 0) + (
                    len(self.cv.informatique) > 0))
            with self.doc.create(
                    pylatex.MiniPage(width='{}\\textwidth'.format(self.vertical_division_coefficient), pos='t')):
                self.doc.append(Command('cvsect', ('Langues')))
                self.doc.append(pylatex.NewLine())
                for certification_item in self.cv.languages:
                    self.doc.append(
                        pylatex.NoEscape('\\textbf{{{}}}'.format(certification_item.name)))
                    self.doc.append(pylatex.NewLine())

    def format_certifications(self):

        if len(self.cv.certifications) > 0:
            self.vertical_division_coefficient = 0.95 / (
                    (len(self.cv.languages) > 0) + (len(self.cv.certifications) > 0) + (
                    len(self.cv.informatique) > 0))
            with self.doc.create(
                    pylatex.MiniPage(width='{}\\textwidth'.format(self.vertical_division_coefficient), pos='t')):
                self.doc.append(Command('cvsect', ('Cerfications')))  # en realité PO et MO inutiles ??
                self.doc.append(pylatex.NewLine())
                for certification_item in self.cv.certifications:
                    self.doc.append(
                        pylatex.NoEscape('\\textbf{{{}}}'.format(certification_item.name)))
                    self.doc.append(pylatex.NewLine())

    def format_informatique(self):
        if len(self.cv.informatique) > 0:
            self.vertical_division_coefficient = 0.95 / (
                    (len(self.cv.languages) > 0) + (len(self.cv.certifications) > 0) + (
                    len(self.cv.informatique) > 0))

            with self.doc.create(
                    pylatex.MiniPage(width='{}\\textwidth'.format(self.vertical_division_coefficient), pos='t')):
                self.doc.append(Command('cvsect', ('Informatique')))  # en realité PO et MO inutiles ??
                self.doc.append(pylatex.NewLine())
                for certification_item in self.cv.informatique:
                    self.doc.append(
                        pylatex.NoEscape('\\textbf{{{}}}'.format(certification_item.name)))
                    self.doc.append(pylatex.NewLine())
