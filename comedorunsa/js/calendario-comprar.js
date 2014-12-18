//Pintar los días sin tickets en rojo
$(document).ready(function(){
	var obj = null;

	dia_num = $(this).find('.dia_num').html();
	var pathArray = window.location.pathname.split( '/' );
	var year_num = pathArray[4];
	var month_num = pathArray[5];
	
	if(year_num == null){
		var f= new Date();
		month_num = f.getMonth() + 1;
		year_num = f.getFullYear();
	}

	$.ajax({
		type: "POST",
		url: base_url + "index.php/usuarios/get_dias",
		data: {
			dia:dia_num,
			year:year_num,
			month:month_num
		},
		success: function(data){

			obj = JSON.parse(data);
			if(obj.length > 0){
				try{
					var items = []; 	
					$.each(obj, function(i,val){
						if(val.tickets_disponibles == 0){
							cadena = 'td:contains('+ val.dia +')';
							$(cadena).first().css('background', '#FFB9C4');
						}
					});			
				}catch(e) {
					alert('Error Grave');
				}
			}else{
				alert("no hay registros sin tickets");
			}
		},
		error: function(){						
			alert('Error en la respuesta');
		}
	});

});

//Seleccionar días y enviarlos al backend
$(document).ready(function(){

	var dias_seleccionados = [];
	
	var q = new Date();
	var m = q.getMonth()+1;
	var d = q.getDay();
	var y = q.getFullYear();
	var hoy = new Date(y,m,d);

	//Seleccionamos los días, los pintamos de color amarillo y los agregamos al array dias_seleccionados para luego enviarlo al servidor
	$('.calendario .dia').click(function(){
		dia_seleccionado = $(this).find('.dia_num').html();
		fecha = new Date(year_num, month_num-1, dia_seleccionado);//Fundamental restar 1. Porque para js 0 = enero, 1 = feb....11 = dic.

		if(($(this).css('background-color')=="rgb(255, 255, 255)" || $(this).css('background-color')=="rgb(221, 238, 255)")){
			if($(this).find('.dia_num').html() != null && fecha >= hoy){
				
				$(this).css('background-color', '#f1c40f');
				dias_seleccionados.push($(this).find('.dia_num').html());
				
			}
		}else if($(this).css('background-color') == "rgb(241, 196, 15)"){
			$(this).css('background-color', '#DEF');
			var index = dias_seleccionados.indexOf($(this).find('.dia_num').html());
			if (index > -1) {
				dias_seleccionados.splice(index, 1);
			}
		}
	});

	//Enviamos los datos para confirmar los días seleccionados
	$('div#calendario #enviar-info').click(function(){
		if(dias_seleccionados.length > 0){
			//Si hay datos para enviar enviamos con ajax, de lo contrario no hacemos nada.
			$.ajax({
				type: "POST",
				url: base_url + "index.php/usuarios/realizar_compra",
				data: {
					year:year_num,
					month:month_num,
					datos:dias_seleccionados
				},
				success: function(data){
					cadena = "<h3>" + data + "</h3>";
					$('div#calendario #respuesta-compra').html(cadena);
					window.location.href = base_url + "usuarios/comprar_tickets";
				},
				error: function(){						
					alert('Error en la respuesta');
				}
			});
		}

	});
});


//Pintamos los días con tickets de color verde.
$(document).ready(function(){

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
		url: base_url + "index.php/usuarios/get_dias_tickets",
		data: {
			year:year_num,
			month:month_num
		},
		success: function(data){

			var obj = JSON.parse(data);
			if(obj.length > 0){
				try{
					var items = []; 	
					$.each(obj, function(i,val){
						cadena = 'td:contains('+ val.dia +')';
						$(cadena).first().css('background', '#2ecc71');
					});			
				}catch(e) {
					alert('Error Grave');
				}
			}else{
				alert("no hay registros comprados");
			}
		},
		error: function(){						
			alert('Error en la respuesta');
		}
	});	
});