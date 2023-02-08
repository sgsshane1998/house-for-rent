from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import pyrebase
from django.db.models import Q
import random 
import json

config ={
    "apiKey": "AIzaSyCSTDeQhNZETTbux1sXd1EXavxGcOtZz4M",
    "authDomain": "dsci551-project-f4553.firebaseapp.com",
    "databaseURL": "https://dsci551-project-f4553-default-rtdb.firebaseio.com",
    "projectId": "dsci551-project-f4553",
    "storageBucket": "dsci551-project-f4553.appspot.com",
    "messagingSenderId": "865743627131",
    "appId": "1:865743627131:web:551541d404454f08f413de",
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def homepage(request):
    access =  []
    accommodates = []
    bathroom = []
    city = []
    country = []
    description = []
    host_name = []
    latitude = []
    longitude = []
    price = []
    neighbhourhood = []
    pro_type = []
    room_type = []
    state = []
    transit = []
    picture = []
    zipcode = []
    indexs = []
    IDs = []
    for i in random.sample(range(140),3):
        Access = database.child('houses').child(i).child('Access').get().val()
        Accommodates = database.child('houses').child(i).child('Accommodates').get().val()
        Bathroom = database.child('houses').child(i).child('Bathroom').get().val()
        City = database.child('houses').child(i).child('City').get().val()
        Country = database.child('houses').child(i).child('Country').get().val()
        Description = database.child('houses').child(i).child('Description').get().val()
        Host_name = database.child('houses').child(i).child('Host Name').get().val()
        Longitude = database.child('houses').child(i).child('Longitude').get().val()
        Latitude = database.child('houses').child(i).child('Latitude').get().val()
        Price = database.child('houses').child(i).child('Monthly Price').get().val()
        Picture = database.child('houses').child(i).child('XL Picture Url').get().val()
        Neighbhourhood = database.child('houses').child(i).child('Neighbourhood Cleansed').get().val()
        Pro_type = database.child('houses').child(i).child('Property Type').get().val()
        Room_type = database.child('houses').child(i).child('Room Type').get().val()
        State = database.child('houses').child(i).child('State').get().val()
        Transit  = database.child('houses').child(i).child('Transit').get().val()
        Zipcode = database.child('houses').child(i).child('Zipcode').get().val()
        ID = database.child('houses').child(i).child('ID').get().val()
        indexs.append(i)
        access.append(Access)
        accommodates.append(Accommodates)
        bathroom.append(Bathroom)
        city.append(City)
        country.append(Country)
        description.append(Description)
        host_name.append(Host_name)
        latitude.append(Latitude)
        longitude.append(Longitude)
        price.append(Price)
        neighbhourhood.append(Neighbhourhood)
        pro_type.append(Pro_type)
        room_type.append(Room_type)
        state.append(State)
        transit.append(Transit)
        picture.append(Picture)
        zipcode.append(Zipcode)
        IDs.append(ID)
    comb_list = zip(price,neighbhourhood,room_type, IDs)
    return render(request, "home.html", {"comb_list":comb_list}) 


def detail(request, IDs):
    db = database.child('houses').order_by_child("ID").equal_to(IDs).get()
    attr = db.each()[0].val()
    
    Longitude = attr['Longitude']
    Latitude = attr['Latitude']
    
    Access = attr['Access']
    Accommodate = attr['Accommodates']
    Bathroom = attr['Bathrooms']
    Bedroom = attr['Bedrooms']
    Description = attr['Description']
    Host_About = attr['Host About']
    Price = attr['Monthly Price']
    Neighbourhood = attr['Neighbourhood Cleansed']
    Property_Type = attr['Property Type']
    Room_Type = attr['Room Type']
    Security_Deposit = attr['Security Deposit']
    Transit = attr['Transit']
    if attr['XL Picture Url'] == "not provided":
        Picture = "https://miro.medium.com/max/800/1*hFwwQAW45673VGKrMPE2qQ.png"
    else:
        Picture = attr['XL Picture Url']

    data = {
        "Access":Access,
        "Accommodate":Accommodate,
        "Bathroom":Bathroom,
        "Bedroom":Bedroom,
        "Description":Description,
        "Host_About":Host_About,
        "Price":Price,
        "Neighbourhood":Neighbourhood,
        "Property_Type":Property_Type,
        "Room_Type":Room_Type,
        "Security_Deposit":Security_Deposit,
        "Transit":Transit,
        "Picture":Picture
    }

    lng_lat = {
        "longi":Longitude,
        "lati":Latitude
    }
    
    
    return render(request, 'detail.html', {"data":data, "data_json": json.dumps(lng_lat)})



def search(request):
    Accommodate = request.GET['accommodate']
    Max_price = request.GET['max_price']
    Min_price = request.GET['min_price']
    Neighbourhood = request.GET['neighbourhood']
    Property_type = request.GET['property_type']

    if not Accommodate:
        Accommodate = 0
    if not Max_price:
        Max_price = 1000000
    if not Min_price:
        Min_price = 0
    data_by_price = database.child("houses").order_by_child("Monthly Price").start_at(int(Min_price)).end_at(int(Max_price)).get()
    result = []
    for house in data_by_price.each():
        key = house.key()
        attr = house.val()
        #print(attr['Access'])
        if Neighbourhood == "any":
            Neighbourhood_base = attr['Neighbourhood Cleansed']
        else:
            Neighbourhood_base = Neighbourhood

        if Property_type == "any":
            Property_type_base = attr['Property Type']
        else:
            Property_type_base = Property_type
        
        if (attr['Accommodates'] >= int(Accommodate)) and (attr['Neighbourhood Cleansed'] == Neighbourhood_base) and (attr['Property Type'] == Property_type_base):
            result.append(attr)
    
    #if result is empty, send to nothing.html
    #package price, property_type, neighbourhood, city, zip code, beds, baths, ID, pic_url
    pic_not_found = 'this is a link to 404'
    if len(result) == 0:
        data = {
            "nothing":" no result."
        }
        return render(request, 'search.html', data)
    else:
        IDs = []
        prices = []
        p_types = []
        bed_num = []
        bath_num = []
        neighbors = []
        cities = []
        zips = []
        pics = []
    
        for a in result:
            IDs.append(a['ID'])
            prices.append(a['Monthly Price'])
            p_types.append(a['Property Type'])
            bed_num.append(a['Bedrooms'])
            bath_num.append(a['Bathrooms'])
            neighbors.append(a['Neighbourhood Cleansed'])
            cities.append(a['City'])
            zips.append(a['Zipcode'])
            if a['XL Picture Url'] == "not provided":
                pics.append(pic_not_found)
            else:
                pics.append(a['XL Picture Url'])   
        result_list = zip(prices, p_types, neighbors, IDs)
        return render(request, "search.html", {"res_list": result_list})
