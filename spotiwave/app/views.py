from django.shortcuts import render
import requests

def homepageview(request): 
    
    def get_access_token():
        access_token = None
        token_url = "https://accounts.spotify.com/api/token"
        token_header = {
            "Content-Type" : "application/x-www-form-urlencoded"
        }
        client_id = "a8ed25a132144d64b507e118bcc450cf"
        client_secret = "f2f9d9833f594a1ea950d512556a14ce"
        token_data = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
     
        access_response = requests.post(url = token_url, headers = token_header, data=token_data)
        
        if access_response.status_code == 200:
            access_token = access_response.json()["access_token"]
        
        return access_token
        
    access_token = get_access_token()
    spotify_url = "https://api.spotify.com/v1/{}"
    spotify_header = {
        "Authorization" : f"Bearer {access_token}"
    }
    print (access_token)
    search_result = None
    
    if request.method == "POST":
        search_value = request.POST.get("search")
        
        search_param = {
            "q" : f"{search_value}",
            "type" : ["album", "artist", "playlist", "track", "show", "episode", "audiobook"],
            "limit" : 20
        }
        
        search_response = requests.get(url=spotify_url.format("search"), headers = spotify_header, params=search_param)
        
        if search_response.status_code == 200:
            search_result = search_response.json()
        else:
            try:
                search_result = search_response.json()
            except ValueError:
                search_result = search_response
    else:
        return render(request, "home.html", {"search_result": search_result})
    
    return render(request, "home.html", {"search_result": search_result})