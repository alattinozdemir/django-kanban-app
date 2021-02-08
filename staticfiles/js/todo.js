$(document).ready(function(){
    $("#loginButton").click(function(){
       try{
       var serializedData=$("#LoginForm").serialize();
        $.ajax({
        url:'/login/',
        data:serializedData,
        type:'post',
        success:function(response){
                if(response.bilgi=="0"){
                    $("#loginresult").text("Kullanıcı adı veya şifre yanlış!");
                    $("#LoginForm")[0].reset();
                 }else if (response.bilgi=="1"){
                 window.location.href = '/'
                }
            },
        error: function(xhr){
          alert(xhr.responseText);
        }
         });
       }
       catch(err) {
           alert(err.message);
       }
    });

    //-----------------------------------------

     $("#addpbiButton").click(function(){
     try{
       var serializedData=$("#AddPbiForm").serialize();
        $.ajax({
        url:'/add_pbi/',
        data:serializedData,
        type:'post',
        success:function(response){
            if(response.bilgi=="1"){
                $("#pbiresult").text("PBI ekleme işlemi başarılı");
                 //$("#AddPbiForm")[0].reset();
             }else if (response.bilgi=="0"){
                 $("#pbiresult").text("PBI ekleme işlemi başarısız");
             }
        },
        error: function(xhr){
          alert(xhr.responseText);
        }
       });
       }
       catch(err) {
           alert(err.message);
       }
    });
    //---------------------------------
    $("#updatepbiButton").click(function(){
        try{
            var id =$("#updatepbiButton").val();
            var drop_box_dep_value =$("#exampleFormControlSelect1").val();
            var drob_box_sprint_value =$("#exampleFormControlSelect2").val();
            var serializedData1=$("#PbiUpdateForm").serialize();
            $.ajax({
            url:"/update_pbi/",
            data:serializedData1 + '&id=' + id+ '&drop_box_dep_value=' + drop_box_dep_value+'&drob_box_sprint_value=' + drob_box_sprint_value,
            type:'post',
            success:function(response){
             if (response.bilgi==1)
            {
                alert("Güncelleme yetkiniz yok!");
                window.location.href = "/pbis/";

            }else if(response.bilgi==0)
            {
                window.location.href = "/login/";

            }else
            {
            table_update(response);

            }
            },
            error: function(xhr){
            alert(xhr.responseText);
            }
             });
          }
        catch(err) {
           alert(err.message);
          }
       });

//--------------------------------------------------
 $("#btnSprintGecisi").click(function(){
        try{
           var drob_box_sprint_value =$("#db_for_sprint_gecisi").val();
           var drob_box_new_sprint_value=$("#db_for_sprint_gecisi_yeni").val();

            if (drob_box_sprint_value==null)
            {
                alert("Lütfen geçişi yapılacak sprtinti seçiniz!");
                return;
            }
            if (drob_box_new_sprint_value==null)
            {
            alert("Lütfen yeni sprint seçiniz!")
            return;
            }
            $.ajax({
            url:"/sprint_gecisi_done/",
            data:'drob_box_sprint_value=' + drob_box_sprint_value+ '&drob_box_new_sprint_value=' + drob_box_new_sprint_value,
            type:'get',
            success:function(response){
               window.opener.location.reload();
               window.close()
             },
            error: function(xhr){
               alert(xhr.responseText);
            }
            });
           }
        catch(err) {
           alert(err.message);
          }
       });
//-------------------------------------

 $("#mod_button").click(function(){
        try{
         var drob_box_sprint_value =$("#db_for_sprint_gecisi").val();
           var drob_box_new_sprint_value=$("#db_for_sprint_gecisi_yeni").val();

            if (drob_box_sprint_value==null)
            {
                alert("Lütfen geçişi yapılacak sprtinti seçiniz!");
                return;
            }
            if (drob_box_new_sprint_value==null)
            {
            alert("Lütfen yeni sprint seçiniz!")
            return;
            }
            $.ajax({
            url:"/sprint_gecisi_done/",
            data:'drob_box_sprint_value=' + drob_box_sprint_value+ '&drob_box_new_sprint_value=' + drob_box_new_sprint_value,
            type:'get',
            success:function(response){
               if(response.bilgi==1){
                 alert("Sprint geçişi yapılımıştır!");
                 $('#exampleModal').hide();
                 window.location.href = "/pbis/";
              }else if(response.bilgi==2)
              {
                alert("Sprint greçişi yapmaya yetkiniz yok!");
                $('#exampleModal').hide();
                 window.location.href = "/pbis/";
              }else if(response.bilgi==0)
              {
                 $('#exampleModal').hide();
                  window.location.href = "/login/";

              }else
              {
               alert("Bir hata oluştu!");
               $('#exampleModal').hide();
                 window.location.href = "/pbis/";

              }
             },
            error: function(xhr){
               alert(xhr.responseText);
            }
            });

        }
        catch(err) {
           alert(err.message);
          }
       });
//----------------------------------------------------
$("body").on('click','#btnDelete',function(){
        try{
        var id =$(this).attr('value');
        var drop_box_dep_value =$("#exampleFormControlSelect1").val();
        var drob_box_sprint_value =$("#exampleFormControlSelect2").val();
        $.ajax({
        url:"/delete_pbi/",
        data:'id=' + id+ '&drop_box_dep_value=' + drop_box_dep_value+'&drop_box_sprint_value=' + drob_box_sprint_value,
        type:'get',
        success:function(response){
            if (response.bilgi==0)
            {
                alert("Silme yetkiniz yok!");
                return;

            }else if(response.bilgi==1)
            {
                window.location.href = "/login/";
                return;
            }else
            {
            table_update(response)

            }



        },
        error: function(xhr){
            alert(xhr.responseText);
         }
        });
        scroll1 = $(window).scrollTop();
        $("html, body").animate({ scrollTop: scroll1 });
        }
        catch(err) {
           alert(err.message);
          }
});
//----------

function convertCanvasToImage(canvas) {
	var image = new Image();
	image.src = canvas.toDataURL("image/png");
	image1 = image.src.replace('data:image/png;base64,', '');
	return image1;
}
$("body").on('click','#btnMail',function(){
        try{
       var drob_box_sprint_value =$("#dbox_sprint_filter_report").val();
      //alert(drob_box_sprint_value);
       var canvas1=document.getElementById('canvas');
       var context1 = canvas1.getContext('2d');
       var canvas2=document.getElementById('pie-chart');
       var context2 = canvas1.getContext('2d');
       // alert('drob_box_sprint_value=' +  convertCanvasToImage(canvas1))
         $.ajax({
         url:"/send_mail_content/",
         data:'base_64_for_bar=' + convertCanvasToImage(canvas1)+ '&base_64_for_pie=' + convertCanvasToImage(canvas2)+ '&drob_box_sprint=' + drob_box_sprint_value,
         type:'get',
         success:function(response){
              if(response.bilgi==1){
                 alert("Mail gönderilmiştir!");

              }else if(response.bilgi==2)
              {
                alert("Mail gönderme yetkiniz yok!");

              }else if(response.bilgi==0)
              {

                  window.location.href = "/login/";

              }else
              {
               alert("Bir hata oluştu!");


              }


          },
          error: function(xhr){

          alert(xhr.responseText);

           }
         });
         }
         catch(err) {
           alert(err.message);
         }

});

//------------------------------------------------------
$('body').on('change', '#exampleFormControlSelect1', function() {
    try {
        var drob_box_department =$(this).val();
        var drob_box_sprint =$("#exampleFormControlSelect2").val();
         $.ajax({
         url:"/filter_pbi/",
         data:'id=' + drob_box_department+ '&drob_box_sprint=' + drob_box_sprint,
         data:'id=' + drob_box_department+ '&drob_box_sprint=' + drob_box_sprint,
         type:'get',
         success:function(response){
            table_update(response)
          },
          error: function(xhr){

           alert(xhr.responseText);

           }
         });
       }
   catch(err) {
      alert(err.message);
    }
});
//------------------------------------------
$('body').on('change', '#exampleFormControlSelect2', function() {
  try{
  var drob_box_sprint =$(this).val();
  var drob_box_department =$("#exampleFormControlSelect1").val();
  //alert(drob_box_sprint);

  $.ajax({
        url:"/filter_pbi/",
         data:'id=' + drob_box_department+ '&drob_box_sprint=' + drob_box_sprint,
        type:'get',
        success:function(response){

            table_update(response)

        },
        error: function(xhr){
           alert(xhr.responseText);
        }
   });
   }
   catch(err) {
      alert(err.message);
    }
});
//-------------------------------------------------------
$('body').on('change', '#dbox_sprint_filter_report', function() {
  try{
  var drob_box_sprint =$(this).val();
  $.ajax({
        url:"/filter_report/",
        data:'drob_box_sprint=' + drob_box_sprint,
        type:'get',
        success:function(response){
        table_update_for_report(response);

        //------pie-----------------------
         $('#div_pie').html(''); //remove canvas from container
         $('#div_pie').html('<canvas id="pie-chart"></canvas>'); //add it b
         var ctx = document.getElementById('pie-chart').getContext('2d');
         var myPieChart = new Chart(ctx, {
         type: 'pie',
          data: {
             datasets: [{
             data: response.data,
             backgroundColor: [
            '#00FF00', '#FF0000'
             ],
             label: 'Population'
            }],
            labels: response.labels
        },

        options:{
            responsive: true,
              plugins: {
              labels: {
              render: 'percentage',
              fontColor: ['black', 'black'],
              precision: 2
               }
        },
            title: {
				display: true,
				text: 'Succes / Fail Durumu'
				}
         }
         });
         //------pie end-----------------------
         var barChartData = {
			labels: ['TODO', 'INPROGRESS', 'DONE'],
			datasets: [{
				label: '3 İş Günü',
				backgroundColor:'#FF0000',//red
                stack: 'Stack 0',
				data: response.data_bar_3_day,
			},
			 {
				label: '5 İş Günü',
				backgroundColor: '#FF8C00',//orange
                stack: 'Stack 0',
				data: response.data_bar_5_day,
			},{
				label: '10 İş Günü',
				backgroundColor: '#FFFF00',//yellow
                stack: 'Stack 0',
				data: response.data_bar_10_day,
			}]

		};
		//var canvas=document.getElementById('canvas');
        //var context = canvas.getContext('2d');

       // alert(canvas.width);

        //context.clearRect(0, 0, canvas.width, canvas.height);
        $('#div_bar').html(''); //remove canvas from container
        $('#div_bar').html('<canvas id="canvas"></canvas>'); //add it back to the container
        var ctx1 = document.getElementById('canvas').getContext('2d');
        var myPieChart1 = new Chart(ctx1, {
         type: 'bar',
         data: barChartData,
         options: {
                    title: {
					    display: true,
					    text: 'PBI Type'
					},
                     plugins: {
                         labels: {
                         render: 'value',
                         fontColor: ['black', 'black', 'black'],
                          precision: 2
                            }
                       },
					tooltips: {
					    mode: 'index',
					    intersect: false
					},
					responsive: true,
					scales: {
					    xAxes: [{
					        stacked: true,
					    }],
					    yAxes: [{
					        stacked: true,
                        }]
					    }
				}
         });
         //------------------------bar end----------------


        },
        error: function(xhr){
           alert(xhr.responseText);
        }
   });
   }
   catch(err) {
      alert(err.message);
    }
});
//---------------------------------------------------
$('body').on('change', '#id_department', function() {
  var drob_box =$(this).val();
   //alert(drob_box);
   //$("#id_pbi_id").val("Kullanıcı adı veya şifre yanlış!");

});
//-------------------------------------------------
     function table_update(response)
         {var table = "<table id='example' class='table table-striped table-bordered table-sm' style='width:100%; font-size: 13px;'>";
          table+="<thead>";
          table+="<tr>"
             table+="<th>Id</th>";
             table+="<th>Department</th>";
             table+="<th>Sprint</th>";
             table+="<th>Type</th>";
             table+="<th>PBI</th>";
             table+="<th>Classification</th>";
             table+="<th>Workorder Date</th>";
             table+="<th>Start Date</th>";
             table+="<th>Finish Date</th>";
             table+=" <th>Actual Date</th>";
             table+="<th>Update</th>";
             table+=" <th>Delete</th>";
             table+=" </tr>";
             table+="</thead>";
             table+="<tbody>";
             for(var i=0; i<response.length;i++)
            {
                //alert(response[i].department);
                 table+="<tr value=";
                 table+=response[i].end_day_index;
                 table+=">";
                 table+="<td class='align-middle'  bgcolor=";
                 if(response[i].end_day_index=="3")
                 {
                    table+="red";
                 }else if(response[i].end_day_index=="5")
                 {
                    table+="orange";
                 }else
                 {
                    table+="yellow";
                 }
                 table+=">"
                 table+=response[i].id;
                 table+="</td>";
                 table+="<td class='align-middle'>";
                 table+=response[i].department;
                 table+="</td>";
                  table+="<td class='align-middle'>";
                 table+=response[i].sprint;
                 table+="</td>";
                  table+="<td class='align-middle'>";
                 table+=response[i].pbi_type;
                 table+="</td>";
                  table+="<td class='align-middle'>";
                 table+=response[i].pbi;
                 table+="</td>";
                  table+="<td class='align-middle'>";
                 table+=response[i].classficition;
                 table+="</td>";
                 table+="<td class='align-middle'>";
                 //table+=$.date(response[i].workorder_date);
                 table+=date_1970(response[i].workorder_date);
                 table+="</td>";
                 table+="<td class='align-middle'>";
                 table+= date_1970(response[i].start_date);
                 table+="</td>";
                  table+="<td class='align-middle'>";
                 table+=date_1970(response[i].finish_date);
                 table+="</td>";
                 table+="<td class='align-middle'>";
                 table+=date_1970(response[i].actual_date);
                 table+="</td>";
                 table+="<td class='align-middle'>";
                 table+="<a href='#' class='btn btn-dark' id='btnSelect' value="+response[i].id +">Update</a>";
                 table+="</td>";
                 table+="<td class='align-middle'>";
                 table+="<a href='#' class='btn btn-dark' id='btnDelete' value="+response[i].id +">Delete</a>";
                 table+="</td>";

                 table+="</tr>"
                 }
             table+="</tbody>";
             table+= "</table>";
              var div = document.getElementById('div_list_pbis');
              div.innerHTML = table;


         }

//-------------------------------------------------
     function table_update_for_report(response)
         {var table = "<table id='example' class='table table-striped table-bordered table-sm' style='width:100%; font-size: 13px;'>";
          table+="<thead>";
          table+="<tr>"

             table+="<th>Department</th>";
             table+="<th>TODO</th>";
             table+="<th>INPROGRESS</th>";
             table+="<th>DONE</th>";

             table+="<tbody>";
             for(var i=0; i<response.list_all_dep_pbi_type.length;i++)
            {
                //alert(response[i].department);
                 table+="<tr>";
                 table+="<td>";
                 table+=response.list_all_dep_pbi_type[i].department;
                 table+="</td>";
                 table+="<td>";
                 table+=response.list_all_dep_pbi_type[i].todo_count;
                 table+="</td>";
                 table+="<td>";
                 table+=response.list_all_dep_pbi_type[i].inporogress_count;
                 table+="</td>";
                  table+="<td>";
                 table+=response.list_all_dep_pbi_type[i].done_count;
                 table+="</td>";
                 table+="</tr>"
                 }
             table+="</tbody>";
             table+= "</table>";
             var div = document.getElementById('div_list_pbi_type_list');
             div.innerHTML = table;


         }
//------------------------------------------------
function date_1970(date_index)
{
            var table_td_val="";
            if(date_index==null)
                {
                table_td_val="";

                }
                else
                {
                 table_td_val=$.date(date_index);
                }
              return table_td_val;
}
//--------------------------------
$.date = function(dateObject) {
    var d = new Date(dateObject);
    var day = d.getDate();
    var month = d.getMonth() + 1;
    var year = d.getFullYear();
    if (day < 10) {
        day = "0" + day;
    }
    if (month < 10) {
        month = "0" + month;
    }
    var date = day + "/" + month + "/" + year;
    return date;


};
//---------------------------
 $("#btnExport").click(function(){
        var drob_box_sprint_value =$("#dbox_sprint_filter_report").val();
        //var csrftoken = $("[name=csrfmiddlewaretoken]").val();


        $.ajax({
        url:"/export_to_excel/",
        data:'drob_box_sprint_value=' + drob_box_sprint_value,
         xhrFields: {
        responseType: 'blob' // to avoid binary data being mangled on charset conversion
         },
        type:'get',
        success:function(blob, status, xhr){
        var filename = "";
        var disposition = xhr.getResponseHeader('Content-Disposition');
        if (disposition && disposition.indexOf('attachment') !== -1) {
            var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
            var matches = filenameRegex.exec(disposition);
            if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
        }

        if (typeof window.navigator.msSaveBlob !== 'undefined') {
            // IE workaround for "HTML7007: One or more blob URLs were revoked by closing the blob for which they were created. These URLs will no longer resolve as the data backing the URL has been freed."
            window.navigator.msSaveBlob(blob, filename);
        } else {
            var URL = window.URL || window.webkitURL;
            var downloadUrl = URL.createObjectURL(blob);

            if (filename) {
                // use HTML5 a[download] attribute to specify filename
                var a = document.createElement("a");
                // safari doesn't support this yet
                if (typeof a.download === 'undefined') {
                    window.location.href = downloadUrl;
                } else {
                    a.href = downloadUrl;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                }
            } else {
                window.location.href = downloadUrl;
            }

            setTimeout(function () { URL.revokeObjectURL(downloadUrl); }, 100); // cleanup
        }

          },
          error: function(xhr){
           alert(xhr.responseText);
        }
        });
     });


});

