import json


class ProfileManager:
    def __init__(self):
        self.__profile_file: dict = json.load(open("profiles.json"))

    def __save_to_file(self):
        with open("profiles.json", "w") as outfile:
            outfile.write(json.dumps(self.__profile_file))

    def GetListOfProfiles(self):
        return list(self.__profile_file["profiles"].keys())

    def GetListOfMappings(self, profile):
        return list(self.__profile_file["profiles"][profile].keys())

    def RemoveProfile(self, name):
        self.__profile_file["profiles"].pop(name, None)
        self.__save_to_file()

    def NewProfile(self, name) -> bool:
        """
        returns true if a new profile was created
        """
        keys: set = set(self.GetListOfProfiles())
        is_profile_in_keys = name in keys

        if not is_profile_in_keys:
            self.__profile_file["profiles"][name] = {"mappings": {}}

            self.__save_to_file()

            return True

        else:
            return False

    def UpdateMapping(self, profile, key, text, action):
        """
        returns true if mapping was updated
        """
        if text == "" or action == "":
            return
        
        profiles: set = set(self.GetListOfProfiles())

        


        if profile in profiles:
            self.__profile_file["profiles"][profile]["mappings"][key] = {
                "action": action,
                "text": text,
            }

            print(self.__profile_file)
            self.__save_to_file()
            return True
        else:
            return False

    def GetMapping(self, profile: str, key: str) -> dict | None:    
        try:
            mapping = self.__profile_file["profiles"][profile]["mappings"][key]
            return mapping
        except:
            return None


