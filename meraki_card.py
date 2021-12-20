card = '''
<
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.2",
    "body": [
        <
            "type": "ColumnSet",
            "columns": [
                <
                    "type": "Column",
                    "width": 2,
                    "items": [
                        <
                            "type": "TextBlock",
                            "text": "Actualización de CMDB",
                            "size": "Large",
                            "weight": "Bolder"
                        >,
                        <
                            "type": "TextBlock",
                            "text": "Meraki {model}",
                            "weight": "Bolder",
                            "size": "ExtraLarge",
                            "spacing": "Medium"
                        >,
                        <
                            "type": "Container",
                            "items": [
                                <
                                    "type": "TextBlock",
                                    "text": "**Serial**: {serial}",
                                    "wrap": true
                                >,
                                <
                                    "type": "TextBlock",
                                    "text": "**MAC**: {mac}",
                                    "wrap": true
                                >
                            ]
                        >
                    ]
                >,
                <
                    "type": "Column",
                    "width": 1,
                    "items": [
                        <
                            "type": "Image",
                            "url": "https://www.brighttalk.com/wp-content/uploads/2019/07/cisco-meraki-logo.png",
                            "size": "auto"
                        >
                    ]
                >
            ]
        >
    ],
    "actions": [
        <
            "type": "Action.OpenUrl",
            "title": "Más información",
            "url": "{url}"
        >
    ]
>
'''