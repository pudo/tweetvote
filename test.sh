echo '<doc><item>Some content.</item></doc>' | curl -X POST -H 'Content-type: text/xml' -d @- http://example.com/restapi