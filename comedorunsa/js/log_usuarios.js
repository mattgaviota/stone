function filtrar_ajax(){
	accion = $('#drop_down').val();
	buscar_dni = $("#buscar_dni").val();
	
	$.ajax({
		type: "post",
		url: base_url + "index.php/log_usuarios/filtrar",
		cache: false,
		data:{
			accion:accion,
			buscar_dni:buscar_dni
		},
		success: function(response){
			$('#destino_resultado').html("");
			var obj = JSON.parse(response);
			if(obj.length > 0){
				try{
					var items = [];
					$.each(obj, function(i,val){
						cadena = '<tr>'+'<td>'+ val.id +'</td>'+'<td>'+ val.dni +'</td>'+'<td>'+ val.fecha +'</td>'+'<td>'+ val.accion +'</td>'+'<td>'+ val.lugar +'</td>'+'<td>'+ val.descripcion +'</td>'+'</tr>';
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

$(document).ready(function() {
	$('#drop_down').change(filtrar_ajax);
	$("#buscar_dni").keyup(filtrar_ajax);
	$("#buscar_fecha").keyup(filtrar_ajax);
});

window.onload = function () { 
    $("#buscar_dni").val("");
    $("#drop_down").val("0");
}