#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import IntEnum


class UserGender(IntEnum):
    WOMAN = 0
    MAN = 1
    UNKNOWN = -1

    def describe(self):
        return USER_GENDER_DESC.get(self.value, '')


USER_GENDER_DESC = {
    UserGender.WOMAN.value: u'女',
    UserGender.MAN.value: u'男',
    UserGender.UNKNOWN.value: u'未知',
}


class UserAffection(IntEnum):
    SINGLE = 1
    SINGLE1 = 2
    IN_LOVE = 3
    MARRIED = 4
    DIVORCED = 5
    LOST_SPOUSE = 6

    def describe(self):
        return USER_AFFECTION_DESC.get(self.value, '')

USER_AFFECTION_DESC = {
    UserAffection.SINGLE.value: u'单身并享受单身的状态',
    UserAffection.SINGLE1.value: u'单身但渴望找到另一半',
    UserAffection.IN_LOVE.value: u'已有男女朋友，但未婚',
    UserAffection.MARRIED.value: u'已婚',
    UserAffection.DIVORCED.value: u'离异，寻觅中',
    UserAffection.LOST_SPOUSE.value: u'丧偶，寻觅中',
}


class IncomeStatus(IntEnum):
    STATUS1 = 1
    STATUS2 = 2
    STATUS3 = 3
    STATUS4 = 4
    STATUS5 = 5
    STATUS6 = 6

    def describe(self):
        return INCOME_STATUS_DESC.get(self.value, '')

INCOME_STATUS_DESC = {
    IncomeStatus.STATUS1: u'10W以下',
    IncomeStatus.STATUS2: u'10W~20W',
    IncomeStatus.STATUS3: u'20W~30W',
    IncomeStatus.STATUS4: u'30W~50W',
    IncomeStatus.STATUS5: u'50W~100W',
    IncomeStatus.STATUS6: u'100W以上',
}


class EducationStatus(IntEnum):
    STATUS1 = 1
    STATUS2 = 2
    STATUS3 = 3
    STATUS4 = 4
    STATUS5 = 5
    STATUS6 = 6
    STATUS7 = 7
    STATUS8 = 8
    STATUS9 = 9

    def describe(self):
        return EDUCATION_STATUS_DESC.get(self.value, '')

EDUCATION_STATUS_DESC = {
    EducationStatus.STATUS1: u'高中',
    EducationStatus.STATUS2: u'技校',
    EducationStatus.STATUS3: u'中专',
    EducationStatus.STATUS4: u'大专',
    EducationStatus.STATUS5: u'大学本科',
    EducationStatus.STATUS6: u'硕士研究生',
    EducationStatus.STATUS7: u'博士研究生',
    EducationStatus.STATUS8: u'博士以上',
    EducationStatus.STATUS9: u'其他',
}


class DrinkStatus(IntEnum):
    STATUS1 = 1
    STATUS2 = 2
    STATUS3 = 3
    STATUS4 = 4

    def describe(self):
        return DRINK_STATUS_DESC.get(self.value, '')


DRINK_STATUS_DESC = {
    DrinkStatus.STATUS1: u'从不',
    DrinkStatus.STATUS2: u'社交时偶尔',
    DrinkStatus.STATUS3: u'兴致时小酌',
    DrinkStatus.STATUS4: u'比较频繁',
}


class SmokeStatus(IntEnum):
    STATUS1 = 1
    STATUS2 = 2
    STATUS3 = 3
    STATUS4 = 4

    def describe(self):
        return SMOKE_STATUS_DESC.get(self.value, '')

SMOKE_STATUS_DESC = {
    SmokeStatus.STATUS1: u'从不，比较反感',
    SmokeStatus.STATUS2: u'不吸烟，但能接受',
    SmokeStatus.STATUS3: u'社交时偶尔',
    SmokeStatus.STATUS4: u'比较频繁',
}


class ReligionEnum(IntEnum):
    NONE = 1
    BUDDHISM = 2
    CHRISTIANISM = 3
    CATHOLICISM = 4
    TAOISM = 5
    ISLAM = 6
    OTHER = 7

    def describe(self):
        return RELIGION_DESC.get(self.value, '')

RELIGION_DESC = {
    ReligionEnum.NONE: u'无宗教信仰',
    ReligionEnum.BUDDHISM: u'佛教',
    ReligionEnum.CHRISTIANISM: u'基督教',
    ReligionEnum.CATHOLICISM: u'天主教',
    ReligionEnum.TAOISM: u'道教',
    ReligionEnum.ISLAM: u'伊斯兰教',
    ReligionEnum.OTHER: u'其他',
}


class ConstellationEnum(IntEnum):
    Capricorn = 1
    Aquarius = 2
    Pisces = 3
    Aries = 4
    Taurus = 5
    Gemini = 6
    Cancer = 7
    Leo = 8
    Virgo = 9
    Libra = 10
    Scorpio = 11
    Sagittarius = 12

    def describe(self):
        return CONSTELLATION_DESC.get(self.value, '')

CONSTELLATION_DESC = {
    ConstellationEnum.Capricorn: u'魔羯座',
    ConstellationEnum.Aquarius: u'水瓶座',
    ConstellationEnum.Pisces: u'双鱼座',
    ConstellationEnum.Aries: u'牡羊座',
    ConstellationEnum.Taurus: u'金牛座',
    ConstellationEnum.Gemini: u'双子座',
    ConstellationEnum.Cancer: u'巨蟹座',
    ConstellationEnum.Leo: u'狮子座',
    ConstellationEnum.Virgo: u'处女座',
    ConstellationEnum.Libra: u'天秤座',
    ConstellationEnum.Scorpio: u' 天蝎座',
    ConstellationEnum.Sagittarius: u' 射手座',
}


class AuthTypeEnum(IntEnum):
    TYPE1 = 1
    TYPE2 = 2
    TYPE3 = 3

    def describe(self):
        return AUTH_TYPE_DESC.get(self.value, '')

AUTH_TYPE_DESC = {
    AuthTypeEnum.TYPE1: u'职业身份认证',
    AuthTypeEnum.TYPE2: u'实名认证',
    AuthTypeEnum.TYPE3: u'电话认证',
}


class InvitationTypeEnum(IntEnum):
    TYPE1 = 1
    TYPE2 = 2
    TYPE3 = 3
    TYPE4 = 4
    TYPE5 = 5
    TYPE6 = 6
    TYPE7 = 7
    TYPE8 = 8
    TYPE9 = 9

    def describe(self):
        return INVITATION_TYPE_DESC.get(self.value, '')

INVITATION_TYPE_DESC = {
    InvitationTypeEnum.TYPE1: u'吃饭、聚餐',
    InvitationTypeEnum.TYPE2: u'喝咖啡',
    InvitationTypeEnum.TYPE3: u'运动、健身',
    InvitationTypeEnum.TYPE4: u'周边游、旅行',
    InvitationTypeEnum.TYPE5: u'K歌',
    InvitationTypeEnum.TYPE6: u'逛街',
    InvitationTypeEnum.TYPE7: u'看电影',
    InvitationTypeEnum.TYPE8: u'演唱会、话剧、展览等演出',
    InvitationTypeEnum.TYPE9: u'其他',
}
