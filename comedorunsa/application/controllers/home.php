<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Home extends CI_Controller {

	//Constructor
	function __construct(){
		parent::__construct();
		$this->load->library('usuarioLib');
		$this->load->model('Model_Usuarios');
		$this->form_validation->set_message('required', 'Debe ingresar un valor para %s');
		$this->form_validation->set_message('loginok', 'Usuario o password incorrecto');
		$this->form_validation->set_message('valid_email', 'El email %s no es válido');
		$this->form_validation->set_message('cambiook', 'No se pudo realizar el cambio de clave');
		$this->form_validation->set_message('max_length', '%s debe ser de a lo sumo %s números');
		$this->form_validation->set_message('numeric', '%s debe ser un valor numérico');
		$this->form_validation->set_message('no_repetir_usuario', 'Existe otro registro con el mismo nombre');
	}

	public function index(){
		$this->session->sess_destroy();//Destruimos cualquier session que haya quedado guardada.
		$data['contenido'] = 'home/index';
		$this->load->view('template-index', $data);
	}

	public function acerca_de(){
		$data['contenido'] = 'home/acerca_de';
		$this->load->view('template-index', $data);//Cargamos la vista y el template
	}

	public function acceso_denegado(){
		$data['contenido'] = 'home/acceso_denegado';
		$this->load->view('template-index', $data);
	}

	public function ingreso(){
		$this->session->sess_destroy();//Destruimos cualquier session que haya quedado guardada.
		$data['contenido'] = 'home/ingreso';
		$data['mostrar_mensaje'] = false;
		$this->load->view('template-index', $data);//Cargamos la vista y el template
	}

	public function ingresar(){
		$this->form_validation->set_rules('dni', 'Usuario', 'required|callback_loginok');
		$this->form_validation->set_rules('password', 'Password', 'required');
		
		if($this->form_validation->run() == FALSE){
			$this->ingreso();//No uso redirect para no perder el valor de los campos ingresados
		}else{
			if($this->session->userdata('estado_usuario') == 1){
				//El usuario aún no esta activo. Lo mando a cambiar su clave.
				redirect('home/cambiar_clave');
			}else if($this->session->userdata('estado_usuario') == 2){
				//Al ingresar lo mando a la página de inicio correspondiente a su perfil
				if($this->session->userdata('perfil_nombre') === 'Alumno'){
					redirect('usuarios/alumno');
				}else if($this->session->userdata('perfil_nombre') === 'Administrador' || $this->session->userdata('perfil_nombre') === 'Super Administrador'){
					redirect('usuarios/admin');
				}else{
					redirect('usuarios/control');
				}
			}else{
				redirect('home/bloqueado');
			}
		}
	}

	public function loginok(){
		$dni = $this->input->post('dni');//El login es el dni
		$password = $this->input->post('password');
		return $this->usuariolib->loginok($dni,$password);
	}

	public function salir(){
		$this->session->sess_destroy();
		redirect('home/index');
	}

	public function cambiar_clave(){
		$data['contenido'] = 'home/cambiar_clave';
		$this->load->view('template-index', $data);
	}

	public function cambiando_clave(){
		$this->form_validation->set_rules('clave_actual', 'Clave Actual', 'required|callback_cambiook');
		$this->form_validation->set_rules('clave_nueva', 'Clave Nueva', 'required|matches[clave_repetida]');
		$this->form_validation->set_rules('clave_repetida', 'Repita Clave', 'required');
		
		if($this->form_validation->run() == FALSE){
			//No se pudo realizar el cambio
			$this->cambiar_clave();//No uso redirect para no perder el valor de los campos ingresados
		}else{
			//Cambio con exito
			if($this->session->userdata('perfil_nombre') === 'Alumno'){
				redirect('usuarios/alumno');
			}else if($this->session->userdata('perfil_nombre') === 'Control'){
				redirect('usuarios/control');
			}else{
				redirect('usuarios/admin');
			}
		}
	}

	public function recordar_clave(){
		$data['contenido'] = 'home/recordar_clave';
		$data['mostrar_mensaje'] = FALSE;
		$this->load->view('template-index', $data);//Cargamos la vista y el template		
	}

	public function existe_usuario(){
		$dni = $this->input->post('dni');
		return $this->usuariolib->existe_usuario($dni);
	}

	public function recordando_clave(){
		$dni = $this->input->post('dni');
		$email = $this->input->post('email');

		$this->form_validation->set_rules('dni', 'Usuario', 'required|callback_existe_usuario');
		$this->form_validation->set_rules('email', 'Email', 'required|valid_email');

		if($this->form_validation->run() == FALSE){
			$this->recordar_clave();//No uso redirect para no perder el valor de los campos ingresados
		}else{
			//genero nuevo password
			$password_generada = $this->usuariolib->generarPassword(10);//Generamos un password aleatorio de 10 caracteres.
			//Actualizo password, estado y email en el usuario.
			$registro['dni'] = $dni;
			$registro['email'] = $email;
			$registro['estado'] = 2;
			$registro['password'] = $this->usuariolib->encriptar($password_generada);//Encripto la password
			$this->Model_Usuarios->update($registro);
			//Enviar email con la nueva contraseña
			$usuario = $this->Model_Usuarios->find_simple($dni);//Recupero los datos
			
			$nombre = $usuario->row('nombre');
			$email = $usuario->row('email');
			$this->usuariolib->enviar_email($nombre, $email, $password_generada);

			$data['contenido'] = 'home/ingreso';
			$data['mostrar_mensaje'] = TRUE;
			$this->load->view('template-index', $data);//Cargamos la vista y el template
		}
	}

	public function cambiook(){
		$actual = $this->input->post('clave_actual');
		$nueva = $this->input->post('clave_nueva');
		return $this->usuariolib->cambiarPWD($actual,$nueva);
	}

	public function registro(){
		$this->load->model('Model_Perfiles');
		$this->load->model('Model_Categorias');
		$data['contenido'] = 'home/registro';
		$data['titulo'] = 'Registro de Usuario';
		$data['provincias'] = $this->Model_Usuarios->get_provincias();
		$data['facultades'] = $this->Model_Usuarios->get_facultades();
		$data['perfil'] = $this->Model_Perfiles->findNombre('Alumno');
		$data['categoria'] = $this->Model_Categorias->findNombre('Regular');

		$this->load->view('template-index', $data);
	}

	public function no_repetir_usuario(){
		return $this->usuariolib->no_repetir_usuario($this->input->post(), 'insertar');
	}

	public function registrarse(){
		$registro = $this->input->post();

		$this->form_validation->set_rules('dni', 'Usuario', 'required|max_length[8]|numeric|callback_no_repetir_usuario');
		$this->form_validation->set_rules('nombre', 'Nombre', 'required');
		$this->form_validation->set_rules('email', 'Email', 'required|valid_email');
		$this->form_validation->set_rules('lu', 'Libreta Universitaria', 'required|max_length[7]|numeric');

		if($this->form_validation->run() == FALSE){
			//Fallo alguna validación
			$this->registro();
		}else{
			//Los datos son correctos. Intentamos enviar en mail. Registramos el usuarios.
			$nombre = $this->input->post('nombre');
			$email = $this->input->post('email');
			$password_generada = $this->usuariolib->generarPassword(10);//Generamos un password aleatorio de 10 caracteres.
			$this->usuariolib->enviar_email($nombre, $email, $password_generada);//Intentamos enviar el mail. Si falla, lo registramos de todas formas.
			//El registro está ok, entonces lo agregamos a la tabla usuarios
			$registro['password'] = $this->usuariolib->encriptar($password_generada);
			$registro['estado'] = 1;//0 = bloqueado, 1 = registrado, 2 = activo, 3 = suspendido
			
			$this->Model_Usuarios->insert($registro);
			$dni = $this->input->post('dni');
			//Registro el log de usuario para registro
			$fecha_log = date('Y/m/d H:i:s');
			$this->usuariolib->cargar_log_usuario($dni, $fecha_log, 'registrar');

			$data = array();//limpiamos el array.
			$data['contenido'] = 'home/ingreso';
			$data['mostrar_mensaje'] = TRUE;
			$this->load->view('template-index', $data);//Cargamos la vista y el template

		}
	}

}
