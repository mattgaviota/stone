<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

/*
 * Esta clase se encarga de la mayoría de las tareas que realizan todos los usuarios con
 * distintos perfiles. Comprar ticket, anular ticket, imprimir ticket, generar las contraseñas, etc.
 */
class UsuarioLib {

	function __construct(){
		$this->CI = & get_instance();//Obtener la instancia del objeto por referencia.
		//Cargamos los distintos modelos que vamos a necesitar.
		$this->CI->load->model('Model_Usuarios');
		$this->CI->load->model('Model_Perfiles');
		$this->CI->load->model('Model_Dias');
		$this->CI->load->model('Model_Log_Usuarios');
		$this->CI->load->model('Model_Tickets');
		$this->CI->load->model('Model_Configuraciones');
	}

	/*
	 * Verifica que los datos ingresados en el login sean correctos y crea las variables
	 * de session necesarias. Además cargamos el log de usuario para el ingreso.
	 */
	public function loginok($dni, $password){
		$query = $this->CI->Model_Usuarios->get_login($dni);

		if($query->num_rows() > 0){
			$passwordDB = $query->row('password');
			$passwordDB = substr($passwordDB, 4, 32);

			if(md5($password) == $passwordDB){
				$usuario = $query->row();
				$perfil = $this->CI->Model_Perfiles->find($usuario->id_perfil);
				$datosSession = array('nombre_usuario' => $usuario->nombre, 'dni_usuario' => $usuario->dni,'estado_usuario' => $usuario->estado, 'id_perfil' => $usuario->id_perfil, 'perfil_nombre'=>$perfil->nombre);
				$this->CI->session->set_userdata($datosSession);

				//Cargar el log de usuarios con la acción ingreso
				$fecha_log = date('Y/m/d H:i:s');
				$dni = $this->CI->session->userdata('dni_usuario');
				$this->cargar_log_usuario($dni, $fecha_log, 'ingresar');

				return TRUE;				
			}else{
				return FALSE;
			}
		}else{
			$this->CI->session->sess_destroy();
			return FALSE;
		}
	}

	/*
	 * Cambia la contraseña del usuario por una nueva que el ingresa.
	 * Se realiza una encriptación a la nueva password y se la guarda en la DB.
	 */
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
			//Hacemos el cambio de clave, y seteamos el estado en 2 de activo.
			$data = array('dni' => $dni, 'password' => $this->encriptar($nueva), 'estado' => 2);//Mandamos el dni porque la consulta necesita ubicar el registro que se va a modificar.
			$this->CI->Model_Usuarios->update($data);
			return TRUE;
		}else{
			//No coincide su clave guardada en la BD con la que ingreso como actual
			return FALSE;
		}
	}

	//Función en observación!! CUIDADO
	public function my_validation($registro){
		$this->CI->db->where('nombre', $registro['nombre']);
		$query = $this->CI->db->get('usuarios');
		if($query->num_rows() > 0 AND (!isset($registro['dni']) OR ($registro['dni'] != $query->row('dni')))){
			return FALSE;
		}else{
			return TRUE;
		}
	}

	/*
	 * Dependiendo del tipo de acción (insertar o update) controla que el número de registros en
	 * la DB sea el correcto. 0 para insertar, 1 para update.
	 */
	public function no_repetir_usuario($registro, $tipo_accion){
		$this->CI->db->where('dni', $registro['dni']);
		$query = $this->CI->db->get('usuarios');
		if($query->num_rows() > 0 AND $tipo_accion === 'insertar'){
			return FALSE;
		}else if ($query->num_rows() != 1 AND $tipo_accion === 'update'){
			return FALSE;
		}else{
			return TRUE;
		}
	}

	/*
	 * Genera una contraseña con los caracteres que se indican.
	 * 
	 * @param: $long: longitud de la contraseña que se va a generar.
	 */
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

	/*
	 * Encripta la contraseña que se pasa por parámetro. Para encriptar concatena cuatro valores
	 * randómicos al inicio y al final, en el medio es un md5 tradicional.
	 */
	public function encriptar($password){
		$resultado = $this->generarPassword(4).md5($password).$this->generarPassword(4);
		return $resultado;
	}

	/*
	 * Carga el registro en la tabla log_usuarios
	 */
	public function cargar_log_usuario($dni, $fecha, $accion){
		$query = $this->CI->Model_Log_Usuarios->find_accion($accion);
		$registro['fecha'] = $fecha;
		$registro['lugar'] = 1;//1 -> WEB, 2 -> Máquina
		$registro['id_accion'] = $query->row('id');
		$registro['dni'] = $dni;
		$registro['descripcion'] = $query->row('nombre');
		$id_log =  $this->CI->Model_Log_Usuarios->add_log($registro);
		return $id_log;
	}

	/*
	 * Esta función realiza todos los pasos necesarios para la compra de tickets
	 * esta es la función que utiliza el usuario con perfil de alumno para comprar los tickets.
	 */
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

	/*
	 * Genera el código de barra de 20 caracteres. Se forma con la fecha acutal en formato unix,
	 * concatenada con ceros y el id del ticket. El número de ceros + la longitud del id deben
	 * sumar 10. Fecha unix (10) + (ceros + id) (10) = (20)
	 */
	public function generar_barcode($id_ticket, $num_ceros){
		$barcode = strtotime(date('Y-m-d H:i:s'));
		$num_ceros = $num_ceros - strlen($id_ticket);
		for($i = 0; $i < $num_ceros; $i++){
			$barcode = $barcode.'0';
		}
		$barcode = $barcode.$id_ticket;
		return $barcode;
	}

	/*
	 * Realiza la anulación del ticket, segun el id pasado como parámetro.
	 */
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

	/*
	 * Verifica que exista el usuario de acuerdo al dni pasado como parámetro.
	 */
	public function existe_usuario($dni){
		$query = $this->CI->Model_Usuarios->find_simple($dni);
		if($query->num_rows() == 1){
			return TRUE;
		}else{
			return FALSE;
		}
	}

	/*
	 * Función para el envió de email, utilizamos primitivas de codeigniter.
	 *
	 * @param
	 * $nombre: nombre del usuario al que se le enviará el email.
	 * $email: email del usuario a donde enviaremos el email.
	 * $password_generada: password que enviaremos al usuario para su login.
	 */
	public function enviar_email($nombre, $email, $password_generada){
		//----------------Configuración--------------------//
		$query = $this->CI->Model_Configuraciones->find(0);
		$config = Array(
		    'protocol' => 'smtp',
		    'smtp_host' => 'ssl://'.$query->smtp,
		    'smtp_port' => 465,
		    'smtp_user' => $query->email,
		    'smtp_pass' => $query->password,
		    'mailtype'  => $query->email_type, 
		    'charset'   => $query->charset
		);
		$this->CI->load->library('email', $config);
		$this->CI->email->set_newline("\r\n");//Sin esta linea de código no se envía.
		
		$this->CI->email->from($query->email, 'UNSA');
		$this->CI->email->to($email);
		$this->CI->email->subject('Registración UNSA comedor');//Título del mail
		$cadena = '<h2>gracias '.$nombre.' por registrarte en el comedor de la UNSA</h2><hr><br><br>';
		$cadena = $cadena.'<div><p>Su contraseña es: '.$password_generada.' </p></div>';
		$this->CI->email->message($cadena);

		//-----------realizamos el envío------------------//
		if(! $this->CI->email->send()){
			//show_error($this->email->print_debugger());
			return FALSE;
		}else{
			return TRUE;
		}
	}

	/*
	 * Obtiene del código de barra el id del ticket.
	 */
	public function obtener_id_ticket($barcode){
		return (int) (substr($barcode, 10));
	}

}