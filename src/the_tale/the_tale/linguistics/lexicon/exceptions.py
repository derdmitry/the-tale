# coding: utf-8

from the_tale.linguistics import exceptions


class LexiconError(exceptions.LinguisticsError):
    MSG = None


class NoFreeVerificatorSubstitutionError(exceptions.LinguisticsError):
    MSG = 'No free verificator substitution for key %(key)s and variable %(variable)s'

class WrongFormNumberError(exceptions.LinguisticsError):
    MSG = 'Wrong forms number'
