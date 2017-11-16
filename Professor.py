import re


class Professor():

    def __init__(self, first_name, job_title, phone, department, building, room, email_address, url):
        '''
        Default constructor for the Professor class. A data type with the purpose of correlating all of a specific
        faculty members information.
        :param first_name: the faculty member's first name
        :param job_title: the faculty member's job title
        :param phone: the faculty member's phone number
        :param department: the faculty member's department
        :param building: the faculty member's building
        :param room: the faculty member's room
        :param email_address: the faculty member's email_address
        :param url: the faculty member's url
        self.last_name: the faculty member's last name
        :return:
        '''
        self.department = department
        self.first_name = first_name
        self.last_name = ""
        self.job_title = job_title
        self.phone = phone
        self.building = building
        self.room = room
        self.email_address = email_address
        self.URL = url

    def change_department(self, change):
        self.department = change

    def add_name(self, name):
        self.first_name = name

    def add_job_title(self, job_title):
        self.job_title = job_title

    def add_phone(self, phone):
        self.phone = phone

    def add_building(self, building):
        self.building = building

    def add_room(self, room):
        self.room = room

    def add_email_address(self, email_address):
        self.email_address = email_address

    def add_URL(self, URL):
        self.URL = URL

    def clean_phone_number(self):
        '''
        Cleans the phone number according to a 10+ digit standard (i.e. area code-7 digit number-extension).
        '''
        self.phone = re.sub(r"[^0-9]", "", self.phone)
        if len(self.phone) < 7:
            self.phone = ""
        elif len(self.phone) < 10:
            self.phone = "707"+self.phone
        elif len(self.phone) > 11:
            self.phone = self.phone[:10] + 'x' + self.phone[10:]

    def fix_name(self):
        '''
        removes the suffix and splits the name into first and last names.
        '''
        names = self.first_name.split()
        self.first_name = names[0]
        if ("jr" in names[-1].lower()) and (len(names[-1]) < 4):
            self.last_name = names[-2]
        else:
            self.last_name = names[-1]

    def write_Professor(self, filename):
        '''
        Writes the faculty members information properly formatted to filename.
        :param filename: the file to write the information to.
        :return:
        '''
        filename.write('        {\n            "first name" : "'+self.first_name + '",\n')
        filename.write('            "last name" : "'+self.last_name+'",\n')
        filename.write('            "job title" : "'+self.job_title+'",\n')
        filename.write('            "phone" : "'+self.phone+'",\n')
        filename.write('            "department" : "'+self.department+'",\n')
        filename.write('            "building" : "'+self.building+'",\n')
        filename.write('            "room" : "'+self.room+'",\n')
        filename.write('            "email address" : "'+self.email_address+'",\n')
        filename.write('            "URL" : "'+self.URL+'"\n        },\n')

    def write_last_Professor(self, filename):
        '''
        Writes the faculty members information properly formatted to filename. The formatting is slightly different
        for the last item.
        :param filename: the file to write the information to.
        :return:
        '''
        filename.write('        {\n            "first name" : "'+self.first_name + '",\n')
        filename.write('            "last name" : "'+self.last_name+'",\n')
        filename.write('            "job title" : "'+self.job_title+'",\n')
        filename.write('            "phone" : "'+self.phone+'",\n')
        filename.write('            "department" : "'+self.department+'",\n')
        filename.write('            "building" : "'+self.building+'",\n')
        filename.write('            "room" : "'+self.room+'",\n')
        filename.write('            "email address" : "'+self.email_address+'",\n')
        filename.write('            "URL" : "'+self.URL+'"\n        }\n')

