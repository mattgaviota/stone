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

  	$("#desde").datepicker({
   		changeMonth: true
   	});

  	$("#hasta").datepicker({
   		changeMonth: true
   	});

   	$("input[name=dia]").datepicker({
   		changeMonth: true
   	});

  	$("#desde2").datepicker({
   		changeMonth: true
   	});

  	$("#hasta2").datepicker({
   		changeMonth: true
   	});

   	$("input[name=dia2]").datepicker({
   		changeMonth: true
   	});

  	$(".filtro").hide();
  	$(".filtrodia").show();
	$("input[name=filtro_radio]").click(function(){
		var seleccion = $(this).val();
    	$(".filtro").hide();
    	$("."+seleccion).show();
    });

	$(".filtro2").hide();
  	$(".filtrodia2").show();
	$("input[name=filtro_radio2]").click(function(){
		var seleccion = $(this).val();
    	$(".filtro2").hide();
    	$("."+seleccion).show();
    });

	/*
	 * Petición ajax que se realiza al presionar el botón de filtrar en la pestaña servicios por facultad
	 */
	$(".boton-filtrar").click(function(){

		if( $("input[name=filtro_radio]:checked").val() === "filtrodia"){
			desde = $("input[name=dia]").val();
			hasta = $("input[name=dia]").val();
		}else if ($("input[name=filtro_radio]:checked").val() === "filtrointervalo"){
			desde = $("input[name=desde]").val();
			hasta = $("input[name=hasta]").val();
		}

		//Si tenemos valor distinto de nulo, hacemos la petición ajax
		if(desde != '' && hasta != '' && desde <= hasta){
			
			$.ajax({
				type: "post",
				url: base_url + "index.php/reportes/obtener_registros_tickets",
				cache: false,				
				data:{
					desde: desde,
					hasta: hasta
				},
				success: function(response){
					
					$('#resultado_tickets_tabla').html("");
					var obj = JSON.parse(response);
					
					if(obj.tickets.length > 0){
						try{
							var items = [];
							$.each(obj.tickets, function(i,val){
								cadena = '<tr>'+'<td>'+ val.facultad +'</td>'+'<td>'+ val.total_tickets +'</td>'+'<td>'+ val.becados +'</td>'+'<td>'+ val.regulares +'</td>' +'<td>'+ val.gratuitos +'</td>'+'<td>'+ val.total_pesos +'</td></tr>';
								items.push(cadena);	
							});
							$.each(obj.totales, function(i,val){
								cadena = '<tr class="info">'+ '<td>Totales</td>' + '<td>'+ val.total_tickets +'</td>' + '<td>'+ val.becados +'</td>' + '<td>'+ val.regulares +'</td>' + '<td>'+ val.gratuitos +'</td>' + '<td>'+ val.total_importe +'</td>' + '</tr>';
								items.push(cadena);
							});
							$('#resultado_tickets_tabla').append.apply($('#resultado_tickets_tabla'), items);
						}catch(e) {		
							alert('Error');
						}		
					}else{
						$('#resultado_tickets_tabla').html($('<tr/>').text(" No Se encontraron registros"));		
					}		
				},
				error: function(){						
					alert('Error en la respuesta');
				}
			});//fin ajax
		}//Fin if
	});//fin evento
	
	

	/*
	 * Petición ajax que se realiza al presionar el botón de filtrar en la pestaña clasificación de tickets
	 */
	$(".boton-filtrar2").click(function(){

		if( $("input[name=filtro_radio2]:checked").val() === "filtrodia2"){
			desde2 = $("input[name=dia2]").val();
			hasta2 = $("input[name=dia2]").val();
		}else if ($("input[name=filtro_radio2]:checked").val() === "filtrointervalo2"){
			desde2 = $("input[name=desde2]").val();
			hasta2 = $("input[name=hasta2]").val();
		}

		//Si tenemos valor distinto de nulo, hacemos la petición ajax
		if(desde != '' && hasta != '' && desde <= hasta){
			
			$.ajax({
				type: "post",
				url: base_url + "index.php/reportes/obtener_clasificacion_tickets",
				cache: false,
				data:{
					desde2: desde2,
					hasta2: hasta2
				},
				success: function(response){
					
					$('#resultado_tickets_tabla2').html("");
					var obj = JSON.parse(response);
					
					if(obj.tickets2.length > 0){
						try{
							var items = [];
							$.each(obj.tickets2, function(i,val){
								cadena = '<tr>'+'<td>'+ val.facultad +'</td>'+'<td>'+ val.total_tickets +'</td>'+'<td>'+ val.anulados +'</td>'+'<td>'+ val.activos +'</td>' +'<td>'+ val.impresos +'</td>'+'<td>'+ val.consumidos +'</td></tr>';
								items.push(cadena);	
							});
							$.each(obj.totales2, function(i,val){
								cadena = '<tr class="info">'+ '<td>Totales</td>' + '<td>'+ val.total_tickets +'</td>' + '<td>'+ val.anulados +'</td>' + '<td>'+ val.activos +'</td>' + '<td>'+ val.impresos +'</td>' + '<td>'+ val.consumidos +'</td>' + '</tr>';
								items.push(cadena);
							});							
							$('#resultado_tickets_tabla2').append.apply($('#resultado_tickets_tabla2'), items);
						}catch(e) {		
							alert('Error');
						}		
					}else{
						$('#resultado_tickets_tabla2').html($('<tr/>').text(" No Se encontraron registros"));		
					}		
				},
				error: function(){						
					alert('Error en la respuesta');
				}
			});//fin ajax
		}//Fin if
	});//fin evento

});

window.onload = function () { 
    $("input[value='filtrodia']").prop("checked", true);
    $("input[value='filtrodia2']").prop("checked", true);
}