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
    "skype_database_orginal": "C:\\Users\\{system.username}\\AppData\\Roaming\\Skype\\{skype.login}\\main.db",
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
$: python skype-exporter.py config.json
```

## Web service

Script send data to webservice as payloaded JSON.

### Example payload

```json
[
  {
    "Author": "user.name.1",
    "Id": 17196,
    "Content": "<a href=\"https://www.facebook.com/ODN/videos/904190422960927/\">https://www.facebook.com/ODN/videos/904190422960927/</a>\r\n<ss type=\"surprised\">:O</ss>",
    "ConversationName": "My SPAM Chat",
    "Date": 1431593629,
    "ConversationId": 1438
  },
  {
    "Author": "user.name.2",
    "Id": 17200,
    "Content": "<a href=\"http://devopsreactions.tumblr.com/post/118933329057/bash-ls-command-not-found\">http://devopsreactions.tumblr.com/post/118933329057/bash-ls-command-not-found</a>",
    "ConversationName": "My SPAM Chat",
    "Date": 1431594202,
    "ConversationId": 1438
  },
  {
    "Author": "user.name.3",
    "Id": 17207,
    "Content": "Haha, very nice!",
    "ConversationName": "My SPAM Chat",
    "Date": 1431594386,
    "ConversationId": 1438
  }
]
```

### Example of receiver

*receive.php*:

```php
$payload = file_get_contents('php://input');
file_put_contents('payload-' . time() . '.json', $payload);
```

```bash
$: php -S localhost:5757 receive.php
```