<?php  if ( ! defined('BASEPATH')) exit('No direct script access allowed');

if ( ! function_exists('my_validation_errors'))
{
	function my_validation_errors($errors)
	{
		$salida = "";
		if($errors){
			$salida = "<div class='alert alert-dismissable alert-danger'>";
			$salida = $salida."<button type='button' class='close' data-dismiss='alert'>×</button>";
			$salida = $salida."<h4>Mensaje de validación</h4>";
			$salida = $salida."<strong>".$errors."</strong>";
			$salida = $salida."</div>";
		}
		return $salida;
	}
}

if ( ! function_exists('my_mensaje_confirmacion'))
{
	function my_mensaje_confirmacion($mostrar)
	{
		$salida = "";
		if($mostrar){
			$salida = "<div class='alert alert-dismissable alert-success'>";
			$salida = $salida."<button type='button' class='close' data-dismiss='alert'>×</button>";
			$salida = $salida."<h4>Mensaje de validación</h4>";
			$salida = $salida."<strong>"."Registración exitosa, revise su correo para obtener la contraseña"."</strong>";
			$salida = $salida."</div>";
		}
		return $salida;
	}
}

if( ! function_exists('my_menu_principal'))
{
	function my_menu_principal()
	{
		$opciones = '<li>'.anchor('home/index', 'Inicio').'</li>';
		if(get_instance()->session->userdata('dni_usuario')){
			$opciones = $opciones.'<li>'.anchor('usuarios/comprar_tickets', 'Comprar Tickets').'</li>';
		}else{
			$opciones = $opciones.'<li>'.anchor('home/ingreso', 'Ingreso').'</li>';
		}
		$opciones = $opciones.'<li>'.anchor('home/acerca_de', 'Acerca de').'</li>';
		return $opciones;
	}
}

if( ! function_exists('my_menu_principal_derecha'))
{
	function my_menu_principal_derecha()
	{
		$opciones = '';
		if(get_instance()->session->userdata('dni_usuario')){
			$opciones = $opciones.'<li>'.anchor('home/salir', 'Salir').'</li>';
		}else{
			$opciones = $opciones.'<li>'.anchor('home/ingreso', 'Ingreso').'</li>';
		}
		return $opciones;
	}
}

if( ! function_exists('my_menu_aplicacion'))
{
	function my_menu_aplicacion()
	{
		$opciones = null;
		if(get_instance()->session->userdata('dni_usuario')){
			$opciones = '';
			get_instance()->load->model('Model_Menu');
			$query = get_instance()->Model_Menu->allForMenu();

			foreach($query as $opcion){
				if($opcion->url != ''){
					$irA = $opcion->url;
					$parametros = array('target'=>'blank');
				}else{
					$irA = $opcion->controlador.'/'.$opcion->accion;
					$parametros = array();
				}
				$opciones = $opciones.'<li>'.anchor($irA, $opcion->nombre, $parametros).'</li>';
			}
		}
		return $opciones;
	}
}

if( ! function_exists('my_menu_collapse'))
{
	function my_menu_collapse()
	{
		$opciones = null;
		get_instance()->load->model('Model_Menu');
		get_instance()->load->model('Model_Tipos_Operaciones');
		if(get_instance()->session->userdata('dni_usuario')){
			$opciones = '';
			$query = get_instance()->Model_Menu->allForMenu();			

			foreach($query as $opcion){
				
				$contenido = '<ul>';

				$operaciones = get_instance()->Model_Tipos_Operaciones->get_operaciones($opcion->id);
				foreach ($operaciones as $operacion) {
					$irA = $operacion->controlador.'/'.$operacion->accion;
					$contenido = $contenido.'<li>'.anchor($irA, $operacion->nombre).'</li>';
				}
				$contenido = $contenido.'</ul>';

				$opciones = $opciones.'<div class="panel panel-default">';
				$opciones = $opciones.'<div class="panel-heading">';
				$opciones = $opciones.'<h4 class="panel-title">';
				$opciones = $opciones.'<a data-toggle="collapse" data-parent="#accordion" href="#'.$opcion->id.'" >';
				$opciones = $opciones.$opcion->nombre.'</a></h4></div>';
				$opciones = $opciones.'<div id="'.$opcion->id.'" class="panel-collapse collapse">';
				$opciones = $opciones.'<div class="panel-body">';
				$opciones = $opciones.$contenido.'</div></div></div>';
			}
		}else{

		}
		return $opciones;
	}
}

