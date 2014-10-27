<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

//Validar login de usuario, cambio de clave y CRUD en la tabla de usuarios
class UsuarioLib {

	function __construct(){
		$this->CI = & get_instance();//Obtener la instancia del objeto por referencia.
		$this->CI->load->model('Model_Usuarios');//Cargamos el modelo.
		$this->CI->load->model('Model_Perfiles');
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
		$this->CI->db->where('dni', $registro['dni']);
		$query = $this->CI->db->get('usuarios');
		if($query->num_rows() > 0){
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


}