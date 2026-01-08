"""
Mock patient data for Central Patient Registry
Contains 20+ realistic Kenyan patient records
"""

MOCK_PATIENTS = [
    {
        "patient_id": "PAT-001234",
        "national_id": "12345678",
        "first_name": "John",
        "last_name": "Kamau",
        "date_of_birth": "1985-03-15",
        "gender": "male",
        "phone": "+2547123456xx",
        "email": "john.kamau@example.com",
        "address": {
            "county": "Nairobi",
            "sub_county": "Westlands",
            "ward": "Parklands"
        },
        "emergency_contact": {
            "name": "Mary Kamau",
            "relationship": "Spouse",
            "phone": "+2547876543xx"
        }
    },
    {
        "patient_id": "PAT-001235",
        "national_id": "23456789",
        "first_name": "Sarah",
        "last_name": "Wanjiku",
        "date_of_birth": "1990-07-22",
        "gender": "female",
        "phone": "+2547234567xx",
        "email": "sarah.wanjiku@example.com",
        "address": {
            "county": "Nairobi",
            "sub_county": "Dagoretti",
            "ward": "Kawangware"
        },
        "emergency_contact": {
            "name": "Peter Wanjiku",
            "relationship": "Father",
            "phone": "+2547987654xx"
        }
    },
    {
        "patient_id": "PAT-001236",
        "national_id": "34567890",
        "first_name": "James",
        "last_name": "Ochieng",
        "date_of_birth": "1978-11-10",
        "gender": "male",
        "phone": "+2547345678xx",
        "email": "james.ochieng@example.com",
        "address": {
            "county": "Kisumu",
            "sub_county": "Kisumu Central",
            "ward": "Migosi"
        },
        "emergency_contact": {
            "name": "Grace Ochieng",
            "relationship": "Sister",
            "phone": "+2547098765xx"
        }
    },
    {
        "patient_id": "PAT-001237",
        "national_id": "45678901",
        "first_name": "Faith",
        "last_name": "Akinyi",
        "date_of_birth": "1995-05-18",
        "gender": "female",
        "phone": "+2547456789xx",
        "email": "faith.akinyi@example.com",
        "address": {
            "county": "Mombasa",
            "sub_county": "Mvita",
            "ward": "Tononoka"
        },
        "emergency_contact": {
            "name": "David Otieno",
            "relationship": "Brother",
            "phone": "+2547109876xx"
        }
    },
    {
        "patient_id": "PAT-001238",
        "national_id": "56789012",
        "first_name": "David",
        "last_name": "Kipchoge",
        "date_of_birth": "1982-09-25",
        "gender": "male",
        "phone": "+2547567890xx",
        "email": "david.kipchoge@example.com",
        "address": {
            "county": "Nakuru",
            "sub_county": "Nakuru Town East",
            "ward": "Biashara"
        },
        "emergency_contact": {
            "name": "Jane Kipchoge",
            "relationship": "Spouse",
            "phone": "+2547210987xx"
        }
    },
    {
        "patient_id": "PAT-001239",
        "national_id": "67890123",
        "first_name": "Lucy",
        "last_name": "Mutua",
        "date_of_birth": "1988-12-03",
        "gender": "female",
        "phone": "+2547678901xx",
        "email": "lucy.mutua@example.com",
        "address": {
            "county": "Machakos",
            "sub_county": "Machakos Town",
            "ward": "Mumbuni"
        },
        "emergency_contact": {
            "name": "Paul Mutua",
            "relationship": "Husband",
            "phone": "+2547321098xx"
        }
    },
    {
        "patient_id": "PAT-001240",
        "national_id": "78901234",
        "first_name": "Peter",
        "last_name": "Mwangi",
        "date_of_birth": "1975-06-14",
        "gender": "male",
        "phone": "+2547789012xx",
        "email": "peter.mwangi@example.com",
        "address": {
            "county": "Kiambu",
            "sub_county": "Thika Town",
            "ward": "Hospital"
        },
        "emergency_contact": {
            "name": "Anne Mwangi",
            "relationship": "Daughter",
            "phone": "+2547432109xx"
        }
    },
    {
        "patient_id": "PAT-001241",
        "national_id": "89012345",
        "first_name": "Grace",
        "last_name": "Nyambura",
        "date_of_birth": "1992-02-28",
        "gender": "female",
        "phone": "+2547890123xx",
        "email": "grace.nyambura@example.com",
        "address": {
            "county": "Nairobi",
            "sub_county": "Embakasi",
            "ward": "Umoja"
        },
        "emergency_contact": {
            "name": "Joseph Nyambura",
            "relationship": "Father",
            "phone": "+2547543210xx"
        }
    },
    {
        "patient_id": "PAT-001242",
        "national_id": "90123456",
        "first_name": "Michael",
        "last_name": "Owino",
        "date_of_birth": "1987-08-19",
        "gender": "male",
        "phone": "+2547901234xx",
        "email": "michael.owino@example.com",
        "address": {
            "county": "Kakamega",
            "sub_county": "Lurambi",
            "ward": "Mahiakalo"
        },
        "emergency_contact": {
            "name": "Christine Owino",
            "relationship": "Spouse",
            "phone": "+2547654321xx"
        }
    },
    {
        "patient_id": "PAT-001243",
        "national_id": "01234567",
        "first_name": "Catherine",
        "last_name": "Chebet",
        "date_of_birth": "1993-04-07",
        "gender": "female",
        "phone": "+2547012345xx",
        "email": "catherine.chebet@example.com",
        "address": {
            "county": "Uasin Gishu",
            "sub_county": "Eldoret East",
            "ward": "Kimumu"
        },
        "emergency_contact": {
            "name": "Daniel Korir",
            "relationship": "Brother",
            "phone": "+2547765432xx"
        }
    },
    {
        "patient_id": "PAT-001244",
        "national_id": "11223344",
        "first_name": "Daniel",
        "last_name": "Njoroge",
        "date_of_birth": "1980-01-30",
        "gender": "male",
        "phone": "+2547112233xx",
        "email": "daniel.njoroge@example.com",
        "address": {
            "county": "Nairobi",
            "sub_county": "Kasarani",
            "ward": "Ruai"
        },
        "emergency_contact": {
            "name": "Helen Njoroge",
            "relationship": "Spouse",
            "phone": "+2547876543xx"
        }
    },
    {
        "patient_id": "PAT-001245",
        "national_id": "22334455",
        "first_name": "Angela",
        "last_name": "Adhiambo",
        "date_of_birth": "1989-10-12",
        "gender": "female",
        "phone": "+2547223344xx",
        "email": "angela.adhiambo@example.com",
        "address": {
            "county": "Siaya",
            "sub_county": "Bondo",
            "ward": "Yala Township"
        },
        "emergency_contact": {
            "name": "George Ouma",
            "relationship": "Husband",
            "phone": "+2547987654xx"
        }
    },
    {
        "patient_id": "PAT-001246",
        "national_id": "33445566",
        "first_name": "Samuel",
        "last_name": "Kiprotich",
        "date_of_birth": "1984-07-05",
        "gender": "male",
        "phone": "+2547334455xx",
        "email": "samuel.kiprotich@example.com",
        "address": {
            "county": "Kericho",
            "sub_county": "Kericho Town",
            "ward": "Kapsoit"
        },
        "emergency_contact": {
            "name": "Ruth Kiprotich",
            "relationship": "Sister",
            "phone": "+2547098765xx"
        }
    },
    {
        "patient_id": "PAT-001247",
        "national_id": "44556677",
        "first_name": "Joyce",
        "last_name": "Wambui",
        "date_of_birth": "1991-03-21",
        "gender": "female",
        "phone": "+2547445566xx",
        "email": "joyce.wambui@example.com",
        "address": {
            "county": "Nyeri",
            "sub_county": "Nyeri Central",
            "ward": "Ruring'u"
        },
        "emergency_contact": {
            "name": "Patrick Wambui",
            "relationship": "Father",
            "phone": "+2547109876xx"
        }
    },
    {
        "patient_id": "PAT-001248",
        "national_id": "55667788",
        "first_name": "Robert",
        "last_name": "Muturi",
        "date_of_birth": "1986-11-16",
        "gender": "male",
        "phone": "+2547556677xx",
        "email": "robert.muturi@example.com",
        "address": {
            "county": "Meru",
            "sub_county": "Imenti North",
            "ward": "Ntima East"
        },
        "emergency_contact": {
            "name": "Alice Muturi",
            "relationship": "Spouse",
            "phone": "+2547210987xx"
        }
    },
    {
        "patient_id": "PAT-001249",
        "national_id": "66778899",
        "first_name": "Elizabeth",
        "last_name": "Nafula",
        "date_of_birth": "1994-09-08",
        "gender": "female",
        "phone": "+2547667788xx",
        "email": "elizabeth.nafula@example.com",
        "address": {
            "county": "Bungoma",
            "sub_county": "Kanduyi",
            "ward": "Bukembe West"
        },
        "emergency_contact": {
            "name": "Moses Wekesa",
            "relationship": "Brother",
            "phone": "+2547321098xx"
        }
    },
    {
        "patient_id": "PAT-001250",
        "national_id": "77889900",
        "first_name": "Francis",
        "last_name": "Kariuki",
        "date_of_birth": "1979-05-24",
        "gender": "male",
        "phone": "+2547778899xx",
        "email": "francis.kariuki@example.com",
        "address": {
            "county": "Murang'a",
            "sub_county": "Murang'a South",
            "ward": "Makuyu"
        },
        "emergency_contact": {
            "name": "Margaret Kariuki",
            "relationship": "Spouse",
            "phone": "+2547432109xx"
        }
    },
    {
        "patient_id": "PAT-001251",
        "national_id": "88990011",
        "first_name": "Beatrice",
        "last_name": "Chepkoech",
        "date_of_birth": "1996-12-11",
        "gender": "female",
        "phone": "+2547889900xx",
        "email": "beatrice.chepkoech@example.com",
        "address": {
            "county": "Nandi",
            "sub_county": "Nandi Hills",
            "ward": "Chepkunyuk"
        },
        "emergency_contact": {
            "name": "Agnes Chepkoech",
            "relationship": "Mother",
            "phone": "+2547543210xx"
        }
    },
    {
        "patient_id": "PAT-001252",
        "national_id": "99001122",
        "first_name": "Anthony",
        "last_name": "Otieno",
        "date_of_birth": "1983-02-14",
        "gender": "male",
        "phone": "+2547990011xx",
        "email": "anthony.otieno@example.com",
        "address": {
            "county": "Homa Bay",
            "sub_county": "Homa Bay Town",
            "ward": "Homa Bay Central"
        },
        "emergency_contact": {
            "name": "Phoebe Atieno",
            "relationship": "Spouse",
            "phone": "+2547654321xx"
        }
    },
    {
        "patient_id": "PAT-001253",
        "national_id": "00112233",
        "first_name": "Caroline",
        "last_name": "Nyokabi",
        "date_of_birth": "1990-08-27",
        "gender": "female",
        "phone": "+2547001122xx",
        "email": "caroline.nyokabi@example.com",
        "address": {
            "county": "Embu",
            "sub_county": "Manyatta",
            "ward": "Gaturi South"
        },
        "emergency_contact": {
            "name": "Stephen Nyokabi",
            "relationship": "Husband",
            "phone": "+2547765432xx"
        }
    },
    {
        "patient_id": "PAT-001254",
        "national_id": "11224488",
        "first_name": "Vincent",
        "last_name": "Mwaniki",
        "date_of_birth": "1977-04-03",
        "gender": "male",
        "phone": "+2547112244xx",
        "email": "vincent.mwaniki@example.com",
        "address": {
            "county": "Nairobi",
            "sub_county": "Makadara",
            "ward": "Harambee"
        },
        "emergency_contact": {
            "name": "Jane Mwaniki",
            "relationship": "Daughter",
            "phone": "+2547876543xx"
        }
    }
]