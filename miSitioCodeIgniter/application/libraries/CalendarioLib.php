<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class CalendarioLib {

	function __construct(){
		$this->CI = & get_instance();//Obtener la instancia del objeto por referencia.
		$this->CI->load->model('Model_Calendario');//Cargamos el modelo.
	}

	public function my_validation($desde, $hasta){
		$unix_desde = strtotime($desde);
		$unix_hasta = strtotime($hasta);

		if($unix_desde < $unix_hasta){
			return TRUE;
		}else{
			return FALSE;
		}
	}

	//Generar los dias entre las fechas pasadas como parámetros y los insertará en la BD
	public function generar_dias($desde, $hasta){

		$this->CI->db->where('desde', $desde);
		$this->CI->db->where('hasta', $hasta);
		$query = $this->CI->db->get('calendario');

		//Si existe un único calendario con esas fechas de inicio y fin.
		if($query->num_rows() == 1){
			//generamos los dias
			$fechaInicio = strtotime($desde);
			$fechaFin = strtotime($hasta);

			//Obtenemos el id del calendario
			$id = $query->row('id');

			$data = array();

			//Incrementamos de 86400 segundos que representa un día
			for($i = $fechaInicio; $i <= $fechaFin; $i += 86400){

				//Nos saltamos los días domingo y sabado.
				if(date('l', $i) != 'Sunday' && date('l', $i) != 'Saturday'){
					$data['fecha'] = date('Y-m-d',$i);
					$data['tickets_totales'] = 700;
					$data['tickets_vendidos'] = 0;
					$data['id_calendario'] = $id;
					$data['evento'] = 'Día Hábil';
					$this->CI->db->set($data);
	    			$this->CI->db->insert('dias');					
	    			//echo date('d-m-Y',$i).'</br>';
				}
			}
		}
	}

}