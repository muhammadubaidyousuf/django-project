  const OpenNav = () => {
    document.getElementById('sidenavbarid').style.width = "250px";
  }

    const closeNave = () => {
    document.getElementById('sidenavbarid').style.width = "0";
  }



function showImg(h) {
	var link = "http://127.0.0.1:8000/media_files/cars/img/"; 
 	const showImage = document.querySelector('.showImage').innerHTML = "<img src='"+ link + h + ".png' />";
 	document.getElementById('select-image').value = link + h + ".png"
  document.getElementById('showText').innerHTML = 'This image just for showing car category';

  
}



// for geolocations 

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else { 
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  // x.value = position.coords.latitude;
  // y.value = position.coords.longitude;
	document.getElementById("c-let").value = position.coords.latitude;
	document.getElementById("c-log").value = position.coords.longitude;
}


// for geolocations end

// Add car velidation 