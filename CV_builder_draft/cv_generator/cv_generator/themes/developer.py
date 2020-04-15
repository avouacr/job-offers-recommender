import pylatex
from pylatex import Command
import random
import cv_generator


class ThemeDeveloper(cv_generator.BaseTheme):
    class BarChart(pylatex.base_classes.Environment):
        _latex_name = 'barchart'

    class EntryList(pylatex.base_classes.Environment):
        _latex_name = 'entrylist'

    def __init__(self, cv, logger):
        super(ThemeDeveloper, self).__init__('developer', cv, logger)

    def format(self):
        self.set_lang()
        self._format_header()
        self._format_experience()
        self._format_education()
        self._format_languages()
        # self._format_languages()
        self._format_certifications()
        self._format_informatique()
        return self.doc

    def _format_header(self):

        with self.doc.create(pylatex.MiniPage(width='0.60\\textwidth', pos='c')):
            self.doc.append(Command('headername', self.cv.basic.name + ' ' + self.cv.basic.surnames))
            self.doc.append(pylatex.NewLine())
            self.doc.append(Command('cvsect', _('DEVELOPER_BIOGRAPHY_TITLE')))
            self.doc.append(self.cv.basic.biography)
            # self._format_skills()
        self.doc.append(pylatex.HFill())
        with self.doc.create(pylatex.MiniPage(width='0.25\\textwidth', pos='c')):
            self.doc.append(pylatex.NoEscape('\\textbf{{{}}} : {}'.format("Mobilité", self.cv.basic.disponibilite_geographique)))
            self.doc.append(pylatex.NewLine())
            self.doc.append(Command('icon', ['MapMarker', 12, str(self.cv.basic.residence)]))
            self.doc.append(pylatex.NewLine())
            self.doc.append(Command('icon', ['Phone', 12, self.cv.contact.phone]))
            self.doc.append(pylatex.NewLine())
            self.doc.append(Command('icon', ['At', 12, self.cv.contact.email]))


    def _format_experience(self):
        if self.cv.experience and len(self.cv.experience) > 0:
            self.doc.append(Command('cvsect', _('DEVELOPER_EXPERIENCE_TITLE')))
            entry_list = self.EntryList()
            for experience_item in self.cv.experience:
                experience_item_date_start = experience_item.date_start.strftime('%m/%Y')
                experience_item_date_end = experience_item.date_end.strftime('%m/%Y') \
                    if experience_item.date_end is not None else _('DEVELOPER_DATES_NOW')
                experience_period = '{} - {}'.format(experience_item_date_start, experience_item_date_end)
                experience_item_args = [experience_period, experience_item.position,
                                        experience_item.institution, experience_item.description]
                entry_list.append(Command('entry', experience_item_args))
            self.doc.append(entry_list)

    def _format_education(self):
        if self.cv.education and len(self.cv.education) > 0:
            self.doc.append(Command('cvsect', _('DEVELOPER_EDUCATION_TITLE')))
            entry_list = self.EntryList()
            for education_item in self.cv.education:
                education_item_date_start = education_item.date_start.strftime('%m/%Y')
                education_item_date_end = education_item.date_end.strftime('%m/%Y') \
                    if education_item.date_end is not None else _('DEVELOPER_DATES_NOW')
                education_period = '{} - {}'.format(education_item_date_start, education_item_date_end)
                education_item_args = [
                    education_period, education_item.degree, education_item.institution, education_item.description
                ]
                entry_list.append(Command('entry', education_item_args))

            self.doc.append(entry_list)



    def _format_languages(self):
        with self.doc.create(pylatex.MiniPage(width='0.33\\textwidth', pos='t')):
            self.doc.append(Command('cvsect', _('DEVELOPER_LANGUAGES_TITLE')))
            self.doc.append(pylatex.NewLine())
            for language_item in self.cv.languages:
                self.doc.append(pylatex.NoEscape('\\textbf{{{}}} - {}'.format(language_item.name, language_item.level)))
                self.doc.append(pylatex.NewLine())

    def _format_certifications(self):
        with self.doc.create(pylatex.MiniPage(width='0.33\\textwidth', pos='t')):
            self.doc.append(Command('cvsect', _('CERTIFICATIONS'))) # en realité PO et MO inutiles ??
            self.doc.append(pylatex.NewLine())
            for certification_item in self.cv.certifications:
                self.doc.append(
                    pylatex.NoEscape('\\textbf{{{}}}'.format(certification_item.name)))
                self.doc.append(pylatex.NewLine())


    def _format_informatique(self):
        with self.doc.create(pylatex.MiniPage(width='0.33\\textwidth', pos='t')):
            self.doc.append(Command('cvsect', _('INFORMATIQUE'))) # en realité PO et MO inutiles ??
            self.doc.append(pylatex.NewLine())
            for certification_item in self.cv.informatique:
                self.doc.append(
                    pylatex.NoEscape('\\textbf{{{}}}'.format(certification_item.name)))
                self.doc.append(pylatex.NewLine())

