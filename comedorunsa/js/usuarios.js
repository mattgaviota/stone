function buscar_ajax(){
	if($("#buscar_nombre").val().length >= 0 || $("#buscar_dni").val().length >= 0 || $("#buscar_lu").val().length >= 0){

		buscar_nombre = $("#buscar_nombre").val();
		buscar_dni = $("#buscar_dni").val();
		buscar_lu = $("#buscar_lu").val();

		$.ajax({
			type: "post",
			url: base_url + "index.php/usuarios/search",
			cache: false,				
			data:{
				buscar_nombre:buscar_nombre,
				buscar_dni:buscar_dni,
				buscar_lu:buscar_lu
			},
			success: function(response){
				$('#destino_resultado').html("");
				var obj = JSON.parse(response);
				if(obj.length > 0){
					try{
						var items = []; 	
						$.each(obj, function(i,val){
							if(val.estado == '0'){
								clase = 'danger';
							}else if(val.estado == '3'){
								clase = 'warning';
							}else{
								clase = '';
							}
							cadena = '<tr class="' + clase + '">'+'<td>'+ val.dni +'</td>'+'<td>'+ val.nombre +'</td>'+'<td>'+ val.lu +'</td>'+'<td>'+ val.facultad +'</td>'+'<td>'+ val.categoria +'</td>';
							ruta = "'"+base_url+ "usuarios/edit/" +val.dni +"'";
							cadena = cadena + '<td><a class="glyphicon glyphicon-pencil" href='+ ruta +'"> </a></td>'+'</tr>';
							items.push(cadena);
						});	
						$('#destino_resultado').append.apply($('#destino_resultado'), items);
					}catch(e) {		
						alert('Error');
					}		
				}else{
					$('#destino_resultado').html($('<tr/>').text("No Se encontraron registros"));
				}		
				
			},
			error: function(){						
				alert('Error en la respuesta');
			}
		});
	}
	//return false;	
}

$(document).ready(function(){
	$("#buscar_nombre").keyup(buscar_ajax);
	$("#buscar_dni").keyup(buscar_ajax);
	$("#buscar_lu").keyup(buscar_ajax);
});

window.onload = function () {
 	$("#buscar_nombre").val("");
    $("#buscar_dni").val("");
    $("#buscar_lu").val("");
}