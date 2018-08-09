config = {
    "scan_interval": 1, # seconds
    "host": None,
    "server": "Matrikon.OPC.Simulation.1",
    "items": [
        {
            "host": "SANDBOX3",
            "key": "opcrandomint",
            "item_id": "Test.Int"
        },
        {
            "host": "SANDBOX3",
            "key": "opcrandomdouble",
            "item_id": "Test.Double"
        },
        {
            "host": "SANDBOX3",
            "key": "InvalidItem",
            "item_id": "Invalid.Item"
        },
        {
            "host": "INVALIDHOST",
            "key": "InvalidItem2",
            "item_id": "Invalid.Item2"
        }
    ],
    "output":{
        "verbose": True,
        "use_json": False,
        "to_console": True,
        "to_file": False,
        "to_zabbix": True,
        "zabbix_server": "10.10.10.33",
        "zabbix_port": 5665,
        "zabbix_quality_suffix": "_quality",
        "zabbix_timestamp_suffix": "_timestamp",
        "zabbix_delay_suffix": "_delay"
    }
}