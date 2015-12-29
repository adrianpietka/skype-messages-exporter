# Skype Messages Exporter

Export messages from Skype channels to a remote web service.

Tested on Python 3.5

## Configuration

Example of config.json file:

```json
{
    "api_url": "http://localhost:5757",
    "messages_limit": 50,
    "cycle_time": 5,
    "skype_database_original": "C:\\Users\\{system.username}\\AppData\\Roaming\\Skype\\{skype.login}\\main.db",
    "channels": {
        "1438": 1
    }
}
```

"channels" key is a definition:

```
"channels": {
    "channel-id-1": last-message-id (integer, default should be equal 0),
    "channel-id-2": 0,
    "channel-id-3": 0,
    (...)
}
```

Then script send only new messages from chats defined in "channels" object.

## Running

```bash
$: python -u skype-exporter.py config.json
```

## Web service

Script send data to webservice as payloaded JSON.

### Example payload

```json
[
  {
    "author": "user.name.1",
    "id": 17196,
    "content": "<a href=\"https://www.facebook.com/ODN/videos/904190422960927/\">https://www.facebook.com/ODN/videos/904190422960927/</a>\r\n<ss type=\"surprised\">:O</ss>",
    "conversation": {
        "id": "1438",
        "name": "My SPAM Chat"
    },
    "date": 1431593629
  },
  {
    "author": "user.name.2",
    "id": 17200,
    "content": "<a href=\"http://devopsreactions.tumblr.com/post/118933329057/bash-ls-command-not-found\">http://devopsreactions.tumblr.com/post/118933329057/bash-ls-command-not-found</a>",
    "conversation": {
        "id": "1438",
        "name": "My SPAM Chat"
    },
    "date": 1431594202
  },
  {
    "author": "user.name.3",
    "id": 17207,
    "content": "Haha, very nice!",
    "conversation": {
        "id": "1438",
        "name": "My SPAM Chat"
    },
    "date": 1431594386
  }
]
```

### Example of receiver

*receive.php*:

```php
$payload = file_get_contents('php://input');
file_put_contents('temp/payload-' . time() . '.json', $payload);
```

```bash
$: php -S localhost:5757 receive.php
```