<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Reportes extends CI_Controller {

	function __construct(){
		parent::__construct();
		//Cargo la librería html2pdf
		$this->load->library('ConvertToPDF');
		//Cargo el modelo
		$this->load->model('Model_Facultades');
		$this->load->model('Model_Usuarios');
		$this->load->model('Model_Tickets');
	}

	public function informes_contables(){

	}

	public function informes_estadisticos(){
		$data['contenido'] = 'reportes/informes_estadisticos';
		//Datos para el informe de usuarios por facultad
		$data['registros'] = $this->Model_Facultades->clasificacion_usuarios();
		$data['totales'] = $this->Model_Usuarios->total_usuarios();
		//Datos para el informe de servicios por facultad
		$hoy = date('Y-m-d');
		$data['desde'] = $hoy;
		$data['hasta'] = $hoy;
		$data['registros2'] = $this->Model_Tickets->servicios_tickets($hoy, $hoy);//por defecto, el día actual.
		$data['totales2'] = $this->Model_Tickets->get_total_servicios($hoy, $hoy)->row();
		//Datos para la clasificación de tickets
		$data['registros3'] = $this->Model_Tickets->clasificacion_tickets($hoy, $hoy);//por defecto, el día actual.
		$data['totales3'] = $this->Model_Tickets->get_total_tickets($hoy, $hoy)->row();

		$this->load->view('template-admin', $data);
	}

	public function obtener_registros_tickets(){
		$desde = $this->input->post('desde');
		$hasta = $this->input->post('hasta');

		$data['tickets'] = $this->Model_Tickets->servicios_tickets($desde, $hasta);
		$data['totales'] = $this->Model_Tickets->get_total_servicios($desde, $hasta)->result();
		echo json_encode($data);
	}

	public function obtener_clasificacion_tickets(){
		$desde = $this->input->post('desde2');
		$hasta = $this->input->post('hasta2');

		$data['tickets2'] = $this->Model_Tickets->clasificacion_tickets($desde, $hasta);
		$data['totales2'] = $this->Model_Tickets->get_total_tickets($desde, $hasta)->result();
		echo json_encode($data);
	}

	public function generar_pdf(){
		if($this->input->post('PDF1')){
			$data['registros'] = $this->Model_Facultades->clasificacion_usuarios();
			$data['totales'] = $this->Model_Usuarios->total_usuarios();
			$html = $this->load->view('reportes/reporte_pdf1', $data, true);
			$this->converttopdf->doPDF('informe_usuarios',$html,true,'');
		}else if($this->input->post('PDF2')){
			if($this->input->post('filtro_radio') == 'filtrointervalo' && $this->input->post('desde') != '' && $this->input->post('hasta') != ''){
				//Imprimo pdf según el intervalo.
				$desde = $this->input->post('desde');
				$hasta = $this->input->post('hasta');
			}else if($this->input->post('filtro_radio') == 'filtrodia' && $this->input->post('dia') != ''){
				//Imprimo según el día actual. Por defecto el día actual
				$desde = $this->input->post('dia');
				$hasta = $this->input->post('dia');
			}else{
				$hoy = date('Y-m-d');
				$desde = $hoy;
				$hasta = $hoy;
			}
			$data['registros2'] = $this->Model_Tickets->servicios_tickets($desde, $hasta);//por defecto, el día actual.
			$data['totales2'] = $this->Model_Tickets->get_total_servicios($desde, $hasta)->row();
			$data['desde'] = $desde;
			$data['hasta'] = $hasta;
			$html = $this->load->view('reportes/reporte_pdf2', $data, true);
			$this->converttopdf->doPDF('informe_servicios',$html,true,'');
		}else if($this->input->post('PDF3')){
			if($this->input->post('filtro_radio2') == 'filtrointervalo2' && $this->input->post('desde2') != '' && $this->input->post('hasta2') != ''){
				//Imprimo pdf según el intervalo.
				$desde = $this->input->post('desde2');
				$hasta = $this->input->post('hasta2');
			}else if($this->input->post('filtro_radio2') == 'filtrodia2' && $this->input->post('dia2') != ''){
				//Imprimo según el día actual. Por defecto el día actual
				$desde = $this->input->post('dia2');
				$hasta = $this->input->post('dia2');
			}else{
				$hoy = date('Y-m-d');
				$desde = $hoy;
				$hasta = $hoy;
			}
			$data['registros3'] = $this->Model_Tickets->clasificacion_tickets($desde, $hasta);//por defecto, el día actual.
			$data['totales3'] = $this->Model_Tickets->get_total_tickets($desde, $hasta)->row();
			$data['desde'] = $desde;
			$data['hasta'] = $hasta;
			$html = $this->load->view('reportes/reporte_pdf3', $data, true);
			$this->converttopdf->doPDF('informe_tickets',$html,true,'');
		}
	}

	public function informes_ausentismos(){

	}

	public function plantilla_unsa(){
		$this->load->view('reportes/plantilla_unsa');
	}

}