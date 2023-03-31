# json-fields-extractor
## Example

```py
from json_fields_extractor import JsonFieldsExtractor

data = {
    "menu": {
        "id": "file",
        "value": "File",
        "popup": {
            "menuitem": [
                {
                    "value": "New",
                    "onclick": "CreateNewDoc()"
                },
                {
                    "value": "Open",
                    "onclick": "OpenDoc()"
                },
                {
                    "value": "Close",
                    "onclick": "CloseDoc()"
                }
            ]
        }
    }
}

field_paths = {
    "id": ["menu", "id"],
    "all_item_values": ["menu", "popup", "menuitem",  "*", "value"],
    "first_item_value": ["menu", "popup", "menuitem", "_0", "value"],
    "item_values_except_first": ["menu", "popup", "menuitem", ("$idx", lambda x: x >= 1), "value"],
    "open_action": ["menu", "popup", "menuitem", ("value", lambda x: x == 'Open'), "onclick"],
}

extractor = JsonFieldsExtractor(field_paths=field_paths)
fields = extractor(data)
print(fields)
```

We will get results
```text
OrderedDict([('id', 'file'), ('all_item_values', ['New', 'Open', 'Close']), ('first_item_value', 'New'), ('item_values_except_first', ['Open', 'Close']), ('open_action', 'OpenDoc()')])
```
