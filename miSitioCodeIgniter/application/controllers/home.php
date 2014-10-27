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
		$this->form_validation->set_message('my_validation', 'Existe otro registro con el mismo nombre');
		
		$config = Array(
		    'protocol' => 'smtp',
		    'smtp_host' => 'ssl://smtp.googlemail.com',
		    'smtp_port' => 465,
		    'smtp_user' => 'ferroxido@gmail.com',
		    'smtp_pass' => 'valarmorgulis',
		    'mailtype'  => 'html', 
		    'charset'   => 'utf-8'
		);
		$this->load->library('email', $config);
		$this->email->set_newline("\r\n");//La papucha
	}

	public function index(){
		$data['contenido'] = 'home/index';
		$data['titulo'] = 'Inicio';
		$this->load->view('template', $data);
	}

	public function acerca_de(){
		$data['contenido'] = 'home/acerca_de';
		$data['titulo'] = 'Acerca de';
		$this->load->view('template', $data);//Cargamos la vista y el template
	}

	public function acceso_denegado(){
		$data['contenido'] = 'home/acceso_denegado';
		$data['titulo'] = 'Denegado';
		$this->load->view('template', $data);
	}

	public function ingreso(){
		$data['contenido'] = 'home/ingreso';
		$data['titulo'] = 'Ingreso';
		$data['mostrar'] = false;
		$this->load->view('template', $data);//Cargamos la vista y el template
	}

	public function ingresar(){
		$this->form_validation->set_rules('dni', 'Usuario', 'required|callback_loginok');
		$this->form_validation->set_rules('password', 'Password', 'required');
		
		if($this->form_validation->run() == FALSE){
			$this->ingreso();//No uso redirect para no perder el valor de los campos ingresados
		}else{
			//Al ingresar lo mando al index
			redirect('usuarios/perfil_usuario');
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
		$data['titulo'] = 'Cambiar Clave';
		$this->load->view('template', $data);
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
			redirect('home/index');
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
		$data['perfil'] = $this->Model_Perfiles->findNombre("Alumno");
		$data['provincias'] = $this->Model_Usuarios->get_provincias();
		$data['facultades'] = $this->Model_Usuarios->get_facultades();
		$data['categoria'] = $this->Model_Categorias->findNombre('Regular');

		$this->load->view('template', $data);
	}

	public function my_validation(){
		return $this->usuariolib->my_validation($this->input->post());
	}	

	public function registrarse(){
		$registro = $this->input->post();

		$this->form_validation->set_rules('dni', 'Usuario', 'required|max_length[8]|numeric|callback_my_validation');
		$this->form_validation->set_rules('nombre', 'Nombre', 'required');
		$this->form_validation->set_rules('email', 'Email', 'required|valid_email');
		$this->form_validation->set_rules('lu', 'Libreta Universitaria', 'required|max_length[7]|numeric');

		if($this->form_validation->run() == FALSE){
			//Fallo alguna validación
			$this->registro();
		}else{
			$password_generada = $this->usuariolib->generarPassword(10);//Generamos un password aleatorio de 10 caracteres.
			
			//---------Envío el email----------------------//
			$this->email->from('ferroxido@gmail.com', 'UNSA');
			$this->email->to($registro['email']);
			$this->email->subject('Registración UNSA comedor');//Título del mail
			$cadena = '<h2>gracias por registrarte en el comedor de la UNSA</h2><hr><br><br>';
			$cadena = $cadena.'<div><p>Su contraseña es: '.$password_generada.' </p></div>';
			$this->email->message($cadena);
			
			if(! $this->email->send()){
				show_error($this->email->print_debugger());
			}

			//El registro está ok, entonces lo agregamos a la tabla usuarios
			$registro['password'] = $this->usuariolib->encriptar($password_generada);
			$registro['estado'] = 2;//0 = inactivo, 1 = activo, 2 = wait
			$this->Model_Usuarios->insert($registro);


			//Saltamos al ingreso para que ingrese.
			$data = array();//limpiamos el array.
			$data['contenido'] = 'home/ingreso';
			$data['titulo'] = 'Ingreso';
			$data['mostrar'] = true;
			$this->load->view('template', $data);//Cargamos la vista y el template
		}
	}

}
