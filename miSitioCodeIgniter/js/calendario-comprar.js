$(document).ready(function(){
	dia_num = $(this).find('.dia_num').html();
	nueva_url = window.location.protocol + "://" + window.location.host + "/" + window.location.pathname;
	var pathArray = window.location.pathname.split( '/' );
	year_num = pathArray[4];
	month_num = pathArray[5];
	
	if(year_num == null){
		var f= new Date();
		month_num = f.getMonth() + 1;
		year_num = f.getFullYear();
	}

	$.ajax({
		type: "POST",
		url: "http://localhost/miSitioCodeIgniter/index.php/usuarios/get_dias_calendario",
		data: {
			dia:dia_num,
			year:year_num,
			month:month_num
		},
		success: function(data){
			var obj = JSON.parse(response);
			if(obj.length > 0){
				try{
					var items = []; 	
					$.each(obj, function(i,val){
						if(val.tickets_disponibles == 0){
							$('td:contains(dia_num)').css('color', 'red');
						}
					});			
				}catch(e) {
					alert('Error');
				}
			}else{
				
			}
		},
		error: function(){						
			alert('Error en la respuesta');
		}
	});

});