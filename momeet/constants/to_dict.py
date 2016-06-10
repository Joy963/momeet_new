#!/usr/bin/env python
# coding=utf-8

from user import *

# l = [AUTH_TYPE_DESC,
#      CONSTELLATION_DESC,
#      DRINK_STATUS_DESC,
#      EDUCATION_STATUS_DESC,
#      INCOME_STATUS_DESC,
#      INDUSTRY_TYPE_DESC,
#      RELIGION_DESC,
#      SMOKE_STATUS_DESC,
#      USER_AFFECTION_DESC,
#      USER_GENDER_DESC]


# r = map(lambda x: dict([(v, k.value) for k, v in x.items()]), l)
# print (r)


result = {}

gender = dict([(v, k.value) for k, v in USER_GENDER_DESC.items()])
result['gender'] = gender

affection = dict([(v, k.value) for k, v in USER_AFFECTION_DESC.items()])
result['affection'] = affection

income = dict([(v, k.value) for k, v in INCOME_STATUS_DESC.items()])
result['income'] = income

education = dict([(v, k.value) for k, v in EDUCATION_STATUS_DESC.items()])
result['education'] = education

drink = dict([(v, k.value) for k, v in DRINK_STATUS_DESC.items()])
result['drink'] = drink

smoke = dict([(v, k.value) for k, v in SMOKE_STATUS_DESC.items()])
result['smoke'] = smoke

religion = dict([(v, k.value) for k, v in RELIGION_DESC.items()])
result['religion'] = religion

constellation = dict([(v, k.value) for k, v in CONSTELLATION_DESC.items()])
result['constellation'] = constellation

auth_type = dict([(v, k.value) for k, v in AUTH_TYPE_DESC.items()])
result['auth_type'] = auth_type

invitation = dict([(v, k.value) for k, v in INVITATION_TYPE_DESC.items()])
result['invitation'] = invitation

industry = dict([(v, k.value) for k, v in INDUSTRY_TYPE_DESC.items()])
result['industry'] = industry

if __name__ == '__main__':
    print(result)
