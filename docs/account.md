## USER_SIGNIN: *POST* `/api/account/user/signin`
>**request**
```json
{
    "openid": "openid_string"            [required]
    "union_id": "union_id"               [required]
    "nickname": "user_nick_name_string"  [required]
    "head_img_url": "url of head img"    [required]
    
    "province": "beijing"
    "city": "beijing"
    "country": "China"
    "sex": 1
}
``` 
>**reponse**
```json
{
    "success": True or False
}
```

## USER_LOGIN *POST* `/api/account/user/login`
>**request**
```json
{
    "openid": "openid string",
    "access_token": "access_token_string" [optional]
}
```
>**response**
```json
failed:
{
    "success": False
}
success:
{
    "success": False,
    "uid": 2
}
```

## USER_LOGOUT *POST* `/api/account/user/logout`
>**reponse**
```json
{
    "success": True or False
}
```

## USER_CHECK *POST* `/api/account/user/check`
>**request**
```json
{
    "openid": "openid_string"
}
``` 
>**response**
```json
{
    "success": True or False
}
```
