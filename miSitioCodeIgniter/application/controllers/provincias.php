<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Provincias extends CI_Controller {

	//Constructor
	function __construct(){
		parent::__construct();
		$this->load->model('Model_Provincias');
		$this->load->library('provinciasLib');
		$this->form_validation->set_message('required', 'Debe ingresar un valor para %s');
		$this->form_validation->set_message('norepeat', 'Ya existe un registro con el mismo nombre');
	}

	public function index(){
		$data['contenido'] = 'provincias/index';
		$data['titulo'] = 'Provincias';
		$data['registros'] = $this->Model_Provincias->all();
		$this->load->view('template-admin', $data);
	}

	public function search(){

		$buscar = $this->input->post('buscar');
		$query = $this->Model_Provincias->get_provincias($buscar);
		echo json_encode($query);
		//$this->load->view('template', $data);
	}

	public function norepeat(){
		return $this->provinciaslib->norepetir($this->input->post());
	}

	public function edit($id){
		//$id = $this->uri->segment(3);//1->controlador, 2->accion, 3->el id
		$data['contenido'] = 'provincias/edit';
		$data['titulo'] = 'Editar Provincias';
		$data['registro'] = $this->Model_Provincias->find($id);
		$this->load->view('template-admin',$data);
	}

	public function update(){
		$registro = $this->input->post();

		$this->form_validation->set_rules('nombre', 'Nombre', 'required|callback_norepeat');
		if($this->form_validation->run() == FALSE){
			//Si no cumplio alguna de las reglas
			$this->edit($registro['id']);
		}else{
			$registro['updated'] = date('Y/m/d H:i');
			$this->Model_Provincias->update($registro);
			redirect('provincias/index');
		}
	}

	public function create(){
		$data['contenido'] = 'provincias/create';
		$data['titulo'] = 'Agregar Provincias';
		$this->load->view('template-admin',$data);
	}

	public function insert(){
		$registro = $this->input->post();

		$this->form_validation->set_rules('nombre', 'Nombre', 'required|callback_norepeat');
		if($this->form_validation->run() == FALSE){
			//Si no cumplio alguna de las reglas
			$this->create();
		}else{
			$registro['created'] = date('Y/m/d H:i');
			$registro['updated'] = date('Y/m/d H:i');
 			$this->Model_Provincias->insert($registro);
			redirect('provincias/index');
		}
	}

	public function delete($id){
		$this->Model_Provincias->delete($id);
		redirect('provincias/index');
	}

}