<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Usuarios extends CI_Controller {

	//Constructor
	function __construct(){
		parent::__construct();
		$this->load->model('Model_Usuarios');
		$this->load->library('usuarioLib');
		$this->form_validation->set_message('required', 'Debe ingresar un valor para %s');
		$this->form_validation->set_message('valid_email', '%s no es un email válido');
		$this->form_validation->set_message('my_validation', 'Existe otro registro con el mismo nombre');
	}

	//Para el usuario administrador
	public function index(){
		$data['contenido'] = 'usuarios/index';
		$data['titulo'] = 'Usuarios';
		$data['registros'] = $this->Model_Usuarios->allRecargado();
		$this->load->view('template-admin', $data);
	}

	public function search(){
		$data['contenido'] = 'usuarios/index';
		$data['titulo'] = 'Usuarios';
		$valor = $this->input->post('buscar');
		$data['registros'] = $this->Model_Usuarios->allFilter('usuarios.nombre', $valor);
		$this->load->view('template-admin', $data);
	}

	public function my_validation(){
		return $this->usuariolib->my_validation($this->input->post());
	}

	//Para el usuario administrador
	public function edit($dni){
		$data['contenido'] = 'usuarios/edit';
		$data['titulo'] = 'Editar Usuario';
		$data['registro'] = $this->Model_Usuarios->find($dni);
		$data['provincias'] = $this->Model_Usuarios->get_provincias();//Obtener lista de provincias
		$data['facultades'] = $this->Model_Usuarios->get_facultades();//Obtener lista de facultades
		$data['perfiles'] = $this->Model_Usuarios->get_perfiles();//Obtener lista de perfiles
		$data['categorias'] = $this->Model_Usuarios->get_categorias();//Obtener lista de categorías
		$this->load->view('template-admin',$data);
	}

	//Para el usuario administrador
	public function update(){
		$registro = $this->input->post();

		$this->form_validation->set_rules('nombre', 'Nombre', 'required');
		$this->form_validation->set_rules('email', 'Email', 'required|valid_email');
		$this->form_validation->set_rules('dni', 'DNI', 'required|callback_my_validation');
		if($this->form_validation->run() == FALSE){
			//Si no cumplio alguna de las reglas
			$this->edit($registro['dni']);
		}else{
			//El registro está ok, entonces lo actualizamos en la tabla usuarios
			$this->Model_Usuarios->update($registro);
			redirect('usuarios/index');
		}
	}

	//Para el usuario administrador
	public function create(){
		$data['contenido'] = 'usuarios/create';
		$data['titulo'] = 'Crear Usuario';
		$data['perfiles'] = $this->Model_Usuarios->get_perfiles();//Obtener lista de perfiles
		$this->load->view('template-admin',$data);
	}

	//Para el usuario administrador
	public function insert(){
		$registro = $this->input->post();

		$this->form_validation->set_rules('nombre', 'Nombre', 'required');
		$this->form_validation->set_rules('email', 'Email', 'required|valid_email');
		$this->form_validation->set_rules('dni', 'DNI', 'required|callback_my_validation');
		if($this->form_validation->run() == FALSE){
			//Si no cumplio alguna de las reglas
			$this->create();
		}else{
 			$this->Model_Usuarios->insert($registro);
			redirect('usuarios/index');
		}
	}

	//Para el usuario administrador
	public function delete($dni){
		$this->Model_Usuarios->delete($dni);
		redirect('usuarios/index');
	}

	//Para el usuario alumnos
	public function comprar_tickets($year = null, $month = null){
		if($this->session->userdata('dni_usuario') != null){
			$dni = $this->session->userdata('dni_usuario');
			$data['registro'] = $this->Model_Usuarios->find($dni);
			$data['contenido'] = 'usuarios/comprar_tickets';
			$data['calendario'] = $this->Model_Usuarios->generate($year, $month);
			$this->load->view('template_usuario', $data);
		}
	}

	public function realizar_compra(){
		if($this->session->userdata('dni_usuario') != null){
			$dni = $this->session->userdata('dni_usuario');
			//Si estamos en este punto, es porque el hay días disponibles y el usuario realizó correctamente todo.
			$dias = $this->input->post('datos');//$dias contiene todos los dias seleccionados por el usuario
			$year = $this->input->post('year');
			$month = $this->input->post('month');

			$fecha_log = date('Y/m/d H:i:s');//Necesitaré la fecha para luego recuperar el id del log
			
			//La siguiente función realiza la compra de los tickets.
			$this->usuariolib->realizar_compra($dni, $fecha_log, $dias, $year, $month);//Aquí necesito la fecha del log.

			echo "Se enviaron los datos";
		}else{
			echo "Hubo un error";
		}
	}

	//Recupero los días para poder pintar los días NO hábiles.
	public function get_dias(){
		$year = $this->input->post('year');
		$month = $this->input->post('month');
		//$dia = $this->input->post('dia');
		$this->load->model('Model_Dias');
		$query = $this->Model_Dias->get_dias($year.'-'.$month.'%');//Optimizar trayendo en la consulta solo los días where tickets_totales - tickets_vendidos > 0
		echo json_encode($query);
	}

	//Recupero los días que el usuario logueado tiene tickets
	public function get_dias_tickets(){
		if($this->session->userdata('dni_usuario') != null){
			$dni = $this->session->userdata('dni_usuario');
			$year = $this->input->post('year');
			$month = $this->input->post('month');

			$this->load->model('Model_Tickets');
			$registros = $this->Model_Tickets->get_dias_tickets($year.'-'.$month.'%', $dni);
			echo json_encode($registros);
		}
	}

	//Para el usuario alumnos
	public function alumno(){
		if($this->session->userdata('dni_usuario')){
			$dni = $this->session->userdata('dni_usuario');
			$data['contenido'] = 'usuarios/alumno';
			$data['registro'] = $this->Model_Usuarios->find($dni);
			$this->load->view('template_usuario', $data);
		}
	}

	public function admin(){
		if($this->session->userdata('dni_usuario')){
			$data['contenido'] = 'usuarios/admin';
			$this->load->view('template-admin', $data);
		}	
	}

	//Para el usuario alumnos
	public function editar_perfil(){
		$dni = $this->session->userdata('dni_usuario');
		$data['contenido'] = 'usuarios/editar_perfil';
		$data['registro'] = $this->Model_Usuarios->find($dni);
		$data['provincias'] = $this->Model_Usuarios->get_provincias();//Obtener lista de provincias
		$data['facultades'] = $this->Model_Usuarios->get_facultades();//Obtener lista de facultades
		$this->load->view('template_usuario', $data);
	}

	//Para el usuario alumnos
	public function editando_perfil(){
		$registro = $this->input->post();

		$this->form_validation->set_rules('nombre', 'Nombre', 'required');
		$this->form_validation->set_rules('email', 'Email', 'required|valid_email');
		$this->form_validation->set_rules('dni', 'DNI', 'required|callback_my_validation');
		if($this->form_validation->run() == FALSE){
			//Si no cumplio alguna de las reglas
			$this->editar_perfil();
		}else{
			//Información necesaria para cargar la vista		
			$dni = $this->session->userdata('dni_usuario');
			$data['contenido'] = 'usuarios/alumno';
			$data['registro'] = $this->Model_Usuarios->find($dni);
			
			//Si todo va bien hasta aquí, entonces tratamos de subir la imagen al servidor.
			$config['upload_path'] = './img/fotos-usuarios/';
			$config['allowed_types'] = 'gif|jpg|png';
			$config['max_size']	= '2048';
			$config['max_width']  = '1024';
			$config['max_height']  = '768';
			$config['overwrite'] = true;
			$config['file_name'] = $dni;

			$this->load->library('upload', $config);

			if ( ! $this->upload->do_upload()){
				$this->Model_Usuarios->update($registro);
			}
			else{
				//El registro está ok, entonces lo actualizamos en la tabla usuarios
				$info = $this->upload->data();
				$registro['ruta_foto'] = base_url('img/fotos-usuarios/'.$info['file_name']);
				$this->Model_Usuarios->update($registro);
				
			}
			redirect('usuarios/alumno');
		}
	}

	public function anular(){
		if($this->session->userdata('dni_usuario')){
			$dni = $this->session->userdata('dni_usuario');
			$data['contenido'] = 'usuarios/anular';
			$data['registro'] = $this->Model_Usuarios->find($dni);

			$this->load->model('Model_Tickets');
			$data['tickets_proximos'] = $this->Model_Tickets->get_tickets_proximos($dni);

			$this->load->view('template_usuario', $data);
		}
	}

	public function anulando_ticket($id_ticket){
		if($this->session->userdata('dni_usuario')){
			//Realizar anulación
			$dni = $this->session->userdata('dni_usuario');
			$this->usuariolib->realizar_anulacion($id_ticket,$dni);
		}
		redirect('usuarios/anular');
	}

	public function imprimir(){
		if($this->session->userdata('dni_usuario')){
			$dni = $this->session->userdata('dni_usuario');
			$data['contenido'] = 'usuarios/imprimir';
			$data['registro'] = $this->Model_Usuarios->find($dni);

			$this->load->model('Model_Tickets');
			$data['tickets_proximos'] = $this->Model_Tickets->get_tickets_proximos($dni);

			$this->load->view('template_usuario', $data);
		}	
	}

	public function descargar(){
		$this->load->helper('download');
		$data = 'Here is some text!';
		$name = 'mytext.txt';
		force_download($name, $data);
		$data['contenido'] = 'usuarios/descargar';
		$this->load->view('template_usuario', $data);
	}
}