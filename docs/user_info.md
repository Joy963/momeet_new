## BASE_INFO *GET or POST* `/api/user/base_info/<string:uid>`
####GET
>**response**
```json
{
    "age": 0,
    "avatar": "avatar url",
    "gender": 1,
    "id": 2516877003,
    "user_name": " $$name##"
}
```

####POST
>**request (form-data to change)**
```form
"key1": "value1"
"key2": "value2"
...
```

>**reponse**
```json
{
    "success": True or False
}
```

## USR_AVATAR *POST* `/api/user/avatar/<string:uid>`
>**request (form-data of file)**
```form
"avatar": "some file"
```

>**reponse**
```json
{"success": True, "avatar": avatar_uri}
```
or
```json
{"success": False, "msg": "failed update avatar!"}
```

## EDU_INFO *GET or POST* `/api/user/edu_info/<string:uid>`
####GET 获取教育信息
>**response (json)**
```json
{"success": True, "results": [edu_obj_list]}
```

####POST 创建教育信息
>**request (form-data)**
```form
"graduated": "毕业院校"
"education": "学历"
"major": "专业"
...
```

>**reponse**
```json
{"success": True, "msg": "add edu exprience success"}
```

## WORK_INFO *GET or POST* `/api/user/work_info/<string:uid>`
####GET 获取教育信息
>**response (json)**
```json
{"success": True, "results": [workinfo_obj_list]}
```

####POST 创建教育信息
>**request (form-data)**
```form
"company_name": "公司名称"
"profession": "职位"
"income": "年收入"
...
```

>**reponse**
```json
{"success": True, "msg": "add work exprience success"}
