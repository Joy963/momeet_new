## 邀约活动 
### GET `/api/engagement/list/<string:uid>`
>**response**
```json
{
    results: [
        {
            "created": "2016-06-12 14:32:49",
            "description": "asdfafd",
            "id": 9,
            "is_active": true,
            "user_id": 17,
            "theme": [
                {
                    id: 84,
                    price: 50,
                    theme: "1"
                },
                {
                    id: 85,
                    price: 50,
                    theme: "2"
                },
                {
                    id: 86,
                    price: 50,
                    theme: "8"
                }
            ]
            }
        ],
    success: true
}
```


### POST `/api/engagement/list/<string:uid>`
```json
{
    description: "description...",
    "theme": "1,2,3"
}
```

> response
```json
{"success": true}
```
