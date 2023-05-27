import json
import re


class EasyRiderEntry:
    meta = {
        "stop_name": {"type": str, "required": True},
        "stop_type": {"type": str, "required": False, "names": ["S", "O", "F", ""]},
        "a_time": {"type": str, "required": True},
    }
    errors = dict.fromkeys(meta, 0)

    def __init__(self, data: str):
        self.data = json.loads(data)

    def check_fields(self):
        for objet in self.data:
            for key, value in objet.items():
                if key != "bus_id" and key != "stop_id" and key != "next_stop":
                    specification = self.meta[key]
                    if self.is_type_ok(value, specification["type"]):
                        if self.is_required_ok(value, specification["required"]):
                            if self.check_stop_name_a_time(key, value):
                                self.errors[key] += 1
                            if self._is_in_list(value, specification):
                                self.errors[key] += 1
                        else:
                            self.errors[key] += 1
                    else:
                        self.errors[key] += 1

    @staticmethod
    def is_type_ok(value, _type_) -> bool:
        if type(value) == _type_:
            return True
        else:
            return False

    @staticmethod
    def is_required_ok(value, required) -> bool:
        if required and value == "":
            return False
        else:
            return True

    @staticmethod
    def check_stop_name_a_time(key, _value_) -> bool:
        if key == "stop_name":
            pattern = re.compile(r'([A-Z][a-z]+ ?)+(Road|Avenue|Boulevard|Street)$')
            if pattern.search(_value_):
                return False
            else:
                return True
        elif key == "a_time":
            pattern = re.compile(r'^([01]\d|2[0-3]):([0-5]\d)$')
            if pattern.search(_value_):
                return False
            else:
                return True
        return False

    @staticmethod
    def _is_in_list(value, item: dict) -> bool:
        if "names" in item.keys():
            if value in item["names"]:
                return False
            else:
                return True
        return False

    @classmethod
    def print_errors(cls):
        print("Format validation:", sum(cls.errors.values()), "errors")
        print(*[f"{k}: {v}" for k, v in cls.errors.items()], sep="\n")


def main():
    app = EasyRiderEntry(input())
    app.check_fields()
    app.print_errors()


if __name__ == "__main__":
    main()