# elasticsearch-web-export
Export Elasticsearch data using an HTTP/web based interface using 
[stash-query](https://github.com/robbydyer/stash-query) by robbydyer

This is a very basic interface to elasticsearch that can be used in a web browser for users who are less 
comfortable with the command line (and who are likely already in a browser based interface using Kibana). 
It has a lot of room for improvement to make it more user-friendly. **Pull requests welcome!**

## Usage
Start the flask webserver 
```
python main.py
```

The server listens on port 8085. To make a request, construct a URL as follows (Example):

```
[hostname:port]/query?start_time=2015-03-20T10:36:47.621Z&end_time=2015-03-20T10:40:47.621Z&query=type:"apache"
```
Depending on the size of the query, it will take some time before you get any response (an obvious opportunity for improvment), but once the query completes a file download should initiate in your browser (or curl, other HTTP client you use).   

## Requirements 
- [flask](http://flask.pocoo.org/)
- [stash-query](https://github.com/robbydyer/stash-query), installed in the user's path: 
