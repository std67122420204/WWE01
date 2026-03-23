
wwe_gender = [
    'Male', 'Female'
]

from WWE.models import Type
types = [Type(name=g) for g in wwe_gender]