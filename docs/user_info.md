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

## EDU_INFO 教育信息*GET or POST or PUT or DELETE* 
>####GET所有 `/api/user/edu_info`
**response (json)**
```json
{"success": True, "results": [edu_obj_list]}
```

>####GET单个 `/api/user/edu_info/<string:uid>`
```json
{
  "edu_experience": {},
  "success": true
}
```

####POST创建 `/api/user/edu_info`
>**request (form-data)**
```form
"user_id": "openid or user_id" [required]
"graduated": "毕业院校"
"education": "学历"
"major": "专业"
...
```

>**reponse**
```json
{"success": True, "msg": "add edu exprience success"}
```

#### PUT 修改 `/api/user/edu_info/<string:uid>`
>**request (form-data)**
```form
"user_id": "openid or user_id" [required]
"graduated": "毕业院校"
"education": "学历"
"major": "专业"
...
```

>**reponse**
```json
{"success": True, "msg": "update edu exprience success"}
```

#### DELETE 删除 `/api/user/edu_info/<string:uid>`
>**reponse**
```json
{"success": True, "msg": "delete edu exprience success"}
```



## WORK_INFO 工作信息*GET or POST or PUT or DELETE* 
>####GET所有 `/api/user/work_info`
**response (json)**
```json
{"success": True, "results": [work_obj_list]}
```

>####GET单个 `/api/user/work_info/<string:uid>`
```json
{
  "edu_experience": {},
  "success": true
}
```

####POST 创建 `/api/user/work_info`
>**request (form-data)**
```form
"user_id": "openid or user_id" [required]
"company_name": "公司名称"
"profession": "职位"
"income": "年收入"
...
```

>**reponse**
```json
{"success": True, "msg": "add work exprience success"}

#### PUT 修改 `/api/user/work_info/<string:uid>`
>**request (form-data)**
```form
"user_id": "openid or user_id" [required]
"company_name": "公司名称"
"profession": "职位"
"income": "年收入"
...
```

>**reponse**
```json
{"success": True, "msg": "update work exprience success"}
```

#### DELETE 删除 `/api/user/work_info/<string:uid>`
>**reponse**
```json
{"success": True, "msg": "delete work exprience success"}
```


