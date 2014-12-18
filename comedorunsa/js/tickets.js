function filtrar_ajax(){
	buscar_nombre = $('#buscar_nombre').val();
	buscar_dni = $("#buscar_dni").val();
	buscar_id = $("#buscar_id").val();
	buscar_fecha = $("#buscar_fecha").val();
	
	$.ajax({
		type: "post",
		url: base_url + "index.php/tickets/filtrar",
		cache: false,
		data:{
			buscar_nombre:buscar_nombre,
			buscar_dni:buscar_dni,
			buscar_id:buscar_id,
			buscar_fecha:buscar_fecha
		},
		success: function(response){
			$('#destino_resultado').html("");
			var obj = JSON.parse(response);
			if(obj.length > 0){
				try{
					var items = [];
					$.each(obj, function(i,val){
						var string_fecha = val.fecha;
						var fecha = string_fecha.substring(8,10) + '/' + string_fecha.substring(5,7) + '/' + string_fecha.substring(0,4);
						cadena = '<tr>'+'<td>'+ val.id_ticket +'</td>'+'<td>'+ fecha +'</td>'+'<td>'+ val.importe_ticket +'</td>'+'<td>'+ val.estado_ticket +'</td>'+'<td>'+ val.dni +'</td>'+'<td>'+ val.nombre_usuario +'</td>';
						ruta = "'"+base_url+ "tickets/detalles/" +val.id_ticket +"'";
						cadena = cadena + '<td><a class="glyphicon glyphicon-search" href='+ ruta +'"> </a></td>'+'</tr>';
						items.push(cadena);
					});
					$('#destino_resultado').append.apply($('#destino_resultado'), items);
				}catch(e) {
					alert('Error');
				}
			}else{
				$('#destino_resultado').html($('<tr/>').text(" No Se encontraron registros"));
			}		
			
		},
		error: function(){						
			alert('Error en la respuesta');
		}
	});
}

$(function($){
	$.datepicker.regional['es'] = {
	closeText: 'Cerrar',
	prevText: '&#x3c;Ant',
	nextText: 'Sig&#x3e;',
	currentText: 'Hoy',
	monthNames: ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
	'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
	monthNamesShort: ['Ene','Feb','Mar','Abr','May','Jun',
	'Jul','Ago','Sep','Oct','Nov','Dic'],
	dayNames: ['Domingo','Lunes','Martes','Mi&eacute;rcoles','Jueves','Viernes','S&aacute;bado'],
	dayNamesShort: ['Dom','Lun','Mar','Mi&eacute;','Juv','Vie','S&aacute;b'],
	dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','S&aacute;'],
	weekHeader: 'Sm',
	dateFormat: 'yy/mm/dd',
	firstDay: 1,
	isRTL: false,
	showMonthAfterYear: false,
	yearSuffix: ''};
	$.datepicker.setDefaults($.datepicker.regional['es']);
}); 


$(document).ready(function() {
  	$("#buscar_fecha").datepicker({
   		changeMonth: true
   	});

   	$('#buscar_nombre').keyup(filtrar_ajax);
	$("#buscar_dni").keyup(filtrar_ajax);
	$("#buscar_id").keyup(filtrar_ajax);
	$("#buscar_fecha").change(filtrar_ajax);
});


window.onload = function () { 
    $("#buscar_nombre").val("");
    $("#buscar_dni").val("");
    $("#buscar_id").val("");
    $("#buscar_fecha").val("");
}