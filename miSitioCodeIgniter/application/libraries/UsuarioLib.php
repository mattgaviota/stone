<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

//Validar login de usuario, cambio de clave y CRUD en la tabla de usuarios
class UsuarioLib {

	function __construct(){
		$this->CI = & get_instance();//Obtener la instancia del objeto por referencia.
		$this->CI->load->model('Model_Usuarios');//Cargamos el modelo.
		$this->CI->load->model('Model_Perfiles');
		$this->CI->load->model('Model_Dias');
		$this->CI->load->model('Model_Log_Usuarios');
		$this->CI->load->model('Model_Tickets');
	}

	public function loginok($dni, $password){
		$query = $this->CI->Model_Usuarios->get_login($dni);

		if($query->num_rows() > 0){
			$passwordDB = $query->row('password');
			$passwordDB = substr($passwordDB, 4, 32);

			if(md5($password) == $passwordDB){
				$usuario = $query->row();
				$perfil = $this->CI->Model_Perfiles->find($usuario->id_perfil);
				$datosSession = array('nombre_usuario' => $usuario->nombre, 'dni_usuario' => $usuario->dni, 'id_perfil' => $usuario->id_perfil, 'perfil_nombre'=>$perfil->nombre);
				$this->CI->session->set_userdata($datosSession);
				return TRUE;				
			}else{
				return FALSE;
			}
		}else{
			$this->CI->session->sess_destroy();
			return FALSE;
		}
	}

	public function cambiarPWD($actual, $nueva){
		//Preguntamos si tiene iniciada la session
		if($this->CI->session->userdata('dni_usuario') == null){
			return FALSE;
		}

		$dni = $this->CI->session->userdata('dni_usuario');
		$query = $this->CI->Model_Usuarios->get_login($dni);
		$passwordDB = $query->row('password');
		$passwordDB = substr($passwordDB, 4, 32);//Desencriptamos

		//Si la clave que ingreso como actual es igual a la que está en la BD
		if($passwordDB == md5($actual)){
			//Hacemos el cambio de clave
			$data = array('dni' => $dni, 'password' => $this->encriptar($nueva));//Mandamos el dni porque la consulta necesita ubicar el registro que se va a modificar.
			$this->CI->Model_Usuarios->update($data);
			return TRUE;
		}else{
			//No coincide su clave guardada en la BD con la que ingreso como actual
			return FALSE;
		}
	}

	public function my_validation($registro){
		$this->CI->db->where('nombre', $registro['nombre']);
		$query = $this->CI->db->get('usuarios');
		if($query->num_rows() > 0 AND (!isset($registro['dni']) OR ($registro['dni'] != $query->row('dni')))){
			return FALSE;
		}else{
			return TRUE;
		}
	}

	public function generarPassword($long){
	    //Se define una cadena de caractares. Te recomiendo que uses esta.
	    $cadena = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890#$%&?.";
	    //Obtenemos la longitud de la cadena de caracteres
	    $longitudCadena=strlen($cadena);
	     
	    //Se define la variable que va a contener la contraseña
	    $pass = "";
	    //Se define la longitud de la contraseña, en mi caso 10, pero puedes poner la longitud que quieras
	    $longitudPass=$long;
	     
	    //Creamos la contraseña
	    for($i=1 ; $i<=$longitudPass ; $i++){
	        //Definimos numero aleatorio entre 0 y la longitud de la cadena de caracteres-1
	        $pos=rand(0,$longitudCadena-1);
	     
	        //Vamos formando la contraseña en cada iteraccion del bucle, añadiendo a la cadena $pass la letra correspondiente a la posicion $pos en la cadena de caracteres definida.
	        $pass .= substr($cadena,$pos,1);
	    }
	    return $pass;
	}

	public function encriptar($password){
		$resultado = $this->generarPassword(4).md5($password).$this->generarPassword(4);
		return $resultado;
	}

	public function cargar_log_usuario($dni, $fecha, $accion){
		$query = $this->CI->Model_Log_Usuarios->find_accion($accion);
		$registro['fecha'] = $fecha;
		$registro['lugar'] = 1;//1 -> WEB, 2 -> Máquina
		$registro['id_accion'] = $query->row('id');
		$registro['dni'] = $dni;
		$id_log =  $this->CI->Model_Log_Usuarios->add_log($registro);
		return $id_log;
	}

	//Esta función realiza todos los pasos necesarios para la compra de tickets
	public function realizar_compra($dni, $fecha_log, $dias, $year, $month){
		//No dejar comprar a un usuarios dos tickets para el mismo día
		foreach ($dias as $dia) {
			//Verificamos si el día existe
			$fecha = $year.'-'.$month.'-'.$dia;
			$query_dias = $this->CI->Model_Dias->find($fecha);
			if($query_dias->num_rows() == 1){
				//Si la siguiente consulta arroja exactamente 0 filas, entonces permitimos comprar.
				$query_tickets = $this->CI->Model_Dias->consultar_dia_con_ticket($fecha, $dni);
				if($query_tickets->num_rows() == 0){
					//Actualizamos la cantidad de tickets vendidos para el día en particular
					$registro_dia = $query_dias->row();
					$tickets_vendidos = $registro_dia->tickets_vendidos + 1;
					$data = array('fecha'=>$fecha, 'tickets_vendidos'=>$tickets_vendidos);
					$this->CI->Model_Dias->update($data);

					//Cargamos el registro en la tabla log_usuarios
					$id_log = $this->cargar_log_usuario($dni, $fecha_log,'comprar');
					
					$usuario = $this->CI->Model_Usuarios->find($dni);//Necesito el usuario para saber el importe que paga ese usuario

					//Cargo el ticket para el día en cuestión
					$registro['id_dia'] = $query_dias->row('id');//Cargo el id del día.
					$registro['unidad'] = 0;//por defecto...reveer esto.
					$registro['importe'] = $usuario->importe;//Este importe depende de acuerto a la beca que tiene el usuario
					$registro['estado'] = 1;//0 -> anulado, 1 -> activo
					$registro['id_log_usuario'] = $id_log;
					$id_ticket = $this->CI->Model_Tickets->add_ticket($registro);

					$registro = array();
					$registro['id'] = $id_ticket;
					$registro['barcode'] = $this->generar_barcode($id_ticket, 10);
					$this->CI->Model_Tickets->update($registro);
				}
			}
		}
	}

	public function generar_barcode($id_ticket, $num_ceros){
		$barcode = strtotime(date('Y-m-d H:i:s'));
		$num_ceros = $num_ceros - strlen($id_ticket);
		for($i = 0; $i < $num_ceros; $i++){
			$barcode = $barcode.'0';
		}
		$barcode = $barcode.$id_ticket;
		return $barcode;
	}

	public function realizar_anulacion($id_ticket,$dni){
		//Incrementar Saldo
		$registro = $this->CI->Model_Usuarios->find($dni);
		$data['dni'] = $dni;
		$data['saldo'] = $registro->saldo + $registro->importe;
		$this->CI->Model_Usuarios->update($data);
		//Cambiar estado del ticket
		$data = array();//Reinicio la variable data
		$data['id'] = $id_ticket;
		$data['estado'] = 0;
		$this->CI->Model_Tickets->update($data);
		//Registrar el nuevo log.
		$fecha_log = date('Y/m/d H:i:s');
		$this->cargar_log_usuario($dni, $fecha_log,'anular');
	}

	public function recordar_clave($dni, $email){
		$query = $this->CI->Model_Usuarios->find_simple($dni);
		if($query->num_rows() == 1){
			//Cambiamos el mail en la base de datos por el que ingreso
			$data['dni'] = $dni;
			$data['email'] = $email;
			$this->CI->Model_Usuarios->update($data);
			//enviamos un mail con la nueva contraseña.
			

		}

	}



}