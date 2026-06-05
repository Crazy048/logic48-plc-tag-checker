from plc_tag_checker.checker import validate_tags


def test_valid_tags_have_no_issues():
    tags = [
        {
            "name": "Pump_101_Start",
            "type": "Bool",
            "address": "%M0.0",
            "description": "Start command for pump 101",
            "area": "OilStation",
        },
        {
            "name": "Tank_101_Level",
            "type": "Real",
            "address": "%MD10",
            "description": "Measured oil level in tank 101",
            "area": "OilStation",
        },
    ]

    issues = validate_tags(tags)

    assert issues == []


def test_duplicate_tag_name_is_error():
    tags = [
        {
            "name": "Pump_101_Start",
            "type": "Bool",
            "address": "%M0.0",
            "description": "Start command for pump 101",
            "area": "OilStation",
        },
        {
            "name": "Pump_101_Start",
            "type": "Bool",
            "address": "%M0.1",
            "description": "Duplicate tag name example",
            "area": "OilStation",
        },
    ]

    issues = validate_tags(tags)

    assert any(issue.severity == "error" for issue in issues)
    assert any("Duplicated tag name" in issue.message for issue in issues)


def test_unsupported_data_type_is_error():
    tags = [
        {
            "name": "Tank_101_Level",
            "type": "Float",
            "address": "%MD10",
            "description": "Measured oil level in tank 101",
            "area": "OilStation",
        },
    ]

    issues = validate_tags(tags)

    assert any(issue.field == "type" for issue in issues)
    assert any("Unsupported data type" in issue.message for issue in issues)


def test_missing_description_is_warning():
    tags = [
        {
            "name": "Motor_101_RunFb",
            "type": "Bool",
            "address": "%I2.0",
            "description": "",
            "area": "OilStation",
        },
    ]

    issues = validate_tags(tags)

    assert any(issue.field == "description" for issue in issues)
    assert any(issue.severity == "warning" for issue in issues)
