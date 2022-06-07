import numpy as np
import json


class Words:

    def __init__(self):
        #self._ACTIONS = np.array(['לא', 'איפה', 'שלום', 'אתה', 'מה', 'שמח', 'עומד', 'השעה'])
        self._ACTIONS = np.array(['אתה', 'מה', 'שמח', 'עומד', 'השעה', 'אני', 'איפה', 'השם', 'לא', 'עצוב', 'שלום', 'שלך'])

    def get(self):
        return self._ACTIONS
