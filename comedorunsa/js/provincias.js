$(document).ready(function(){
	$("#buscar").keyup(function(){
		if($("#buscar").val().length >= 0){
			$.ajax({
				type: "post",
				url: base_url + "index.php/provincias/search",
				cache: false,				
				data:'buscar='+$("#buscar").val(),
				success: function(response){
					$('#destinoResultado').html("");
					var obj = JSON.parse(response);
					if(obj.length > 0){
						try{
							var items = []; 	
							$.each(obj, function(i,val){
								cadena = '<tr>'+'<td>'+ val.id +'</td>'+'<td>'+ val.nombre +'</td>'+'<td>'+ val.created +'</td>'+'<td>'+ val.updated +'</td>';
								cadena = cadena + '<td><a class="glyphicon glyphicon-pencil" data-toggle="modal" data-target="' + '#myModal' + val.id + '"></a></td>'+'</tr>';
								items.push(cadena);
							});	
							$('#destinoResultado').append.apply($('#destinoResultado'), items);
						}catch(e) {		
							alert('Error');
						}		
					}else{
						$('#destinoResultado').html($('<tr/>').text(" No Se encontraron registros"));		
					}		
					
				},
				error: function(){						
					alert('Error en la respuesta');
				}
			});
		}
		//return false;
	});
});