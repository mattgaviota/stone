$(document).ready(function(){
	$('input#barcode').focus();	

	$(document).keypress(function(event){
		if (event.which == 13) {
		    event.preventDefault();

		    datos = $('input#barcode').val();

		    $('input#barcode').val("");//Borrar texto en el input text.
		    
		    if( datos != ''){

				$.ajax({
					type: "post",
					url: base_url + "index.php/usuarios/procesar_barcode",
					cache: false,
					data: {
						barcode:datos
					},
					success: function(response){
						$('div#info-usuario').html("");
						$('div#info-ticket').html("");
						var obj = JSON.parse(response);
						
						if(obj.length > 0){
							try{
								var items = [];
								$.each(obj, function(i,val){
									html_info_usuario = '<img data-src="holder.js/100%x180" style="width: 100%;" src="' + val.ruta + '"><br /><br />';
									html_info_usuario = html_info_usuario + '<label>DNI: ' + val.dni + '</label><br />';
									html_info_usuario = html_info_usuario + '<label>Nombre: ' + val.usuario_nombre + '</label><br />';
									html_info_usuario = html_info_usuario + '<label>L.U: '+ val.usuario_lu +'</label><br />';
									html_info_usuario = html_info_usuario + '<label>Facultad: '+ val.facultad_nombre +'</label><br />';
									html_info_usuario = html_info_usuario + '<label>Categoria: '+ val.categoria_nombre +'</label><br />';
									
									html_info_ticket = '<label>Número Ticket: ' + val.id_ticket + '</label><br />';
									html_info_ticket = html_info_ticket + '<label>Fecha: ' + val.fecha + '</label><br />';
									html_info_ticket = html_info_ticket + '<label>Importe: $' + val.importe + '</label><br />';
									html_info_ticket = html_info_ticket + '<label>Estado: ' + val.estado + '</label><br />';
									if(val.estado == 2){
										html_info_ticket = html_info_ticket + '<h1 class="valido">VÁLIDO</h1>';
									}else if(val.estado == 3) {
										html_info_ticket = html_info_ticket + '<div class="novalido"><h1>NO VÁLIDO</h1><span>Consumido el '+ val.fecha +'</span></div>';
									}else{
										html_info_ticket = html_info_ticket + '<div class="novalido"><h1>NO VÁLIDO</h1><span>Anulado el '+ val.fecha_log +'</span></div>';
									}
								});
								$('div#info-usuario').append(html_info_usuario);
								$('div#info-ticket').append(html_info_ticket);
							}catch(e) {
								alert('Error');
							}
						}else{
							//$('div#info-usuario').append('<h2>Usuario No Valido</h2>');
							$('div#info-ticket').append('<h2>Ticket No Valido</h2><br /><h3>No es del día de hoy</h3>');
						}
					},
					error: function(){
						alert('Error en la respuesta');
					}
				});//fin ajax
		    }//fin de if
		    
    	}
	});
});

