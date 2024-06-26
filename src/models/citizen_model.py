from dataclasses import dataclass, field
from typing import Callable, List


class CitizenInfo:
    citizen_code = ""
    date_of_birth = ""
    date_of_provision = ""
    nation = ""
    father_name = ""
    full_name = ""
    sex = ""
    place_of_origin = ""
    personal_identification = ""
    mother_name = ""
    nationality = ""
    old_citizen_code = ""
    date_of_expiry = ""
    photo_bytes = bytearray()
    photo_base64 = ""
    place_of_residence = ""
    religion = ""
    spouse_name = ""
    challenge = bytearray()
    chip_authentication = False
    active_authentication = False
    
    def fromCardData(self, ci):
        
        if ci is not None:
            self.citizen_code = ci.CitizenCode
            self.date_of_birth = ci.DateOfBirth
            self.date_of_provision = ci.DateOfProvision
            self.nation = ci.Nation
            self.father_name = ci.FatherName
            self.full_name = ci.FullName
            self.sex = ci.Sex
            self.place_of_origin = ci.PlaceOfOrigin
            self.personal_identification = ci.PersonalIdentification
            self.mother_name = ci.MotherName
            self.nationality = ci.Nationality
            self.old_citizen_code = ci.OldCitizenCode
            self.date_of_expiry = ci.DateOfExpiry
            self.photo_bytes = ci.PhotoBytes
            self.photo_base64 = ci.PhotoBase64
            self.place_of_residence = ci.PlaceOfResidence
            self.religion = ci.Religion
            self.spouse_name = ci.SpouseName
            self.challenge = ci.Challenge
            self.chip_authentication = ci.ChipAuthentication
            self.active_authentication = ci.ActiveAuthentication
            
    def toJson(self):
        return {
            "citizen_code": self.citizen_code,
            "date_of_birth": self.date_of_birth,
            "date_of_provision": self.date_of_provision,
            "nation": self.nation,
            "father_name": self.father_name,
            "full_name": self.full_name,
            "sex": self.sex,
            "place_of_origin": self.place_of_origin,
            "personal_identification": self.personal_identification,
            "mother_name": self.mother_name,
            "nationality": self.nationality,
            "old_citizen_code": self.old_citizen_code,
            "date_of_expiry": self.date_of_expiry,
            "photo_bytes": self.photo_bytes,
            "photo_base64": self.photo_base64,
            "place_of_residence": self.place_of_residence,
            "religion": self.religion,
            "spouse_name": self.spouse_name,
            "challenge": self.challenge,
            "chip_authentication": self.chip_authentication,
            "active_authentication": self.active_authentication
        }
    