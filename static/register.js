
window.onload = function () {
  document.getElementById('regBtn').onclick = update;
}

function update(){
    var formData = new FormData();
    // var myid=$("#ID");
    var myid = document.getElementById('ID').value;
    var myfile = document.getElementById('image').files[0];
    // var myfile=$("#image");
    formData.append('id', myid);
    formData.append('image',myfile);
    // formData.append('image', $('#image')[0].files);
    // formData.append('id', $('#ID').val());
    // var formData = new FormData($('#uploadForm')[0]);
    $.ajax({
        //url: "/file_upload",
        // url: "/testpost",
        url: "/signup",
        type: "post",
        async: false,
        data: formData,
        //dataType: "json",
        cache: false,
        processData: false,
        contentType: false,
        success: function (data) {
            alert(data);
            alert("success");
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyStatus);
            alert(textstatus);
        }
    });
}

// $('#regBtn').on('click', function () {
//   alert("update");
//   var formData = new FormData($("#regForm")[0]);
//   $.ajax({
//     url: "/file_upload",
//     type: "POST",
//     async: false,
//     data: formData,
//     dataType: "json",
//     cache: false,
//     processData: false,
//     contentType: false,
//     success: function (data) {
//       if(data[0]=='success'){
//         alert("success!");
//         show();
//       }
//       else{
//         alert("err");
//       }
//     },
//     error: function (XMLHttpRequest, textStatus, errorThrown) {
//       alert(XMLHttpRequest.status);
//       alert(XMLHttpRequest.readyStatus);
//       alert(textstatus);
//     }
//   });
// });
