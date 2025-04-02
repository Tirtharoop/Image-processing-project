import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("F:/project/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancesystem-9acfd-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

ref=db.reference('students')

data={
    "121":
    {
        
        "name":"Elon MUsk",
        "major":"Astronomy",
        "standing":"A",
        "year":4,
        "starting_year":2021,
        "total_attendance":11,
        "last_attendance":"2022-12-11  00:54:34"
    
    },
    "321":
    {
        
        "name":"Emily Blunt",
        "major":"Robotics",
        "standing":"B",
        "year":2,
        "starting_year":2020,
        "total_attendance":7,
        "last_attendance":"2022-12-11  00:54:34"
    
    },
    "421":
    {
        
        "name":"Tony Stark",
        "major":"Astronomy",
        "standing":"D",
        "year":5,
        "starting_year":2019,
        "total_attendance":16,
        "last_attendance":"2022-12-11  00:54:34"
    
    },
    "521":
    {
        
        "name":"Tirtharoop Banerjee",
        "major":"Computer Sc.",
        "standing":"A",
        "year":6,
        "starting_year":2022,
        "total_attendance":21,
        "last_attendance":"2022-12-11  00:54:34"
    
    },
    "621":
    {
        "name":"Umesh Kumar Pandey",
        "major":"Computer Sc.",
        "standing":"A",
        "year":6,
        "starting_year":2022,
        "total_attendance":21,
        "last_attendance":"2022-12-11  00:54:34"

    }

    
}

for key,value in data.items():
    ref.child(key).set(value)