#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import IntEnum


class UserGender(IntEnum):
    MAN = 1
    WOMAN = 2

    def describe(self):
        return USER_GENDER_DESC.get(self.value, u'')


USER_GENDER_DESC = {
    UserGender.WOMAN: u'女',
    UserGender.MAN: u'男',
}


class UserAffection(IntEnum):
    SINGLE = 1
    SINGLE1 = 2
    IN_LOVE = 3
    MARRIED = 4
    DIVORCED = 5
    LOST_SPOUSE = 6

    def describe(self):
        return USER_AFFECTION_DESC.get(self.value, u'')

USER_AFFECTION_DESC = {
    UserAffection.SINGLE: u'单身并享受单身的状态',
    UserAffection.SINGLE1: u'单身但渴望找到另一半',
    UserAffection.IN_LOVE: u'已有男女朋友，但未婚',
    UserAffection.MARRIED: u'已婚',
    UserAffection.DIVORCED: u'离异，寻觅中',
    UserAffection.LOST_SPOUSE: u'丧偶，寻觅中',
}


class IncomeStatus(IntEnum):
    STATUS1 = 1
    STATUS2 = 2
    STATUS3 = 3
    STATUS4 = 4
    STATUS5 = 5
    STATUS6 = 6

    def describe(self):
        return INCOME_STATUS_DESC.get(self.value, u'')

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

    def describe(self):
        return EDUCATION_STATUS_DESC.get(self.value, u'')

EDUCATION_STATUS_DESC = {
    EducationStatus.STATUS1: u'专科',
    EducationStatus.STATUS2: u'本科',
    EducationStatus.STATUS3: u'硕士',
    EducationStatus.STATUS4: u'博士',
    EducationStatus.STATUS5: u'博士后',
    EducationStatus.STATUS6: u'MBA',
    EducationStatus.STATUS7: u'其他',
}


class DrinkStatus(IntEnum):
    STATUS1 = 1
    STATUS2 = 2
    STATUS3 = 3
    STATUS4 = 4

    def describe(self):
        return DRINK_STATUS_DESC.get(self.value, u'')


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
        return SMOKE_STATUS_DESC.get(self.value, u'')

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
        return RELIGION_DESC.get(self.value, u'')

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
        return CONSTELLATION_DESC.get(self.value, u'')

CONSTELLATION_DESC = {
    ConstellationEnum.Capricorn: u'魔羯座',
    ConstellationEnum.Aquarius: u'水瓶座',
    ConstellationEnum.Pisces: u'双鱼座',
    ConstellationEnum.Aries: u'白羊座',
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
        return AUTH_TYPE_DESC.get(self.value, u'')

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
        return INVITATION_TYPE_DESC.get(self.value, u'')

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


class IndustryTypeEnum(IntEnum):
    TYPE1 = 1
    TYPE2 = 2
    TYPE3 = 3
    TYPE4 = 4
    TYPE5 = 5
    TYPE6 = 6
    TYPE7 = 7
    TYPE8 = 8
    TYPE9 = 9
    TYPE10 = 10
    TYPE11 = 11
    TYPE12 = 12
    TYPE13 = 13
    TYPE14 = 14
    TYPE15 = 15
    TYPE16 = 16
    TYPE17 = 17
    TYPE18 = 18
    TYPE19 = 19
    TYPE20 = 20
    TYPE21 = 21

    def describe(self):
        return INDUSTRY_TYPE_DESC.get(self.value, u'')

INDUSTRY_TYPE_DESC = {
    IndustryTypeEnum.TYPE1: u'互联网/软件',
    IndustryTypeEnum.TYPE2: u'金融',
    IndustryTypeEnum.TYPE3: u'重工制造',
    IndustryTypeEnum.TYPE4: u'法律/会计/咨询',
    IndustryTypeEnum.TYPE5: u'贸易',
    IndustryTypeEnum.TYPE6: u'房产建筑',
    IndustryTypeEnum.TYPE7: u'学生',
    IndustryTypeEnum.TYPE8: u'文化/传媒',
    IndustryTypeEnum.TYPE9: u'电子/硬件',
    IndustryTypeEnum.TYPE10: u'轻工制造',
    IndustryTypeEnum.TYPE11: u'教育科研',
    IndustryTypeEnum.TYPE12: u'零售',
    IndustryTypeEnum.TYPE13: u'能源环保水利',
    IndustryTypeEnum.TYPE14: u'酒店旅游',
    IndustryTypeEnum.TYPE15: u'制药/生物科技',
    IndustryTypeEnum.TYPE16: u'医疗',
    IndustryTypeEnum.TYPE17: u'生活服务',
    IndustryTypeEnum.TYPE18: u'交通运输',
    IndustryTypeEnum.TYPE19: u'电信',
    IndustryTypeEnum.TYPE20: u'政府/社会组织',
    IndustryTypeEnum.TYPE21: u'农林牧渔',
}


class EngagementStatusEnum(IntEnum):
    TYPE1 = 1
    TYPE2 = 2
    TYPE3 = 3
    TYPE4 = 4
    TYPE5 = 5
    TYPE6 = 6
    TYPE7 = 7
    TYPE8 = 8
    TYPE9 = 9
    TYPE10 = 10
    TYPE11 = 11

    def describe(self, role):
        return ENGAGEMENT_STATUS_DESC.get(self.value, {}).get(role, u'')

ENGAGEMENT_STATUS_DESC = {
    EngagementStatusEnum.TYPE1: {
        u'guest_list': u'待对方确认',
        u'guest': u'待对方确认',
        u'host_list': u'接受/拒绝约见',
        u'host': u'待确认',
        u'system': u'待host确认'
    },
    EngagementStatusEnum.TYPE2: {
        u'guest_list': u'已取消',
        u'guest': u'已取消',
        u'host_list': u'对方已取消',
        u'host': u'对方已取消',
        u'system': u'guest已取消'
    },
    EngagementStatusEnum.TYPE3: {
        u'guest_list': u'预约未接受',
        u'guest': u'预约未接受',
        u'host_list': u'已关闭',
        u'host': u'已关闭',
        u'system': u'host已拒绝'
    },
    EngagementStatusEnum.TYPE4: {
        u'guest_list': u'待支付',
        u'guest': u'待支付',
        u'host_list': u'待对方付款',
        u'host': u'待对方付款',
        u'system': u'待guest付款'
    },
    EngagementStatusEnum.TYPE5: {
        u'guest_list': u'待见面',
        u'guest': u'待见面',
        u'host_list': u'待对方付款',
        u'host': u'待对方付款',
        u'system': u'待支付平台确认'
    },
    EngagementStatusEnum.TYPE6: {
        u'guest_list': u'待见面',
        u'guest': u'待双方见面',
        u'host_list': u'待见面',
        u'host': u'待双方见面',
        u'system': u'待双方见面'
    },
    EngagementStatusEnum.TYPE7: {
        u'guest_list': u'待退款',
        u'guest': u'待退款',
        u'host_list': u'对方已取消',
        u'host': u'对方已取消',
        u'system': u'guest约见后取消'
    },
    EngagementStatusEnum.TYPE8: {
        u'guest_list': u'已关闭',
        u'guest': u'已关闭',
        u'host_list': u'对方已取消',
        u'host': u'对方已取消',
        u'system': u'guest取消已退款'
    },
    EngagementStatusEnum.TYPE9: {
        u'guest_list': u'待退款',
        u'guest': u'对方已取消，待退款',
        u'host_list': u'已取消',
        u'host': u'已取消',
        u'system': u'host约见后取消'
    },
    EngagementStatusEnum.TYPE10: {
        u'guest_list': u'已退款',
        u'guest': u'已退款',
        u'host_list': u'已取消',
        u'host': u'已取消',
        u'system': u'host取消已退款'
    },
    EngagementStatusEnum.TYPE11: {
        u'guest_list': u'已完成',
        u'guest': u'已完成',
        u'host_list': u'已完成',
        u'host': u'已完成',
        u'system': u'约见已完成'
    }
}
