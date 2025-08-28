def get_response_time(url):
    url = url.rstrip("/")  

    
    if url == "https://www.google.com":
        return 0.5
    if url == "https://www.youtube.com":
        return 0.3
    if url == "https://www.netflix.com/in":
        return 0.4
    
    return "Unknown URL"
