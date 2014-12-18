<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Perfiles extends CI_Controller {

	//Constructor
	function __construct(){
		parent::__construct();
		$this->load->model('Model_Perfiles');
		$this->load->library('perfilesLib');
		$this->form_validation->set_message('required', 'Debe ingresar un valor para %s');
		$this->form_validation->set_message('norepeat', 'Ya existe un registro con el mismo nombre');
	}

	public function index(){
		$data['contenido'] = 'perfiles/index';
		$data['titulo'] = 'Perfiles';
		$data['registros'] = $this->Model_Perfiles->all();
		$this->load->view('template-admin', $data);
	}

	public function search(){
		$data['contenido'] = 'perfiles/index';
		$data['titulo'] = 'Perfiles';
		$valor = $this->input->post('buscar');
		$data['registros'] = $this->Model_Perfiles->allFilter('nombre', $valor);
		$this->load->view('template-admin', $data);
	}

	public function norepeat(){
		return $this->perfileslib->norepetir($this->input->post());
	}

	public function edit($id){
		//$id = $this->uri->segment(3);//1->controlador, 2->accion, 3->el id
		$data['contenido'] = 'perfiles/edit';
		$data['titulo'] = 'Editar Perfiles';
		$data['registro'] = $this->Model_Perfiles->find($id);
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
			$this->Model_Perfiles->update($registro);
			redirect('perfiles/index');
		}
	}

	public function create(){
		$data['contenido'] = 'perfiles/create';
		$data['titulo'] = 'Crear Perfil';
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
 			$this->Model_Perfiles->insert($registro);
			redirect('perfiles/index');
		}
	}

	public function delete($id){
		$this->Model_Perfiles->delete($id);
		redirect('perfiles/index');
	}

	public function perfiles_tipos_operaciones($id){
		$data['contenido'] = 'perfiles/perfiles_tipos_operaciones';
		$data['titulo'] = 'Asignando operaciones';
		
		$operaciones = $this->perfileslib->get_operaciones($id);
		$data['query_izq'] = $operaciones[0];
		$data['query_der'] = $operaciones[1];
		$this->load->view('template-admin', $data);
	}

	public function pto_asignados(){
		$id_tipo_operacion = $this->uri->segment(3);
		$id_perfil = $this->uri->segment(4);
		$this->perfileslib->dar_permiso($id_tipo_operacion, $id_perfil);
		redirect('perfiles/perfiles_tipos_operaciones/'.$id_perfil);
	}

	public function pto_noasignados(){
		$id_tipo_operacion = $this->uri->segment(3);
		$id_perfil = $this->uri->segment(4);
		$this->perfileslib->quitar_permiso($id_tipo_operacion, $id_perfil);
		redirect('perfiles/perfiles_tipos_operaciones/'.$id_perfil);	
	}

}