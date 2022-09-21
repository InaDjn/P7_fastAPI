# -*- coding: utf-8 -*-
"""
@author: Ina
"""
from pydantic import BaseModel

# Prototype du best model
# Garder le notebook benchmark (All variables => 89) à présenter
# Créer un notebook avec un modèle prototype pour tester API

# Class which describes HomeCredit measurements

class HomeCredit(BaseModel):
    NAME_CONTRACT_TYPE: str
    CODE_GENDER: str
    FLAG_OWN_CAR: str
    FLAG_OWN_REALTY: str
    CNT_CHILDREN: int
    AMT_INCOME_TOTAL: float
    AMT_CREDIT: float
    NAME_INCOME_TYPE: str
    NAME_EDUCATION_TYPE: str
    DAYS_BIRTH: int
    EXT_SOURCE_2: float
    FLAG_PHONE: int

    class Config:
        orm_mode = True







