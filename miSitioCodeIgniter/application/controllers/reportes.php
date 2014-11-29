<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Reportes extends CI_Controller {

	function __construct(){
		parent::__construct();
		//Cargo la librería html2pdf
		$this->load->library('ConvertToPDF');
		//Cargo el modelo
		$this->load->model('Model_Facultades');
		$this->load->model('Model_Usuarios');	
	}

	public function informes_contables(){

	}

	public function informes_estadisticos(){
		$data['contenido'] = 'reportes/informes_estadisticos';
		$data['registros'] = $this->Model_Facultades->clasificacion_usuarios();
		$data['totales'] = $this->Model_Usuarios->total_usuarios();
		$this->load->view('template-admin', $data);
	}

	public function generar_pdf(){
		if ($this->input->post('PDF1')){
			$data['registros'] = $this->Model_Facultades->clasificacion_usuarios();
			$data['totales'] = $this->Model_Usuarios->total_usuarios();
			$html = $this->load->view('reportes/plantilla_unsa', $data, true);
			$this->converttopdf->doPDF('informe_estadistico',$html,true,'');
		}
	}

	public function informes_ausentismos(){

	}

	public function plantilla_unsa(){
		$this->load->view('reportes/plantilla_unsa');
	}

}