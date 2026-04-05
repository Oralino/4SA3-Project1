import json

class ExportStrategy:
    # Abstract method to be overridden by subclasses to define specific export behavior
    def export(self, data):
        pass
    
class JsonExportStrategy(ExportStrategy):
    def export(self, data):
        # Converts the dictionary data into a formatted JSON string
        return json.dumps(data, indent=4)

class IniExportStrategy(ExportStrategy):
    def export(self, data):
        # Extracts the raw ini text from the dictionary data
        return data.get("ini_data", "")