<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Reportes extends CI_Controller {

	function __construct(){
		parent::__construct();
		//Cargo la librería html2pdf
		$this->load->library('html2pdf');
		//Cargo el modelo
		$this->load->model('model_reportes');
	}

	






}