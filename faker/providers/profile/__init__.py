import itertools

from .. import BaseProvider


class Provider(BaseProvider):
    """
    This provider is a collection of functions to generate personal profiles and identities.

    """

    def simple_profile(self, sex=None):
        """
        Generates a basic profile with personal informations
        """
        SEX = ["F", "M"]
        if sex not in SEX:
            sex = self.random_element(SEX)
        if sex == 'F':
            name = self.generator.name_female()
        elif sex == 'M':
            name = self.generator.name_male()
        return {
            "username": self.generator.user_name(),
            "name": name,
            "sex": sex,
            "address": self.generator.address(),
            "mail": self.generator.free_email(),
            "birthdate": self.generator.date_of_birth(),
        }

    def simple_profile_consistent(self, sex=None):
        """
        Generates a basic profile with personal information; the username and
        e-mail addresses created will reflect the name generated.  Note that
        unlike ``simple_profile()``, this will not use specified name
        formatting, and instead always returns ``name`` as 'first last'.

        Returns:
            dict: a dictionary containing the profile data::

                {
                    "username": str(),  # A username, based on first & last name
                    "name": str(),  # 'Firstname Lastname'
                    "sex": str(),  # type SEX, from choices 'M' or 'F'
                    "address": str()
                    "mail": str(),  # An e-mail address based on the user's name
                    "birthdate": datetime.date()
                }

        """
        SEX = ["F", "M"]
        if sex not in SEX:
            sex = self.random_element(SEX)
        if sex == 'F':
            first_name = self.generator.first_name_female()
        elif sex == 'M':
            first_name = self.generator.first_name_male()
        last_name = self.generator.last_name()
        name = first_name + ' ' + last_name  # TODO: This should use the correct name formatting
        return {
            "username": self.generator.user_name(first_name=first_name, last_name=last_name),
            "name": name,
            "sex": sex,
            "address": self.generator.address(),
            "mail": self.generator.free_email(first_name=first_name, last_name=last_name),
            "birthdate": self.generator.date_of_birth(),
        }

    def profile(self, fields=None, sex=None):
        """
        Generates a complete profile.
        If "fields" is not empty, only the fields in the list will be returned
        """
        if fields is None:
            fields = []

        d = {
            "job": self.generator.job(),
            "company": self.generator.company(),
            "ssn": self.generator.ssn(),
            "residence": self.generator.address(),
            "current_location": (self.generator.latitude(), self.generator.longitude()),
            "blood_group": "".join(self.random_element(list(itertools.product(["A", "B", "AB", "O"], ["+", "-"])))),
            "website": [self.generator.url() for _ in range(1, self.random_int(2, 5))],
        }

        d = dict(d, **self.generator.simple_profile(sex))
        # field selection
        if len(fields) > 0:
            d = {k: v for k, v in d.items() if k in fields}

        return d

    def profile_consistent(self, fields=None, sex=None):
        """
        Generates a complete profile, attempting to be more internally
        consistent than the standard ``profile()`` at the probable cost of some
        flexibility with formatting choices elsewhere.

        Important note: the dictionary returned is **not** the same structure;
        the address information is split into ``street_address``, ``city``,
        ``state,`` - the abbreviation, and ``zip`` (created via
        ``zipcode_in_state()``, should be consistent with ``state`` as given).
        Also, unlike ``profile()``, this will not use custom name formatting,
        and instead always returns ``name`` as 'first last.'

        If "fields" is not empty, only the fields in the list will be returned.
        The username and e-mail addresses created here will reflect the name
        generated.

        Args:
            fields (list, optional): The fields to include (skipping all others)
            sex (str, optional): The sex of the individual to create

        Returns:
            dict: a dictionary containing the profile data::

                {
                    "username": str(),  # A username, based on first & last name
                    "name": str(),  # 'Firstname Lastname'
                    "sex": str(),  # type SEX, from choices 'M' or 'F'
                    "address": str()
                    "mail": str(),  # An e-mail address based on the user's name
                    "birthdate": datetime.date(),
                    "job": str(),
                    "company": str(),
                    "ssn": str(),
                    "street address": str(),
                    "city": str(),
                    "state": str(),  # Two-letter state abbreviation
                    "blood_group": str(),  # from ["A", "B", "AB", "O"], ["+", "-"]
                    "website": str(),
                    "zip": str()  # A zip based on the included state
                }

        """
        exclude_fields = ['residence', 'address']

        if fields is None:
            fields = []

        d = {
            "job": self.generator.job(),
            "company": self.generator.company(),
            "ssn": self.generator.ssn(),
            "residence": self.generator.address(),
            "street address": self.generator.street_address(),
            "city": self.generator.city(),
            "state": self.generator.state_abbr(),
            "blood_group": "".join(self.random_element(list(itertools.product(["A", "B", "AB", "O"], ["+", "-"])))),
            "website": [self.generator.url() for _ in range(1, self.random_int(2, 5))],
        }

        d['zip'] = self.generator.zipcode_in_state(d['state'])

        d = dict(d, **self.generator.simple_profile_consistent(sex))
        # field selection
        if len(fields) > 0:
            d = {k: v for k, v in d.items() if k in fields}

        # Remove any excluded fields:
        d = {key: d[key] for key in d if key not in exclude_fields}

        return d
