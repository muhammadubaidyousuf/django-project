  const OpenNav = () => {
    document.getElementById('sidenavbarid').style.width = "250px";
  }

    const closeNave = () => {
    document.getElementById('sidenavbarid').style.width = "0";
  }



// function showImg(h) {
// 	var link = "http://127.0.0.1:8000/media_files/cars/img/"; 
//  	const showImage = document.querySelector('.showImage').innerHTML = "<img src='"+ link + h + ".png' />";
//  	document.getElementById('select-image').value = link + h + ".png"
//   document.getElementById('showText').innerHTML = 'This image just for showing car category';

  
// }



// for geolocations 

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else { 
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  document.getElementById('c-let').value = position.coords.latitude;
	document.getElementById('c-log').value = position.coords.longitude;
}


// for geolocations end


// Search open And Close


// post popup box


var booking_modal = document.getElementById("bookingModel");
 
function BookBtn(){
  booking_modal.style.display = "block";
 }
function bookCloseBtn() {
  booking_modal.style.display = "none";
}


// post popup box end

window.onload = intAll;
var subimtBtn

function intAll(){
  var subimtBtn = document.getElementById('add-car-submit')
  subimtBtn.onclick = dataSubmit;
}

function dataSubmit(){
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else { 
    x.innerHTML = "Geolocation is not supported by this browser.";}

  function showPosition(position) {
   var let_1 = position.coords.latitude;
    var long_1 = position.coords.longitude;

    var full_name = document.getElementById('full-name').value;
    var post_title = document.getElementById('post-title').value;
    var post_id = document.getElementById('post-id').value;
    var post_user_id = document.getElementById('post-user-id').value;
    var phone_no = document.getElementById('phone-no').value;
    var address = document.getElementById('address').value;
    var start_date = document.getElementById('start-date').value;
    var end_date = document.getElementById('end-date').value;
    var messages = document.getElementById('messages').value;
    if(full_name == ""){
        document.getElementById('full-name').style.borderColor = "red";
    }else if(post_title==""){
        document.getElementById('post-title').style.borderColor = "red";
    }else if(phone_no=="" && phone_no.length <= 11){
        document.getElementById('phone-no').style.borderColor = "red";
    }else if(address==""){
        document.getElementById('address').style.borderColor = "red";
    }else if(start_date==""){
        document.getElementById('start-date').style.borderColor = "red";
    }else if(end_date==""){
        document.getElementById('end-date').style.borderColor = "red";
    }else if(messages==""){
        document.getElementById('messages').style.borderColor = "red"; 
    }else{
          document.getElementById("loding-img").style.display = "block";
          var req = new XMLHttpRequest();
          var url = '/booking_request?full_name='+full_name+'&post_title='+post_title+'&post_id='+post_id+'&post_user_id='+post_user_id+'&phone_no='+phone_no+'&address='+address+'&start_date='+start_date+'&end_date='+end_date+'&messages='+messages+'&let_1='+let_1+'&long_1='+long_1;
          req.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
          if(req.responseText == 'empty'){
            var msg = "Please fill all fields"
            document.getElementById('show-msg').innerHTML = msg; 
          }else if(req.responseText == 'true'){
            document.getElementById("loding-img").style.display = "none";
            var msg = "Thanks, we will contact you"
            document.getElementById('show-msg').innerHTML = msg; 

            document.getElementById('full-name').value = "";
            document.getElementById('post-title').value = "";
            document.getElementById('post-id').value = "";
            document.getElementById('post-user-id').value = "";
            document.getElementById('phone-no').value = "";
            document.getElementById('address').value = "";
            document.getElementById('start-date').value = "";
            document.getElementById('end-date').value = "";
            document.getElementById('messages').value = "";
          }else{
            var msg = "Please fill this form"
            document.getElementById('show-msg2').innerHTML = msg;
          }
      }
    };
    req.open("GET", url, true);
    req.send();
    }
  }
}   

