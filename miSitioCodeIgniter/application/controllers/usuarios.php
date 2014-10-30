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

	public function index(){
		$data['contenido'] = 'usuarios/index';
		$data['titulo'] = 'Usuarios';
		$data['registros'] = $this->Model_Usuarios->allRecargado();
		$this->load->view('template', $data);
	}

	public function search(){
		$data['contenido'] = 'usuarios/index';
		$data['titulo'] = 'Usuarios';
		$valor = $this->input->post('buscar');
		$data['registros'] = $this->Model_Usuarios->allFilter('usuarios.nombre', $valor);
		$this->load->view('template', $data);
	}

	public function my_validation(){
		return $this->usuariolib->my_validation($this->input->post());
	}

	public function edit($dni){
		$data['contenido'] = 'usuarios/edit';
		$data['titulo'] = 'Editar Usuario';
		$data['registro'] = $this->Model_Usuarios->find($dni);
		$data['provincias'] = $this->Model_Usuarios->get_provincias();//Obtener lista de provincias
		$data['facultades'] = $this->Model_Usuarios->get_facultades();//Obtener lista de facultades
		$data['perfiles'] = $this->Model_Usuarios->get_perfiles();//Obtener lista de perfiles
		$data['categorias'] = $this->Model_Usuarios->get_categorias();//Obtener lista de categorías
		$this->load->view('template',$data);
	}

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

	public function create(){
		$data['contenido'] = 'usuarios/create';
		$data['titulo'] = 'Crear Usuario';
		$data['perfiles'] = $this->Model_Usuarios->get_perfiles();//Obtener lista de perfiles
		$this->load->view('template',$data);
	}

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

	public function delete($dni){
		$this->Model_Usuarios->delete($dni);
		redirect('usuarios/index');
	}

	public function comprar_tickets($year = null, $month = null){
		$dni = $this->session->userdata('dni_usuario');
		$data['registro'] = $this->Model_Usuarios->find($dni);
		$data['contenido'] = 'usuarios/comprar_tickets';
		$data['calendario'] = $this->Model_Usuarios->generate($year, $month);
		$this->load->view('template_usuario', $data);
	}

	public function get_dias_calendario(){
		$year = $this->input->post('year');
		$month = $this->input->post('month');
		$dia = $this->input->post('dia');
		
		$fecha = date('Y-m-d', strtotime($year.'-'.$month.'-'.$dia));
		$query = $this->Model_Usuarios->get_dias($fecha);

		echo json_encode($query);
	}

	public function perfil_usuario(){
		$dni = $this->session->userdata('dni_usuario');
		$data['contenido'] = 'usuarios/perfil_usuario';
		$data['registro'] = $this->Model_Usuarios->find($dni);
		$data['acciones'] = $this->Model_Usuarios->get_ultimas_operaciones($dni);
		$this->load->view('template_usuario', $data);
	}

}