
window.onload = function () {
  document.getElementById('regBtn').onclick = update;
  document.getElementById("open").onclick = open;
  document.getElementById("upload").onclick = upload;
  // 触发拍照动作
  document.getElementById("snap").addEventListener("click", function() {
    //获得Canvas对象
    var canvas = document.getElementById("canvas");
    var context = canvas.getContext("2d");
    context.drawImage(video,0,0,640,480);
  });
}

function open(){
  //获得video摄像头区域
  var video = document.getElementById("video");
  var videoObj = {
    "video" : true
  };
  var errBack = function(error) {
    console.log("Video capture error: ", error.code);
  };
  //获得摄像头并显示到video区域
  if (navigator.getUserMedia) { // Standard
    navigator.getUserMedia(videoObj, function(stream) {
      video.srcObject = stream;
      video.play();
    }, errBack);
  } else if (navigator.webkitGetUserMedia) { // WebKit-prefixed
    navigator.webkitGetUserMedia(videoObj, function(stream) {
      video.src = window.webkitURL.createObjectURL(stream);
      video.play();
    }, errBack);
  } else if (navigator.mozGetUserMedia) { // Firefox-prefixed
    navigator.mozGetUserMedia(videoObj, function(stream) {
      video.src = window.URL.createObjectURL(stream);
      video.play();
    }, errBack);
  }
}

function convertBase64UrlToBlob(urlData,type){
    var bytes=window.atob(urlData.split(',')[1]);        //去掉url的头，并转换为byte
    //处理异常,将ascii码小于0的转换为大于0
    var ab = new ArrayBuffer(bytes.length);
    var ia = new Uint8Array(ab);
    for (var i = 0; i < bytes.length; i++) {
        ia[i] = bytes.charCodeAt(i);
    }
    return new Blob( [ab] , {type : 'image/'+type});
}

function upload(){
  var canvas = document.getElementById("canvas");
  var dataURL = canvas.toDataURL("image/png",1.0);
  var file1=convertBase64UrlToBlob(dataURL,"png");

  var formData = new FormData();
  // var myid=$("#ID");
  var myid = document.getElementById('ID').value;
  var myfile = file1;
  // var myfile=$("#image");
  formData.append('id', myid);
  formData.append('image',myfile);
  // formData.append('image', $('#image')[0].files);
  // formData.append('id', $('#ID').val());
  // var formData = new FormData($('#uploadForm')[0]);
  $.ajax({
      // url: "127.0.0.1:8081/file_upload",
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
      }
  });
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
