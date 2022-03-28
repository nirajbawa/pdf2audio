console.log("success");

function inputtagvalidation()
{
    let start = document.getElementById("start");
    let end = document.getElementById("end");
    let formfile = document.getElementById("formFile");
    let getform = document.getElementById("upload");
    let getselect = document.getElementById("langpannel");
    // console.log("valudeis" + getselect.value);
    let fileinp = true;
  
    if (typeof (formfile.files) != "undefined") {
        var size = parseFloat(formfile.files[0].size / (1024 * 1024)).toFixed(2); 
        if(size > 300) {
            let alertmes = alert('make sure your file size if less then 300MB');
            location.reload();
            fileinp = false;
        }
    } 
    if(fileinp==true)
    {
    if(getselect.value==" ")
    {
            let getselectcheck = alert("alert you not select your pdf language please select your pdf text language");
    }
    else if(start.value==""||end.value=="")  
    {
        let getuserper = confirm("alert you not give page number form start and end.\n(if you not give page number we convert your pdf's first page only in audio)\npress 'ok' for continue and 'no' for cancel");
        if(getuserper==true)
        {
            start.value = 1;
            end.value = 1;
            loader();
            getform.submit();
        }
        else{
            location.reload();
        }
    }
    else{
        loader();
        getform.submit();
    }
    
}

else{
    location.reload();
}

}