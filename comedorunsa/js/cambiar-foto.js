$(document).ready(function(){
	$('.img-subir').click(function(){
    	$("input[name=userfile]").trigger('click');
	});
	$("input[name=userfile]").change(function(){
		$("#form-foto").submit();
		alert('cambio!');
	});

});