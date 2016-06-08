#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms import (
    StringField, FileField,
    DateTimeField, SelectField,
    TextAreaField, IntegerField,
    validators, DateField
)
from wtforms.validators import DataRequired, Optional

from momeet.forms.base import BaseForm
from momeet.views.dashboard.error import ErrorsEnum
from momeet.utils.view import (
    CustomRadioField as RadioField,
    CustomQuerySelectField as QuerySelectField,
    MultiCheckboxField
)
from momeet.constants.user import *
from momeet.constants.city import CITY_DATA
from momeet.models.industry import get_all_industry, get_industry
from momeet.models.user import (
    get_user, User,
    UserProcess,
    UserInfoProcess,
)
from momeet.models.engagement import Engagement
from momeet.utils import safe_int, ClearElement, logger, utf8
from momeet.utils.upload import save_upload_file_to_qiniu, allowed_file

from .fields_name import UserFields


class UserForm(BaseForm):

    avatar = FileField(
        UserFields.AVATAR
    )

    def validate_avatar(self, field):
        data = field.data
        if not data:
            return
        filename = data.filename
        if not allowed_file(filename):
            raise ValueError(ErrorsEnum.IMAGE_ERROR.describe())

    user_name = StringField(
        UserFields.USER_NAME,
        validators=[
            DataRequired(
                message=ErrorsEnum.USER_NAME_REQUIRED.describe()
            ),
        ],
    )

    # def validate_user_name(self, field):
    #     name = field.data.strip().lower()
    #     u = get_user_by_name(name)
    #     if not self._obj and u:
    #         raise ValueError(ErrorsEnum.USER_NAME_EXISTS.describe())
    #     if self._obj and self._obj.user_name != name and u:
    #         raise ValueError(ErrorsEnum.USER_NAME_EXISTS.describe())

    real_name = StringField(
        UserFields.REAL_NAME,
    )

    id_card = StringField(
        UserFields.ID_CARD,
    )

    gender = RadioField(
        UserFields.GENDER,
    )

    birthday = DateTimeField(
        UserFields.BIRTHDAY,
        format='%Y-%m-%d',
        validators=[
            Optional(),
        ]
    )

    height = StringField(
        UserFields.HEIGHT,
    )

    def validate_height(self, field):
        data = field.data
        if not data:
            return
        try:
            int(data)
        except:
            raise ValueError(ErrorsEnum.HEIGHT_ERROR.describe())

    mobile_num = StringField(
        UserFields.MOBILE_NUM,
    )

    weixin_num = StringField(
        UserFields.WEIXIN_NUM,
    )

    location = StringField(
        UserFields.LOCATION,
    )

    def _validate_province_city(self, data):
        province = -1
        city = -1
        try:
            p, c = data.split(',')
            for city_data in CITY_DATA:
                if province >= 0 and city >= 0:
                    break
                if city_data.get('id') != int(p):
                    continue
                province = int(p)
                cities = city_data.get('cities')
                for _city in cities:
                    if _city.get('id') != int(c):
                        continue
                    city = int(c)
        except:
            return False
        else:
            if province >= 0 and city >= 0:
                return True
            else:
                return False

    def validate_localtion(self, field):
        data = field.data
        if not self._validate_province_city(data):
            raise ValueError(ErrorsEnum.LOCATION_ERROR.describe())

    industry = QuerySelectField(
        UserFields.INDUSTRY,
        query_factory=get_all_industry,
        allow_blank=True,
        blank_text=u'-- 请选择 --'
    )

    company_name = StringField(
        UserFields.COMPANY_NAME,
    )

    profession = StringField(
        UserFields.PROFESSION,
    )

    affection = SelectField(
        UserFields.AFFECTION,
    )

    income = SelectField(
        UserFields.INCOME,
    )

    graduated = StringField(
        UserFields.GRADUATED,
    )

    education = SelectField(
        UserFields.EDUCATION,
    )

    hometown = StringField(
        UserFields.HOMETOWN,
    )

    def validate_hometown(self, field):
        data = field.data
        if not self._validate_province_city(data):
            raise ValueError(ErrorsEnum.HOMETOWN_ERROR.describe())

    drink = SelectField(
        UserFields.DRINK,
    )

    smoke = SelectField(
        UserFields.SMOKE,
    )

    constellation = SelectField(
        UserFields.CONSTELLATION,
    )

    religion = SelectField(
        UserFields.RELIGION,
    )

    def init_choices(self):
        self.gender.choices = [
            (str(_.value), _.describe())
            for _ in [UserGender.MAN, UserGender.WOMAN]
        ]
        if self._obj:
            self.gender.default = str(self._obj.gender)
        else:
            self.gender.default = str(UserGender.MAN.value)

        if self._obj:
            self.industry.selected = get_industry(self._obj.industry_id)

        field_dict = {
            'affection': UserAffection,
            'education': EducationStatus,
            'income': IncomeStatus,
            'drink': DrinkStatus,
            'smoke': SmokeStatus,
            'religion': ReligionEnum,
            'constellation': ConstellationEnum
        }

        for f in field_dict:
            field = getattr(self, f)
            _enum = field_dict.get(f)
            _choices = [
                (str(_.value), _.describe())
                for _ in sorted(_enum.__members__.values())
            ]
            _choices.insert(0, ('0', u'请选择'))
            field.choices = _choices
            if self._obj:
                field.default = str(getattr(self._obj, f))
            else:
                field.default = '0'

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.init_choices()

    def save(self):
        if self._obj:
            user = self._obj
        else:
            user = User()
        for k, v in self.data.items():
            if k == 'avatar':
                if v:
                    _avatar = save_upload_file_to_qiniu(v)
                    setattr(user, 'avatar', _avatar)
                continue
            if k == 'height':
                setattr(user, k, safe_int(v))
                continue
            if k == 'industry':
                if v:
                    setattr(user, 'industry_id', v.id)
                continue
            if k == 'user_name':
                setattr(user, 'user_name', v.strip().lower())
                continue
            setattr(user, k, v)
        user.save()
        return user


class UserInfoUpdateForm(BaseForm):
    user_name = StringField(UserFields.USER_NAME)
    real_name = StringField(UserFields.REAL_NAME)
    id_card = StringField(UserFields.ID_CARD)
    gender = IntegerField(UserFields.GENDER)
    birthday = DateField(UserFields.BIRTHDAY)
    height = IntegerField(UserFields.HEIGHT)
    mobile_num = StringField(UserFields.MOBILE_NUM)
    weixin_num = StringField(UserFields.WEIXIN_NUM)
    location = StringField(UserFields.LOCATION)
    industry = IntegerField(UserFields.INDUSTRY)
    company_name = StringField(UserFields.COMPANY_NAME)
    profession = StringField(UserFields.PROFESSION)
    affection = IntegerField(UserFields.AFFECTION)
    income = IntegerField(UserFields.INCOME)
    graduated = StringField(UserFields.GRADUATED)
    education = IntegerField(UserFields.EDUCATION)
    hometown = StringField(UserFields.HOMETOWN)
    drink = IntegerField(UserFields.DRINK)
    smoke = IntegerField(UserFields.SMOKE)
    constellation = IntegerField(UserFields.CONSTELLATION)
    religion = IntegerField(UserFields.RELIGION)

    def init_choices(self):
        field_dict = {}

        for f in field_dict:
            field = getattr(self, f)
            _enum = field_dict.get(f)
            _choices = [(str(_.value), _.describe()) for _ in sorted(_enum.__members__.values())]
            _choices.insert(0, ('0', u'请选择'))
            field.choices = _choices
            field.default = '0'

    def __init__(self, *args, **kwargs):
        super(UserInfoUpdateForm, self).__init__(*args, **kwargs)
        self.init_choices()

    def save(self, uid):
        user = get_user(uid)
        if not user:
            return False
        for k in self.data.keys():
            if self.data.get(k):
                setattr(user, k, self.data.get(k))
        return user.save()


class UserPhotoForm(BaseForm):
    photo = FileField(
        UserFields.PHOTO
    )

    def validate_photo(self, field):
        data = field.data
        if not data:
            return
        filename = data.filename
        if not allowed_file(filename):
            raise ValueError(ErrorsEnum.IMAGE_ERROR.describe())

    def save(self, user_id):
        process = UserInfoProcess(user_id)
        _file = self.photo.data
        _photo = save_upload_file_to_qiniu(_file)
        photos = process.add_photo(_photo)
        return photos


class UserAvatarForm(BaseForm):
    avatar = FileField(UserFields.AVATAR)

    def validate_avatar(self, field):
        if not field.data:
            return
        filename = field.data.filename
        if not allowed_file(filename):
            raise ValueError(ErrorsEnum.IMAGE_ERROR.describe())

    def save(self, openid):
        process = UserProcess(openid)
        _file = self.avatar.data
        _avatar = save_upload_file_to_qiniu(_file)
        return process.update_avatar(_avatar)


class UserDetailForm(BaseForm):
    description = TextAreaField(
        UserFields.DESCRIPTION,
        validators=[],
    )
    detail = TextAreaField(
        UserFields.DETAIL,
        validators=[],
    )

    def save(self):
        info = self._obj
        info.description = self.description.data.strip()
        if self.detail.data:
            clear_obj = ClearElement(self.detail.data)
            content = utf8(clear_obj.clearup_content())
            print
            info.detail = content
        info.save()
        return info


class UserAuthForm(BaseForm):
    auth_type_list = MultiCheckboxField(
        UserFields.AUTH_TYPE
    )

    def __init__(self, *args, **kwargs):
        super(UserAuthForm, self).__init__(*args, **kwargs)
        _choices = [
            (str(_.value), _.describe())
            for _ in sorted(AuthTypeEnum.__members__.values())
        ]
        self.auth_type_list.choices = _choices
        if self._obj and self._obj.auth_info:
            self.auth_type_list.checked_list = [_ for _ in self._obj.auth_info]

    def save(self):
        p = UserInfoProcess(self._obj.user_id)
        p.save_auth_info(self.auth_type_list.data)
        return


class UserEduInfoForm(BaseForm):
    user_id = StringField('', [validators.required()])
    graduated = StringField(UserFields.GRADUATED)
    education = IntegerField(UserFields.EDUCATION)
    major = StringField(UserFields.SPECIALTY)

    _fields = ['edu_id', 'graduated', 'education', 'major']

    def curd(self, method, eid=None):
        process = UserProcess(self.user_id.data)
        d = dict(filter(lambda x: x[0] != 'user_id' and x[1], self.data.items()))
        if method == 'add':
            return process.add_edu_experience(d)
        elif method == 'update':
            return process.update_edu_experience(d, eid=int(eid))
        # elif method == 'delete':
        #     return process.delete_edu_experience(eid=eid)
        else:
            return None


class UserWorkInfoForm(BaseForm):
    user_id = StringField('', [validators.required()])
    industry = IntegerField(UserFields.INDUSTRY)
    company_name = StringField(UserFields.COMPANY_NAME)
    profession = StringField(UserFields.PROFESSION)
    income = IntegerField(UserFields.INCOME)

    def curd(self, method, wid=None):
        process = UserProcess(self.user_id.data)
        d = dict(filter(lambda x: x[0] != 'user_id' and x[1], self.data.items()))
        if method == 'add':
            return process.add_work_experience(d)
        elif method == 'update':
            return process.update_work_experience(d, wid=int(wid))
        # elif method == 'delete':
        #     return process.delete_work_experience(wid=wid)
        else:
            return None


