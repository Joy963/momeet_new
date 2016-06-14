#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms import *
from wtforms.validators import DataRequired, Optional
from momeet.constants.city import CITY_DATA
from momeet.constants.user import *
from momeet.forms.base import BaseForm
from momeet.models.user import *
from momeet.utils import safe_int
from momeet.utils.upload import save_upload_file_to_qiniu, allowed_file
from momeet.utils.view import (
    CustomRadioField as RadioField,
    MultiCheckboxField
)
from momeet.utils.error import ErrorsEnum
from .fields_name import UserFields


class UserForm(BaseForm):

    avatar = FileField(UserFields.AVATAR)

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

    real_name = StringField(UserFields.REAL_NAME)

    id_card = StringField(UserFields.ID_CARD)

    gender = RadioField(UserFields.GENDER)

    birthday = DateTimeField(
        UserFields.BIRTHDAY,
        format='%Y-%m-%d',
        validators=[
            Optional(),
        ]
    )

    height = StringField(UserFields.HEIGHT)

    def validate_height(self, field):
        data = field.data
        if not data:
            return
        try:
            int(data)
        except:
            raise ValueError(ErrorsEnum.HEIGHT_ERROR.describe())

    mobile_num = StringField(UserFields.MOBILE_NUM)

    weixin_num = StringField(UserFields.WEIXIN_NUM)

    location = StringField(UserFields.LOCATION)

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

    company_name = StringField(UserFields.COMPANY_NAME)

    profession = StringField(UserFields.PROFESSION)

    affection = SelectField(UserFields.AFFECTION)

    industry = SelectField(UserFields.INDUSTRY)
    income = SelectField(UserFields.INCOME)

    graduated = StringField(UserFields.GRADUATED)

    education = SelectField(UserFields.EDUCATION)

    hometown = StringField(UserFields.HOMETOWN)

    def validate_hometown(self, field):
        data = field.data
        if not self._validate_province_city(data):
            raise ValueError(ErrorsEnum.HOMETOWN_ERROR.describe())

    drink = SelectField(UserFields.DRINK)

    smoke = SelectField(UserFields.SMOKE)

    constellation = SelectField(UserFields.CONSTELLATION)

    religion = SelectField(UserFields.RELIGION)

    def init_choices(self):
        self.gender.choices = [(str(_.value), _.describe()) for _ in [UserGender.MAN, UserGender.WOMAN]]
        self.gender.default = str(self._obj.gender) if self._obj else str(UserGender.MAN.value)

        work = self._obj.work.order_by(WorkExperience.id.desc()).first() if self._obj else None
        edu = self._obj.edu.order_by(EduExperience.id.desc()).first() if self._obj else None

        self.company_name.data = work.company_name if work else ""
        self.profession.data = work.profession if work else ""
        self.graduated.data = edu.graduated if edu else ""

        field_dict = {
            'affection': UserAffection,
            'education': EducationStatus,
            'industry': IndustryTypeEnum,
            'income': IncomeStatus,
            'drink': DrinkStatus,
            'smoke': SmokeStatus,
            'religion': ReligionEnum,
            'constellation': ConstellationEnum
        }

        for f in field_dict:
            field = getattr(self, f)
            _enum = field_dict.get(f)
            _choices = [(str(_.value), _.describe()) for _ in sorted(_enum.__members__.values())]
            _choices.insert(0, ('0', u'请选择'))
            field.choices = _choices
            if self._obj:
                if f == 'education':
                    field.default = str(getattr(edu, f)) if edu else '0'
                else:
                    field.default = str(getattr(self._obj, f)) or "0"
            else:
                field.default = '0'

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.init_choices()

    def save(self):
        user = self._obj or User()
        work = user.work.order_by(WorkExperience.id.desc()).first() or WorkExperience()
        edu = user.edu.order_by(EduExperience.id.desc()).first() or EduExperience()
        for k, v in self.data.items():
            if k == 'avatar':
                if v:
                    _avatar = save_upload_file_to_qiniu(v)
                    setattr(user, 'avatar', _avatar)
                continue
            if k == 'height':
                setattr(user, k, safe_int(v))
                continue
            if k == 'user_name':
                setattr(user, 'user_name', v.strip().lower())
                continue
            if k == 'company_name':
                setattr(work, 'company_name', v)
                continue
            if k == 'profession':
                setattr(work, 'profession', v)
                continue
            if k == 'graduated':
                setattr(edu, 'graduated', v)
                continue
            if k == 'education':
                setattr(edu, 'education', safe_int(v))
                continue
            if k == 'major':
                setattr(edu, 'major', v)
                continue
            setattr(user, k, v)
        user.save()
        work.user_id = user.id
        work.save()
        edu.user_id = user.id
        edu.save()
        return user


class UserBaseInfoUpdateForm(BaseForm):
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
    job_label = StringField(UserFields.JOB_LABEL)
    personal_label = StringField(UserFields.PERSONAL_LABEL)

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
        super(UserBaseInfoUpdateForm, self).__init__(*args, **kwargs)
        self.init_choices()

    def save(self, uid):
        user = get_user(uid)
        if not user:
            return False
        for k in self.data.keys():
            if self.data.get(k):
                if k == 'job_label':
                    for v in self.data.get(k).split(','):
                        job_label = get_job_label_or_create(name=v, user_id=uid)
                        job_label.save()
                elif k == 'personal_label':
                    for v in self.data.get(k).split(','):
                        personal_label = get_personal_label_or_create(name=v, user_id=uid)
                        personal_label.save()
                else:
                    setattr(user, k, self.data.get(k))
        return user.save()


class UserPhotoForm(BaseForm):
    photo = FileField(UserFields.PHOTO)

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
        print self.photo.data
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


class UserCoverPhotoForm(BaseForm):
    photo = FileField(UserFields.COVER_PHOTO)

    def validate_avatar(self, field):
        if not field.data:
            return
        filename = field.data.filename
        if not allowed_file(filename):
            raise ValueError(ErrorsEnum.IMAGE_ERROR.describe())

    def save(self, uid):
        process = UserInfoProcess(uid)
        _file = self.photo.data
        if not self.photo.data:
            return None
        _avatar = save_upload_file_to_qiniu(_file)
        return process.update_cover_photo(_avatar)


class UserDetailForm(BaseForm):
    title = StringField(UserFields.DETAIL_TYPE)
    content = TextAreaField(UserFields.DETAIL_CONTENT)
    photo = FileField(UserFields.DETAIL_PHOTO, render_kw={'multiple': True})

    def save(self, files):
        info = self._obj
        user_detail = UserDetail(user_info_id=info.user_id)
        user_detail.title = self.title.data
        user_detail.content = self.content.data
        photo = []
        for f in files.getlist('photo'):
            _photo = save_upload_file_to_qiniu(f)
            photo.append(_photo)
        user_detail.photo = ','.join(photo)
        return user_detail.save()

    def update(self, detail_id, files=None):
        user_detail = UserDetail.query.get(detail_id)
        if not user_detail:
            return None
        d = dict(filter(lambda x: x[0] != 'photo' and x[1], self.data.items()))
        for k, v in d.items():
            setattr(user_detail, k, v) if v else None

        if files:
            photo = []
            for f in files:
                _photo = save_upload_file_to_qiniu(f)
                photo.append(_photo)
            user_detail.photo = ','.join(photo)
        return user_detail.save()


class UserDescriptionForm(BaseForm):
    description = TextAreaField(UserFields.DESCRIPTION, validators=[])

    def save(self):
        info = self._obj
        info.description = self.description.data.strip()
        return info.save()


class UserAuthForm(BaseForm):
    auth_type_list = MultiCheckboxField(UserFields.AUTH_TYPE)

    def __init__(self, *args, **kwargs):
        super(UserAuthForm, self).__init__(*args, **kwargs)
        _choices = [
            (str(_.value), _.describe())
            for _ in sorted(AuthTypeEnum.__members__.values())
        ]
        self.auth_type_list.choices = _choices
        if self._obj and self._obj.auth_info:
            self.auth_type_list.checked_list = [int(_) for _ in self._obj.auth_info]

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
        else:
            return None


class UserWorkInfoForm(BaseForm):
    user_id = StringField('', [validators.required()])
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


class UserSystemInfoForm(BaseForm):
    device_token = StringField('设备token')
    app_version = StringField('app 版本')
    mobile_model = StringField('手机型号')
    os_version = StringField('os 版本')
    system_language = StringField('系统语言')

    def save(self, uid):
        user = get_user(uid)
        if not user:
            return False
        for k, v in self.data.items():
            if v:
                setattr(user, k, v)
        return user.save()


class UserSearchForm(BaseForm):
    text = StringField(u'用户搜索', [validators.required()])


class UserJobLabelForm(BaseForm):
    text = StringField(u'工作标签', [validators.required()])

    def save(self):
        job_label = get_job_label_or_create(name=self.text.data)
        return job_label.save()


class UserPersonalLabelForm(BaseForm):
    text = StringField(u'个人标签', [validators.required()])

    def save(self):
        personal_label = get_personal_label_or_create(name=self.text.data)
        return personal_label.save()
