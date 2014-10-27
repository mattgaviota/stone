<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');


class Model_Alumnos extends CI_Model {

    function __construct()
    {
        parent::__construct();
    }

    function all(){
    	$query = $this->db->get('alumnos_guarani');
    	return $query->result();
    }

    function allFilter($campo, $valor){
        $this->db->like($campo, $valor);
        $query = $this->db->get('alumnos_guarani');
        return $query->result();
    }

    function find($id){
    	$this->db->where('id',$id);
    	return $this->db->get('alumnos_guarani')->row();
    }

    //Encontrar un registro según el login, es decir, el documento ó DNI
    function findLogin($documento){
        $this->db->where('documento', $documento);
        return $this->db->get('alumnos_guarani');
    }

    function findNombre($nombre){
        $this->db->where('nombre',$nombre);
        return $this->db->get('alumnos_guarani');   
    }

    function insert($registro){
    	$this->db->set($registro);
    	$this->db->insert('alumnos_guarani');
    }

    function update($registro){
    	$this->db->set($registro);
    	$this->db->where('id',$registro['id']);
    	$this->db->update('alumnos_guarani');
    }

    function delete($id){
    	$this->db->where('id',$id);
    	$this->db->delete('alumnos_guarani');
    }

}