## Invitation_code 
### GET

`http://senzapps.cc/api/invitation/code/`

```json
{
    code: {
        code: "RQ1FvL3",
        created: "2016-06-03 11:56:47",
        id: 2516876998,
        is_used: false
    },
    success: true
}
```

## Invitation_code check
### POST
`http://senzapps.cc/api/invitation/check/`
```json
{
    code: "code_string"
}
```

> response
```json
{"success": true}
```
