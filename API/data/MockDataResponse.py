from ..helper.time_tostamp import to_timestamp
from datetime import datetime
from uuid import uuid4
DATA = {
"uuid":str(uuid4()),
"date": to_timestamp(str(datetime.now())),
"error": {
"message": "hi",
"code": "shit",
"localeMessage": "hey ass hole"
},
"location":{
"lat": 51.35,
"lon":35.34,
"name":"Mumbai,India"
},
"data":{
"AQIIndex": 205,
"pm10":151,
"pm2":205,
"co2":13,
"others":[]
},
"offerToDo":[
{
"imageUrl":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZLsGAoFKVrWJ9FgxLaMD49a3YZRMkDdNf5NsphJUcOJ7B7RoaOw&s",
"text":"Children, seniors and individuals with heart or lung diseases should stay indoors and avoid outdoor activities. General population should reduce outdoor activities."
},{
"imageUrl": "https://png.pngtree.com/svg/20151006/unhappy_91394.png",
"text":"you should wear a mask"
}
]

}
