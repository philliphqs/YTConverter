function success() {
    var data = JSON.parse(this.responseText); //parse the string to JSON
    console.log(data);
}

// function to handle error
function error(err) {
    console.log('Request Failed', err); //error details will be in the "err" object
}

chrome.tabs.query({'active': true, 'windowId': chrome.windows.WINDOW_ID_CURRENT},
   function(tabs){
      var currenturl = tabs[0].url

      fetch('http://localhost:54230/download', {
        method: "GET",
        headers: {"url": currenturl}

      })
      .then(response => response.json())
      .then(json => console.log(json))
      .catch(err => console.log(err));
}

);

